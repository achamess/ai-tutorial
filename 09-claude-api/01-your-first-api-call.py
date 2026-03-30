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
    # 01: Your First API Call

    You already use Claude in two ways: **Claude chat** (the web/app interface) and **Claude Code** (the CLI agent in your terminal). This notebook introduces a third way -- the **Claude API** -- which is the key to building custom research tools that work exactly the way you need them to.

    By the end of this notebook, you'll be able to send messages to Claude programmatically from Python and understand exactly what comes back.

    **Key references:** [Anthropic API: Getting Started](https://docs.anthropic.com/en/api/getting-started) | [Anthropic Python SDK (GitHub)](https://github.com/anthropics/anthropic-sdk-python) | [Anthropic Pricing](https://www.anthropic.com/pricing)

    **Local reference:** [resources/references/anthropic-api-getting-started.md](../resources/references/anthropic-api-getting-started.md)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Probability and AI Math](../08-math-you-need/03-probability-and-ai-math.py) | [Module Index](../README.md) | [Next: Structured Outputs \u2192](02-structured-outputs.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - The API is how you go from asking Claude one question at a time to building automated research tools. Instead of manually pasting 50 paper abstracts into Claude chat, you write a script that processes them all and returns structured data.
    > - For your binder design work, the API lets you batch-annotate gene lists, classify screening hits, and generate structured summaries of experimental results -- all programmatically.
    > - Understanding the API is the foundation for everything in the remaining modules: structured outputs, batch processing, literature pipelines, and data analysis workflows.
    > - The cost model (tokens = money) is important to understand before you start building pipelines that process hundreds or thousands of items.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## API vs Chat vs Claude Code — when to use which

    | Tool | Best for | Example |
    |------|----------|--------|
    | **Claude chat** | One-off questions, brainstorming, exploring ideas | "What's the current understanding of NaV1.7's role in inflammatory pain?" |
    | **Claude Code** | Working with files, writing code, editing projects | "Add error bars to this calcium imaging plot" |
    | **Claude API** | Automation, batch processing, building custom tools | Process 200 paper abstracts and extract targets + mechanisms |

    The API is what you reach for when you need Claude to do the **same kind of task many times**, or when you want to **embed Claude inside a larger workflow**. Think of it as the difference between pipetting by hand (chat) and setting up a plate reader protocol (API).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Setting up your API key

    The API authenticates with an **API key** — a secret string that identifies your account. You get one from [console.anthropic.com](https://console.anthropic.com/).

    The safe way to provide it is via an **environment variable** called `ANTHROPIC_API_KEY`. You should have this set already (Claude Code uses the same key). Let's verify:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Security rule:** Never paste your API key directly into a notebook or Python file. Always use environment variables. If you accidentally commit a key to git, rotate it immediately at console.anthropic.com.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The Anthropic Python SDK

    The `anthropic` package is already installed in our environment. Let's import it and create a **client** — the object we'll use for all API calls.
    """)
    return


@app.cell
def _():
    from anthropic import Anthropic

    # Create the client — it automatically reads ANTHROPIC_API_KEY from the environment
    client = Anthropic()

    print("Client ready.")
    return (client,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's all the setup. Two lines: import and create. Now let's make our first call.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Anatomy of an API call

    Every API call has the same basic structure:

    ```python
    message = client.messages.create(
        model="claude-sonnet-4-6",         # which Claude model to use
        max_tokens=1024,                    # maximum length of the response
        system="...",                       # optional: system prompt (sets behavior)
        messages=[                           # the conversation
            {"role": "user", "content": "your question here"}
        ]
    )
    ```

    Let's break down each parameter:

    | Parameter | What it does |
    |-----------|-------------|
    | `model` | Which Claude model to use. We'll use `claude-sonnet-4-6` — fast and cost-effective for most tasks. |
    | `max_tokens` | Cap on response length. 1024 tokens is ~750 words — plenty for most answers. |
    | `system` | Sets Claude's role/behavior for the whole conversation. Optional but very useful. |
    | `messages` | A list of messages. Each has a `role` ("user" or "assistant") and `content`. |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### API Call Lifecycle

    """),
    mo.mermaid(
        """
        sequenceDiagram
            participant You as Your Python Code
            participant SDK as Anthropic SDK
            participant HTTP as HTTPS Request
            participant API as Anthropic Servers
        
            You->>SDK: client.messages.create(model, messages, ...)
            SDK->>HTTP: POST /v1/messages<br/>+ API key header<br/>+ JSON body
            HTTP->>API: Encrypted request<br/>over the internet
        
            Note over API: Claude processes your prompt<br/>generates response tokens
        
            API->>HTTP: JSON response<br/>(content, usage, stop_reason)
            HTTP->>SDK: Parse HTTP response
            SDK->>You: Message object<br/>.content[0].text = "..."<br/>.usage.input_tokens = N<br/>.usage.output_tokens = M
        """
    ),
    mo.md(r"""

    Each API call follows this lifecycle. Your code never communicates with Claude directly -- the SDK handles authentication, serialization, error handling, and retries. The response comes back as a structured `Message` object that you can inspect for both the text content and metadata like token usage.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Your first call: ask Claude about a pain biology concept

    Let's ask Claude to explain a concept relevant to your work.
    """)
    return


@app.cell
def _(client):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": "Explain in 3 sentences how NaV1.7 gain-of-function mutations cause pain disorders."
            }
        ]
    )

    # Extract the text from the response
    print(message.content[0].text)
    return (message,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's it. You just called an LLM from Python. Let's understand what came back.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Understanding the response object

    The `message` variable isn't just text — it's a structured object with useful metadata.
    """)
    return


@app.cell
def _(message):
    # The full response object
    print("Type:", type(message))
    print("Model used:", message.model)
    print("Stop reason:", message.stop_reason)
    print()

    # Token usage — this is what determines cost
    print("Input tokens:", message.usage.input_tokens)
    print("Output tokens:", message.usage.output_tokens)
    print()

    # The actual content
    print("Number of content blocks:", len(message.content))
    print("Content type:", message.content[0].type)
    print("Text:", message.content[0].text[:100], "...")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Key fields:

    - **`message.content[0].text`** — the actual response text. This is what you'll use 99% of the time.
    - **`message.usage`** — token counts, which determine cost.
    - **`message.stop_reason`** — why Claude stopped. `"end_turn"` means it finished naturally. `"max_tokens"` means it was cut off (you should increase `max_tokens`).
    - **`message.model`** — confirms which model was used.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Adding a system prompt

    The **system prompt** tells Claude how to behave. It's like briefing a research assistant before they start. This is where you set the expertise level, output format, and constraints.
    """)
    return


