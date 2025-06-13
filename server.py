from mcp.server.fastmcp import FastMCP
import math
import os
from pathlib import Path
from typing import Dict, Optional

# Create an MCP server
mcp = FastMCP("Calculator Server")

# Define the path to the resource file
DESKTOP_FILE_PATH = r"C:\Users\Arnold\Desktop\typesdk.md"

# Define the path to the prompt template
PROMPT_TEMPLATE_PATH = os.path.join(os.path.dirname(__file__), "templates", "Prompt.md")

@mcp.resource("file://typesdk")
async def get_typesdk_resource() -> str:
    """
    Provides access to the TypeScript SDK MCP documentation.
    This resource contains information about the TypeScript SDK for MCP.
    """
    try:
        # Read the file from desktop
        if os.path.exists(DESKTOP_FILE_PATH):
            with open(DESKTOP_FILE_PATH, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        else:
            return "Error: typesdk.md file not found on desktop"
    except Exception as e:
        return f"Error reading typesdk.md: {str(e)}"

@mcp.prompt("meeting_summary")
async def meeting_summary_prompt(
    meeting_date: str,
    meeting_title: str,
    transcript: str
) -> str:
    """
    A prompt template for generating executive meeting summaries.
    
    Args:
        meeting_date: The date of the meeting
        meeting_title: The title or purpose of the meeting
        transcript: The meeting transcript or notes
    
    Returns:
        A structured meeting summary with key points, decisions, and action items.
    """
    try:
        # Read the template file
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
        
    except Exception as e:
        raise RuntimeError(f"Error executing meeting summary prompt: {str(e)}")

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

if __name__ == "__main__":
    mcp.run() 