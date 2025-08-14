#!/usr/bin/env python3
"""
Simple Fast-Agent Example (Corrected)
======================================

A minimal example showing how to create and use a fast-agent with the correct package.

Installation:
    uv pip install fast-agent-mcp

Usage:
    uv run simple_fast_agent.py
    # or 
    python simple_fast_agent.py
"""

import asyncio
from mcp_agent.core.fastagent import FastAgent

# Create a simple agent
fast = FastAgent("Simple MCP Assistant")

@fast.agent(
    instruction="You are a helpful assistant that explains MCP (Model Context Protocol) concepts clearly and concisely."
)
async def main():
    """Simple agent that can answer MCP questions."""
    async with fast.run() as agent:
        print("🤖 Simple MCP Assistant is ready!")
        print("-" * 40)
        
        # Single query example
        response = await agent("What is MCP in simple terms?")
        print(f"🤖 Agent: {response}")
        
        print("\n💬 Starting interactive chat...")
        print("Type 'exit' to quit, or ask me about MCP!")
        
        # Interactive mode
        await agent.interactive()

if __name__ == "__main__":
    print("🚀 Simple Fast-Agent MCP Example")
    print("=" * 40)
    print("Make sure you have installed: uv pip install fast-agent-mcp")
    print()
    asyncio.run(main())