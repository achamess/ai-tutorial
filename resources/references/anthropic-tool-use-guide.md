# Anthropic Tool Use Guide
Source: https://docs.anthropic.com/en/docs/build-with-claude/tool-use/overview
Downloaded: 2026-03-25
Note: This is a local copy for reference. Check the source URL for the most current version.

---

## Overview

Claude is capable of interacting with tools and functions, allowing you to extend Claude's capabilities to perform a wider variety of tasks. Each tool defines a contract: you specify what operations are available and what they return; Claude decides when and how to call them.

## How Tool Use Works

Claude supports two types of tools:

1. **Client tools**: Tools that execute on your systems, including:
   - User-defined custom tools that you create and implement
   - Anthropic-defined tools like computer use and text editor that require client implementation

2. **Server tools**: Tools that execute on Anthropic's servers, like web search and web fetch tools. These must be specified in the API request but don't require implementation on your part.

### Client Tools Workflow

1. **Provide Claude with tools and a user prompt**: Define client tools with names, descriptions, and input schemas in your API request. Include a user prompt that might require these tools.

2. **Claude decides to use a tool**: Claude assesses if any tools can help. If yes, it constructs a properly formatted tool use request. The API response has a `stop_reason` of `tool_use`.

3. **Execute the tool and return results**: Extract the tool name and input from Claude's request. Execute the tool on your system. Return results in a new `user` message containing a `tool_result` content block.

4. **Claude uses tool result to formulate a response**: Claude analyzes the tool results to craft its final response.

### Server Tools Workflow

1. **Provide Claude with tools and a user prompt**: Server tools like web search and web fetch have their own parameters.

2. **Claude executes the server tool**: Claude executes the tool, and results are automatically incorporated. The server runs a sampling loop that may execute multiple tool calls.

3. **Claude uses results to formulate a response**: No additional user interaction is needed.

## Basic Example (Python)

```python
import anthropic

client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    tools=[
        {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "input_schema": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    }
                },
                "required": ["location"],
            },
        }
    ],
    messages=[{"role": "user", "content": "What's the weather like in San Francisco?"}],
)
print(response)
```

## Basic Example (curl)

```bash
curl https://api.anthropic.com/v1/messages \
  -H "content-type: application/json" \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -d '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "tools": [
      {
        "name": "get_weather",
        "description": "Get the current weather in a given location",
        "input_schema": {
          "type": "object",
          "properties": {
            "location": {
              "type": "string",
              "description": "The city and state, e.g. San Francisco, CA"
            }
          },
          "required": ["location"]
        }
      }
    ],
    "messages": [
      {
        "role": "user",
        "content": "What is the weather like in San Francisco?"
      }
    ]
  }'
```

## Using MCP Tools with Claude

If you're building an application that uses the Model Context Protocol (MCP), you can use tools from MCP servers directly with Claude's Messages API. MCP tool definitions use a schema format similar to Claude's tool format -- just rename `inputSchema` to `input_schema`.

```python
from mcp import ClientSession

async def get_claude_tools(mcp_session: ClientSession):
    """Convert MCP tools to Claude's tool format."""
    mcp_tools = await mcp_session.list_tools()

    claude_tools = []
    for tool in mcp_tools.tools:
        claude_tools.append(
            {
                "name": tool.name,
                "description": tool.description or "",
                "input_schema": tool.inputSchema,  # Rename inputSchema to input_schema
            }
        )

    return claude_tools
```

When Claude responds with a `tool_use` block, execute the tool on your MCP server using `call_tool()` and return the result in a `tool_result` block.

## Key Concepts

- **Tool definitions**: Each tool needs a `name`, `description`, and `input_schema` (JSON Schema format)
- **Structured Outputs**: Add `strict: true` to tool definitions for guaranteed schema validation
- **Parallel tool calling**: Claude can execute multiple independent tool calls simultaneously
- **Server-side tools**: Web search and web fetch run on Anthropic's servers automatically
- **Versioned tool types**: Anthropic-defined tools use versioned types (e.g., `web_search_20250305`) for compatibility

## Further Reading

- [Structured Outputs](https://docs.anthropic.com/en/build-with-claude/structured-outputs) -- Guaranteed schema validation for tool inputs
- [MCP Connector](https://docs.anthropic.com/en/agents-and-tools/mcp-connector) -- Connect to remote MCP servers from the Messages API
- [Build an MCP client](https://modelcontextprotocol.io/docs/develop/build-client) -- Complete guide to building MCP clients
- [Anthropic Tool Use Cookbook](https://github.com/anthropics/anthropic-cookbook) -- More examples and patterns
