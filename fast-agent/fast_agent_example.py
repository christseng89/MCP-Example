#!/usr/bin/env python3
"""
Fast-Agent Python Example
=========================

This example demonstrates how to use the fast-agent framework to create
AI agents that can integrate with MCP (Model Context Protocol) services.

Requirements:
- fast-agent library
- Python 3.8+
- UV package manager (recommended)

Usage:
    uv run fast_agent_example.py
    # or
    python fast_agent_example.py
"""

import asyncio
import logging
from typing import Optional
from fastagent import FastAgent

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


def create_advanced_agent_example():
    """Advanced fast-agent example with multiple specialized agents."""
    
    # Create the main FastAgent application
    fast = FastAgent("Advanced MCP Toolkit")
    
    @fast.agent(
        instruction="""You are a Python development assistant specialized in MCP integration.
        
        Focus on:
        - Writing Python code for MCP servers and clients
        - Explaining MCP Python SDK usage
        - Debugging MCP connection issues
        - Performance optimization for MCP implementations
        
        Always provide working code examples with proper error handling."""
    )
    async def python_mcp_agent():
        """Agent specialized in Python MCP development."""
        async with fast.run() as agent:
            return await agent("Help me create a Python MCP server")
    
    @fast.agent(
        instruction="""You are a security consultant for MCP implementations.
        
        Your expertise includes:
        - MCP server security best practices
        - API key management and rotation
        - Permission and access control for MCP servers
        - Identifying and mitigating security risks in MCP deployments
        
        Provide actionable security recommendations with specific implementation steps."""
    )
    async def security_mcp_agent():
        """Agent specialized in MCP security."""
        async with fast.run() as agent:
            return await agent("What are the main security risks when using MCP servers?")
    
    return python_mcp_agent, security_mcp_agent


async def interactive_agent_demo():
    """Demonstration of interactive agent capabilities."""
    
    fast = FastAgent("Interactive MCP Demo")
    
    @fast.agent(
        instruction="""You are an interactive MCP learning assistant.
        
        Help users learn MCP step by step:
        1. Start with basic concepts
        2. Progress to practical implementations
        3. Provide hands-on examples
        4. Answer follow-up questions
        
        Use emojis and clear formatting. Be encouraging and supportive."""
    )
    async def interactive_demo():
        async with fast.run() as agent:
            print("🎓 Welcome to the Interactive MCP Learning Assistant!")
            print("I'll help you learn Model Context Protocol step by step.\n")
            
            # Start with an introduction
            intro_response = await agent(
                "Give me a friendly introduction to MCP and ask what I'd like to learn first."
            )
            print(f"🤖 Assistant: {intro_response}\n")
            
            # Interactive learning loop
            await agent.interactive()
    
    await interactive_demo()


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
                response = await agent(query)
                print(f"🤖 Response: {response}\n")
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
        async with fast.run(model="gpt-4") as agent:  # Specify model
            query = "Create a quick start guide for setting up MCP with Claude Desktop"
            response = await agent(query)
            print("📚 Generated Documentation:")
            print("=" * 50)
            print(response)
    
    await documentation_agent()


async def main():
    """Main function demonstrating various fast-agent usage patterns."""
    
    print("🚀 Fast-Agent MCP Examples")
    print("=" * 50)
    
    try:
        # Example 1: Basic interactive agent
        print("\n1️⃣  Basic Interactive Agent Demo")
        basic_agent = create_basic_agent_example()
        # Uncomment the line below to run the interactive demo
        # await basic_agent()
        
        # Example 2: Advanced specialized agents
        print("\n2️⃣  Advanced Specialized Agents Demo")
        python_agent, security_agent = create_advanced_agent_example()
        
        print("Python MCP Agent Response:")
        python_response = await python_agent()
        print(python_response)
        
        print("\nSecurity MCP Agent Response:")
        security_response = await security_agent()
        print(security_response)
        
        # Example 3: Batch processing
        print("\n3️⃣  Batch Processing Demo")
        await batch_processing_example()
        
        # Example 4: Model-specific usage
        print("\n4️⃣  Model-Specific Demo")
        await model_specific_example()
        
        # Example 5: Interactive learning (uncomment to enable)
        # print("\n5️⃣  Interactive Learning Demo")
        # await interactive_agent_demo()
        
    except Exception as e:
        logger.error(f"Error in main execution: {e}")
        print(f"❌ An error occurred: {e}")


if __name__ == "__main__":
    print("🎯 Starting Fast-Agent MCP Examples...")
    print("Note: Make sure you have the 'fast-agent' library installed:")
    print("   pip install fast-agent")
    print("   # or")
    print("   uv add fast-agent")
    print()
    
    asyncio.run(main())
