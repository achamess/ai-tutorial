import marimo

__generated_with = "0.21.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 03: Networking and APIs

    When you ask Claude a question through the API, or when a Python script fetches gene data from NCBI, your computer sends a message across the internet and waits for a reply. This notebook explains what's actually happening in that exchange.

    You don't need to become a networking expert. But having a mental model of HTTP requests, JSON, and API keys will make you much more effective when things go wrong (timeouts, rate limits, authentication errors).

    > **References:**
    > - [MIT Missing Semester — Lecture 1: The Shell](https://missing.csail.mit.edu/2020/course-shell/) — foundational concepts for command-line tools that make HTTP requests
    > - [MDN Web Docs: HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) — the authoritative reference for all HTTP status codes (200, 401, 429, etc.)
    > - [NCBI E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/) — documentation for the NCBI API used in this notebook's examples
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Processes and Environment](02-processes-and-environment.py) | [Module Index](../README.md) | [Next: Your AI Toolkit \u2192](04-your-ai-toolkit.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Every Claude API call is an HTTP request carrying JSON. When you get a "429 rate limit" or "401 unauthorized" error, understanding HTTP means you can diagnose it in seconds instead of hours.
    > - Querying external databases (NCBI for gene info, UniProt for protein structures, PDB for cryo-EM coordinates) is HTTP requests under the hood. This notebook teaches you the pattern so you can build automated tools that pull data from any biological database.
    > - JSON is the format Claude's API uses to send and receive data. It's also how you'll structure automated pipelines — passing binder candidate data between scripts, storing experimental metadata, and logging analysis results.
    > - Understanding API keys, authentication, and rate limits is essential for building any automated workflow that calls Claude, NCBI, or other services. Without this, your automated research digest or batch analysis pipeline will break in ways you can't debug.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The journey of an API call

    When your code calls the Anthropic API, here's what happens:

    ```
    Your Python code
        │
        ▼
    Creates an HTTP request (POST to https://api.anthropic.com/v1/messages)
        │
        ▼
    Your Mac's network stack sends it over the internet
        │
        ▼
    DNS resolves "api.anthropic.com" to an IP address (like 104.18.32.7)
        │
        ▼
    The request arrives at Anthropic's servers
        │
        ▼
    Their server checks your API key, processes your prompt, generates a response
        │
        ▼
    The response travels back to your Mac
        │
        ▼
    Your Python code receives it and continues
    ```

    This whole round trip typically takes 1-30 seconds, depending on how long the response is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    sequenceDiagram
        participant Code as Your Python Code
        participant Net as Mac Network Stack
        participant DNS as DNS Server
        participant API as Anthropic API Server

        Code->>Net: POST https://api.anthropic.com/v1/messages<br/>(JSON body + API key header)
        Net->>DNS: What IP is api.anthropic.com?
        DNS-->>Net: 104.18.32.7
        Net->>API: HTTP request over TLS (encrypted)
        Note over API: Check API key<br/>Process prompt<br/>Generate response<br/>(1-30 seconds)
        API-->>Net: HTTP 200 OK + JSON response
        Net-->>Code: Response object with Claude's text

        Note over Code,API: The whole round trip: 1-30 seconds depending on response length
    ```

    This same request-response pattern applies to every API call -- whether you're querying Claude, NCBI for gene data, or UniProt for protein structures. The only differences are the URL, the data format, and whether you need an API key.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## URLs: what the parts mean

    Let's break down a URL:

    ```
    https://api.anthropic.com/v1/messages
    │       │                 │
    │       │                 └── path (which resource on the server)
    │       └── domain (which server)
    └── protocol (https = encrypted HTTP)
    ```

    Some URLs have more parts:
    ```
    https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=TRPV1
    │       │                       │                           │
    │       │                       │                           └── query parameters (filters)
    │       │                       └── path
    │       └── domain
    └── protocol
    ```

    Query parameters (after the `?`) are like function arguments — they tell the server what you want.

    ### Ports

    A port is like an apartment number at an address. The domain is the building; the port is which door to knock on.

    - Port **443** — HTTPS (encrypted web traffic). Used by default when you see `https://`
    - Port **80** — HTTP (unencrypted). Rarely used anymore.
    - Port **2718** — Common for marimo notebooks running locally
    - Port **8080** — Common for local development servers

    You usually don't see ports in URLs because browsers and tools use the default ones. But you'll see them when running things locally (like `http://localhost:2718` for marimo).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** HTTP status codes tell you *why* your API call failed, and what to do about it. The first digit is all you need: **2xx = success**, **4xx = your mistake** (bad URL, wrong key, too many requests), **5xx = their problem** (server error). The most common ones you'll see: `200` (success), `401` (check your API key), `404` (check the URL), `429` (you're sending too many requests — wait and retry), `500` (server is down — try again later).

    ```mermaid
    graph TD
        REQ["API call returns a status code"] --> Q1{"Code starts with?"}
        Q1 -->|"2xx"| OK["**200 OK**<br/>Success! Parse the response."]
        Q1 -->|"4xx"| CLIENT["**Client error** — something<br/>wrong on YOUR side"]
        Q1 -->|"5xx"| SERVER["**Server error** — something<br/>wrong on THEIR side"]

        CLIENT --> C1{"Which 4xx?"}
        C1 -->|"400"| BAD["Bad Request<br/>*Check your parameters*"]
        C1 -->|"401"| AUTH["Unauthorized<br/>*Check ANTHROPIC_API_KEY*"]
        C1 -->|"404"| NOTF["Not Found<br/>*Check the URL*"]
        C1 -->|"429"| RATE["Rate Limited<br/>*Wait, then retry*"]

        SERVER --> S1["Wait 30-60 seconds<br/>and try again"]

        style OK fill:#44aa88,color:#fff
        style CLIENT fill:#cc8844,color:#fff
        style SERVER fill:#cc4444,color:#fff
        style AUTH fill:#cc4444,color:#fff
        style RATE fill:#cc8844,color:#fff
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## HTTP: the language of the web

    **HTTP** (HyperText Transfer Protocol) is how computers talk to each other on the web. It's a simple pattern: **request** and **response**.

    ### Request methods

    | Method | When you use it | Analogy |
    |--------|----------------|--------|
    | **GET** | Fetch data ("give me this resource") | Looking up a paper in PubMed |
    | **POST** | Send data ("here's something to process") | Submitting a prompt to Claude |
    | **PUT** | Update data ("replace this resource") | Updating a database record |
    | **DELETE** | Remove data | Deleting an entry |

    For AI work, you'll mostly use **GET** (fetching data) and **POST** (sending prompts).

    ### Response status codes

    Every response comes with a number:

    | Code | Meaning | What to do |
    |------|---------|------------|
    | **200** | OK — success | You're good |
    | **400** | Bad request — something wrong with your request | Check your parameters |
    | **401** | Unauthorized — bad or missing API key | Check your `ANTHROPIC_API_KEY` |
    | **403** | Forbidden — you don't have permission | Check your account/plan |
    | **404** | Not found — that URL doesn't exist | Check the URL |
    | **429** | Rate limited — too many requests | Wait and try again |
    | **500** | Server error — their problem, not yours | Wait and try again |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## JSON: the language of APIs

    **JSON** (JavaScript Object Notation) is how APIs send structured data back and forth. If you know Python dictionaries and lists, you already know JSON — they look almost identical.

    ```json
    {
      "gene": "TRPV1",
      "full_name": "transient receptor potential cation channel subfamily V member 1",
      "organism": "Homo sapiens",
      "gene_id": 7442,
      "aliases": ["VR1", "OTRPC1"],
      "expressed_in": ["DRG neurons", "trigeminal ganglia", "nodose ganglia"]
    }
    ```

    That's exactly a Python dictionary. The only real difference: JSON uses `true`/`false`/`null` where Python uses `True`/`False`/`None`.
    """)
    return


@app.cell
def _():
    import json

    # Python dict → JSON string
    gene_data = {
        "gene": "TRPV1",
        "full_name": "transient receptor potential cation channel subfamily V member 1",
        "organism": "Homo sapiens",
        "gene_id": 7442,
        "is_ion_channel": True,
        "aliases": ["VR1", "OTRPC1"]
    }

    json_string = json.dumps(gene_data, indent=2)
    print("As JSON:")
    print(json_string)
    return json, json_string


@app.cell
def _(json, json_string):
    # JSON string → Python dict
    parsed = json.loads(json_string)

    print(f"Gene: {parsed['gene']}")
    print(f"Aliases: {parsed['aliases']}")
    print(f"Type of parsed: {type(parsed)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Making HTTP requests with Python

    Let's make a real API call. We'll use a free public API to demonstrate the concepts before you spend API credits.

    We'll use Python's built-in `urllib` module (no extra installation needed).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use `urllib` (built-in) vs. the `requests` library?
    >
    > | Option | Pros | Cons | Use when... |
    > |--------|------|------|-------------|
    > | **`urllib`** (built-in) | No installation required, always available, no dependencies | Verbose syntax, error handling is clunky, no built-in JSON parsing, awkward for POST requests | Simple one-off GET requests, minimal scripts where you don't want extra dependencies, learning how HTTP works |
    > | **`requests`** (third-party) | Clean API (`requests.get(url)`), automatic JSON parsing (`.json()`), built-in session handling, elegant error handling | Requires `pip install requests` | Any real project, scripts with multiple API calls, POST requests with JSON bodies, authentication, anything beyond a quick GET |
    >
    > **In this tutorial** we use `urllib` because it's built-in and shows you what's happening under the hood. In your real research scripts, use `requests` — it's what Claude will generate, and it's what the `anthropic` library uses internally.
    """)
    return


@app.cell
def _(json):
    import urllib.request
    _url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=TRPV1+AND+human[organism]&retmode=json'
    print(f'Requesting: {_url[:80]}...')
    print()
    with urllib.request.urlopen(_url) as _response:
        print(f'Status code: {_response.status}')
        print(f"Content type: {_response.headers['Content-Type']}")
        raw_data = _response.read().decode('utf-8')
        data = json.loads(raw_data)
    print()
    print('Response (formatted):')
    print(json.dumps(data, indent=2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You just made a real API call to a real biomedical database. That's the same pattern the Anthropic API uses — just a different URL and different data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What "localhost" means

    When you run marimo, you see a URL like `http://localhost:2718`. What does that mean?

    - **localhost** (also written as `127.0.0.1`) means "this computer" — your own Mac
    - **8888** is the port number

    So `http://localhost:2718` means: "talk to the web server running on my own computer, on port 2718." The marimo server is running as a process on your Mac, and your browser connects to it locally — no internet involved.

    You'll see localhost used for:
    - marimo notebooks (`localhost:2718`)
    - Local development servers
    - Database connections
    """)
    return


@app.cell
def _():
    import socket

    # localhost always resolves to your own machine
    print(f"localhost resolves to: {socket.gethostbyname('localhost')}")
    print(f"Your computer's name: {socket.gethostname()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## API keys and authentication

    Most useful APIs require an **API key** — a long string of characters that identifies you. Here's why this matters:

    1. **The API provider needs to know who's making requests** — for billing, rate limiting, and security
    2. **Your key is like a password** — anyone who has it can make requests as you (and spend your money)
    3. **That's why it's an environment variable** — it stays out of your code, out of git, off GitHub

    ### The golden rule: never put API keys in code

    ```python
    # BAD — if you share this code or push to GitHub, your key is exposed
    client = anthropic.Anthropic(api_key="sk-ant-api03-ACTUAL-KEY-HERE")

    # GOOD — reads from environment variable
    client = anthropic.Anthropic()  # automatically reads ANTHROPIC_API_KEY
    ```

    The `anthropic` Python library automatically reads `ANTHROPIC_API_KEY` from your environment. That's the standard pattern — and now you know *why* it works (environment variable inheritance, from the previous notebook).
    """)
    return