@app.cell
def _(client):
    message_1 = client.messages.create(model='claude-sonnet-4-6', max_tokens=1024, system='You are an expert pain neurobiologist. Give precise, technical answers suitable for a researcher who designs de novo protein binders targeting ion channels. Keep answers concise — no more than 4 sentences.', messages=[{'role': 'user', 'content': 'What makes the NaV1.8 channel a promising target for pain therapeutics compared to NaV1.7?'}])
    print(message_1.content[0].text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice how the system prompt shapes the response — you get a technical, focused answer instead of a broad textbook explanation. The system prompt is your most powerful lever for controlling Claude's output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## A reusable helper function

    You'll be making lots of API calls. Let's wrap the pattern in a function so we don't repeat ourselves.
    """)
    return


@app.cell
def _(client):
    def ask_claude(prompt, system=None, model='claude-sonnet-4-6', max_tokens=1024):
        """Send a prompt to Claude and return the response text."""
        kwargs = {'model': model, 'max_tokens': max_tokens, 'messages': [{'role': 'user', 'content': prompt}]}
        if system:
            kwargs['system'] = system
        message = client.messages.create(**kwargs)
        return message.content[0].text
    _answer = ask_claude('What is TRPV1 and why is it important in nociception?', system='Answer in exactly 2 sentences.')
    # Test it
    print(_answer)
    return (ask_claude,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now you can call `ask_claude("your question")` anywhere in this notebook (or copy the function into other notebooks).

    > **Think Python connection:** This is the same function pattern from Module 01 — `def`, parameters with defaults, a docstring, and `return`. The only new thing is that the function body calls an external API instead of doing math.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Cost awareness

    API calls cost money. Not much per call, but it adds up if you're processing thousands of items. Here's what you need to know:

    ### Models and pricing (approximate, as of early 2026)

    | Model | Input (per 1M tokens) | Output (per 1M tokens) | When to use |
    |-------|----------------------|------------------------|-------------|
    | `claude-sonnet-4-6` | ~$3 | ~$15 | **Default choice.** Great for most tasks. |
    | `claude-opus-4-6` | ~$15 | ~$75 | Complex reasoning, nuanced analysis. |
    | `claude-haiku-3-5` | ~$0.80 | ~$4 | High-volume, simpler tasks (classification, extraction). |

    ### Token intuition

    - 1 token is roughly 4 characters or 0.75 words
    - A typical abstract: ~200-300 tokens
    - A page of text: ~400-500 tokens
    - Your question + Claude's answer in the example above: check the usage below
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Warning:** API costs add up quickly when processing large batches. A single call costs fractions of a cent, but processing 1,000 paper abstracts through Opus can cost $5-15. Always start development and testing with Haiku (cheapest), switch to Sonnet for production runs, and reserve Opus for tasks that truly need its reasoning capability. Monitor your spending at [console.anthropic.com](https://console.anthropic.com/) and set billing alerts.

    > **Tip:** Use Haiku for testing, Sonnet for production. When building a new pipeline, use `claude-haiku-3-5` during development -- it's 4x cheaper than Sonnet and fast enough to iterate quickly. Once your prompts and parsing logic are working correctly, switch to `claude-sonnet-4-6` for the final run. This saves real money: debugging 20 iterations on Haiku costs ~$0.10 vs ~$0.40 on Sonnet.

    > **Decision point: Which Claude model for which task**
    >
    > | Model | Cost (input/output per 1M tokens) | Speed | Quality | Use when |
    > |-------|-----------------------------------|-------|---------|----------|
    > | **Haiku 3.5** | ~$0.80 / $4 | Fastest | Good for simple tasks | Classification, extraction, testing/development, high-volume processing |
    > | **Sonnet 4** | ~$3 / $15 | Fast | Great for most tasks | Production pipelines, structured outputs, analysis, your default choice |
    > | **Opus 4** | ~$15 / $75 | Slower | Best reasoning | Complex interpretation, nuanced scientific analysis, multi-step reasoning |
    >
    > **Rule of thumb:** Start with Sonnet. Only upgrade to Opus if Sonnet's answers are noticeably worse for your specific task. Downgrade to Haiku for anything that's simple pattern matching (e.g., "is this gene an ion channel? yes/no").
    """)
    return


