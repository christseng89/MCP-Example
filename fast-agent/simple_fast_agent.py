#!/usr/bin/env python3
"""
Simple Fast-Agent Example
==========================

A minimal example showing how to create and use a fast-agent.

Usage:
    uv run simple_fast_agent.py
    # or 
    python simple_fast_agent.py
"""

import asyncio
from fastagent import FastAgent

# Create a simple agent
fast = FastAgent("Simple MCP Assistant")

@fast.agent(
    instruction="You are a helpful assistant that explains MCP concepts clearly and concisely."
)
async def main():
    """Simple agent that can answer MCP questions."""
    async with fast.run() as agent:
        # Single query example
        response = await agent("What is MCP in simple terms?")
        print(f"🤖 Agent: {response}")
        
        # Interactive mode (uncomment to enable)
        # print("\n💬 Starting interactive chat...")
        # await agent.interactive()

if __name__ == "__main__":
    print("🚀 Simple Fast-Agent MCP Example")
    print("=" * 40)
    asyncio.run(main())
