"""
Simple Gradio chatbot example using MCP tools.

This example demonstrates how to create a basic chatbot with a Gradio interface
that can handle conversations and perform various tasks using MCP tools.
"""

import os
import warnings
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import gradio as gr

from mcp_use import MCPAgent, MCPClient


class SimpleChatbot:
    """A simple chatbot that can handle conversations and perform tasks."""
    
    def __init__(self):
        """Initialize the chatbot with necessary components."""
        # Load environment variables
        load_dotenv()
        
        # Create MCPClient with configuration
        self.client = MCPClient.from_config_file(os.path.join(os.path.dirname(__file__), "airbnb_mcp.json"))
        # Create LLM - using GPT-4o-mini
        self.llm = ChatOpenAI(model="gpt-4o-mini")
        # Create agent with the client
        self.agent = MCPAgent(llm=self.llm, client=self.client, max_steps=30)
        
    async def process_message(self, message: str) -> str:
        """Process a user message and return a response."""
        try:
            result = await self.agent.run(message, max_steps=30)
            return str(result)
        except Exception as e:
            return f"Sorry, I encountered an error: {str(e)}"
    
    async def close(self):
        """Clean up resources."""
        if self.client.sessions:
            await self.client.close_all_sessions()


def create_chatbot_interface():
    """Create and launch the Gradio interface for the chatbot."""
    chatbot = SimpleChatbot()
    
    def respond(message, history):
        """Process the message and return the response."""
        import asyncio
        response = asyncio.run(chatbot.process_message(message))
        return response
    
    # Create the Gradio interface
    interface = gr.ChatInterface(
        fn=respond,
        title="Simple Chatbot",
        description="A simple chatbot that can handle conversations and perform tasks using MCP tools.",
        examples=["Hello!", "What can you do?", "Tell me about yourself"],
        theme=gr.themes.Soft()
    )
    
    return interface


def main():
    """Main entry point."""
    # Suppress resource warnings
    warnings.filterwarnings("ignore", category=ResourceWarning)
    
    # Create and launch the interface
    interface = create_chatbot_interface()
    interface.launch()


if __name__ == "__main__":
    main() 