@app.cell
def _(client):
    # Let's check the cost of our earlier call
    # We'll make a fresh call and inspect usage
    message_2 = client.messages.create(model='claude-sonnet-4-6', max_tokens=512, messages=[{'role': 'user', 'content': 'What is the role of SCN9A in inherited pain disorders? Answer in 3 sentences.'}])
    inp = message_2.usage.input_tokens
    out = message_2.usage.output_tokens
    cost_input = inp * 3.0 / 1000000
    cost_output = out * 15.0 / 1000000
    total = cost_input + cost_output
    print(f'Input tokens:  {inp}')
    print(f'Output tokens: {out}')
    print(f'Estimated cost: ${total:.5f}')
    print(f'\nAt this rate, processing 1000 similar questions would cost ~${total * 1000:.2f}')
    # Approximate cost for claude-sonnet-4-6
    print(f'\n{message_2.content[0].text}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Rule of thumb:** For the batch-processing tasks you'll build in this module, a run of a few hundred items will typically cost well under $1. Just stay aware of it — especially if you're using Opus or sending large inputs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Choosing max_tokens wisely

    Setting `max_tokens` too low cuts off responses. Setting it too high doesn't cost extra (you only pay for tokens actually generated), but it's good practice to set a reasonable cap. Some guidelines:

    | Task | Suggested max_tokens |
    |------|---------------------|
    | Short answer (1-3 sentences) | 256 |
    | Paragraph explanation | 512-1024 |
    | Detailed analysis | 2048-4096 |
    | Long-form generation | 4096-8192 |
    """)
    return


@app.cell
def _(client):
    # What happens when max_tokens is too low?
    message_3 = client.messages.create(model='claude-sonnet-4-6', max_tokens=20, messages=[{'role': 'user', 'content': 'Describe the mechanism of TRPV1 activation.'}])
    print('Stop reason:', message_3.stop_reason)
    print('Response:', message_3.content[0].text)  # way too low for a real answer  # will be "max_tokens" instead of "end_turn"
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    When `stop_reason` is `"max_tokens"`, Claude was cut off mid-answer. Always check this if your responses look incomplete.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Gene summary function

    Write a function called `gene_pain_summary` that:

    1. Takes a **gene name** (e.g., `"SCN9A"`, `"TRPV1"`, `"CALCA"`)
    2. Sends it to Claude with a system prompt that asks for a structured summary of the gene's role in pain biology
    3. Returns the text response

    Then call it for at least 3 different pain-related genes and print the results.

    Hint: use the `ask_claude` helper function we built above, or write the `client.messages.create` call directly — either approach works.
    """)
    return


