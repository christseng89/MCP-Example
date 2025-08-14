#!/usr/bin/env python3
"""
Fast-Agent Setup and Configuration Example (Corrected)
======================================================

This script demonstrates different ways to set up and configure fast-agent-mcp
for MCP development and usage.

Installation:
    uv pip install fast-agent-mcp

Usage:
    uv run setup_fast_agent.py
"""

import asyncio
import os
from typing import Optional
from pathlib import Path
from mcp_agent.core.fastagent import FastAgent

def setup_environment():
    """Setup environment variables and configuration for fast-agent."""
    
    print("🔧 Setting up Fast-Agent Environment")
    print("=" * 40)
    
    # Check for environment variables
    env_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for GPT models',
        'ANTHROPIC_API_KEY': 'Anthropic API key for Claude models',
        'FAST_AGENT_MODEL': 'Default model to use (e.g., gpt-4, sonnet)',
        'FAST_AGENT_LOG_LEVEL': 'Logging level (DEBUG, INFO, WARNING, ERROR)'
    }
    
    print("Checking environment variables:")
    for var, description in env_vars.items():
        value = os.getenv(var)
        status = "✅ Set" if value else "❌ Not set"
        print(f"  {var}: {status} - {description}")
    
    print("\n💡 Tip: Create a .env file with your API keys:")
    print("OPENAI_API_KEY=your_openai_key_here")
    print("ANTHROPIC_API_KEY=your_anthropic_key_here")
    print("FAST_AGENT_MODEL=sonnet")
    print()

def create_agent_configs():
    """Create different agent configurations for various use cases."""
    
    configs = {
        'basic': {
            'name': 'Basic Assistant',
            'instruction': 'You are a helpful AI assistant.',
        },
        'mcp_expert': {
            'name': 'MCP Expert',
            'instruction': '''You are an expert in Model Context Protocol (MCP).
            
            Provide detailed, technical guidance on:
            - MCP server development and deployment
            - MCP client integration
            - Best practices and security considerations
            - Troubleshooting common MCP issues
            
            Always include practical code examples and step-by-step instructions.''',
        },
        'code_reviewer': {
            'name': 'Code Reviewer',
            'instruction': '''You are an expert code reviewer specializing in Python and MCP development.
            
            When reviewing code:
            - Check for security vulnerabilities
            - Suggest performance improvements
            - Ensure proper error handling
            - Verify MCP protocol compliance
            - Recommend best practices
            
            Provide constructive, specific feedback with examples.''',
        }
    }
    
    return configs

async def demo_basic_setup():
    """Demonstrate basic fast-agent setup."""
    
    print("📝 Basic Fast-Agent Setup Demo")
    print("-" * 30)
    
    try:
        # Simple agent creation
        fast = FastAgent("Demo Agent")
        
        @fast.agent(instruction="You are a friendly assistant that explains things clearly.")
        async def basic_demo():
            async with fast.run() as agent:
                response = await agent("Explain what fast-agent is in one sentence.")
                return response
        
        result = await basic_demo()
        print(f"🤖 Response: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have a valid API key configured!")
        print("💡 Install the package: uv pip install fast-agent-mcp")

async def demo_mcp_expert():
    """Demonstrate MCP expert agent."""
    
    print("\n🔬 MCP Expert Agent Demo")
    print("-" * 30)
    
    try:
        fast = FastAgent("MCP Expert")
        
        @fast.agent(
            instruction="""You are an expert in Model Context Protocol (MCP).
            Provide clear, concise explanations about MCP concepts, implementation, and best practices."""
        )
        async def mcp_expert():
            async with fast.run() as agent:
                questions = [
                    "What is MCP and why is it important?",
                    "How do I create a basic MCP server?",
                    "What are common MCP security considerations?"
                ]
                
                for question in questions:
                    print(f"\n❓ Question: {question}")
                    try:
                        response = await agent(question)
                        print(f"🤖 Expert: {response[:200]}...")  # Truncate for demo
                    except Exception as e:
                        print(f"❌ Error: {e}")
        
        await mcp_expert()
        
    except Exception as e:
        print(f"❌ MCP Expert demo error: {e}")

