from mcp.server.fastmcp import FastMCP
import math
import os
from pathlib import Path
from typing import Dict, Optional, Union

from dotenv import load_dotenv
import asyncio

load_dotenv()


# Create an MCP server
mcp = FastMCP("Calculator Server")

# Define the path to the resource file
def _secure_join(base, *paths):
    #This function is designed to prevent path traversal attacks by ensuring that the resulting path is always within the intended base directory.
    base_path = Path(base).resolve()
    path = base_path.joinpath(*paths).resolve()
    if base_path not in path.parents and path != base_path:
        raise ValueError("Attempted path traversal")
    return str(path)

TS_SDK_FILE_PATH = _secure_join(os.path.dirname(__file__), "README-typeSdk.md")
PY_SDK_FILE_PATH = _secure_join(
    os.path.dirname(__file__), "README-pythonSdk.md")

# Define the path to the prompt template
PROMPT_TEMPLATE_PATH = _secure_join(
    os.path.dirname(__file__), "templates", "Prompt.md")

async def _read_resource_file(file_path: str, error_message_prefix: str) -> str:
    """
    Reads a resource file and returns its content.
    """
    try:
        if not Path(file_path).is_file():
            return f"Error: {Path(file_path).name} file not found in the folder"
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        return f"Error reading {Path(file_path).name}: {e}"
    except Exception as e:
        # Log the exception for debugging purposes
        print(f"An unexpected error occurred: {e}")
        return f"An unexpected error occurred while reading {Path(file_path).name}."

@mcp.resource("file://typesdk")
async def get_typesdk_resource() -> str:
    """
    Provides access to the TypeScript SDK MCP documentation.
    This resource contains information about the TypeScript SDK for MCP.
    """
    return await _read_resource_file(TS_SDK_FILE_PATH, "typesdk.md")


@mcp.resource("file://pythonsdk")
async def get_pythonsdk_resource() -> str:
    """
    Provides access to the Python SDK MCP documentation.
    This resource contains information about the Python SDK for MCP.
    """
    return await _read_resource_file(PY_SDK_FILE_PATH, "pythonSdk.md")


@mcp.prompt("meeting_summary")
async def meeting_summary_prompt(
    meeting_date: str,
    meeting_title: str,
    transcript: str
) -> str:
    """
    A prompt template for generating executive meeting summaries.

    Args:
        'meeting_date': The date of the meeting
        'meeting_title': The title or purpose of the meeting
        'transcript': The meeting transcript or notes

    Returns:
        A structured meeting summary with key points, decisions, and action items.
    """
    try:
        # Read the template file
        if not Path(PROMPT_TEMPLATE_PATH).is_file():
            raise FileNotFoundError(f"Template file not found at {PROMPT_TEMPLATE_PATH}")
        with open(PROMPT_TEMPLATE_PATH, 'r', encoding='utf-8') as file:
            template = file.read()

        # Fill in the template variables
        variables = {
            "meeting_date": meeting_date,
            "meeting_title": meeting_title,
            "transcript": transcript
        }

        for key, value in variables.items():
            placeholder = f"{{{{ {key} }}}}"
            template = template.replace(placeholder, str(value))

        # Here you would typically send the filled template to an LLM
        # For now, we'll return the filled template
        return template

    except (FileNotFoundError, KeyError) as e:
        raise RuntimeError(f"Error executing meeting summary prompt: {e}") from e


@mcp.tool()
def add(a: float, b: float) -> float:
    """Add two numbers together."""
    return a + b


@mcp.tool()
def subtract(a: float, b: float) -> float:
    """Subtract the second number from the first number."""
    return a - b


@mcp.tool()
def multiply(a: float, b: float) -> float:
    """Multiply two numbers together."""
    return a * b


@mcp.tool()
def divide(a: float, b: float) -> float:
    """Divide the first number by the second number."""
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b


@mcp.tool()
def power(base: float, exponent: float) -> float:
    """Raise a number to a power."""
    return base ** exponent


@mcp.tool()
def square_root(x: float) -> float:
    """Calculate the square root of a number."""
    if x < 0:
        raise ValueError("Cannot calculate square root of negative number")
    return math.sqrt(x)


@mcp.tool()
def factorial(n: int) -> int:
    """Calculate the factorial of a non-negative integer."""
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers")
    if n > 100:
        raise ValueError("Number too large for factorial calculation")
    return math.factorial(n)


@mcp.tool()
def calculate_percentage(value: float, percentage: float) -> float:
    """Calculate a percentage of a value."""
    return (value * percentage) / 100


async def main():
    transport = os.getenv("TRANSPORT", "stdio").lower()
    print(f"Transport: {transport}")
    if transport == 'stdio':
        # Run the MCP server with stdio transport
        await mcp.run_stdio_async()
    else:
        # Run the MCP server with streamable http transport
        await mcp.run_streamable_http_async()


if __name__ == "__main__":
    asyncio.run(main())