@app.cell
def _(ask_claude):
    # Your code here

    def gene_pain_summary(gene_name):
        """Get a summary of a gene's role in pain biology from Claude."""
        system = (
            "You are an expert pain neurobiologist. When given a gene name, provide a brief "
            "summary covering: (1) what protein it encodes, (2) where it's expressed in the "
            "pain pathway, (3) its role in nociception, and (4) any known link to human pain "
            "disorders. Keep it to 4-5 sentences."
        )
        return ask_claude(
            f"Summarize the role of {gene_name} in pain biology.",
            system=system
        )


    # Test with pain-relevant genes
    genes = ["SCN9A", "SCN10A", "TRPV1"]

    for gene in genes:
        print(f"=== {gene} ===")
        print(gene_pain_summary(gene))
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Experiment with parameters

    Try modifying the API call to see how different parameters change the output:

    1. Change the system prompt to request a different format (e.g., bullet points instead of sentences)
    2. Try different `max_tokens` values and observe how `stop_reason` changes
    3. Compare the same question with and without a system prompt
    """)
    return


@app.cell
def _(ask_claude):
    # Your experiments here
    _answer = ask_claude('What are the main classes of nociceptors in DRG?', system='Answer using bullet points. Be concise — one line per bullet.')
    # Example: bullet-point format
    print(_answer)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - **API vs chat vs Claude Code** — the API is for automation and custom tools
    - **Authentication** — `ANTHROPIC_API_KEY` environment variable, never hardcoded
    - **The SDK** — `from anthropic import Anthropic`, then `client = Anthropic()`
    - **Making a call** — `client.messages.create(model, max_tokens, messages)`
    - **System prompts** — control Claude's behavior and output format
    - **The response object** — `message.content[0].text` for the answer, `message.usage` for token counts
    - **Cost awareness** — tokens drive cost; Sonnet is the cost-effective default

    Next up: getting **structured data** (JSON) from Claude instead of free text — which is what makes the API truly powerful for research pipelines.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Probability and AI Math](../08-math-you-need/03-probability-and-ai-math.py) | [Module Index](../README.md) | [Next: Structured Outputs \u2192](02-structured-outputs.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created notebook with initial content
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: QA pass — removed duplicate security rule cell (code cell with markdown content)
    - 2026-03-25: QA pass — added "Why this matters" rationale section
    - 2026-03-25: Added standardized callouts and decision frameworks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created notebook with initial content
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: QA pass — removed duplicate security rule cell (code cell with markdown content)
    - 2026-03-25: QA pass — added "Why this matters" rationale section
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

