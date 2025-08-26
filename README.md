# MCP Calculator Server

A comprehensive Model Context Protocol (MCP) server built with FastMCP that provides 24 tools across calculator and file system operations, SDK documentation resources, and prompt templates. This server demonstrates multiple MCP capabilities including tools, resources, and prompts with robust security features and dual transport support (stdio/HTTP).

## Features

### 🛡️ Security
- **Path Traversal Protection**: All file system operations use a custom `_secure_join` function to prevent path traversal attacks
- **Secure File Operations**: All file system operations are wrapped in `try...except` blocks to handle exceptions gracefully
- **Environment Variable Access**: Safe access to OS environment variables

### 🧮 Calculator Tools
- **Basic Operations**: Addition, subtraction, multiplication, division
- **Advanced Math**: Power, square root, factorial calculations
- **Utility Functions**: Percentage calculations
- **Error Handling**: Division by zero protection, negative square root protection, factorial range limits

### 📁 File System Tools
- **File Operations**: Read file contents, get file metadata, check file existence
- **Directory Operations**: List directories, create directories, get current working directory
- **Path Utilities**: Get absolute paths, join paths, extract filenames and extensions
- **Permission Management**: Change file permissions (where supported)
- **System Information**: Access home directory, environment variables

### 📖 Document Resources
- **TypeScript SDK Resource**: Access to MCP TypeScript SDK documentation (`file://typesdk`)
- **Python SDK Resource**: Access to MCP Python SDK documentation (`file://pythonsdk`)
- **Dynamic File Reading**: Reads from local markdown files
- **Error Handling**: Graceful handling of missing files

### 📝 Prompt Templates
- **Meeting Summary Template**: Executive meeting summary generator
- **Variable Substitution**: Dynamic template variable replacement
- **Structured Output**: Professional meeting summary format

## SonarQube Compliance

The codebase has been updated to be compliant with SonarQube rules. This includes:

- **Reduced Code Duplication**: The `get_typesdk_resource` and `get_pythonsdk_resource` functions have been refactored to reduce code duplication.
- **Specific Exception Handling**: Broad `except` clauses have been replaced with more specific ones.
- **Improved Readability**: The code has been made more readable and easier to maintain.

## Quick Start

### Prerequisites
- Python 3.12 or later
- `uv` package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/christseng89/MCP-Example.git
   cd MCP-Example
   ```

2. **Install dependencies**
   ```bash
   uv sync
   ```

3. **Test the server**
   ```bash
   # Using MCP development tools (after installing mcp[cli])
   uv add "mcp[cli]"
   uv run mcp dev server.py
   
   # Or using NPX MCP Inspector
   npx @modelcontextprotocol/inspector -- uv run python server.py
   ```
   
   The MCP Inspector will open in your browser for testing.

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

### File System Tools

The server provides 16 file system tools:

| Tool | Description | Example |
|------|-------------|---------|
| `get_file_content` | Read and return file contents | `get_file_content("test.txt")` |
| `list_files` | List files in directory | `list_files("./")` |
| `get_os_environment_variable` | Get environment variable value | `get_os_environment_variable("PATH")` |
| `get_current_working_directory` | Get current working directory | `get_current_working_directory()` |
| `create_directory` | Create new directory | `create_directory("new_folder")` |
| `get_file_metadata` | Get file metadata (size, dates) | `get_file_metadata("file.txt")` |
| `change_file_permissions` | Change file permissions | `change_file_permissions("file.txt", 0o755)` |
| `get_absolute_path` | Convert relative to absolute path | `get_absolute_path("./file.txt")` |
| `check_path_exists` | Check if path exists | `check_path_exists("file.txt")` |
| `get_path_type` | Determine if file or directory | `get_path_type("path")` |
| `get_home_directory` | Get user's home directory | `get_home_directory()` |
| `get_file_extension` | Extract file extension | `get_file_extension("file.txt") → .txt` |
| `join_paths` | Safely join path components | `join_paths("dir", "file.txt")` |
| `get_parent_directory` | Get parent directory | `get_parent_directory("/path/file.txt")` |
| `get_filename` | Extract filename from path | `get_filename("/path/file.txt") → file.txt` |
| `get_filename_without_extension` | Get filename without extension | `get_filename_without_extension("file.txt") → file` |

### SDK Documentation Resources

Access MCP SDK documentation for both TypeScript and Python:

**TypeScript SDK Resource**:
```python
# Resource URI: file://typesdk
# Returns the contents of README-typeSdk.md
```

**Python SDK Resource**:
```python
# Resource URI: file://pythonsdk
# Returns the contents of README-pythonSdk.md
```

**File Configuration**: The server reads from these local files:
```python
TS_SDK_FILE_PATH = os.path.join(os.path.dirname(__file__), "README-typeSdk.md")
PY_SDK_FILE_PATH = os.path.join(os.path.dirname(__file__), "README-pythonSdk.md")
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

