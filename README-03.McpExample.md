# MCP Example

```cmd
git clone https://github.com/christseng89/MCP-Example.git
cd MCP-Example
uv sync

uv run mcp dev server.py
```

## Building MCP with LLMs

<https://modelcontextprotocol.io/tutorials/building-mcp-with-llms>

### Add into Cursor IDE - Indexing & Docs

<https://modelcontextprotocol.io/llms-full.txt>
<https://github.com/modelcontextprotocol/python-sdk/blob/main/README.md>
<https://github.com/modelcontextprotocol/typescript-sdk/blob/main/README.md>

```CursorChat to create a mcp server
I want to create a mcp server from the @MCP LLM Full use the @Python SDK MCP Readme the server should have 1 tool, a calculator.

Write a detailed README with every single step included.

Installation of uv, Python, etc. — every step should be documented, including how to verify that the version works.
Assume that I have already created and opened a folder.
The server should run in a virtual environment.
The mcp[cli] package should also be installed using uv.
```

```CursorChat to create a claude desktop configfile
i need a claude desktop configfile to connect this server. use the @MCP LLMs Full to create one. 
Also make sure, to use stdio and to point to my exact folder
```

```CursorChat to create a prompt template
I want to include a prompt template in my server. use the info from @MCP LLMs Full to implement it as a prompt template.  

Here is the path to my prompt: "D:\development\mcp-BuildAgents\MCP-Example\templates\Prompt.md"

Make sure to include a mcp.prompt in my server.py and not a resource. 
```

## Dynamic Prompt (*Multiple*) Templates for MCP Server

```cmd
cd ..
git clone https://github.com/christseng89/mcp-prompt-templates.git
cd mcp-prompt-templates

uv init
uv add -r requirements.txt

uv run server.py

```

```cmd
npx @modelcontextprotocol/inspector uv --directory D:\\development\\mcp-BuildAgents\\mcp-prompt-templates run py
thon server.py
```

## Enhance the server.py to use both stdio and streamable http transport

Using .env to set the transport: 

- TRANSPORT=stdio or 
- TRANSPORT=streamable-http

### Streamable HTTP

```cmd
npx @modelcontextprotocol/inspector uv --directory D:\\development\\mcp-BuildAgents\\mcp-prompt-templates run python server.py
```

- Transport: Streamable HTTP
- URL: <http://127.0.0.1:8000/mcp>
