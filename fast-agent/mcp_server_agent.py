#!/usr/bin/env python3
"""
MCP Server Creation Agent
=========================

A specialized fast-agent example for creating MCP servers.

This agent helps users understand and create MCP (Model Context Protocol) servers
with practical code examples and best practices.

Usage:
    uv run mcp_server_agent.py
"""

import asyncio
import json
from typing import Dict, Any
from fastagent import FastAgent

# Create a specialized MCP server development agent
fast = FastAgent("MCP Server Builder")

@fast.agent(
    instruction="""You are an expert MCP (Model Context Protocol) server developer.

Your expertise includes:
- Creating MCP servers using Python
- Understanding MCP protocol specifications
- Implementing tools, resources, and prompts in MCP servers
- Best practices for MCP server architecture
- Debugging MCP server implementations
- Performance optimization for MCP servers

Always provide:
1. Working code examples with proper imports
2. Clear explanations of MCP concepts
3. Step-by-step implementation guidance
4. Security considerations
5. Testing recommendations

Format your responses with clear markdown structure and include practical examples."""
)
async def mcp_server_builder():
    """Agent specialized in MCP server development."""
    
    async with fast.run() as agent:
        print("🛠️  MCP Server Builder Assistant")
        print("=" * 50)
        print("I'll help you create and understand MCP servers!")
        print("Ask me about:")
        print("• Creating basic MCP servers")
        print("• Implementing MCP tools and resources")
        print("• MCP server best practices")
        print("• Debugging MCP implementations")
        print("\nType 'examples' for common use cases or 'exit' to quit")
        print("-" * 50)
        
        # Predefined examples
        examples = {
            "basic": "Create a basic MCP server with a simple tool",
            "file": "Create an MCP server that can read and write files",
            "api": "Create an MCP server that calls external APIs",
            "database": "Create an MCP server that connects to a database",
            "resources": "Create an MCP server that provides resources",
            "prompts": "Create an MCP server with prompt templates"
        }
        
        while True:
            try:
                user_input = input("\n💬 You: ").strip()
                
                if user_input.lower() in ['exit', 'quit', 'bye']:
                    print("👋 Happy coding! Remember to test your MCP servers thoroughly.")
                    break
                
                if user_input.lower() == 'examples':
                    print("\n📚 Available Examples:")
                    for key, desc in examples.items():
                        print(f"   • '{key}': {desc}")
                    print("\nJust type the example name to get started!")
                    continue
                
                # Handle predefined examples
                if user_input.lower() in examples:
                    query = examples[user_input.lower()]
                    print(f"\n🔍 Generating: {query}")
                else:
                    query = user_input
                
                if query:
                    response = await agent(query)
                    print(f"\n🤖 MCP Expert: {response}")
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print("Please try again or type 'exit' to quit.")

async def quick_mcp_examples():
    """Generate quick MCP server examples."""
    
    fast_quick = FastAgent("Quick MCP Examples")
    
    @fast_quick.agent(
        instruction="""Generate concise, working MCP server code examples.
        
        Focus on:
        - Minimal, functional code
        - Clear comments explaining key concepts
        - Proper error handling
        - Standard MCP patterns
        
        Keep examples under 50 lines when possible."""
    )
    async def quick_examples():
        async with fast_quick.run() as agent:
            examples = [
                "Simple calculator tool MCP server",
                "File reader MCP server",
                "Weather API MCP server"
            ]
            
            print("⚡ Quick MCP Server Examples")
            print("=" * 40)
            
            for i, example in enumerate(examples, 1):
                print(f"\n{i}. {example}")
                print("-" * 30)
                response = await agent(f"Create a {example}")
                print(response)
                print()
    
    await quick_examples()

async def main():
    """Main function with different agent modes."""
    
    print("🎯 MCP Server Agent Examples")
    print("Choose a mode:")
    print("1. Interactive MCP Server Builder")
    print("2. Quick Examples Generation")
    print("3. Both (examples first, then interactive)")
    
    try:
        choice = input("\nEnter choice (1-3): ").strip()
        
        if choice == "1":
            await mcp_server_builder()
        elif choice == "2":
            await quick_mcp_examples()
        elif choice == "3":
            await quick_mcp_examples()
            print("\n" + "="*50)
            await mcp_server_builder()
        else:
            print("Invalid choice. Running interactive mode...")
            await mcp_server_builder()
            
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(main())
