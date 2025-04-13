"""
Simple chatbot example using MCP tools.

This example demonstrates how to create a basic chatbot that can handle
conversations and perform various tasks using MCP tools.
"""

import asyncio
import os
import sys
import warnings

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

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


async def run_chatbot():
    """Run the chatbot in interactive mode."""
    chatbot = SimpleChatbot()
    print("\nWelcome to Simple Chatbot!")
    print("Type 'quit' or 'exit' to end the conversation.")
    
    try:
        while True:
            # Get user input
            user_input = input("\nYou: ").strip()
            
            # Check for exit commands
            if user_input.lower() in ['quit', 'exit']:
                print("Goodbye!")
                break
                
            # Process the message and get response
            response = await chatbot.process_message(user_input)
            print(f"\nBot: {response}")
            
    finally:
        # Clean up resources
        await chatbot.close()


def main():
    """Main entry point."""
    # Suppress resource warnings
    warnings.filterwarnings("ignore", category=ResourceWarning)
    
    try:
        asyncio.run(run_chatbot())
    except KeyboardInterrupt:
        print("\nProgram interrupted by user")
    except Exception as e:
        print(f"\nAn error occurred: {e}")


if __name__ == "__main__":
    main()