@app.cell
def _():
    import os

    # How the anthropic library finds your key (simplified)
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        print("Your API key is available in the environment.")
        print(f"Starts with: {api_key[:8]}...")
        print(f"Length: {len(api_key)} characters")
        print()
        print("The anthropic library finds this automatically — you never need to paste it in code.")
    else:
        print("ANTHROPIC_API_KEY is not set in your environment.")
        print("To set it, add this line to your ~/.zshrc file:")
        print('  export ANTHROPIC_API_KEY="sk-ant-..."')
        print("Then open a new terminal (or run: source ~/.zshrc)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What can go wrong: errors at the network level

    API calls can fail for reasons that have nothing to do with your code:

    | Problem | What you see | What to do |
    |---------|-------------|------------|
    | **No internet** | `ConnectionError`, `URLError` | Check your wifi |
    | **DNS failure** | "Name resolution failed" | The domain might be down, or you have a typo |
    | **Timeout** | `TimeoutError` | The server is slow — try again |
    | **Rate limit** | Status 429 | You're sending too many requests — wait and retry |
    | **Server error** | Status 500-599 | Their problem — wait and retry |
    | **Bad API key** | Status 401 | Check that `ANTHROPIC_API_KEY` is set correctly |

    When Claude gives you a long response and your connection drops mid-stream, that's a network issue — the model generated the answer, but the bytes didn't all make it to your computer.

    Let's see what some of these errors look like:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** API rate limits will bite you when you start automating. Most APIs (including Anthropic's and NCBI's) limit how many requests you can make per minute. If you send 100 requests in a loop without pausing, you'll get `429 Too Many Requests` errors and potentially get temporarily blocked. Always add a short delay between API calls in loops (`import time; time.sleep(1)`), and implement retry logic for 429 errors. NCBI specifically asks for no more than 3 requests per second without an API key.
    """)
    return


@app.cell
def _(urllib_1):
    import urllib.request
    import urllib.error
    try:
    # Example 1: A URL that doesn't exist (404)
        urllib_1.request.urlopen('https://api.anthropic.com/v1/nonexistent-endpoint')
    except urllib_1.error.HTTPError as e:
        print(f'HTTP Error: {e.code} — {e.reason}')
        print(f"This means: the URL path doesn't exist on that server")
    print()
    return


@app.cell
def _(urllib_1):
    # Example 2: A domain that doesn't exist (DNS failure)
    try:
        urllib_1.request.urlopen('https://this-domain-definitely-does-not-exist-xyz123.com', timeout=5)
    except urllib_1.error.URLError as e:
        print(f'URL Error: {e.reason}')
        print(f"This means: your computer couldn't find that server on the internet")
    return


@app.cell
def _(urllib_1):
    # Example 3: A request that times out
    try:
        urllib_1.request.urlopen('https://api.anthropic.com', timeout=0.001)  # 0.001 second timeout — basically guaranteed to fail
    except Exception as e:
        print(f'Error type: {type(e).__name__}')
        print(f'Message: {e}')
        print(f"This means: the server didn't respond fast enough")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now when you see these errors in Claude Code or in your own scripts, you'll know what's happening and what to try.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## How this connects to the Anthropic API

    Here's what the `anthropic` Python library does when you call `client.messages.create()`:

    1. **Builds a JSON request** with your prompt, model name, and parameters
    2. **Adds your API key** as an HTTP header (`x-api-key: sk-ant-...`)
    3. **Sends a POST request** to `https://api.anthropic.com/v1/messages`
    4. **Waits** for the response (this is where the model "thinks")
    5. **Parses the JSON response** and gives you a Python object

    Under the hood, it's the same pattern as the NCBI request we made above — just with authentication and a more complex response.

    Let's peek at what a raw Anthropic API request looks like (without actually making one):
    """)
    return


