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
    # 01: What Is an LLM?

    You already use Claude every day for grant writing and research digests. This module gives you the mental model of what's actually happening under the hood — not to make you an ML engineer, but to make you a sharper user.

    By the end of this notebook you'll understand:
    - What LLMs actually are (and what they aren't)
    - How training works at a high level
    - The difference between training and inference
    - Why text is the universal interface to knowledge
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Your AI Toolkit](../02-your-computer/04-your-ai-toolkit.py) | [Module Index](../README.md) | [Next: Tokens and Context Windows \u2192](02-tokens-and-context.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The one-sentence explanation

    **A large language model is a pattern-completion machine trained on text.**

    That's it. Everything else is details. When you ask Claude to summarize a paper on NaV1.7 gain-of-function mutations, it's not "understanding" the paper the way you do. It's predicting what text should come next, based on patterns it learned from an enormous amount of training data.

    But here's the remarkable thing: pattern completion at sufficient scale looks a lot like understanding. Enough patterns over enough text, and the model learns to write coherent paragraphs, reason about experimental design, and explain the difference between TTX-sensitive and TTX-resistant sodium channels.

    > The architecture behind modern LLMs is the **Transformer**, introduced in the seminal paper "Attention Is All You Need" ([Vaswani et al., 2017](https://arxiv.org/abs/1706.03762)). For a visual, intuitive explanation, see Jay Alammar's [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — one of the best introductions to how attention mechanisms work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** LLMs are probability machines, not knowledge databases. Claude doesn't store facts in a table and look them up. It stores *patterns* in billions of neural network weights. When it says "NaV1.7 is expressed in nociceptors," it's generating the most probable continuation of your text — not retrieving a stored fact. This distinction matters because it explains both why LLMs are remarkably capable (they generalize from patterns) and why they hallucinate (they generate plausible-sounding text even when no fact supports it).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## A pain biology analogy

    Think of how you read a calcium imaging trace. You see a fluorescence spike in a DRG neuron after capsaicin application and you immediately predict what comes next — the signal will decay, the neuron will either desensitize or fire again, and neighboring non-TRPV1-expressing neurons will stay quiet.

    You can make those predictions because you've seen thousands of calcium traces. You've internalized the **patterns** of neuronal responses.

    An LLM does the same thing, but with text. It has "seen" billions of documents — papers, textbooks, code, conversations. It has internalized patterns of how text follows text. When you give it a prompt like:

    > *"The NaV1.7 channel is important for pain because..."*

    It predicts the most likely continuation based on all the text it trained on. Not by looking up a stored fact, but by generating text that fits the pattern.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Next-token prediction: the core mechanism

    At its heart, an LLM does one thing: given a sequence of tokens (roughly, words or word-pieces), predict the next token.

    Let's build a toy version of this to make it concrete.
    """)
    return


@app.cell
def _():
    import numpy as np
    import matplotlib.pyplot as plt

    # Imagine these are the probabilities an LLM assigns to the next word
    # after seeing: "NaV1.7 is expressed in"

    next_word_probs = {
        "nociceptors": 0.32,
        "DRG": 0.28,
        "sensory": 0.15,
        "peripheral": 0.10,
        "small-diameter": 0.06,
        "pain-sensing": 0.04,
        "the": 0.03,
        "neurons": 0.02,
    }

    words = list(next_word_probs.keys())
    probs = list(next_word_probs.values())

    fig, ax = plt.subplots(figsize=(10, 4))
    bars = ax.barh(words, probs, color="steelblue")
    ax.set_xlabel("Probability")
    ax.set_title('Next-token probabilities after: "NaV1.7 is expressed in ___"')
    ax.invert_yaxis()

    # Label each bar
    for bar, p in zip(bars, probs):
        ax.text(bar.get_width() + 0.005, bar.get_y() + bar.get_height() / 2,
                f"{p:.0%}", va="center", fontsize=9)

    plt.tight_layout()
    plt.show()
    return np, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The model doesn't "know" that NaV1.7 is expressed in nociceptors the way you know it from reading Dib-Hajj et al. It has learned that in its training data, the word **"nociceptors"** frequently follows phrases about NaV1.7 expression.

    The key insight: **this is a probability distribution, not a lookup table.** The model doesn't retrieve a stored answer — it generates a ranked set of possibilities.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Let's simulate token-by-token generation

    Here's how an LLM builds a sentence. At each step it picks the next token, adds it to the sequence, then predicts again. This is called **autoregressive generation**.
    """)
    return


@app.cell
def _(np):
    # A toy "language model" — hand-coded probability tables for demonstration
    # In a real LLM, a neural network computes these probabilities

    toy_model = {
        "TRPV1 is": {
            "a": 0.35, "activated": 0.25, "expressed": 0.15, 
            "the": 0.10, "an": 0.08, "important": 0.07
        },
        "TRPV1 is a": {
            "receptor": 0.30, "channel": 0.25, "nociceptor": 0.10, 
            "nonselective": 0.15, "polymodal": 0.12, "key": 0.08
        },
        "TRPV1 is a nonselective": {
            "cation": 0.75, "ion": 0.15, "receptor": 0.05,
            "channel": 0.03, "ligand-gated": 0.02
        },
        "TRPV1 is a nonselective cation": {
            "channel": 0.85, "receptor": 0.08, "transporter": 0.04,
            "pore": 0.02, "conductance": 0.01
        },
    }

    def generate_token(context, model, temperature=1.0):
        """Pick the next token based on probability distribution."""
        if context not in model:
            return None
        options = model[context]
        words = list(options.keys())
        probs = np.array(list(options.values()))
    
        # Temperature adjusts randomness (we'll cover this in notebook 03)
        adjusted = probs ** (1.0 / temperature)
        adjusted = adjusted / adjusted.sum()
    
        return np.random.choice(words, p=adjusted)

    # Generate step by step
    np.random.seed(42)
    context = "TRPV1 is"
    print(f"Start: '{context}'")
    print()

    for step in range(4):
        next_token = generate_token(context, toy_model, temperature=0.5)
        if next_token is None:
            print(f"  (no more predictions available)")
            break
        print(f"  Step {step + 1}: chose '{next_token}' → \"{context} {next_token}\"")
        context = context + " " + next_token

    print(f"\nFinal: '{context}'")
    return generate_token, toy_model


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's the fundamental mechanism: predict, append, repeat. A real LLM like Claude does this with a massive neural network instead of a hand-coded table, and it handles millions of possible next tokens at each step. But the core loop is identical.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph LR
        subgraph "LLM Architecture at a High Level"
            INPUT["<b>Input Text</b><br/>'NaV1.7 is expressed in'"] --> TOK["<b>Tokenizer</b><br/>Text → tokens<br/>(subword pieces)"]
            TOK --> TRANS["<b>Transformer</b><br/>Neural network with<br/>billions of parameters<br/>Processes all tokens<br/>in parallel via<br/><i>attention mechanism</i>"]
            TRANS --> PROB["<b>Probability<br/>Distribution</b><br/>A score for every<br/>possible next token<br/>(~50,000+ options)"]
            PROB --> SAMPLE["<b>Sampling</b><br/>Pick one token<br/>(temperature controls<br/>how random)"]
            SAMPLE --> OUTPUT["<b>Output Token</b><br/>'nociceptors'"]
        end

        OUTPUT -.->|"append to input,<br/>repeat"| INPUT

        style INPUT fill:#4488cc,color:#fff
        style TOK fill:#44aa88,color:#fff
        style TRANS fill:#cc8844,color:#fff
        style PROB fill:#aa44aa,color:#fff
        style SAMPLE fill:#cc4444,color:#fff
        style OUTPUT fill:#4488cc,color:#fff
    ```

    This loop -- predict one token, append it, predict the next -- is called **autoregressive generation**. The code demo below simulates exactly this process with a toy model.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## How training works (the 30,000-foot view)

    Training an LLM happens in stages. You don't need to understand the math — just the logic.

    ### Stage 1: Pre-training (learning to predict text)

    The model reads an enormous corpus of text — web pages, books, scientific papers, code. For each passage, it tries to predict the next word. When it gets it wrong, its internal weights get nudged slightly in the direction of the right answer.

    **Pain biology analogy:** This is like a new graduate student reading 10,000 papers in their first year. They don't understand everything, but they start to internalize the patterns — how methods sections are structured, what words appear near "nociceptor," how results relate to hypotheses.

    After pre-training, the model can complete text fluently but it's not yet a good assistant. It might continue your prompt by writing more of a Wikipedia article rather than answering your question.

    ### Stage 2: Fine-tuning with human feedback (RLHF)

    Human trainers show the model examples of good and bad responses. "When someone asks about NaV1.7 mutations, this response is helpful and accurate; this one is vague and wrong." The model learns to produce responses that humans rate as helpful, harmless, and honest. For more on this process, see [Anthropic's research page](https://www.anthropic.com/research).

    **Analogy:** This is like a postdoc getting feedback from their PI. "That's a good summary of the DRG data. But this paragraph about calcium imaging — you're confusing peak amplitude with AUC. Fix that."

    ### Stage 3: Ongoing refinement

    Anthropic continues to refine Claude based on real-world usage patterns, safety evaluations, and capability benchmarks. The model gets better at specific tasks over time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Training vs. Inference

    This distinction matters for how you think about using AI tools.

    | | **Training** | **Inference** |
    |---|---|---|
    | **When** | Before you ever see the model | Every time you chat with Claude |
    | **What happens** | Model learns patterns from data | Model generates text from your prompt |
    | **Who does it** | Anthropic (with massive compute) | You (through the API or chat interface) |
    | **Compute cost** | Millions of dollars | Fractions of a cent per response |
    | **Analogy** | Grad school + postdoc training | Answering questions at lab meeting |

    **Key implication:** Claude's knowledge comes from training data. It doesn't learn from your conversations (unless you're using a system that explicitly saves context). Each conversation starts fresh.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why text is the universal interface

    Here's why LLMs are so useful for research: **almost everything in science can be expressed as text.**

    - Your grant aims? Text.
    - A protein sequence? Text (MANLGCWMLV...).
    - RNA-seq results? A table, which is structured text.
    - Experimental protocols? Text.
    - A PDB structure? Text (ATOM records).
    - Code to analyze calcium imaging data? Text.

    Because LLMs operate on text, they can help with all of these. A single model can draft a specific aims page, explain a Python error in your analysis script, suggest controls for a behavioral assay, and convert a binder sequence to FASTA format — all because these are text-to-text transformations.
    """)
    return


app._unparsable_cell(
    r"""
    > 🤔 **Decision point:** When should you use an LLM vs. a search engine vs. a database?
    >
    > | Tool | Pros | Cons | Use when... |
    > |------|------|------|-------------|
    > | **LLM (Claude)** | Synthesizes, drafts, explains, transforms text; handles nuance and context; generates code | Can hallucinate facts; has a training cutoff date; unreliable for precise numbers | You need to draft, summarize, explain, brainstorm, or transform text. Sweet spot: tasks where the *quality of thinking* matters more than the *recency of facts* |
    > | **Search engine (PubMed, Google Scholar)** | Returns real, citable papers; always up-to-date; you can verify sources directly | No synthesis — just links; you still have to read and interpret the papers yourself | You need to find specific papers, check whether something has been published, or get results from the last few months |
    > | **Database (UniProt, PDB, NCBI Gene)** | Authoritative, curated data; exact numbers you can cite; structured and queryable | No interpretation — just raw data; requires knowing the right query syntax | You need specific, verified facts: a protein sequence, a gene ID, a crystal structure, an IC50 value from a specific assay |
    >
    > **Best practice:** Use Claude to help you *think* about your data and *draft* your text. Use databases to *verify* specific claims. Use search engines to *find* recent papers. Then feed those papers back to Claude for synthesis.

    ```mermaid
    graph TD
        TASK["I need to..."] --> Q1{"What kind of task?"}

        Q1 -->|"Draft, summarize,<br/>explain, brainstorm"| LLM["Use **Claude**<br/>(text transformation)"]
        Q1 -->|"Look up a specific<br/>fact or number"| DB["Use the **source**<br/>(paper, database, docs)"]
        Q1 -->|"Find recent papers"| SEARCH["Use **PubMed / Google Scholar**<br/>(search engine)"]
        Q1 -->|"Calculate something<br/>precisely"| CALC["Use **Python / calculator**<br/>(exact computation)"]
        Q1 -->|"Design a protein<br/>sequence"| TOOL["Use **specialized tools**<br/>(RFdiffusion, AlphaFold2)"]

        LLM --> TIP1["High reliability<br/>This is the sweet spot"]
        DB --> TIP2["Verify LLM claims here"]
        SEARCH --> TIP3["LLMs have a training<br/>cutoff date"]
        CALC --> TIP4["LLMs are unreliable<br/>at precise math"]
        TOOL --> TIP5["LLMs can help you<br/>USE these tools"]

        style LLM fill:#44aa88,color:#fff
        style DB fill:#4488cc,color:#fff
        style SEARCH fill:#cc8844,color:#fff
        style CALC fill:#aa44aa,color:#fff
        style TOOL fill:#cc4444,color:#fff
    ```
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph TD
        TASK["I need to..."] --> Q1{"What kind of task?"}

        Q1 -->|"Draft, summarize,<br/>explain, brainstorm"| LLM["Use <b>Claude</b><br/>(text transformation)"]
        Q1 -->|"Look up a specific<br/>fact or number"| DB["Use the <b>source</b><br/>(paper, database, docs)"]
        Q1 -->|"Find recent papers"| SEARCH["Use <b>PubMed / Google Scholar</b><br/>(search engine)"]
        Q1 -->|"Calculate something<br/>precisely"| CALC["Use <b>Python / calculator</b><br/>(exact computation)"]
        Q1 -->|"Design a protein<br/>sequence"| TOOL["Use <b>specialized tools</b><br/>(RFdiffusion, AlphaFold2)"]

        LLM --> TIP1["High reliability<br/>This is the sweet spot"]
        DB --> TIP2["Verify LLM claims here"]
        SEARCH --> TIP3["LLMs have a training<br/>cutoff date"]
        CALC --> TIP4["LLMs are unreliable<br/>at precise math"]
        TOOL --> TIP5["LLMs can help you<br/>USE these tools"]

        style LLM fill:#44aa88,color:#fff
        style DB fill:#4488cc,color:#fff
        style SEARCH fill:#cc8844,color:#fff
        style CALC fill:#aa44aa,color:#fff
        style TOOL fill:#cc4444,color:#fff
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this section matters most:** The "what LLMs are NOT" list is your cheat sheet for avoiding the most common mistakes. The researchers who get burned by AI are the ones who treat it as a database (trusting hallucinated citations) or a search engine (asking about last week's preprints). Internalize these limits and you'll avoid those traps.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** Never treat LLM output as fact without verification. Claude will confidently generate citations that don't exist, Kd values that were never measured, and mechanisms that sound right but are wrong. The risk scales with how specific and niche the claim is: "NaV1.7 is a sodium channel" is almost certainly correct (well-established, widely published). "The Kd of antibody X for NaV1.7 is 2.3 nM (Smith et al., 2023)" could be entirely fabricated. Your rule: trust Claude for well-established knowledge and text transformation tasks; verify specific numbers, citations, and niche claims against primary sources.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What LLMs are NOT

    Understanding what LLMs *aren't* will save you from a lot of frustration and misuse.

    ### Not a database
    An LLM doesn't store facts in a table that it looks up. It stores *patterns* in neural network weights. This means:
    - It can "know" that NaV1.7 is encoded by SCN9A because that pattern appears frequently in training data
    - But it might confidently state a wrong Kd value because it's generating plausible-sounding numbers, not looking up a measured value

    **Rule of thumb:** Trust LLMs for well-established, widely-published facts. Verify specific numbers, citations, and niche claims.

    ### Not a search engine
    Claude doesn't search the internet when you ask it something (unless it has explicit web search tools). Its knowledge comes from training data with a cutoff date. If a paper was published last week describing a new NaV1.7 variant, Claude won't know about it.

    ### Not a reasoning engine (in the way you are)
    LLMs can do impressive multi-step reasoning, but they're doing it through pattern completion, not through the kind of causal reasoning you use when designing an experiment. They can sometimes get "reasoning" wrong in ways that look right on the surface.

    ### Not deterministic
    Ask the same question twice and you may get different answers. The generation process involves randomness (sampling). This is a feature, not a bug — it allows creative variation — but it means you can't rely on exact reproducibility.
    """)
    return


@app.cell
def _(generate_token, toy_model):
    # Demonstration: the same "model" can give different outputs due to sampling
    prompt = 'TRPV1 is'
    print(f"Prompt: '{prompt}'\n")
    print('Five different completions from the same toy model:')
    print('-' * 50)
    for i in range(5):
        context_1 = prompt
        tokens = []
        for _ in range(4):  # No fixed seed — each run samples differently
            token = generate_token(context_1, toy_model, temperature=1.0)
            if token is None:
                break
            tokens.append(token)
            context_1 = context_1 + ' ' + token
        print(f"  Run {i + 1}: '{prompt} {' '.join(tokens)}'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice how each run can produce a different continuation. Some runs will produce the "textbook" answer ("a nonselective cation channel"), others will take different paths. The higher the temperature, the more variation you get. We'll explore this in detail in notebook 03.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The scale that makes it work

    Our toy model above had a few dozen entries. A real LLM has:

    - **Billions of parameters** (weights) — these encode patterns learned during training
    - **Trillions of tokens** of training data — books, papers, websites, code
    - **Thousands of GPUs** running for weeks during training

    The surprising discovery of the last few years is that scaling up this simple recipe — predict the next token, but with more data and more parameters — produces increasingly capable models. This is sometimes called the **scaling laws** of LLMs.
    """)
    return


@app.cell
def _(plt):
    # Visualize the scale difference
    models = {'Our toy model': 30, 'GPT-2 (2019)': 1500000000.0, 'GPT-3 (2020)': 175000000000.0, 'Claude 3.5 Sonnet': None}
    labels = ['Our toy model\n(~30 values)', 'GPT-2 (2019)\n(1.5B params)', 'GPT-3 (2020)\n(175B params)']
    values = [30, 1500000000.0, 175000000000.0]
    fig_1, ax_1 = plt.subplots(figsize=(10, 4))
    bars_1 = ax_1.barh(labels, values, color=['#cc4444', '#4488cc', '#44aa88'])
    ax_1.set_xscale('log')  # Not publicly disclosed; we'll estimate
    ax_1.set_xlabel('Number of parameters (log scale)')
    ax_1.set_title('Model scale comparison')
    # We'll just show the ones with known parameter counts
    for bar_1, v in zip(bars_1, values):
        if v < 1000:
            label = str(int(v))
        elif v < 1000000000.0:
            label = f'{v / 1000000.0:.0f}M'
        else:
            label = f'{v / 1000000000.0:.1f}B'
        ax_1.text(bar_1.get_width() * 1.5, bar_1.get_y() + bar_1.get_height() / 2, label, va='center', fontsize=10, fontweight='bold')
    plt.tight_layout()
    plt.show()
    print(f'\nGPT-3 has roughly {175000000000.0 / 30:.0e}x more parameters than our toy model.')
    print('Modern models like Claude are even larger (exact sizes not publicly disclosed).')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Build your own probability table

    Create a next-token probability table for a pain biology sentence. Pick a short prompt related to your work and fill in plausible next-word probabilities.

    Requirements:
    1. Choose a 3-4 word prompt related to your research
    2. List at least 5 possible next words with probabilities
    3. Probabilities should sum to ~1.0 (they can be approximate)
    4. Visualize it as a bar chart
    """)
    return


@app.cell
def _(plt):
    # YOUR TURN: Fill in your own prompt and probability table
    my_prompt = 'Chronic pain is'
    my_next_word_probs = {'caused': 0.2, 'characterized': 0.18, 'a': 0.15, 'associated': 0.14, 'mediated': 0.12, 'defined': 0.08, 'often': 0.07, 'not': 0.06}  # Change this to something from your work
    words_1 = list(my_next_word_probs.keys())
    probs_1 = list(my_next_word_probs.values())
    fig_2, ax_2 = plt.subplots(figsize=(10, 4))
    bars_2 = ax_2.barh(words_1, probs_1, color='coral')
    ax_2.set_xlabel('Probability')
    ax_2.set_title(f'Next-token probabilities after: "{my_prompt} ___"')
    ax_2.invert_yaxis()
    for bar_2, p_1 in zip(bars_2, probs_1):
        ax_2.text(bar_2.get_width() + 0.005, bar_2.get_y() + bar_2.get_height() / 2, f'{p_1:.0%}', va='center', fontsize=9)
    plt.tight_layout()
    plt.show()
    print(f'\nTotal probability: {sum(probs_1):.2f}')
    # Visualize it
    print('(In a real LLM, this sums to exactly 1.0 over ALL possible tokens — typically 50,000+)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Spot the limitations

    For each scenario below, decide whether an LLM is a good tool or a risky one, and why. Write your answers in the markdown cell after the list.

    1. **Drafting a specific aims page** for an R01 on NaV1.7 targeted degradation
    2. **Looking up the exact Kd** of a published antibody for NaV1.8
    3. **Explaining the difference** between TTX-sensitive and TTX-resistant sodium channels
    4. **Finding papers published last month** on KCNQ2 openers for neuropathic pain
    5. **Writing Python code** to plot calcium imaging traces
    6. **Calculating the molecular weight** of a 400-residue protein binder
    7. **Summarizing a paper** you paste into the conversation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Your answers here:**

    1. Good / Risky? Why?
    2. ...
    3. ...

    (Double-click this cell to edit it, then Shift+Enter to render.)

    ---

    **Answer key** (read after you've written your own answers):

    1. **Good** — drafting text is an LLM's sweet spot. You provide the scientific content and structure; Claude handles the prose. Always review for accuracy.
    2. **Risky** — specific numerical values can be hallucinated. Always verify in the original paper. Use Claude to *find* the paper, not to *be* the source.
    3. **Good** — this is well-established textbook knowledge that appears extensively in training data.
    4. **Risky** — LLMs have a training cutoff date and don't search the internet by default. Use PubMed for recent literature.
    5. **Good** — code generation is one of the strongest LLM capabilities. Test the code, but the drafts are usually solid.
    6. **Risky** — LLMs are unreliable at precise arithmetic. Use Python or a calculator. (Though Claude can write the Python code to do the calculation!)
    7. **Good** — when you give Claude the full text, it's working from the source material, not from memory. This is one of the most reliable use cases.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Key takeaways

    1. **LLMs are pattern-completion machines** — they predict the next token based on learned patterns from training data.
    2. **Training and inference are separate** — the model learns during training (done by Anthropic); you use it during inference (every chat or API call).
    3. **Text is the universal interface** — sequences, protocols, data tables, and code are all text that LLMs can work with.
    4. **LLMs are not databases** — they generate plausible text, which is often but not always accurate. Verify specific facts.
    5. **Scale matters** — the same basic mechanism (next-token prediction) produces dramatically different capabilities at different scales.

    Next up: [02-tokens-and-context.py](./02-tokens-and-context.py) — we'll look at how text gets broken into tokens and why context windows matter for your work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [← Previous: Your AI Toolkit](../02-your-computer/04-your-ai-toolkit.py) | [Module Index](../README.md) | [Next: Tokens and Context Windows →](02-tokens-and-context.py)
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
    - 2026-03-25: QA pass — removed duplicate "one-sentence explanation" and "how training works" sections
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - [Anthropic Research](https://www.anthropic.com/research) — Anthropic's published research on AI safety, interpretability, and model capabilities
    - **"Attention Is All You Need"** ([Vaswani et al., 2017](https://arxiv.org/abs/1706.03762)) — the foundational paper introducing the Transformer architecture that all modern LLMs are built on
    - [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) — Jay Alammar's visual, step-by-step explanation of how Transformers work; the best non-technical introduction available
    - [The Illustrated GPT-2](https://jalammar.github.io/illustrated-gpt2/) — Jay Alammar's follow-up showing how GPT-style autoregressive language models generate text token by token
    - [Anthropic: Core Views on AI Safety](https://www.anthropic.com/research) — Anthropic's perspective on why AI safety research matters, including Constitutional AI
    - [What are LLMs? (Anthropic docs)](https://docs.anthropic.com/en/docs/about-claude/models) — Anthropic's own documentation on Claude's models, capabilities, and limitations
    - [Scaling Laws for Neural Language Models](https://arxiv.org/abs/2001.08361) (Kaplan et al., 2020) — the paper that established how model performance improves predictably with scale
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
    - 2026-03-25: QA pass — removed duplicate "one-sentence explanation" and "how training works" sections
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

