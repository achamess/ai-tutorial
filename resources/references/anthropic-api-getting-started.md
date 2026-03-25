# Anthropic Claude API -- Getting Started
Source: https://docs.anthropic.com/en/api/getting-started
Downloaded: 2026-03-25
Note: This is a local copy for reference. Check the source URL for the most current version.

---

## API Overview

The Claude API is a RESTful API at `https://api.anthropic.com` that provides programmatic access to Claude models. The primary API is the Messages API (`POST /v1/messages`) for conversational interactions.

## Prerequisites

To use the Claude API, you'll need:

- An [Anthropic Console account](https://platform.claude.com)
- An [API key](https://platform.claude.com/settings/keys)

## Available APIs

**General Availability:**
- **Messages API**: Send messages to Claude for conversational interactions (`POST /v1/messages`)
- **Message Batches API**: Process large volumes of Messages requests asynchronously with 50% cost reduction (`POST /v1/messages/batches`)
- **Token Counting API**: Count tokens in a message before sending (`POST /v1/messages/count_tokens`)
- **Models API**: List available Claude models and their details (`GET /v1/models`)

**Beta:**
- **Files API**: Upload and manage files for use across multiple API calls
- **Skills API**: Create and manage custom agent skills

## Authentication

All requests to the Claude API must include these headers:

| Header | Value | Required |
|--------|-------|----------|
| `x-api-key` | Your API key from Console | Yes |
| `anthropic-version` | API version (e.g., `2023-06-01`) | Yes |
| `content-type` | `application/json` | Yes |

### Getting API Keys

The API is available via the web [Console](https://platform.claude.com/). Use the [Workbench](https://platform.claude.com/workbench) to try out the API in the browser, then generate API keys in [Account Settings](https://platform.claude.com/settings/keys). Use [workspaces](https://platform.claude.com/settings/workspaces) to segment API keys and control spend by use case.

## Client SDKs

Anthropic provides official SDKs that simplify API integration:

**Benefits:**
- Automatic header management
- Type-safe request and response handling
- Built-in retry logic and error handling
- Streaming support
- Request timeouts and connection management

**Python example:**
```python
from anthropic import Anthropic

client = Anthropic()  # Reads ANTHROPIC_API_KEY from environment
message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude"}],
)
```

SDKs are available for Python, TypeScript, Java, Go, C#, Ruby, and PHP.

## Basic Example (curl)

```bash
curl https://api.anthropic.com/v1/messages \
  --header "x-api-key: $ANTHROPIC_API_KEY" \
  --header "anthropic-version: 2023-06-01" \
  --header "content-type: application/json" \
  --data '{
    "model": "claude-opus-4-6",
    "max_tokens": 1024,
    "messages": [
      {"role": "user", "content": "Hello, Claude"}
    ]
  }'
```

**Response:**
```json
{
  "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
  "type": "message",
  "role": "assistant",
  "content": [
    {
      "type": "text",
      "text": "Hello! How can I assist you today?"
    }
  ],
  "model": "claude-opus-4-6",
  "stop_reason": "end_turn",
  "usage": {
    "input_tokens": 12,
    "output_tokens": 8
  }
}
```

## Request Size Limits

| Endpoint | Maximum Size |
|----------|--------------|
| Standard endpoints (Messages, Token Counting) | 32 MB |
| Batch API | 256 MB |
| Files API | 500 MB |

## Rate Limits and Availability

The API enforces rate limits organized into usage tiers that increase automatically as you use the API. Each tier has:
- **Spend limits**: Maximum monthly cost
- **Rate limits**: Maximum requests per minute (RPM) and tokens per minute (TPM)

View your limits in the [Console](https://platform.claude.com/settings/limits).

## Claude API vs Third-Party Platforms

### Direct API
- Direct access to the latest models and features first
- Anthropic billing and support
- Best for new integrations and full feature access

### Third-Party Platforms
- **Amazon Bedrock** (AWS): Integrated with AWS billing and IAM
- **Vertex AI** (Google Cloud): Integrated with GCP billing
- **Azure AI** (Microsoft): Integrated with Azure billing

## Next Steps

- [Working with Messages](https://docs.anthropic.com/en/build-with-claude/working-with-messages) -- Request/response patterns and best practices
- [Messages API Reference](https://docs.anthropic.com/en/api/messages) -- Complete API specification
- [Client SDKs](https://docs.anthropic.com/en/api/client-sdks) -- Installation guides for all languages
- [Rate limits](https://docs.anthropic.com/en/api/rate-limits) -- Usage tiers and rate limiting details