async def demo_official_setup():
    """Demonstrate the official fast-agent setup process."""
    
    print("\n🏗️  Official Fast-Agent Setup Demo")
    print("-" * 30)
    
    print("The official setup process involves:")
    print("1. uv pip install fast-agent-mcp")
    print("2. uv run fast-agent setup  # Creates agent.py and config files")
    print("3. uv run agent.py          # Runs the generated agent")
    print()
    print("You can also use quickstart for workflows:")
    print("uv run fast-agent quickstart workflow")
    print()
    
    # Demonstrate a simple version of what setup creates
    sample_agent_code = '''
# Sample agent.py (similar to what fast-agent setup creates)
import asyncio
from mcp_agent.core.fastagent import FastAgent

fast = FastAgent("Generated Agent")

@fast.agent(
    instruction="You are a helpful assistant."
)
async def main():
    async with fast.run() as agent:
        await agent.interactive()

if __name__ == "__main__":
    asyncio.run(main())
    '''
    
    print("Sample generated agent.py:")
    print(sample_agent_code)

def create_sample_env_file():
    """Create a sample .env file for configuration."""
    
    env_content = """# Fast-Agent Configuration
# Copy this file to .env and add your actual API keys

# OpenAI Configuration (for GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Configuration (for Claude models)  
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Default model to use (common options: gpt-4, sonnet, haiku)
FAST_AGENT_MODEL=sonnet

# Logging level
FAST_AGENT_LOG_LEVEL=INFO

# Optional: Custom endpoint URLs
# OPENAI_BASE_URL=https://api.openai.com/v1
# ANTHROPIC_BASE_URL=https://api.anthropic.com
"""
    
    sample_path = Path('.env.sample')
    sample_path.write_text(env_content)
    print(f"📄 Created sample environment file: {sample_path}")
    print("💡 Copy this to .env and add your actual API keys!")

async def interactive_setup():
    """Interactive setup wizard for fast-agent."""
    
    print("\n🧙 Interactive Fast-Agent Setup Wizard")
    print("=" * 40)
    
    try:
        # Get user preferences
        name = input("Enter a name for your agent: ").strip() or "My Agent"
        
        print("\nChoose an agent type:")
        print("1. General Assistant")
        print("2. MCP Expert")
        print("3. Size Estimator")
        print("4. Custom")
        
        choice = input("Enter choice (1-4): ").strip() or "1"
        
        if choice == "1":
            instruction = "You are a helpful AI assistant."
        elif choice == "2":
            instruction = "You are an expert in Model Context Protocol (MCP). Provide clear, detailed guidance."
        elif choice == "3":
            instruction = "Given an object, respond only with an estimate of its size."
        else:
            instruction = input("Enter custom instruction: ").strip() or "You are a helpful assistant."
        
        # Create and test the agent
        fast = FastAgent(name)
        
        @fast.agent(instruction=instruction)
        async def custom_agent():
            async with fast.run() as agent:
                print(f"\n🤖 {name} is ready!")
                test_query = "Hello! Please introduce yourself."
                response = await agent(test_query)
                print(f"🤖 {name}: {response}")
                
                # Optional interactive mode
                if input("\nStart interactive chat? (y/N): ").lower().startswith('y'):
                    await agent.interactive()
        
        await custom_agent()
        
    except KeyboardInterrupt:
        print("\n👋 Setup cancelled.")
    except Exception as e:
        print(f"❌ Setup error: {e}")

async def main():
    """Main setup and demo function."""
    
    print("🚀 Fast-Agent Setup and Configuration (Corrected)")
    print("=" * 50)
    print("Package: fast-agent-mcp")
    print("Import: from mcp_agent.core.fastagent import FastAgent")
    print()
    
    # Setup environment
    setup_environment()
    
    # Create sample env file
    create_sample_env_file()
    
    print("\nChoose a demo:")
    print("1. Basic Setup Demo")
    print("2. MCP Expert Demo") 
    print("3. Official Setup Process")
    print("4. Interactive Setup Wizard")
    print("5. Run All Demos")
    
    try:
        choice = input("\nEnter choice (1-5): ").strip() or "1"
        
        if choice == "1":
            await demo_basic_setup()
        elif choice == "2":
            await demo_mcp_expert()
        elif choice == "3":
            await demo_official_setup()
        elif choice == "4":
            await interactive_setup()
        elif choice == "5":
            await demo_basic_setup()
            await demo_mcp_expert()
            await demo_official_setup()
        else:
            print("Invalid choice, running basic demo...")
            await demo_basic_setup()
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled.")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("\n💡 Tips:")
        print("- Make sure you have fast-agent-mcp installed: uv pip install fast-agent-mcp")
        print("- Set up your API keys in a .env file")
        print("- Check the sample configuration files")

if __name__ == "__main__":
    asyncio.run(main())