@app.cell
def _(json):
    example_request = {'model': 'claude-sonnet-4-20250514', 'max_tokens': 1024, 'messages': [{'role': 'user', 'content': 'What ion channels are most important for nociception in DRG neurons?'}]}
    print('What gets sent to https://api.anthropic.com/v1/messages:')
    # This is what the anthropic library builds and sends on your behalf
    print()
    print('Headers:')
    print('  x-api-key: sk-ant-...YOUR_KEY...')
    print('  content-type: application/json')
    print('  anthropic-version: 2023-06-01')
    print()
    print('Body (JSON):')
    print(json.dumps(example_request, indent=2))
    return


@app.cell
def _(json):
    # And here's what a response looks like (simplified)
    example_response = {
        "id": "msg_01XFDUDYJgAACzvnptvVoYEL",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "The key ion channels for nociception in DRG neurons include..."
            }
        ],
        "model": "claude-sonnet-4-20250514",
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 18,
            "output_tokens": 245
        }
    }

    print("What comes back:")
    print(json.dumps(example_response, indent=2))
    print()
    print(f"The actual text: {example_response['content'][0]['text']}")
    print(f"Tokens used: {example_response['usage']['input_tokens']} in, {example_response['usage']['output_tokens']} out")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercises

    ### Exercise 1: Query a public API

    Use the NCBI API to search for a gene involved in pain signaling. Try searching for `SCN9A` (which encodes NaV1.7, a key pain channel). Parse the JSON response and print the gene IDs found.
    """)
    return


@app.cell
def _(json, urllib_2):
    import urllib.request
    _url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=gene&term=SCN9A+AND+human[organism]&retmode=json'
    with urllib_2.request.urlopen(_url) as _response:
        data_1 = json.loads(_response.read().decode('utf-8'))
    gene_ids = data_1['esearchresult']['idlist']
    print(f'Search: SCN9A in human')
    print(f'Gene IDs found: {gene_ids}')
    print(f"Total results: {data_1['esearchresult']['count']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Handle an error gracefully

    Write code that tries to fetch a URL that will fail (use `https://httpstat.us/500` — a test URL that always returns a 500 error). Use a try/except block to catch the error and print a helpful message instead of crashing.
    """)
    return


