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
    # 03: How Claude "Thinks"

    Now that you understand what LLMs are (pattern-completion machines) and how they process text (as tokens within a context window), let's look at how Claude specifically works — the conversation structure, the sampling process, and the practical implications for your research.

    **This notebook requires an `ANTHROPIC_API_KEY` environment variable.** If you haven't set one up yet, you can still read through the markdown explanations — the code cells will just fail with an auth error.

    > To set your API key, run this in your terminal:
    > ```bash
    > export ANTHROPIC_API_KEY="your-key-here"
    > ```
    > Or add it to your `~/.zshrc` (Mac) / `~/.bashrc` (Linux) for persistence.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Tokens and Context Windows](02-tokens-and-context.py) | [Module Index](../README.md) | [Next: Anatomy of a Prompt \u2192](../04-prompt-engineering/01-anatomy-of-a-prompt.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - System prompts are how you turn Claude from a generic assistant into a specialized pain biology and protein engineering advisor. The difference between "tell me about NaV1.7" and getting a tailored analysis of binder target sites comes down to system prompt design.
    > - Understanding temperature lets you choose between deterministic data extraction (temperature 0 for parsing screening results) and creative brainstorming (temperature 1 for novel binder strategies). Using the wrong setting wastes time and produces worse output.
    > - Knowing when and why Claude hallucinates — especially with citations and specific numbers — means you'll always provide source material for critical tasks and verify claims before putting them in a grant or paper.
    > - The conversation structure (system prompt + message history) is exactly what you'll control when building automated workflows via the API. This notebook is the conceptual foundation for everything in Modules 04 and 05.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## How Claude was trained

    Claude is built by Anthropic using a three-stage process (we covered this briefly in notebook 01, but here's the detail):

    ### Stage 1: Pre-training
    Claude reads a massive corpus of text from the internet, books, and other sources. It learns to predict the next token. After this stage, it can write fluent text but isn't a good conversational assistant yet.

    ### Stage 2: RLHF (Reinforcement Learning from Human Feedback)
    Human trainers rate Claude's responses. "This answer about NaV1.7 pharmacology is accurate and helpful — 5/5. This one contains a made-up citation — 1/5." Claude's weights get adjusted to produce more of the high-rated responses.

    This is why Claude:
    - Tends to be helpful and respond to what you actually asked
    - Hedges when it's uncertain ("I'm not sure, but...")
    - Refuses clearly harmful requests
    - Formats responses nicely with headers, lists, etc.

    ### Stage 3: Constitutional AI (Anthropic's approach)
    Anthropic uses a technique called **Constitutional AI** where Claude evaluates its own outputs against a set of principles — helpfulness, harmlessness, honesty. This is like an internal peer review process.

    **Analogy:** Pre-training is like reading every textbook and paper in the field. RLHF is like getting feedback from your PI on your writing. Constitutional AI is like developing your own internal standards for scientific rigor.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The conversation structure

    When you talk to Claude — whether through the chat interface or the API — the conversation has a specific structure:

    ```
    ┌──────────────────────────────────────┐
    │  System prompt                       │  ← Sets Claude's behavior and context
    │  (invisible to the user in chat)     │
    ├──────────────────────────────────────┤
    │  User message 1                      │  ← Your first message
    ├──────────────────────────────────────┤
    │  Assistant message 1                 │  ← Claude's first response
    ├──────────────────────────────────────┤
    │  User message 2                      │  ← Your follow-up
    ├──────────────────────────────────────┤
    │  Assistant message 2                 │  ← Claude's next response
    ├──────────────────────────────────────┤
    │  ...                                 │
    └──────────────────────────────────────┘
    ```

    Every time Claude generates a response, it sees the **entire conversation history** — system prompt, all previous user and assistant messages, and the current user message. This is all crammed into the context window.

    **Key insight:** Claude doesn't have memory between conversations. Each conversation starts completely fresh. When you open a new chat, Claude doesn't remember anything from your previous chats.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        graph TD
            subgraph CONV ["What Claude sees at each turn"]
                SYS["<b>System Prompt</b><br/>'You are a pain biology expert...'<br/><i>Sets behavior for entire conversation</i>"]
                U1["<b>User Message 1</b><br/>'What controls should I include<br/>for my NaV1.7 binder assay?'"]
                A1["<b>Assistant Message 1</b><br/>'You should include a vehicle control,<br/>a scrambled binder, and...'"]
                U2["<b>User Message 2</b><br/>'How would I measure selectivity<br/>over NaV1.5?'"]
                A2["<b>Assistant Message 2</b><br/><i>(Claude generates this now,<br/>seeing ALL of the above)</i>"]
        
                SYS --> U1 --> A1 --> U2 --> A2
            end
        
            NOTE["Each turn, Claude sees the<br/><b>entire history</b> above.<br/>No memory between conversations —<br/>each new chat starts fresh."]
        
            style SYS fill:#aa44aa,color:#fff
            style U1 fill:#4488cc,color:#fff
            style A1 fill:#44aa88,color:#fff
            style U2 fill:#4488cc,color:#fff
            style A2 fill:#44aa88,color:#fff,stroke:#cc4444,stroke-width:3px
            style NOTE fill:#fff,stroke:#999
        """
    )
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## System prompts: setting the stage

    The **system prompt** is a special message that sets Claude's behavior for the entire conversation. It's like briefing a new lab member before they start a task.

    In the chat interface, system prompts are set behind the scenes. In the API, you control them directly — and this is one of the most powerful tools for getting good output.
    """)
    return


@app.cell
def _():
    import anthropic

    # Create the client — reads ANTHROPIC_API_KEY from your environment automatically
    client = anthropic.Anthropic()
    print("Anthropic client ready.")
    return (client,)


@app.cell
def _(client):
    # Without a system prompt — generic response
    response_generic = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": "What are the main challenges in developing NaV1.7 inhibitors?"
            }
        ]
    )

    print("WITHOUT system prompt:")
    print("=" * 50)
    print(response_generic.content[0].text)
    print(f"\n({response_generic.usage.output_tokens} tokens)")
    return


