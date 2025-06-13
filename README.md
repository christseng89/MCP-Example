# MCP Multi-Tool Server

A comprehensive Model Context Protocol (MCP) server built with FastMCP that provides calculator tools, document resources, and prompt templates. This server demonstrates multiple MCP capabilities including tools, resources, and prompts in a single implementation.

## Features

### 🧮 Calculator Tools
- **Basic Operations**: Addition, subtraction, multiplication, division
- **Advanced Math**: Power, square root, factorial calculations  
- **Utility Functions**: Percentage calculations
- **Error Handling**: Division by zero protection, negative square root protection, factorial range limits

### 📖 Document Resources  
- **TypeScript SDK Resource**: Access to MCP TypeScript SDK documentation
- **Dynamic File Reading**: Reads from configurable file paths
- **Error Handling**: Graceful handling of missing files

### 📝 Prompt Templates
- **Meeting Summary Template**: Executive meeting summary generator
- **Variable Substitution**: Dynamic template variable replacement
- **Structured Output**: Professional meeting summary format

## Quick Start

### Prerequisites
- Python 3.12 or later
- `uv` package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd mcp-multi-tool-server
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Test the server**
   ```bash
   uv run mcp dev server.py
   ```
   
   Open http://localhost:3000 to test the server in MCP Inspector.

## Usage

### Calculator Tools

The server provides 8 calculator tools:

| Tool | Description | Example |
|------|-------------|---------|
| `add` | Add two numbers | `add(5, 3) → 8` |
| `subtract` | Subtract second from first | `subtract(10, 4) → 6` |
| `multiply` | Multiply two numbers | `multiply(6, 7) → 42` |
| `divide` | Divide first by second | `divide(15, 3) → 5` |
| `power` | Raise to power | `power(2, 8) → 256` |
| `square_root` | Calculate square root | `square_root(16) → 4` |
| `factorial` | Calculate factorial | `factorial(5) → 120` |
| `calculate_percentage` | Calculate percentage | `calculate_percentage(200, 15) → 30` |

### TypeScript SDK Resource

Access the TypeScript SDK documentation:

```python
# Resource URI: file://typesdk
# Returns the contents of the TypeScript SDK documentation
```

**Configuration**: Update `DESKTOP_FILE_PATH` in `server.py` to point to your documentation file:
```python
DESKTOP_FILE_PATH = r"C:\Users\Arnold\Desktop\typesdk.md"
```

### Meeting Summary Prompt

Generate structured meeting summaries:

```python
# Prompt: meeting_summary
# Required parameters:
# - meeting_date: Date of the meeting
# - meeting_title: Title or purpose of the meeting  
# - transcript: Meeting transcript or notes
```

**Output Structure**:
- Overview (purpose, participants, topics)
- Key Decisions (major decisions, strategic changes)
- Action Items (next steps, responsibilities, deadlines)
- Follow-up Required (pending discussions, future meetings)

## Claude Desktop Integration

### Configuration

Add to your Claude Desktop config file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "multi-tool-server": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/your/server/directory",
        "run",
        "python",
        "server.py"
      ],
      "env": {
        "UV_PROJECT_ENVIRONMENT": ".venv"
      }
    }
  }
}
```

### Restart Claude Desktop

After updating the configuration, restart Claude Desktop to load the server.

## Development

### Project Structure

```
mcp-multi-tool-server/
├── server.py                 # Main server implementation
├── templates/
│   └── Prompt.md             # Meeting summary template
├── pyproject.toml            # Project configuration
├── claude_desktop_config.json # Claude Desktop config example
├── README.md                 # This file
└── .venv/                    # Virtual environment
```

### Testing

**MCP Inspector (Recommended)**
```bash
uv run mcp dev server.py
```

**Direct Server Testing**
```bash
python server.py
```

**Testing Individual Components**

1. **Calculator Tools**: Use MCP Inspector to call each tool with test parameters
2. **Resource Access**: Check the resource tab in MCP Inspector for `file://typesdk`  
3. **Prompt Templates**: Test the `meeting_summary` prompt with sample data

### Customization

**Adding New Calculator Tools**:
```python
@mcp.tool()
def new_calculation(param1: float, param2: float) -> float:
    """Description of the new calculation."""
    return param1 + param2  # Your calculation logic
```

**Adding New Resources**:
```python
@mcp.resource("file://your-resource")
async def get_your_resource() -> str:
    """Description of your resource."""
    # Your resource logic
    return "Resource content"
```

**Adding New Prompts**:
```python
@mcp.prompt("your_prompt")
async def your_prompt(param1: str, param2: str) -> str:
    """Description of your prompt."""
    # Your prompt logic
    return f"Processed: {param1}, {param2}"
```

## Error Handling

The server includes comprehensive error handling:

- **Division by Zero**: Returns appropriate error message
- **Negative Square Roots**: Prevents invalid operations
- **Factorial Limits**: Restricts calculations to reasonable ranges (n ≤ 100)
- **File Not Found**: Graceful handling of missing resource files
- **Template Errors**: Proper error reporting for prompt template issues

## Configuration Options

### File Paths

Update these paths in `server.py` for your environment:

```python
# TypeScript SDK documentation path
DESKTOP_FILE_PATH = r"C:\Users\YourUser\Desktop\typesdk.md"

# Prompt template path (relative to server.py)
PROMPT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "Prompt.md")
```

### Server Name

Change the server name in `server.py`:
```python
mcp = FastMCP("Your Server Name")
```

## Troubleshooting

### Common Issues

**Server won't start**:
- Check Python version (3.12+ required)
- Verify `uv` installation: `uv --version`
- Check virtual environment: `uv sync`

**Tools not appearing in Claude**:
- Verify Claude Desktop config file location
- Check file paths in configuration
- Restart Claude Desktop after config changes

**Resource file not found**:
- Verify `DESKTOP_FILE_PATH` points to correct file
- Check file permissions
- Ensure file exists and is readable

**Prompt template errors**:
- Verify `templates/Prompt.md` exists
- Check template syntax
- Ensure proper variable placeholders: `{{ variable_name }}`

### Debug Mode

Run with debug output:
```bash
uv run python server.py --debug
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## License

This project is licensed under the MIT License. See LICENSE file for details.

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
- [Claude Desktop MCP Setup](https://claude.ai/docs)

---

**Built with FastMCP** - A high-level Python library for building MCP servers. 