@app.cell
def _(urllib_3):
    import urllib.request
    import urllib.error
    _url = 'https://httpstat.us/500'
    try:
        with urllib_3.request.urlopen(_url) as _response:
            print(f'Success: {_response.status}')
    except urllib_3.error.HTTPError as e:
        print(f'HTTP Error {e.code}: {e.reason}')
        print('This is a server error — not your fault. Try again later.')
    except urllib_3.error.URLError as e:
        print(f'URL Error: {e.reason}')
        print('Could not reach the server. Check your internet connection.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Inspect JSON structure

    The cell below fetches data about the human TRPV1 gene from NCBI. Your task: navigate the JSON response to extract and print (a) the gene name, (b) the description, and (c) the genomic location (chromosome and map location).
    """)
    return


@app.cell
def _(json, urllib_4):
    import urllib.request
    _url = 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=gene&id=7442&retmode=json'
    with urllib_4.request.urlopen(_url) as _response:
        data_2 = json.loads(_response.read().decode('utf-8'))
    print('Full response structure:')
    print(json.dumps(data_2, indent=2)[:2000])
    print('\n... (truncated)')
    return (data_2,)


@app.cell
def _(data_2):
    # Your code here — extract the gene name, description, and genomic location
    gene_info = data_2['result']['7442']
    print(f"Gene name: {gene_info['name']}")
    print(f"Description: {gene_info['description']}")
    print(f"Chromosome: {gene_info.get('chromosome', 'N/A')}")
    print(f"Map location: {gene_info.get('maplocation', 'N/A')}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Missing Semester, Lecture 1**: [The Shell](https://missing.csail.mit.edu/2020/course-shell/) — covers `curl`, pipes, and command-line tools for making HTTP requests
    - [Python docs: `urllib.request`](https://docs.python.org/3/library/urllib.request.html) — the built-in HTTP client used in this notebook
    - [Python docs: `json` module](https://docs.python.org/3/library/json.html) — the built-in JSON encoder/decoder for parsing API responses
    - [Python `requests` library](https://docs.python-requests.org/en/latest/) — the standard third-party HTTP library; much more ergonomic than `urllib` for complex use cases
    - [MDN Web Docs: HTTP Status Codes](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status) — the authoritative reference for understanding 200, 401, 404, 429, 500, and all other status codes
    - [MDN Web Docs: An Overview of HTTP](https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview) — a clear explanation of HTTP request/response, methods, headers, and the protocol structure
    - [NCBI E-utilities Documentation](https://www.ncbi.nlm.nih.gov/books/NBK25501/) — full documentation for the NCBI Entrez API used in this notebook to query gene databases
    - [REST API Concepts (MDN)](https://developer.mozilla.org/en-US/docs/Glossary/REST) — what REST means and why most modern APIs (including Anthropic's) follow this pattern
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - An **API call** is just an HTTP request that travels over the internet and gets a response
    - **URLs** have parts: protocol, domain, path, and query parameters
    - **HTTP methods**: GET (fetch), POST (send/create), PUT (update), DELETE (remove)
    - **Status codes** tell you what happened: 200 = success, 4xx = your error, 5xx = server error
    - **JSON** is how APIs send structured data — it maps directly to Python dicts and lists
    - **localhost** means "this computer" — that's where marimo runs
    - **API keys** are stored as environment variables to keep them out of code
    - Network errors (timeouts, rate limits, DNS failures) are normal — handle them with try/except

    With this module complete, you now have a working mental model of your computer: the **filesystem** (where things are stored), **processes** (how things run), and **networking** (how things communicate). When AI tools manipulate files, run commands, or make API calls, you know what's happening under the hood.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Processes and Environment](02-processes-and-environment.py) | [Module Index](../README.md) | [Next: Your AI Toolkit \u2192](04-your-ai-toolkit.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created notebook with initial content
    - 2026-03-25: Added "Why this matters" rationale section
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: QA pass — removed code cell containing markdown text (duplicate of adjacent markdown cell)
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

