# Fast-Agent Python Examples

This directory contains comprehensive examples for using the **fast-agent** framework to create AI agents that work with MCP (Model Context Protocol).

## 🎯 What is Fast-Agent?

Fast-Agent is a Python framework for building AI agents quickly and efficiently. It provides a simple, decorator-based approach to creating agents that can:

- Interact with multiple LLM providers (OpenAI, Anthropic, etc.)
- Handle both single queries and interactive conversations
- Process multiple queries in batch
- Integrate with MCP (Model Context Protocol) services

## 📁 Example Files

### 1. `simple_fast_agent.py` 
**Simplest possible example** - A minimal fast-agent implementation to get you started.

```python
from fastagent import FastAgent

fast = FastAgent("Simple Assistant")

@fast.agent(instruction="You are helpful.")
async def main():
    async with fast.run() as agent:
        response = await agent("What is MCP?")
        print(response)
```

### 2. `fast_agent_example.py`
**Comprehensive example** with multiple agent patterns:
- Basic interactive agent
- Specialized agents for different tasks
- Batch processing capabilities
- Model-specific configurations

### 3. `mcp_server_agent.py`
**MCP-specialized agent** that helps you create and understand MCP servers:
- Interactive MCP server builder
- Quick example generation
- Practical code examples with explanations

### 4. `setup_fast_agent.py`
**Setup and configuration** examples:
- Environment setup
- Different agent configurations
- Interactive setup wizard
- Batch processing demos

## 🚀 Quick Start

### Installation

Using UV (recommended) [[memory:3183744]]:
```bash
uv add fast-agent --dev
```

Or using pip:
```bash
pip install fast-agent
```

### Basic Usage

1. **Install dependencies**:
   ```bash
   uv run pip install -r requirements.txt
   ```

2. **Set up API keys** (copy `.env.sample` to `.env` and add your keys):
   ```bash
   OPENAI_API_KEY=your_openai_key
   ANTHROPIC_API_KEY=your_anthropic_key
   ```

3. **Run a simple example**:
   ```bash
   uv run simple_fast_agent.py
   ```

4. **Try the interactive examples**:
   ```bash
   uv run fast_agent_example.py
   uv run mcp_server_agent.py
   uv run setup_fast_agent.py
   ```

## 🎮 Usage Patterns

### Single Query
```python
async with fast.run() as agent:
    response = await agent("Your question here")
    print(response)
```

### Interactive Chat
```python
async with fast.run() as agent:
    await agent.interactive()  # Starts chat loop
```

### Batch Processing
```python
async with fast.run() as agent:
    queries = ["Question 1", "Question 2", "Question 3"]
    for query in queries:
        response = await agent(query)
        print(f"Q: {query}\nA: {response}\n")
```

### Model Selection
```python
async with fast.run(model="gpt-4") as agent:
    response = await agent("Complex question requiring GPT-4")
```

## 🛠 MCP Integration

These examples are designed to work with MCP (Model Context Protocol) systems:

- **MCP Server Creation**: Use `mcp_server_agent.py` to learn about building MCP servers
- **MCP Best Practices**: Get guidance on security and performance
- **MCP Troubleshooting**: Debug common issues with MCP implementations

## 🔧 Configuration Options

### Agent Instructions
Define your agent's behavior:
```python
@fast.agent(
    instruction="""You are an expert in MCP development.
    
    Provide:
    - Working code examples
    - Best practices
    - Security recommendations
    - Step-by-step guides"""
)
```

### Environment Variables
- `OPENAI_API_KEY` - For GPT models
- `ANTHROPIC_API_KEY` - For Claude models  
- `FAST_AGENT_MODEL` - Default model (e.g., "gpt-4", "claude-3-sonnet")
- `FAST_AGENT_LOG_LEVEL` - Logging level

### Model Options
- `gpt-3.5-turbo` - Fast, cost-effective
- `gpt-4` - More capable, slower
- `gpt-4-turbo` - Latest GPT-4 variant
- `claude-3-sonnet` - Anthropic's balanced model
- `claude-3-opus` - Anthropic's most capable model

## 🔍 Example Use Cases

1. **MCP Learning Assistant**: Interactive agent that teaches MCP concepts
2. **Code Review Agent**: Reviews Python/MCP code for best practices
3. **Documentation Generator**: Creates MCP server documentation
4. **Batch Query Processor**: Processes multiple MCP-related questions
5. **Setup Assistant**: Helps configure MCP development environment

## 🚨 Error Handling

Common issues and solutions:

**"No API key found"**
- Set up your `.env` file with valid API keys
- Check environment variable names

**"Model not found"**
- Verify model name spelling
- Check if you have access to the specified model

**"Connection error"**
- Verify internet connection
- Check API service status

## 📚 Further Reading

- [Fast-Agent Documentation](https://fast-agent.ai)
- [MCP Official Docs](https://modelcontextprotocol.io)
- [OpenAI API Docs](https://platform.openai.com/docs)
- [Anthropic API Docs](https://docs.anthropic.com)

## 🤝 Contributing

Feel free to:
- Add more examples
- Improve existing code
- Fix bugs or issues
- Enhance documentation

## 📄 License

These examples are provided for educational purposes and follow the project's license terms.