@app.cell
def _(client):
    # With a system prompt — tailored response
    response_tailored = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=(
            "You are a scientific advisor helping a pain biologist who designs "
            "de novo protein binders for ion channels (NaV1.7, NaV1.8, KCNQ2/3). "
            "They use computational protein design tools like RFdiffusion and ProteinMPNN. "
            "Give concise, technically precise answers. Focus on practical implications "
            "for their protein binder approach rather than small-molecule drug development."
        ),
        messages=[
            {
                "role": "user",
                "content": "What are the main challenges in developing NaV1.7 inhibitors?"
            }
        ]
    )

    print("WITH system prompt (tailored to your work):")
    print("=" * 50)
    print(response_tailored.content[0].text)
    print(f"\n({response_tailored.usage.output_tokens} tokens)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Temperature and sampling

    Remember from notebook 01 that LLMs produce a probability distribution over possible next tokens. **Temperature** controls how Claude samples from that distribution. See the [Anthropic API docs on temperature](https://docs.anthropic.com/en/api/messages) for the parameter specification.

    - **Temperature 0**: Always pick the highest-probability token. Deterministic, repetitive, "safe."
    - **Temperature 1**: Sample proportionally to the probabilities. Creative, varied, sometimes surprising.
    - **Temperature > 1**: Even more random. Rarely useful — outputs become incoherent.

    **Analogy:** Imagine you're writing a methods section. At temperature 0, you'd write the most standard, textbook version. At temperature 1, you might choose slightly unusual phrasing that's still correct. At temperature 2, you'd start writing poetry about your Western blots.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** Temperature is your creativity dial. At temperature 0, Claude always picks the highest-probability next token — giving you deterministic, consistent, "safe" output. At temperature 1, it samples proportionally from the probability distribution — giving you creative variation. Think of it as the difference between a cautious methods section (temperature 0) and a brainstorming whiteboard session (temperature 1). For most research tasks (summaries, analysis, data extraction), use 0. For brainstorming, hypothesis generation, or when you want diverse ideas, use 0.7-1.0.
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt
    tokens = ['NaV1.7', 'multiple', 'several', 'high', 'various', 'the', 'both', 'specific']
    # Visualize how temperature affects token selection
    # These are hypothetical probabilities for next token after "DRG neurons express"
    base_probs = np.array([0.3, 0.2, 0.15, 0.12, 0.1, 0.06, 0.04, 0.03])

    def apply_temperature(probs, temperature):
        """Apply temperature scaling to a probability distribution."""
        if temperature == 0:
            result = np.zeros_like(probs)
            result[np.argmax(probs)] = 1.0
            return result  # Deterministic: all probability on the top choice
        log_probs = np.log(probs + 1e-10)
        scaled = log_probs / temperature
        scaled = scaled - np.max(scaled)
        exp_scaled = np.exp(scaled)
        return exp_scaled / exp_scaled.sum()
    temperatures = [0, 0.3, 0.7, 1.0, 1.5]  # numerical stability
    _fig, axes = plt.subplots(1, len(temperatures), figsize=(18, 4), sharey=True)
    for _ax, _temp in zip(axes, temperatures):
        adjusted = apply_temperature(base_probs, _temp)
        colors = ['#cc4444' if p == max(adjusted) else 'steelblue' for p in adjusted]
        _ax.barh(tokens, adjusted, color=colors)
        _ax.set_title(f'Temp = {_temp}', fontsize=11)
        _ax.set_xlim(0, 1.05)
        _ax.invert_yaxis()
        if _temp == 0:
            _ax.set_ylabel('Next token')
    _fig.suptitle('How temperature affects token probabilities after: "DRG neurons express ___"', fontsize=12, y=1.02)
    plt.tight_layout()
    plt.show()
    print("Temperature 0:   Always picks 'NaV1.7' — deterministic but repetitive")
    print('Temperature 0.3: Strongly favors top choices — focused but with slight variation')
    print("Temperature 0.7: Good balance — Claude's typical default range")
    print('Temperature 1.0: Samples proportionally — more creative/varied')
    print('Temperature 1.5: Very flat — even unlikely tokens get picked often')
    return (plt,)


@app.cell
def _(client):
    # Let's see temperature in action with the API
    # We'll ask the same question at different temperatures
    question = 'Suggest a creative name for a de novo protein binder targeting NaV1.7.'
    print('Same question, three different temperatures:')
    print('=' * 60)
    for _temp in [0.0, 0.5, 1.0]:
        _response = client.messages.create(model='claude-sonnet-4-20250514', max_tokens=100, temperature=_temp, messages=[{'role': 'user', 'content': question}])
        print(f'\nTemperature {_temp}:')
        print(f'  {_response.content[0].text[:200]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** What temperature setting for different research tasks?
    >
    > | Task | Recommended temperature | Why |
    > |------|------------------------|-----|
    > | Data extraction (parsing screening results into JSON) | 0.0 | You want deterministic, consistent output — the same input should always give the same output |
    > | Paper summaries, grant section drafts | 0.0 - 0.3 | You want accuracy and consistency, with just enough variation to avoid robotic phrasing |
    > | Code generation, debugging | 0.0 | Code either works or doesn't — you want the most likely correct answer |
    > | Rewriting a paragraph for clarity | 0.3 - 0.5 | Some creative latitude in phrasing, but still grounded |
    > | Brainstorming experimental approaches | 0.7 - 1.0 | You want diverse ideas; run the same prompt multiple times to get different suggestions |
    > | Generating hypotheses or alternative interpretations | 0.7 - 1.0 | Creative exploration of possibility space |
    > | Naming compounds, writing titles | 0.5 - 0.7 | Balance between creative and sensible |
    >
    > **Default to 0.0** and only increase when you specifically want variation. Most research tasks benefit from consistency, not randomness.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### When to use which temperature

    | Temperature | Use case | Example |
    |-------------|----------|----------|
    | 0 - 0.3 | Factual answers, data extraction, code | "Extract all gene names from this abstract" |
    | 0.5 - 0.7 | General writing, summaries | "Summarize this paper's findings on NaV1.7" |
    | 0.7 - 1.0 | Creative writing, brainstorming | "Suggest alternative approaches to NaV1.7 inhibition" |

    For most research tasks, the default temperature (which Claude uses in the chat interface) works well. You mainly need to think about temperature when using the API.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why understanding hallucination matters for you specifically:** As someone writing grants and designing experiments based on AI output, a hallucinated citation in your R01 or a fabricated Kd value in your analysis could have real consequences. The strategies below are not theoretical — they're the specific practices that keep your work scientifically sound when using AI tools.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** Hallucination risk varies dramatically by task type. Claude is highly reliable for summarizing text you provide, explaining well-established concepts, and generating code. It is unreliable for generating specific citations (it will fabricate plausible-looking author names, journals, and DOIs), recalling exact numerical values (Kd, IC50, p-values from specific papers), and claiming knowledge of recent events past its training cutoff. The risk increases with specificity: "NaV1.7 is important for pain" (low risk) vs. "The Kd of antibody MAB-127 for NaV1.7 is 3.2 nM (Zhang et al., Nature 2024)" (high risk — this could be entirely fabricated).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why Claude hallucinates (and how to reduce it)

    **Hallucination** is when Claude generates text that sounds authoritative but is factually wrong. This happens because Claude is a pattern-completion machine, not a fact database.

    ### Why it happens

    1. **Training data gaps**: If Claude never saw a specific fact during training (e.g., the exact Kd of your unpublished binder), it will generate a plausible-sounding number rather than saying "I don't know."

    2. **Pattern over precision**: Claude learned that sentences like "The Kd was 12.3 nM (Smith et al., 2023)" are common in papers. It can generate sentences with that pattern, filling in plausible but invented values and citations.

    3. **Sycophancy**: Due to RLHF training, Claude has a slight tendency to tell you what you want to hear rather than pushing back. If you assert something incorrect, Claude might agree rather than correct you.

    ### Common hallucination patterns in research

    | Type | Example | Risk level |
    |------|---------|------------|
    | Fake citations | "Smith et al. (2023) showed that..." | HIGH — always verify |
    | Wrong numbers | "NaV1.7 has a Kd of 2.3 nM for..." | HIGH — always verify |
    | Plausible but wrong mechanisms | "KCNQ2 is activated by capsaicin" | MEDIUM — verify if unsure |
    | Overgeneralization | "All DRG neurons express NaV1.7" | LOW — you'd catch this |
    | Confident uncertainty | Stating something definitively that is actually debated | MEDIUM |
    """)
    return


@app.cell
def _(client):
    # Let's deliberately trigger a potential hallucination and see how to prevent it

    # BAD: Asking for specific citations without source material
    response_risky = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": (
                    "List 3 specific papers published in 2024 about de novo protein "
                    "binders for voltage-gated sodium channels, with authors, journal, "
                    "and DOIs."
                )
            }
        ]
    )

    print("RISKY PROMPT (asking for specific citations from memory):")
    print("=" * 60)
    print(response_risky.content[0].text)
    print()
    print("⚠ WARNING: These citations may be partially or entirely fabricated!")
    print("Claude generates plausible-LOOKING citations, but they may not exist.")
    return


@app.cell
def _(client):
    # BETTER: Ask Claude to be explicit about uncertainty

    response_safer = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=300,
        system=(
            "You are a careful scientific advisor. When you are uncertain about "
            "specific facts (papers, numbers, dates), say so explicitly. Never "
            "fabricate citations. If you can't recall exact details, describe what "
            "you know approximately and suggest how the user can verify."
        ),
        messages=[
            {
                "role": "user",
                "content": (
                    "What recent work has been done on de novo protein binders "
                    "for voltage-gated sodium channels? I need actual papers I can look up."
                )
            }
        ]
    )

    print("SAFER PROMPT (system prompt encourages honesty about uncertainty):")
    print("=" * 60)
    print(response_safer.content[0].text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Strategies to reduce hallucination

    1. **Provide source material.** Paste the paper, data, or reference text into the conversation. Claude is much more accurate when working from provided text than from "memory."

    2. **Use system prompts that encourage honesty.** Tell Claude to say "I'm not sure" rather than guess.

    3. **Ask for reasoning.** "Explain your reasoning" or "How confident are you?" can surface uncertainty.

    4. **Verify specific claims.** Never trust citations, specific numbers, or niche factual claims without checking the source.

    5. **Use Claude for what it's good at.** Drafting, summarizing provided text, explaining concepts, writing code, brainstorming — these are high-reliability tasks. Looking up specific facts from memory is low-reliability.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Strengths and limitations for research

    Based on everything we've covered, here's a practical map of Claude's capabilities for your work:
    """)
    return


@app.cell
def _(plt):
    import matplotlib.patches as mpatches
    tasks = [('Draft grant aims', 8, 9, 'writing'), ('Summarize a pasted paper', 9, 9, 'analysis'), ('Write Python analysis code', 8, 9, 'coding'), ('Explain a concept', 9, 8, 'knowledge'), ('Brainstorm experiments', 7, 8, 'creative'), ('Compare two papers (pasted)', 8, 8, 'analysis'), ('Edit/improve your writing', 9, 8, 'writing'), ('Debug code errors', 8, 8, 'coding'), ('Generate protein sequences', 3, 4, 'specialized'), ('Recall specific citations', 3, 6, 'knowledge'), ('Precise calculations', 4, 5, 'knowledge'), ('Predict experimental outcomes', 4, 5, 'specialized'), ('Recent literature search', 2, 7, 'knowledge'), ('Design a binder sequence', 2, 3, 'specialized')]
    _fig, _ax = plt.subplots(figsize=(12, 8))
    category_colors = {'writing': '#4488cc', 'analysis': '#44aa88', 'coding': '#cc8844', 'knowledge': '#aa44aa', 'creative': '#ccaa44', 'specialized': '#cc4444'}
    for task, reliability, usefulness, category in tasks:
        _ax.scatter(reliability, usefulness, c=category_colors[category], s=150, zorder=3, edgecolors='white', linewidth=1)
        _ax.annotate(task, (reliability, usefulness), fontsize=8, xytext=(8, 4), textcoords='offset points')
    _ax.axvline(x=5.5, color='gray', linestyle='--', alpha=0.3)
    _ax.axhline(y=5.5, color='gray', linestyle='--', alpha=0.3)
    _ax.text(8, 3, 'Reliable but\nniche use', ha='center', fontsize=9, color='gray', alpha=0.6)
    _ax.text(3, 9, 'Useful but\nverify carefully', ha='center', fontsize=9, color='gray', alpha=0.6)
    _ax.text(8, 9, 'SWEET SPOT\nUse heavily', ha='center', fontsize=11, color='green', fontweight='bold', alpha=0.5)
    _ax.text(3, 3, 'Consider\nother tools', ha='center', fontsize=9, color='gray', alpha=0.6)
    _ax.set_xlabel('Reliability (how often Claude gets it right)', fontsize=11)
    _ax.set_ylabel('Usefulness (time saved / value added)', fontsize=11)
    _ax.set_title("Claude's capabilities for pain biology research", fontsize=13)
    _ax.set_xlim(0, 10.5)
    _ax.set_ylim(0, 10.5)
    legend_patches = [mpatches.Patch(color=c, label=l) for l, c in category_colors.items()]
    _ax.legend(handles=legend_patches, loc='lower right', fontsize=9)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The sweet spot — top right — is where you should focus your AI usage: tasks that are both reliable and high-value. These are primarily **text transformation tasks** (summarize, draft, edit, explain) and **code generation**.

    The bottom left is where you should use specialized tools instead: actual protein design tools (RFdiffusion, ProteinMPNN) for binder sequences, PubMed for literature search, Python for calculations.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: How framing changes output

    One of the most powerful things you can learn as an AI user is that **how you frame your request dramatically changes the output.** Let's demonstrate this with the API.

    We'll ask Claude about the same topic three different ways and compare the responses.
    """)
    return


@app.cell
def _(client):
    # Three different framings of the same question
    framings = {'Vague prompt': 'Tell me about NaV1.7.', 'Specific prompt': "I'm writing an R01 grant on de novo protein binders for NaV1.7. In 2-3 sentences, explain why NaV1.7 is a validated pain target, citing the key human genetic evidence.", 'Role + context prompt': "You are reviewing my grant's significance section. Here is the claim I'm making: 'NaV1.7 is the most genetically validated analgesic target.' Is this defensible? What evidence supports it, and what caveats should I mention? Be brief and direct."}
    for name, prompt in framings.items():
        _response = client.messages.create(model='claude-sonnet-4-20250514', max_tokens=300, messages=[{'role': 'user', 'content': prompt}])
        print(f"\n{'=' * 60}")
        print(f'FRAMING: {name}')
        print(f'PROMPT:  {prompt[:80]}...' if len(prompt) > 80 else f'PROMPT:  {prompt}')
        print(f"{'=' * 60}")
        print(_response.content[0].text)
        print(f'\n({_response.usage.output_tokens} tokens)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice the differences:

    - The **vague prompt** gets a generic Wikipedia-style overview
    - The **specific prompt** gets exactly what you need for your grant
    - The **role + context prompt** gets a critical evaluation with nuance

    Same underlying knowledge, dramatically different outputs. This is why prompt engineering matters — and it's the focus of the entire next module.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Multi-turn conversation

    Let's see how conversation history affects Claude's responses. In the API, you control this explicitly by passing the message history.
    """)
    return


@app.cell
def _(client):
    # Build a multi-turn conversation about experimental design

    system = (
        "You are a scientific advisor for a pain biology lab that designs de novo "
        "protein binders for ion channels. Give concise, practical advice."
    )

    # Turn 1
    messages = [
        {"role": "user", "content": "I'm testing a new NaV1.7 binder in DRG cultures. What's the most important control?"}
    ]

    response_1 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system=system,
        messages=messages
    )

    print("Turn 1 — You: What's the most important control?")
    print(f"Claude: {response_1.content[0].text}")

    # Add Claude's response to the history
    messages.append({"role": "assistant", "content": response_1.content[0].text})

    # Turn 2 — follow up (Claude remembers the context)
    messages.append({"role": "user", "content": "Good point. How would I measure selectivity over NaV1.5 in the same assay?"})

    response_2 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system=system,
        messages=messages
    )

    print(f"\nTurn 2 — You: How would I measure selectivity over NaV1.5?")
    print(f"Claude: {response_2.content[0].text}")

    # Add to history
    messages.append({"role": "assistant", "content": response_2.content[0].text})

    # Turn 3 — reference something from earlier
    messages.append({"role": "user", "content": "Summarize the full experimental plan we've discussed in 3 bullet points."})

    response_3 = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=200,
        system=system,
        messages=messages
    )

    print(f"\nTurn 3 — You: Summarize the plan in 3 bullets.")
    print(f"Claude: {response_3.content[0].text}")

    print(f"\n--- Total tokens across 3 turns: "
          f"{response_1.usage.input_tokens + response_2.usage.input_tokens + response_3.usage.input_tokens} input, "
          f"{response_1.usage.output_tokens + response_2.usage.output_tokens + response_3.usage.output_tokens} output ---")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice that in Turn 3, Claude can summarize the entire conversation — because all previous messages are passed in the `messages` list. This is how "memory" works in the API: it's just the conversation history being re-sent each time.

    **Important implication:** Each turn sends ALL previous messages, so token usage grows with conversation length. A 20-turn conversation sends 20x more context than a 1-turn conversation. This is why starting fresh conversations for new topics is more efficient.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Your turn — test different system prompts

    Modify the system prompt below and see how it changes Claude's response to the same question. Try:
    1. A system prompt that makes Claude respond like a journal reviewer
    2. A system prompt that makes Claude explain things simply (for a lab meeting with non-specialists)
    3. A system prompt with your specific research context
    """)
    return


@app.cell
def _(client):
    # YOUR TURN: Modify this system prompt and see how the response changes
    my_system_prompt = 'You are a tough but fair reviewer for Nature Neuroscience. Point out weaknesses and missing controls, but acknowledge strengths.'
    my_question = 'We designed a de novo protein binder for NaV1.7 using RFdiffusion and validated it with yeast surface display (Kd = 15 nM). We then showed it reduces NaV1.7 currents in HEK293 cells by 80% at 100 nM. We conclude this is a promising therapeutic lead for chronic pain.'
    _response = client.messages.create(model='claude-sonnet-4-20250514', max_tokens=400, system=my_system_prompt, messages=[{'role': 'user', 'content': my_question}])
    print(f'System prompt: {my_system_prompt}')
    print(f'\nQuestion: {my_question[:80]}...')
    print(f"\n{'=' * 60}")
    print(_response.content[0].text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Try changing `my_system_prompt` to different roles and rerunning the cell. For example:

    ```python
    # Option A: Supportive mentor
    my_system_prompt = "You are a supportive senior scientist helping a junior colleague prepare for their committee meeting. Be encouraging but point out areas that need more work."

    # Option B: Pharma industry perspective
    my_system_prompt = "You are a VP of research at a pharmaceutical company evaluating this as a potential licensing deal. Focus on translational potential, IP landscape, and development risk."

    # Option C: Your specific needs
    my_system_prompt = "You are an expert in computational protein design and pain biology. I use RFdiffusion, ProteinMPNN, and AlphaFold2. Help me think through my experimental plan."
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Key takeaways

    1. **Claude was trained in stages** — pre-training (pattern learning), RLHF (learning to be helpful), and Constitutional AI (internal quality standards).

    2. **Conversations have structure** — system prompt, user messages, assistant messages. All are visible to the model at each turn.

    3. **Temperature controls randomness** — low for factual tasks, higher for creative tasks. The default works well for most research.

    4. **Hallucination is predictable** — Claude is most likely to hallucinate citations, specific numbers, and niche facts. Provide source material and encourage honesty.

    5. **Framing matters enormously** — the same question with different framing produces dramatically different outputs. This is the foundation of prompt engineering (Module 03).

    6. **System prompts are your secret weapon** — they set Claude's role, style, and focus for the entire conversation.

    ---

    **Up next: [Module 03 — Prompt Engineering](../03-prompt-engineering/)** where we'll go deep on techniques for getting the best possible output from Claude for your research tasks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created notebook with initial content
    - 2026-03-25: Added "Why this matters" rationale section
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: QA pass — removed 3 duplicate cells (code cells containing markdown text), added missing anthropic client import cell
    - 2026-03-25: Added standardized callouts and decision frameworks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - [Anthropic API: Messages](https://docs.anthropic.com/en/api/messages) — the official API reference for `messages.create()`, including system prompts, temperature, max_tokens, and all parameters demonstrated in this notebook
    - [Anthropic: System Prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) — best practices for writing effective system prompts
    - [Anthropic: Models Overview](https://docs.anthropic.com/en/docs/about-claude/models) — specifications, capabilities, and pricing for all Claude models
    - **Constitutional AI** ([Bai et al., 2022](https://arxiv.org/abs/2212.08073)) — Anthropic's paper on training AI systems using a set of principles (a "constitution") for self-improvement
    - **RLHF Explained**: [Hugging Face: RLHF](https://huggingface.co/blog/rlhf) — a clear, visual explanation of Reinforcement Learning from Human Feedback
    - [Anthropic: Prompt Engineering Overview](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Anthropic's guide to prompt design, covering system prompts, temperature, and techniques for getting better output
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created notebook with initial content
    - 2026-03-25: Added "Why this matters" rationale section
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: QA pass — removed 3 duplicate cells (code cells containing markdown text), added missing anthropic client import cell
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