@mcp.tool()
def get_file_content(file_path: str) -> str:
    """
    Reads and returns the content of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The content of the file.
    """
    try:
        secure_path = _secure_join(os.getcwd(), file_path)
        with open(secure_path, 'r', encoding='utf-8') as file:
            return file.read()
    except (FileNotFoundError, PermissionError) as e:
        return f"Error: {e}"
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@mcp.tool()
def list_files(directory: str = '.') -> list:
    """
    Lists all files and directories in a given directory.

    Args:
        directory (str): The directory to list. Defaults to the current directory.

    Returns:
        list: A list of files and directories.
    """
    try:
        secure_path = _secure_join(os.getcwd(), directory)
        return os.listdir(secure_path)
    except (FileNotFoundError, PermissionError) as e:
        return [f"Error: {e}"]
    except ValueError as e:
        return [f"Error: {e}"]
    except Exception as e:
        return [f"An unexpected error occurred: {e}"]


@mcp.tool()
def get_os_environment_variable(variable_name: str) -> Optional[str]:
    """
    Gets the value of an environment variable.

    Args:
        variable_name (str): The name of the environment variable.

    Returns:
        Optional[str]: The value of the environment variable, or None if it's not set.
    """
    return os.getenv(variable_name)


@mcp.tool()
def get_current_working_directory() -> str:
    """
    Gets the current working directory.

    Returns:
        str: The current working directory.
    """
    return os.getcwd()


@mcp.tool()
def create_directory(directory_path: str) -> str:
    """
    Creates a new directory.

    Args:
        directory_path (str): The path for the new directory.

    Returns:
        str: A confirmation message.
    """

    try:
        secure_path = _secure_join(os.getcwd(), directory_path)
        os.makedirs(secure_path, exist_ok=True)
        return f"Directory created at {secure_path}"
    except (PermissionError, FileExistsError) as e:
        return f"Error: {e}"
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@mcp.tool()
def get_file_metadata(file_path: str) -> Dict[str, Union[int, float, str]]:
    """
    Gets metadata for a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        Dict[str, Union[int, float, str]]: A dictionary with file metadata.
    """
    try:
        secure_path = _secure_join(os.getcwd(), file_path)
        stat = os.stat(secure_path)
        return {
            "size": stat.st_size,
            "last_modified": stat.st_mtime,
            "created": stat.st_ctime,
        }
    except (FileNotFoundError, PermissionError) as e:
        return {"error": f"{e}"}
    except ValueError as e:
        return {"error": f"{e}"}
    except Exception as e:
        return {"error": f"An unexpected error occurred: {e}"}


@mcp.tool()
def change_file_permissions(file_path: str, mode: int) -> str:
    """
    Changes the permissions of a file.

    Args:
        file_path (str): The path to the file.
        mode (int): The new permissions mode (e.g., 0o755).

    Returns:
        str: A confirmation message.
    """
    try:
        secure_path = _secure_join(os.getcwd(), file_path)
        os.chmod(secure_path, mode)
        return f"Permissions changed for {secure_path}"
    except (FileNotFoundError, PermissionError) as e:
        return f"Error: {e}"
    except ValueError as e:
        return f"Error: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"


@mcp.tool()
def get_absolute_path(relative_path: str) -> str:
    """
    Converts a relative path to an absolute path.

    Args:
        relative_path (str): The relative path to convert.

    Returns:
        str: The absolute path.
    """
    return os.path.abspath(relative_path)


@mcp.tool()
def check_path_exists(path: str) -> bool:
    """
    Checks if a path (file or directory) exists.

    Args:
        path (str): The path to check.

    Returns:
        bool: True if the path exists, False otherwise.
    """
    try:
        secure_path = _secure_join(os.getcwd(), path)
        return os.path.exists(secure_path)
    except ValueError:
        return False


@mcp.tool()
def get_path_type(path: str) -> str:
    """
    Determines if a path is a file or a directory.

    Args:
        path (str): The path to check.

    Returns:
        str: "file", "directory", or "not found".
    """
    try:
        secure_path = _secure_join(os.getcwd(), path)
        if os.path.isfile(secure_path):
            return "file"
        elif os.path.isdir(secure_path):
            return "directory"
        else:
            return "not found"
    except ValueError:
        return "not found"


@mcp.tool()
def get_home_directory() -> str:
    """

    Returns the user's home directory.
    """
    return str(Path.home())


@mcp.tool()
def get_file_extension(file_path: str) -> str:
    """
    Extracts the extension of a file.

    Args:
        file_path (str): The path to the file.

    Returns:
        str: The file extension.
    """
    return Path(file_path).suffix


@mcp.tool()
def join_paths(path1: str, path2: str) -> str:
    """
    Joins two path components together.

    Args:
        path1 (str): The first part of the path.
        path2 (str): The second part of the path.

    Returns:
        str: The combined path.
    """
    return _secure_join(path1, path2)


@mcp.tool()
def get_parent_directory(path: str) -> str:
    """
    Gets the parent directory of a given path.

    Args:
        path (str): The path to process.

    Returns:
        str: The parent directory.
    """
    return str(Path(path).parent)


@mcp.tool()
def get_filename(path: str) -> str:
    """
    Extracts the filename from a path.

    Args:
        path (str): The path to process.

    Returns:
        str: The filename.
    """
    return Path(path).name


@mcp.tool()
def get_filename_without_extension(path: str) -> str:
    """
    Extracts the filename from a path without its extension.

    Args:
        path (str): The path to process.

    Returns:
        str: The filename without the extension.
    """
    return Path(path).stem