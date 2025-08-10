#!/usr/bin/env python3
"""
Fast-Agent Setup and Configuration Example
==========================================

This script demonstrates different ways to set up and configure fast-agent
for MCP development and usage.

Usage:
    uv run setup_fast_agent.py
"""

import asyncio
import os
from typing import Optional
from pathlib import Path
from fastagent import FastAgent

def setup_environment():
    """Setup environment variables and configuration for fast-agent."""
    
    print("🔧 Setting up Fast-Agent Environment")
    print("=" * 40)
    
    # Check for environment variables
    env_vars = {
        'OPENAI_API_KEY': 'OpenAI API key for GPT models',
        'ANTHROPIC_API_KEY': 'Anthropic API key for Claude models',
        'FAST_AGENT_MODEL': 'Default model to use (e.g., gpt-4, claude-3-sonnet)',
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
    print("FAST_AGENT_MODEL=gpt-4")
    print()

def create_agent_configs():
    """Create different agent configurations for various use cases."""
    
    configs = {
        'basic': {
            'name': 'Basic Assistant',
            'instruction': 'You are a helpful AI assistant.',
            'model': 'gpt-3.5-turbo'
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
            'model': 'gpt-4'
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
            'model': 'gpt-4'
        }
    }
    
    return configs

async def demo_basic_setup():
    """Demonstrate basic fast-agent setup."""
    
    print("📝 Basic Fast-Agent Setup Demo")
    print("-" * 30)
    
    # Simple agent creation
    fast = FastAgent("Demo Agent")
    
    @fast.agent(instruction="You are a friendly assistant that explains things clearly.")
    async def basic_demo():
        async with fast.run() as agent:
            response = await agent("Explain what fast-agent is in one sentence.")
            return response
    
    try:
        result = await basic_demo()
        print(f"🤖 Response: {result}")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you have a valid API key configured!")

async def demo_configured_agents():
    """Demonstrate agents with different configurations."""
    
    print("\n⚙️  Configured Agents Demo")
    print("-" * 30)
    
    configs = create_agent_configs()
    
    for config_name, config in configs.items():
        print(f"\n🔧 Testing {config['name']}...")
        
        try:
            fast = FastAgent(config['name'])
            
            @fast.agent(
                instruction=config['instruction']
            )
            async def configured_agent():
                async with fast.run(model=config.get('model', 'gpt-3.5-turbo')) as agent:
                    if config_name == 'basic':
                        return await agent("Hello! What can you do?")
                    elif config_name == 'mcp_expert':
                        return await agent("What is MCP and why is it important?")
                    elif config_name == 'code_reviewer':
                        return await agent("What should I look for when reviewing MCP server code?")
            
            response = await configured_agent()
            print(f"   Response: {response[:100]}...")  # Truncate for demo
            
        except Exception as e:
            print(f"   ❌ Error: {e}")
            continue

async def demo_batch_processing():
    """Demonstrate batch processing with fast-agent."""
    
    print("\n📦 Batch Processing Demo")
    print("-" * 30)
    
    fast = FastAgent("Batch Processor")
    
    @fast.agent(
        instruction="Answer questions about MCP concisely and accurately."
    )
    async def batch_processor():
        queries = [
            "What does MCP stand for?",
            "Who created MCP?",
            "What are MCP servers?",
            "How do I install MCP?"
        ]
        
        async with fast.run() as agent:
            print("Processing queries...")
            results = []
            
            for i, query in enumerate(queries, 1):
                try:
                    response = await agent(query)
                    results.append(f"Q{i}: {query}\nA{i}: {response}\n")
                    print(f"  ✅ Processed query {i}")
                except Exception as e:
                    results.append(f"Q{i}: {query}\nA{i}: Error - {e}\n")
                    print(f"  ❌ Error on query {i}")
            
            return results
    
    try:
        results = await batch_processor()
        print("\n📋 Batch Results:")
        for result in results[:2]:  # Show first 2 results
            print(result)
    except Exception as e:
        print(f"❌ Batch processing error: {e}")

def create_sample_env_file():
    """Create a sample .env file for configuration."""
    
    env_content = """# Fast-Agent Configuration
# Copy this file to .env and add your actual API keys

# OpenAI Configuration (for GPT models)
OPENAI_API_KEY=your_openai_api_key_here

# Anthropic Configuration (for Claude models)
ANTHROPIC_API_KEY=your_anthropic_api_key_here

# Default model to use
FAST_AGENT_MODEL=gpt-3.5-turbo

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
        print("3. Code Reviewer")
        print("4. Custom")
        
        choice = input("Enter choice (1-4): ").strip() or "1"
        
        configs = create_agent_configs()
        if choice == "1":
            config = configs['basic']
        elif choice == "2":
            config = configs['mcp_expert']
        elif choice == "3":
            config = configs['code_reviewer']
        else:
            instruction = input("Enter custom instruction: ").strip()
            config = {
                'name': name,
                'instruction': instruction or 'You are a helpful assistant.',
                'model': 'gpt-3.5-turbo'
            }
        
        # Create and test the agent
        fast = FastAgent(name)
        
        @fast.agent(instruction=config['instruction'])
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
    
    print("🚀 Fast-Agent Setup and Configuration")
    print("=" * 50)
    
    # Setup environment
    setup_environment()
    
    # Create sample env file
    create_sample_env_file()
    
    print("\nChoose a demo:")
    print("1. Basic Setup Demo")
    print("2. Configured Agents Demo") 
    print("3. Batch Processing Demo")
    print("4. Interactive Setup Wizard")
    print("5. Run All Demos")
    
    try:
        choice = input("\nEnter choice (1-5): ").strip() or "1"
        
        if choice == "1":
            await demo_basic_setup()
        elif choice == "2":
            await demo_configured_agents()
        elif choice == "3":
            await demo_batch_processing()
        elif choice == "4":
            await interactive_setup()
        elif choice == "5":
            await demo_basic_setup()
            await demo_configured_agents()
            await demo_batch_processing()
        else:
            print("Invalid choice, running basic demo...")
            await demo_basic_setup()
            
    except KeyboardInterrupt:
        print("\n👋 Demo cancelled.")
    except Exception as e:
        print(f"❌ Demo error: {e}")
        print("\n💡 Tips:")
        print("- Make sure you have fast-agent installed: pip install fast-agent")
        print("- Set up your API keys in a .env file")
        print("- Check the sample configuration files")

if __name__ == "__main__":
    asyncio.run(main())
