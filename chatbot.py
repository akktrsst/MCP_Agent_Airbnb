"""
Streamlit chatbot application for Airbnb search with custom styling.
"""

import os
import asyncio
import streamlit as st
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, AIMessage
from mcp_use import MCPAgent, MCPClient

# Load environment variables
load_dotenv()

# Set page configuration
st.set_page_config(
    page_title="Airbnb Search Assistant",
    page_icon="🏠",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        background-color: #ffffff;
    }
    .stTitle {
        color: #FF385C !important;
        font-family: 'Circular', -apple-system, BlinkMacSystemFont, Roboto, Helvetica Neue, sans-serif;
    }
    .stButton>button {
        background-color: #FF385C;
        color: white;
        border-radius: 8px;
        border: none;
        padding: 8px 16px;
    }
    .stButton>button:hover {
        background-color: #E61E4D;
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 0.5rem;
        margin-bottom: 1rem;
        display: flex;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    .user-message {
        background-color: #F7F7F7;
    }
    .assistant-message {
        background-color: #FFF8F6;
    }
    .feature-card {
        background-color: white;
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []
if "use_mcp" not in st.session_state:
    st.session_state.use_mcp = True

# Initialize chat models
@st.cache_resource
def init_models():
    try:
        # Try to initialize MCP agent
        client = MCPClient.from_config_file(os.path.join(os.path.dirname(__file__), "airbnb_mcp.json"))
        llm = ChatOpenAI(model="gpt-4o-mini")
        agent = MCPAgent(llm=llm, client=client, max_steps=30)
        return {"agent": agent, "chat": llm}
    except Exception as e:
        st.warning("⚠️ MCP connection failed. Falling back to basic chat mode.")
        return {"chat": ChatOpenAI(model="gpt-4o-mini")}

# Create the Streamlit interface
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.title("🏠 Airbnb Search Assistant")
    st.write("Let me help you find the perfect place to stay!")

    # Feature cards
    st.markdown("""
    <div class="feature-card">
        <h3>🌟 Popular Features</h3>
        <ul>
            <li>Search properties worldwide</li>
            <li>Filter by amenities and preferences</li>
            <li>Get personalized recommendations</li>
            <li>Compare prices and reviews</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

    # Example queries section
    with st.expander("📝 Example Queries"):
        st.markdown("""
        Try asking questions like:
        - Find me a beachfront villa in Bali for 4 people
        - Show luxury apartments in Paris with Eiffel Tower views
        - Search for pet-friendly houses in London with a garden
        - Find me a place in Tokyo near public transport
        """)

# Display chat history with custom styling
for message in st.session_state.messages:
    message_class = "user-message" if message["role"] == "user" else "assistant-message"
    with st.container():
        st.markdown(f"""
            <div class="chat-message {message_class}">
                <div>{message["content"]}</div>
            </div>
        """, unsafe_allow_html=True)

# Chat input
if prompt := st.chat_input("What kind of place are you looking for?"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Initialize models
    models = init_models()

    # Get response
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching for perfect matches..."):
            try:
                if "agent" in models and st.session_state.use_mcp:
                    # Try using MCP agent
                    response = asyncio.run(models["agent"].run(prompt))
                else:
                    # Fallback to basic chat
                    messages = [
                        HumanMessage(content="You are an Airbnb search assistant. Help users find accommodations and provide detailed responses about properties, including amenities, location benefits, and pricing when possible. Current query: " + prompt)
                    ]
                    response = models["chat"].invoke(messages).content

                st.markdown(response)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
                if st.session_state.use_mcp:
                    st.session_state.use_mcp = False
                    st.warning("Switching to basic chat mode for better stability.")
                    st.rerun()

# Footer with clear chat button and additional info
col1, col2, col3 = st.columns([2, 1, 2])
with col2:
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# Add footer with Airbnb-style information
st.markdown("""
    <div style='text-align: center; color: #717171; padding: 20px;'>
        <p>This is an AI-powered search assistant. Results and availability may vary.</p>
        <p style='font-size: 12px;'>Powered by MCP and OpenAI</p>
    </div>
""", unsafe_allow_html=True) 