## Transport Options

The server supports two transport methods:

### 1. Standard I/O (stdio) - Default
Used for integration with Claude Desktop and other MCP clients:
```bash
# Run with stdio (default)
uv run python server.py

# Or explicitly set transport
TRANSPORT=stdio uv run python server.py
```

### 2. Streamable HTTP
For web-based integrations and HTTP clients:
```bash
# Run with HTTP transport
TRANSPORT=http uv run python server.py
```

The transport method is controlled by the `TRANSPORT` environment variable. If not set, it defaults to `stdio`.

## Claude Desktop Integration

### Configuration

Add to your Claude Desktop config file:

**Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
**macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "calculator-server": {
      "command": "uv",
      "args": [
        "--directory",
        "D:\\development\\mcp-BuildAgents\\MCP-Example",
        "run",
        "python",
        "server.py"
      ]
    }
  }
}
```

### Restart Claude Desktop

After updating the configuration, restart Claude Desktop to load the server.

## Development

### Project Structure

```
MCP-Example/
├── server.py                 # Main server implementation (24 tools total)
├── main.py                   # Alternative entry point
├── templates/
│   └── Prompt.md             # Meeting summary template
├── README-typeSdk.md         # TypeScript SDK documentation
├── README-pythonSdk.md       # Python SDK documentation
├── pyproject.toml            # Project configuration
├── claude_desktop_config.json # Claude Desktop config example
├── security_checklist.md     # Security guidelines and checklist
├── README.md                 # This file
├── uv.lock                   # UV lock file
└── __pycache__/              # Python cache directory
```

### Testing

**MCP Inspector (Recommended)**
```bash
# Using NPX (more reliable)
npx @modelcontextprotocol/inspector -- uv run python server.py

# Or using MCP CLI (after installing mcp[cli])
uv add "mcp[cli]"
```

**Direct Server Testing**
```bash
uv run python server.py
```

**Testing Individual Components**

1. **Calculator Tools**: Use MCP Inspector to call each of the 8 calculator tools with test parameters
2. **File System Tools**: Test the 16 file system tools with appropriate paths and parameters
3. **Resource Access**: Check the resource tab in MCP Inspector for `file://typesdk` and `file://pythonsdk`
4. **Prompt Templates**: Test the `meeting_summary` prompt with sample data

### Customization

**Adding New Calculator Tools**:
```python
@mcp.tool()
```

**Adding New Resources**:
```python
@mcp.resource("file://your-resource")
```

**Adding New Prompts**:
```python
@mcp.prompt("your_prompt")
```

## Error Handling

The server includes comprehensive error handling:

- **Division by Zero**: Returns appropriate error message
- **Negative Square Roots**: Prevents invalid operations
- **Factorial Limits**: Restricts calculations to reasonable ranges (n ≤ 100)
- **File Not Found**: Graceful handling of missing resource files
- **Template Errors**: Proper error reporting for prompt template issues
- **Path Traversal Protection**: Prevents unauthorized file system access
- **Permission Errors**: Graceful handling of file permission issues
- **Invalid Paths**: Proper validation and error reporting for malformed paths

## Configuration Options

### File Paths

The server uses these file paths (already configured correctly):

```python
# TypeScript SDK documentation path
TS_SDK_FILE_PATH = os.path.join(os.path.dirname(__file__), "README-typeSdk.md")

# Python SDK documentation path
PY_SDK_FILE_PATH = os.path.join(os.path.dirname(__file__), "README-pythonSdk.md")

# Prompt template path (relative to server.py)
PROMPT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "Prompt.md")
```

### Server Name

Change the server name in `server.py`:
```python
mcp = FastMCP("Calculator Server")  # Current server name
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
- Verify `README-typeSdk.md` and `README-pythonSdk.md` exist in the project directory
- Check file permissions
- Ensure files exist and are readable

**Prompt template errors**:
- Verify `templates/Prompt.md` exists
- Check template syntax
- Ensure proper variable placeholders: `{{ variable_name }}`

**File system tool errors**:
- Check file paths are within allowed directory boundaries
- Verify file permissions for read/write operations
- Ensure target files and directories exist before operations

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
