#!/usr/bin/env python3
"""
Fast-Agent Python Example (Corrected)
======================================

This example demonstrates how to use the fast-agent-mcp framework to create
AI agents that can integrate with MCP (Model Context Protocol) services.

Requirements:
- fast-agent-mcp library
- Python 3.8+
- UV package manager (recommended)

Installation:
    uv pip install fast-agent-mcp

Usage:
    uv run fast_agent_example.py
    # or
    python fast_agent_example.py
"""

import asyncio
import logging
from typing import Optional
from mcp_agent.core.fastagent import FastAgent

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_basic_agent_example():
    """Basic fast-agent example with simple instructions."""
    
    # Create the FastAgent application
    fast = FastAgent("Basic MCP Assistant")
    
    @fast.agent(
        instruction="""You are an AI assistant specializing in MCP (Model Context Protocol) guidance.
        
        Your role is to:
        - Explain MCP concepts clearly
        - Help users understand how to integrate MCP servers
        - Provide practical examples for MCP implementations
        - Suggest best practices for MCP security
        
        Keep responses concise but informative, using markdown formatting when helpful."""
    )
    async def basic_agent():
        """Basic agent that can answer MCP-related questions."""
        async with fast.run() as agent:
            print("🤖 Basic MCP Assistant is ready!")
            print("Ask me anything about Model Context Protocol...")
            print("Type 'exit' to quit\n")
            
            while True:
                try:
                    user_input = input("You: ").strip()
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        print("👋 Goodbye!")
                        break
                    
                    if user_input:
                        response = await agent(user_input)
                        print(f"🤖 Assistant: {response}\n")
                    
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    logger.error(f"Error: {e}")
                    print(f"❌ Sorry, an error occurred: {e}\n")
    
    return basic_agent


async def batch_processing_example():
    """Example of processing multiple queries with fast-agent."""
    
    fast = FastAgent("MCP Batch Processor")
    
    @fast.agent(
        instruction="""Process MCP-related queries efficiently.
        
        For each query:
        - Provide concise, accurate information
        - Include relevant examples if applicable
        - Format responses consistently
        - Focus on practical, actionable advice"""
    )
    async def batch_processor():
        async with fast.run() as agent:
            queries = [
                "What is MCP?",
                "How do I install an MCP server?",
                "What are the security risks of MCP?",
                "How do I create a custom MCP server?",
                "What's the difference between MCP client and server?"
            ]
            
            print("🔄 Processing batch queries about MCP...\n")
            
            for i, query in enumerate(queries, 1):
                print(f"📝 Query {i}: {query}")
                try:
                    response = await agent(query)
                    print(f"🤖 Response: {response}\n")
                except Exception as e:
                    print(f"❌ Error: {e}\n")
                print("-" * 60 + "\n")
    
    await batch_processor()


async def model_specific_example():
    """Example showing how to use specific models with fast-agent."""
    
    fast = FastAgent("Model-Specific MCP Assistant")
    
    @fast.agent(
        instruction="""You are a technical documentation assistant for MCP.
        
        Generate clear, comprehensive documentation including:
        - Step-by-step tutorials
        - Code examples with comments
        - Best practice recommendations
        - Troubleshooting guides
        
        Format everything in proper markdown with appropriate headings."""
    )
    async def documentation_agent():
        try:
            # Try to use a specific model (you can change this)
            async with fast.run(model="sonnet") as agent:
                query = "Create a quick start guide for setting up MCP with Claude Desktop"
                response = await agent(query)
                print("📚 Generated Documentation:")
                print("=" * 50)
                print(response)
        except Exception as e:
            print(f"❌ Model-specific example error: {e}")
            print("💡 You might need to configure your API keys or use a different model")
    
    await documentation_agent()


async def size_estimator_example():
    """Example from the official fast-agent documentation."""
    
    fast = FastAgent("Size Estimator")
    
    @fast.agent(
        instruction="Given an object, respond only with an estimate of its size."
    )
    async def size_estimator():
        async with fast.run() as agent:
            print("📏 Size Estimator Agent")
            print("Ask me to estimate the size of anything!")
            print("Example: 'the moon', 'a basketball', 'the Eiffel Tower'")
            print("Type 'exit' to quit\n")
            
            while True:
                try:
                    user_input = input("Object to estimate: ").strip()
                    if user_input.lower() in ['exit', 'quit', 'bye']:
                        print("👋 Goodbye!")
                        break
                    
                    if user_input:
                        response = await agent(user_input)
                        print(f"📏 Size estimate: {response}\n")
                    
                except KeyboardInterrupt:
                    print("\n👋 Goodbye!")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}\n")
    
    await size_estimator()


async def main():
    """Main function demonstrating various fast-agent usage patterns."""
    
    print("🚀 Fast-Agent MCP Examples (Corrected)")
    print("=" * 50)
    print("Package: fast-agent-mcp")
    print("Import: from mcp_agent.core.fastagent import FastAgent")
    print()
    
    print("Choose an example to run:")
    print("1. Basic Interactive MCP Assistant")
    print("2. Batch Processing Demo")
    print("3. Model-Specific Demo")
    print("4. Size Estimator (Official Example)")
    print("5. Run All Examples")
    
    try:
        choice = input("\nEnter choice (1-5): ").strip() or "1"
        
        if choice == "1":
            basic_agent = create_basic_agent_example()
            await basic_agent()
        elif choice == "2":
            await batch_processing_example()
        elif choice == "3":
            await model_specific_example()
        elif choice == "4":
            await size_estimator_example()
        elif choice == "5":
            print("\n📦 Running batch processing first...")
            await batch_processing_example()
            print("\n📚 Running model-specific example...")
            await model_specific_example()
            print("\n🤖 Starting interactive assistant...")
            basic_agent = create_basic_agent_example()
            await basic_agent()
        else:
            print("Invalid choice, running basic demo...")
            basic_agent = create_basic_agent_example()
            await basic_agent()
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled.")
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"❌ An error occurred: {e}")
        print("\n💡 Make sure you have installed the package:")
        print("   uv pip install fast-agent-mcp")


if __name__ == "__main__":
    print("🎯 Starting Fast-Agent MCP Examples...")
    print("Installation command: uv pip install fast-agent-mcp")
    print()
    
    asyncio.run(main())