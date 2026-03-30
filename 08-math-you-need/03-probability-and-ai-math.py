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
    # Module: Math You Actually Need -- 03: Probability and AI Math

    **Goal:** Understand the probability concepts that power LLMs -- so you can reason about Claude's behavior, tune generation parameters effectively, and understand *why* prompting techniques work.

    **References:** [Anthropic API: Messages](https://docs.anthropic.com/en/api/messages) (temperature and top_p parameters) | [The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/) (Jay Alammar) | [Think Stats](https://allendowney.github.io/ThinkStats/) (Allen Downey)

    > **Book companion:** The probability foundations in this notebook connect directly to [Think Stats, Chapter 5 (Modeling Distributions)](https://allendowney.github.io/ThinkStats/) and [Chapter 6 (Probability)](https://allendowney.github.io/ThinkStats/) by Allen Downey. Think Stats builds probability from data (the same approach we take here), rather than from abstract axioms. If you want a gentler on-ramp to conditional probability and distribution modeling before diving into the AI-specific math, those two chapters are ideal.

    ---

    ## Why you need this
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Hypothesis Testing and P-values](02-hypothesis-testing-and-pvalues.py) | [Module Index](../README.md) | [Next: Your First API Call \u2192](../09-claude-api/01-your-first-api-call.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Every time Claude generates a response, it samples from a probability distribution over ~100,000 possible next tokens. Understanding this process explains why temperature, top-p, and prompt engineering work -- and why Claude sometimes "hallucinates."
    > - The temperature parameter you set in API calls literally reshapes the softmax distribution: low temperature sharpens it (deterministic, good for data extraction), high temperature flattens it (diverse, good for brainstorming). This notebook lets you see and manipulate that distribution directly.
    > - Conditional probability is why your prompts matter: adding context like "you are an ion channel expert" changes the probability distribution over Claude's outputs, making domain-relevant responses far more likely.
    > - Understanding perplexity and log-probabilities lets you evaluate AI model claims in papers and understand why some prompting strategies work better than others -- essential knowledge as AI tools become central to your research workflow.
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (10, 5)
    plt.rcParams['font.size'] = 12

    rng = np.random.default_rng(42)

    print("Ready to go!")
    return np, plt, rng


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Basic Probability: What Does "40% Probability" Mean for a Token?

    ### Why you need this

    When Claude generates text, at each step it assigns a probability to every possible next token. If the prompt is "The voltage-gated sodium channel NaV1.7 is encoded by the gene", the model might assign:
    - "SCN9A" → 75% probability
    - "SCN" → 10%
    - "Scn" → 5%
    - everything else → 10% total

    This is a **probability distribution**: a set of numbers that are all non-negative and sum to 1. Let's make this concrete.
    """)
    return


@app.cell
def _(np):
    # Simulate: token probabilities for a neuroscience prompt
    # Prompt: "TRPV1 is activated by"
    tokens = ['capsaicin', 'heat', 'acid', 'cap', 'inflammation', 'noxious', 'temperature', 'vanill', 'chemical', 'other']
    # These are illustrative probabilities (not from a real model)
    probs = np.array([0.35, 0.2, 0.12, 0.08, 0.07, 0.05, 0.04, 0.04, 0.03, 0.02])
    print(f"Prompt: 'TRPV1 is activated by'")
    print(f'\nNext token probabilities:')
    for _token, _prob in zip(tokens, probs):
        bar = '#' * int(_prob * 50)
        print(f'  {_token:15s} {_prob:.0%} {bar}')
    print(f'\nTotal probability: {probs.sum():.0%} (must sum to 1)')
    print(f"\nThe model doesn't 'know' the answer — it assigns probabilities to all options.")
    print(f'Then it SAMPLES from this distribution to pick the next token.')
    return probs, tokens


@app.cell
def _(probs, rng, tokens):
    # Demonstrate sampling: run the same prompt 20 times
    print('Sampling from the distribution 20 times:')
    print('(Each run = what Claude might generate as the next token)')
    print()
    _samples = rng.choice(tokens, size=20, p=probs)
    for _i, sample in enumerate(_samples, 1):
        print(f"  Run {_i:2d}: 'TRPV1 is activated by {sample}...'")
    print(f"\n'capsaicin' appeared {list(_samples).count('capsaicin')} times (expected ~{0.35 * 20:.0f})")
    print(f"'heat' appeared {list(_samples).count('heat')} times (expected ~{0.2 * 20:.0f})")
    print(f'\nThis is why Claude can give slightly different answers to the same prompt!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Conditional Probability: Why Context Changes Claude's Outputs

    ### Why you need this

    The key equation behind LLMs is:

    **P(next token | all previous tokens)**

    The `|` means "given" or "conditional on." The probability of the next word depends entirely on what came before. This is why **prompt engineering works** — by changing the context, you change the probability distribution over outputs.

    Let's see this in action with a concrete example.

    For a thorough treatment of conditional probability with Python code and biological examples, see [Think Stats, Chapter 6 (Probability)](https://allendowney.github.io/ThinkStats/). Downey builds conditional probability from Bayes' theorem using real datasets — the same logic that underpins how LLMs update their predictions based on context.
    """)
    return


@app.cell
def _(np, plt):
    # How context shifts the probability distribution
    # Same question, different prompts
    context1_tokens = ['pain', 'inflammation', 'neurons', 'ion', 'sensory', 'nerve', 'signal', 'brain', 'tissue', 'other']
    # Context 1: Vague prompt
    context1_probs = np.array([0.15, 0.12, 0.1, 0.1, 0.09, 0.08, 0.08, 0.07, 0.06, 0.15])
    context2_tokens = ['pain', 'nociceptor', 'DRG', 'sodium', 'SCN9A', 'channel', 'action', 'erythromelalgia', 'mutation', 'other']
    context2_probs = np.array([0.22, 0.18, 0.14, 0.12, 0.1, 0.08, 0.05, 0.04, 0.04, 0.03])
    _fig, _axes = plt.subplots(1, 2, figsize=(14, 5))
    _y_pos = range(len(context1_tokens) - 1, -1, -1)
    # Context 2: Specific prompt mentioning NaV1.7
    _axes[0].barh(_y_pos, context1_probs, color='steelblue', edgecolor='black', alpha=0.7)
    _axes[0].set_yticks(_y_pos)
    _axes[0].set_yticklabels(context1_tokens)
    _axes[0].set_xlabel('Probability')
    _axes[0].set_title('Vague prompt:\n"Tell me about..."', fontsize=12)
    _axes[0].set_xlim(0, 0.3)
    y_pos2 = range(len(context2_tokens) - 1, -1, -1)
    # Vague context
    _axes[1].barh(y_pos2, context2_probs, color='#E24A33', edgecolor='black', alpha=0.7)
    _axes[1].set_yticks(y_pos2)
    _axes[1].set_yticklabels(context2_tokens)
    _axes[1].set_xlabel('Probability')
    _axes[1].set_title('Specific prompt:\n"Explain how NaV1.7 mutations cause..."', fontsize=12)
    _axes[1].set_xlim(0, 0.3)
    plt.suptitle('Conditional probability: context reshapes the distribution', fontsize=14, y=1.02)
    plt.tight_layout()
    # Specific context
    plt.show()
    print('Key insight for prompt engineering:')
    print('- Vague prompt → flat distribution → diverse but unfocused outputs')
    print('- Specific prompt → peaked distribution → focused, relevant outputs')
    print('\nThis is WHY detailed prompts work better — they concentrate probability')
    print('on the tokens you actually want.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The chain rule: how full sentences get generated

    Claude generates text one token at a time, where each token's probability depends on ALL previous tokens:

    ```
    P("TRPV1 is activated by capsaicin") =
        P("TRPV1")
      x P("is" | "TRPV1")
      x P("activated" | "TRPV1 is")
      x P("by" | "TRPV1 is activated")
      x P("capsaicin" | "TRPV1 is activated by")
    ```

    Each step conditions on everything that came before. That's why a good system prompt or few-shot examples at the start of the conversation can influence the entire rest of the output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Temperature: Reshaping the Probability Distribution

    ### Why you need this

    Temperature is the single most important generation parameter you'll control when using the Claude API. It directly controls the "shape" of the probability distribution:
    - **Low temperature (0.0-0.3):** Sharp, peaked distribution → more deterministic, consistent outputs. Use for factual queries, data analysis, coding.
    - **Medium temperature (0.5-0.7):** Balanced. Use for most research tasks.
    - **High temperature (0.8-1.5):** Flat distribution → more varied, creative outputs. Use for brainstorming, generating hypotheses.

    Let's see exactly what temperature does mathematically.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** Temperature IS a probability distribution control. When you set `temperature=0.0`, you're telling Claude to always pick the single most probable next token (greedy decoding). When you set `temperature=1.0`, you're sampling from the full distribution, allowing less likely but potentially creative tokens. This isn't a vague "creativity dial" -- it's a precise mathematical transformation of the probability distribution over the next token.

    > **Decision point: Temperature and top-p settings for different tasks**
    >
    > | Task | Temperature | Top-p | Why |
    > |------|-------------|-------|-----|
    > | Data extraction (JSON from abstracts) | **0.0** | 1.0 | You want the single most likely answer, no variation |
    > | Code generation and debugging | **0.0 - 0.2** | 1.0 | Correctness matters more than creativity |
    > | Factual Q&A (ion channel biology) | **0.2 - 0.3** | 1.0 | Mostly deterministic, slight variation for natural language |
    > | Analysis interpretation | **0.3 - 0.5** | 0.95 | Balance between accuracy and nuanced reasoning |
    > | Brainstorming research directions | **0.7 - 0.9** | 0.95 | Encourage diverse, unexpected ideas |
    > | Creative writing (grant narrative) | **0.8 - 1.0** | 0.9 | Maximum variety in word choice and phrasing |
    >
    > **Rule of thumb:** For anything involving data, code, or facts, keep temperature below 0.3. For anything involving ideas, exploration, or writing, raise it above 0.5.
    """)
    return


@app.cell
def _(np):
    # The softmax function: how raw model scores become probabilities
    def softmax(logits, temperature=1.0):
        """Convert raw scores (logits) to probabilities using softmax with temperature."""
        scaled = logits / temperature
        exp_scaled = np.exp(scaled - np.max(scaled))  # Divide logits by temperature BEFORE softmax
        return exp_scaled / exp_scaled.sum()
    token_labels = ['capsaicin', 'heat', 'acid', 'inflammation', 'light', 'the', 'a', 'water', 'sleep', 'music']  # Subtract max for numerical stability (doesn't change the result)
    logits = np.array([5.2, 4.1, 3.5, 2.8, 0.5, 0.3, 0.1, -1.0, -2.0, -3.0])
    print('Raw model scores (logits):')
    for _token, logit in zip(token_labels, logits):
    # Simulated raw model scores (logits) for next token after "TRPV1 is activated by"
        print(f'  {_token:15s} logit = {logit:+.1f}')
    print()
    print("These aren't probabilities yet — they can be negative and don't sum to 1.")
    print('Softmax converts them to a valid probability distribution.')
    return logits, softmax, token_labels


@app.cell
def _(logits, np, plt, softmax, token_labels):
    temperatures = [0.1, 0.5, 1.0, 2.0]
    _fig, _axes = plt.subplots(1, 4, figsize=(18, 5), sharey=True)
    for _ax, _temp in zip(_axes, temperatures):
        probs_1 = softmax(logits, temperature=_temp)
        _colors = plt.cm.RdYlBu_r(np.linspace(0.1, 0.9, len(token_labels)))
        _y_pos = range(len(token_labels) - 1, -1, -1)
        _bars = _ax.barh(_y_pos, probs_1, color=_colors, edgecolor='black', alpha=0.8)
        _ax.set_yticks(_y_pos)
        _ax.set_yticklabels(token_labels)
        _ax.set_xlabel('Probability')
        _ax.set_title(f'T = {_temp}', fontsize=14, fontweight='bold')
        _ax.set_xlim(0, 1.05)
        max_prob = probs_1[0]
        _ax.text(max_prob + 0.02, len(token_labels) - 1, f'{max_prob:.0%}', va='center', fontsize=10, fontweight='bold')
    plt.suptitle('How temperature reshapes the probability distribution', fontsize=15, y=1.03)
    plt.tight_layout()
    plt.show()
    print("T=0.1: Almost all probability on 'capsaicin' (very deterministic)")
    print("T=0.5: 'capsaicin' still dominant, but other options have a chance")
    print("T=1.0: The model's 'natural' distribution")
    print('T=2.0: Much flatter — even unlikely tokens get sampled sometimes')
    return


@app.cell
def _(np, plt, softmax):
    token_labels_1 = ['capsaicin', 'heat', 'acid', 'capsaicin\nanalogs', 'protons', 'ligands', 'vanilloid\ncompounds', 'noxious\nstimuli', 'inflammatory\nmediators', 'other']
    logits_1 = np.array([4.5, 3.8, 2.5, 2.0, 1.8, 1.2, 0.8, 0.5, 0.3, -0.5])
    _fig, _ax = plt.subplots(figsize=(14, 6))
    temps = [0.2, 0.5, 1.0, 2.0]
    colors_t = ['#E24A33', '#FDB863', '#4878CF', '#55A868']
    width = 0.18
    x = np.arange(len(token_labels_1))
    for _i, (_temp, color) in enumerate(zip(temps, colors_t)):
        probs_2 = softmax(logits_1, temperature=_temp)
        _bars = _ax.bar(x + _i * width - 1.5 * width, probs_2, width, label=f'T={_temp}', color=color, alpha=0.8, edgecolor='black', linewidth=0.5)
    _ax.set_xlabel('Possible next tokens', fontsize=12)
    _ax.set_ylabel('Probability', fontsize=12)
    _ax.set_title('How temperature reshapes the probability distribution\nPrompt: "TRPV1 is activated by ___"', fontsize=13, fontweight='bold')
    _ax.set_xticks(x)
    _ax.set_xticklabels(token_labels_1, fontsize=9)
    _ax.legend(fontsize=11, title='Temperature', title_fontsize=11)
    _ax.annotate('Low temp = nearly\ndeterministic\n(always picks "capsaicin")', xy=(0 - 1.5 * width, softmax(logits_1, 0.2)[0]), xytext=(3, softmax(logits_1, 0.2)[0] * 0.9), fontsize=9, color='#E24A33', arrowprops=dict(arrowstyle='->', color='#E24A33'))
    _ax.annotate('High temp =\nmore uniform\n(explores rare tokens)', xy=(6 + 1.5 * width, softmax(logits_1, 2.0)[6]), xytext=(6.5, 0.2), fontsize=9, color='#55A868', arrowprops=dict(arrowstyle='->', color='#55A868'))
    plt.tight_layout()
    plt.show()
    print("T=0.2: 'capsaicin' gets ~90% probability. Almost no randomness.")
    print("T=1.0: Natural distribution. 'capsaicin' leads but others have a chance.")
    print("T=2.0: Much flatter. Even unlikely tokens like 'inflammatory mediators' get sampled.")
    return logits_1, token_labels_1


@app.cell
def _(logits_1, np, rng, softmax, token_labels_1):
    print('=== Sampling 50 tokens at each temperature ===')
    print(f"Prompt: 'TRPV1 is activated by ___'")
    print()
    for _temp in [0.1, 0.5, 1.0, 2.0]:
        probs_3 = softmax(logits_1, temperature=_temp)
        _samples = rng.choice(token_labels_1, size=50, p=probs_3)
        unique, counts = np.unique(_samples, return_counts=True)
        _sorted_idx = np.argsort(-counts)
        print(f'Temperature = {_temp}:')
        for idx in _sorted_idx[:5]:
            print(f'  {unique[idx]:15s} appeared {counts[idx]:2d}/50 times ({counts[idx] / 50:.0%})')
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Temperature cheat sheet for your API work

    | Temperature | Behavior | Use case |
    |------------|----------|----------|
    | 0.0 | Always picks most likely token | Extracting structured data, factual Q&A |
    | 0.2-0.4 | Nearly deterministic with slight variation | Data analysis, writing code |
    | 0.5-0.7 | Balanced | General research tasks, writing assistance |
    | 0.8-1.0 | More diverse outputs | Brainstorming experiment ideas, hypothesis generation |
    | >1.0 | Very random (often incoherent) | Rarely useful in practice |

    > **Claude API connection:** When you use the Anthropic API in Module 07, you set temperature with `temperature=0.5`. Now you understand exactly what that parameter does to the probability distribution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Top-p (Nucleus) Sampling

    ### Why you need this

    Temperature adjusts the *shape* of the entire distribution. Top-p takes a different approach: it **cuts off the long tail** of unlikely tokens. Instead of considering all 100,000+ tokens, it only considers the smallest set of tokens whose cumulative probability reaches `p`.

    For example, with `top_p=0.9`, the model considers only the most likely tokens that together account for 90% of the probability, and ignores the remaining 10% tail of very unlikely tokens.

    The connection between CDFs and top-p sampling is direct: top-p is essentially reading off a CDF and drawing a cutoff line. If you want to build stronger intuition for CDFs, see [Think Stats, Chapter 5 (Modeling Distributions)](https://allendowney.github.io/ThinkStats/), which covers how to fit analytical distributions to empirical data — the same kind of distribution shaping that temperature and top-p perform.
    """)
    return


@app.cell
def _(logits_1, np, plt, softmax):
    natural_probs = softmax(logits_1, temperature=1.0)
    token_names = ['capsaicin', 'heat', 'acid', 'cap.\nanalogs', 'protons', 'ligands', 'vanilloid\ncomp.', 'noxious\nstim.', 'inflam.\nmed.', 'other']
    _sorted_idx = np.argsort(-natural_probs)
    sorted_probs = natural_probs[_sorted_idx]
    sorted_names = [token_names[_i] for _i in _sorted_idx]
    cumulative = np.cumsum(sorted_probs)
    _fig, _axes = plt.subplots(1, 2, figsize=(16, 5.5))
    p_threshold = 0.9
    nucleus_size = np.searchsorted(cumulative, p_threshold) + 1
    colors_bars = ['#55A868' if _i < nucleus_size else '#cccccc' for _i in range(len(sorted_probs))]
    _axes[0].bar(range(len(sorted_probs)), sorted_probs, color=colors_bars, edgecolor='black', alpha=0.8)
    _axes[0].set_xticks(range(len(sorted_names)))
    _axes[0].set_xticklabels(sorted_names, fontsize=9, rotation=0)
    _axes[0].set_ylabel('Probability', fontsize=11)
    _axes[0].set_title(f'Top-p = 0.9: Keep top {nucleus_size} tokens\n(green = in nucleus, gray = excluded)', fontsize=12, fontweight='bold')
    for _i, p in enumerate(sorted_probs):
        _axes[0].text(_i, p + 0.005, f'{p:.2f}', ha='center', fontsize=9, fontweight='bold')
    _axes[0].axvline(nucleus_size - 0.5, color='red', ls='--', lw=2, label='Nucleus boundary')
    _axes[0].legend(fontsize=10)
    _axes[1].plot(range(len(cumulative)), cumulative, 'o-', color='#4878CF', lw=2, markersize=8)
    _axes[1].axhline(p_threshold, color='red', ls='--', lw=2, label=f'p = {p_threshold}')
    _axes[1].fill_between(range(nucleus_size), cumulative[:nucleus_size], alpha=0.2, color='#55A868')
    _axes[1].set_xticks(range(len(sorted_names)))
    _axes[1].set_xticklabels(sorted_names, fontsize=9, rotation=0)
    _axes[1].set_ylabel('Cumulative probability', fontsize=11)
    _axes[1].set_title('Cumulative probability\n(stop when we reach p threshold)', fontsize=12, fontweight='bold')
    _axes[1].set_ylim(0, 1.05)
    _axes[1].legend(fontsize=10)
    _axes[1].annotate(f'Top {nucleus_size} tokens\ncover {cumulative[nucleus_size - 1]:.0%}\nof probability mass', xy=(nucleus_size - 1, cumulative[nucleus_size - 1]), xytext=(nucleus_size + 1.5, 0.6), fontsize=10, fontweight='bold', arrowprops=dict(arrowstyle='->', color='#55A868', lw=2), color='#55A868')
    plt.suptitle('Top-p sampling: only sample from the most likely tokens', fontsize=13, fontweight='bold', y=1.03)
    plt.tight_layout()
    plt.show()
    print(f'With top_p=0.9, we only consider the top {nucleus_size} tokens.')
    print('The remaining tokens are too unlikely to be worth sampling.')
    print('This prevents Claude from generating truly bizarre/random completions.')
    return


@app.cell
def _(logits_1, np, softmax, token_labels_1):
    def top_p_filter(probs, tokens, p=0.9):
        """Apply top-p (nucleus) filtering to a probability distribution."""
        sorted_indices = np.argsort(-probs)
        sorted_probs = probs[sorted_indices]
        sorted_tokens = [tokens[_i] for _i in sorted_indices]
        cumulative = np.cumsum(sorted_probs)
        cutoff_idx = np.searchsorted(cumulative, p) + 1
        kept_probs = sorted_probs[:cutoff_idx]
        kept_tokens = sorted_tokens[:cutoff_idx]
        kept_probs = kept_probs / kept_probs.sum()
        return (kept_tokens, kept_probs, cutoff_idx)
    natural_probs_1 = softmax(logits_1, temperature=1.0)
    print('Full distribution (all tokens):')
    for _token, _prob in zip(token_labels_1, natural_probs_1):
        print(f'  {_token:15s} {_prob:.3f} ({_prob:.1%})')
    print(f'\n  Total: {natural_probs_1.sum():.3f}')
    return natural_probs_1, top_p_filter


@app.cell
def _(natural_probs_1, np, plt, token_labels_1, top_p_filter):
    _fig, _axes = plt.subplots(1, 3, figsize=(16, 5), sharey=True)
    _sorted_idx = np.argsort(-natural_probs_1)
    sorted_probs_all = natural_probs_1[_sorted_idx]
    sorted_tokens_all = [token_labels_1[_i] for _i in _sorted_idx]
    for _ax, top_p_val in zip(_axes, [0.5, 0.9, 0.99]):
        kept_tokens, kept_probs, cutoff = top_p_filter(natural_probs_1, token_labels_1, p=top_p_val)
        _y_pos = range(len(sorted_tokens_all) - 1, -1, -1)
        _colors = ['#4878CF' if t in kept_tokens else '#CCCCCC' for t in sorted_tokens_all]
        _ax.barh(_y_pos, sorted_probs_all, color=_colors, edgecolor='black', alpha=0.8)
        _ax.set_yticks(_y_pos)
        _ax.set_yticklabels(sorted_tokens_all)
        _ax.set_xlabel('Probability')
        _ax.set_title(f'top_p = {top_p_val}\n({cutoff} tokens kept)', fontsize=13)
        _ax.set_xlim(0, 0.5)
    plt.suptitle('Top-p sampling: blue tokens are in the nucleus (considered), gray are excluded', fontsize=13, y=1.03)
    plt.tight_layout()
    plt.show()
    print('top_p=0.5: Only the top 2-3 tokens considered (very focused)')
    print('top_p=0.9: Top ~5-6 tokens considered (balanced)')
    print('top_p=0.99: Almost all tokens considered (minimal filtering)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Temperature vs top-p

    | Parameter | What it does | Analogy |
    |-----------|-------------|----------|
    | **Temperature** | Reshapes the entire distribution (sharper or flatter) | Adjusting the focus knob on a microscope |
    | **Top-p** | Cuts off the tail of unlikely options | Drawing a boundary around the "reasonable" options |

    In practice, the Claude API defaults to `temperature=1.0` and `top_p=1.0` (no filtering). Most users only adjust temperature. The [Anthropic API docs](https://docs.anthropic.com/en/api/messages) let you set both, but changing one at a time is recommended so you can see the effect clearly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. The Softmax Function: From Raw Scores to Probabilities

    ### Why you need this

    You'll see "softmax" mentioned in almost every AI paper and tutorial. It's the mathematical bridge between the model's internal representations (arbitrary numbers) and probabilities (numbers between 0 and 1 that sum to 1). Understanding it at an intuitive level helps you reason about model behavior.

    The formula is simple:

    ```
    probability(token_i) = exp(score_i) / sum(exp(score_j) for all j)
    ```

    The key insight: **softmax amplifies differences.** A token with score 5 doesn't just get 5x the probability of a token with score 1 — it gets e^5 / e^1 = ~55x the probability.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Deep dive:** <details><summary>Click to expand: Softmax intuition</summary>
    >
    > The softmax function converts a list of arbitrary numbers (logits) into a probability distribution. Here's the intuition:
    >
    > 1. **Exponentiation** (`exp(x)`) makes all values positive and amplifies differences. A logit of 5 vs 3 becomes `exp(5)=148.4` vs `exp(3)=20.1` -- a 7x difference from a 2-point gap.
    >
    > 2. **Normalization** (dividing by the sum) forces everything to sum to 1.0, creating a valid probability distribution.
    >
    > 3. **Temperature** divides the logits before exponentiation: `exp(x/T)`. Low T amplifies differences (the highest logit dominates). High T flattens differences (all tokens become roughly equally likely).
    >
    > Think of it like this: the logits are "how much the model likes each option." Softmax turns those preferences into probabilities. Temperature controls how strongly the model commits to its preferences vs. hedging its bets.
    >
    > In pain biology terms: if a model's logits for "NaV1.7 is expressed in [nociceptors / astrocytes / muscle]" are [8, 2, 1], softmax at T=0.1 gives ~100% to "nociceptors." At T=1.0, it gives ~99.7% to "nociceptors." At T=5.0, it gives ~80% to "nociceptors" -- still favored, but "astrocytes" now has a ~15% chance of being sampled, which could produce a factual error.
    >
    > </details>
    """)
    return


@app.cell
def _(np, plt, softmax):
    # Visualize softmax: how it amplifies differences
    simple_logits = np.array([3.0, 2.0, 1.0, 0.0, -1.0])
    # Simple example: 5 tokens with different scores
    simple_labels = ['Best', 'Good', 'OK', 'Meh', 'Bad']
    shifted = simple_logits - simple_logits.min()
    linear_probs = shifted / shifted.sum()
    # What would "fair" probabilities look like? (proportional to score)
    # But scores can be negative, so we shift to positive first
    softmax_probs = softmax(simple_logits)
    _fig, _axes = plt.subplots(1, 3, figsize=(15, 5))
    _y_pos = range(len(simple_labels))
    # Softmax probabilities
    _axes[0].barh(_y_pos, simple_logits, color='steelblue', edgecolor='black', alpha=0.7)
    _axes[0].set_yticks(_y_pos)
    _axes[0].set_yticklabels(simple_labels)
    _axes[0].set_xlabel('Raw score (logit)')
    _axes[0].set_title("Step 1: Raw model scores\n(can be negative, don't sum to 1)", fontsize=11)
    _axes[1].barh(_y_pos, linear_probs, color='#FDB863', edgecolor='black', alpha=0.7)
    # Raw scores
    _axes[1].set_yticks(_y_pos)
    _axes[1].set_yticklabels(simple_labels)
    _axes[1].set_xlabel('Probability')
    _axes[1].set_title('Naive: linear scaling\n(proportional, less peaky)', fontsize=11)
    _axes[1].set_xlim(0, 0.8)
    _axes[2].barh(_y_pos, softmax_probs, color='#E24A33', edgecolor='black', alpha=0.7)
    # Linear scaling (naive approach)
    _axes[2].set_yticks(_y_pos)
    _axes[2].set_yticklabels(simple_labels)
    _axes[2].set_xlabel('Probability')
    _axes[2].set_title('Softmax\n(amplifies winner, suppresses losers)', fontsize=11)
    _axes[2].set_xlim(0, 0.8)
    for _i, _prob in enumerate(softmax_probs):
        _axes[2].text(_prob + 0.02, _i, f'{_prob:.1%}', va='center', fontsize=10)
    # Softmax (actual approach)
    plt.suptitle('Softmax: how model scores become probabilities', fontsize=14, y=1.02)
    plt.tight_layout()
    plt.show()
    print(f"'Best' (score=3) gets {softmax_probs[0]:.1%} of probability")
    print(f"'Bad' (score=-1) gets {softmax_probs[4]:.1%} of probability")
    print(f'Ratio: {softmax_probs[0] / softmax_probs[4]:.0f}x (not 3x — softmax amplifies!)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The connection to temperature

    Temperature works by dividing the logits before applying softmax:

    ```
    probability(token_i) = exp(score_i / T) / sum(exp(score_j / T) for all j)
    ```

    - **Low T** → logits get divided by a small number → bigger numbers → softmax amplifies even more → very peaked distribution
    - **High T** → logits get divided by a big number → smaller numbers → less amplification → flatter distribution
    - **T → 0** → all probability on the highest logit (argmax)
    - **T → infinity** → uniform distribution (all tokens equally likely)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Log Scales in AI: Perplexity and Loss

    ### Why you need this

    When you read about AI models being evaluated, you'll see metrics like "perplexity" and "cross-entropy loss." These use logarithms because probability products quickly become astronomically small numbers. Understanding the basic idea helps you interpret model comparison benchmarks and training curves.

    You already know log scales from notebook 01 (RNA-seq fold changes, binding affinities). The same principle applies here.
    """)
    return


@app.cell
def _(np):
    # Why we need logs: sentence probability becomes tiny fast

    # Imagine a model assigning these probabilities token by token:
    # "NaV1.7 mutations cause erythromelalgia"
    token_probs_good = [0.05, 0.3, 0.4, 0.6, 0.25]  # fairly confident model
    token_probs_bad = [0.01, 0.05, 0.08, 0.1, 0.03]   # uncertain model

    # Sentence probability = product of token probabilities
    sent_prob_good = np.prod(token_probs_good)
    sent_prob_bad = np.prod(token_probs_bad)

    # Log probability = sum of log token probabilities (much easier to work with)
    log_prob_good = np.sum(np.log(token_probs_good))
    log_prob_bad = np.sum(np.log(token_probs_bad))

    print("Sentence: 'NaV1.7 mutations cause erythromelalgia'")
    print()
    print("Good model (confident):")
    print(f"  Token probabilities: {token_probs_good}")
    print(f"  Sentence probability: {sent_prob_good:.8f} (tiny number!)")
    print(f"  Log probability:      {log_prob_good:.3f} (easier to work with)")
    print()
    print("Bad model (uncertain):")
    print(f"  Token probabilities: {token_probs_bad}")
    print(f"  Sentence probability: {sent_prob_bad:.12f} (astronomically tiny!)")
    print(f"  Log probability:      {log_prob_bad:.3f}")
    print()
    print("Log probabilities are easier to compare and don't underflow to zero.")
    print("Higher (less negative) log probability = better model.")
    return log_prob_bad, log_prob_good, token_probs_good


@app.cell
def _(log_prob_bad, log_prob_good, np, token_probs_good):
    # Perplexity: how "confused" is the model?

    # Perplexity = exp(-average log probability per token)
    # Lower perplexity = better model (less confused)

    n_tokens = len(token_probs_good)
    perplexity_good = np.exp(-log_prob_good / n_tokens)
    perplexity_bad = np.exp(-log_prob_bad / n_tokens)

    print("=== Perplexity ===")
    print()
    print(f"Good model: perplexity = {perplexity_good:.1f}")
    print(f"  Interpretation: at each step, the model is as uncertain as choosing")
    print(f"  randomly among ~{perplexity_good:.0f} equally likely options.")
    print()
    print(f"Bad model: perplexity = {perplexity_bad:.1f}")
    print(f"  Interpretation: at each step, the model is as uncertain as choosing")
    print(f"  randomly among ~{perplexity_bad:.0f} equally likely options.")
    print()
    print("Modern LLMs have perplexities in the range of 5-20 on typical text.")
    print("Lower is better: the model is less 'perplexed' by the text.")
    print()
    print("You don't need to compute perplexity yourself — but now you know")
    print("what it means when you see it in AI papers or model benchmarks.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Connecting to Practice: How This Explains Claude's Behavior

    ### Why you need this

    Now that you understand the probability machinery, here's how it maps to things you've experienced using Claude.
    """)
    return


@app.cell
def _():
    # Phenomenon 1: Why specific prompts give better results

    print("="*60)
    print("PHENOMENON: Specific prompts give better results")
    print("="*60)
    print()
    print("Vague prompt: 'Tell me about NaV1.7'")
    print("  → Flat probability distribution over many possible response directions")
    print("  → Model might talk about genetics, pharmacology, evolution, anything")
    print()
    print("Specific prompt: 'Explain how gain-of-function mutations in SCN9A")
    print("  cause inherited erythromelalgia, focusing on the biophysical mechanism'")
    print("  → Peaked distribution: high probability on relevant technical content")
    print("  → Model focuses on voltage-dependent activation, threshold shifts, etc.")
    print()
    print("Math: P(technical content | specific prompt) >> P(technical content | vague prompt)")
    return


@app.cell
def _():
    # Phenomenon 2: Why hallucinations happen

    print("="*60)
    print("PHENOMENON: Why Claude sometimes hallucinates")
    print("="*60)
    print()
    print("Prompt: 'What is the Kd of retigabine for KCNQ2/3?'")
    print()
    print("The model has probability distributions like:")
    print("  '3.5'  → 8%   (not confident about the exact number)")
    print("  '2.0'  → 6%")
    print("  '5'    → 5%")
    print("  '10'   → 4%")
    print("  '1.5'  → 4%")
    print("  ... (many plausible numbers with similar probability)")
    print()
    print("The distribution is FLAT over many plausible-sounding values.")
    print("The model MUST pick one — so it confidently outputs a specific number")
    print("even though it has low confidence in any particular value.")
    print()
    print("This is why Claude can state wrong numbers with apparent confidence.")
    print("The generation mechanism forces a choice even when uncertainty is high.")
    return


@app.cell
def _():
    # Phenomenon 3: Why few-shot examples work

    print("="*60)
    print("PHENOMENON: Why few-shot examples improve outputs")
    print("="*60)
    print()
    print("Without examples:")
    print("  'Summarize this paper's key findings'")
    print("  → Distribution over many possible summary styles and lengths")
    print()
    print("With examples:")
    print("  'Here are two examples of how I want summaries formatted:")
    print("   Example 1: [structured summary with bullet points]")
    print("   Example 2: [structured summary with bullet points]")
    print("   Now summarize this paper's key findings'")
    print()
    print("  → Distribution HEAVILY peaked toward bullet-point style")
    print("  → P(bullet format | examples) >> P(bullet format | no examples)")
    print()
    print("The examples shift conditional probabilities toward the pattern you want.")
    print("This is the mathematical reason prompt engineering works.")
    return


@app.cell
def _():
    # Phenomenon 4: Why temperature=0 is great for data extraction

    print("="*60)
    print("PHENOMENON: temperature=0 for structured data extraction")
    print("="*60)
    print()
    print("Task: 'Extract gene names from this abstract and return as JSON'")
    print()
    print("At temperature=0:")
    print("  → Always picks the most likely token")
    print("  → Deterministic output: same input → same output")
    print("  → Great for: data extraction, code generation, factual Q&A")
    print()
    print("At temperature=0.8:")
    print("  → Samples probabilistically — might vary run to run")
    print("  → Sometimes picks 'creative' alternatives")
    print("  → Bad for data extraction (inconsistent), good for brainstorming")
    print()
    print("Practical rule: use temperature=0 when you want the SAME answer")
    print("every time (extraction, analysis), higher when you want DIFFERENT")
    print("answers each time (brainstorming, creative writing).")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Build a Token Sampler

    Build a simple token-by-token text generator that demonstrates temperature and top-p effects. You won't be using a real language model — just a lookup table of fake probabilities — but the sampling mechanism is the same as what Claude uses.

    **Step 1:** Run the setup cell to create the vocabulary and transition probabilities.
    """)
    return


@app.cell
def _(np):
    # Simple "language model" for pain biology sentences
    # Each entry maps a context to logits for possible next tokens

    # This is a vastly simplified version of what Claude does.
    # Real models have ~100,000 tokens and continuous context representations.
    # But the SAMPLING part works exactly the same way.

    transitions = {
        '<START>': {
            'tokens': ['NaV1.7', 'TRPV1', 'DRG', 'The', 'Inflammatory'],
            'logits': np.array([3.0, 2.5, 2.0, 1.5, 1.0])
        },
        'NaV1.7': {
            'tokens': ['is', 'mutations', 'channels', 'inhibitors', 'expression'],
            'logits': np.array([3.5, 3.0, 2.0, 1.5, 1.0])
        },
        'TRPV1': {
            'tokens': ['is', 'channels', 'activation', 'expression', 'receptors'],
            'logits': np.array([3.0, 2.5, 2.5, 1.5, 1.0])
        },
        'DRG': {
            'tokens': ['neurons', 'tissue', 'ganglia', 'expression', 'cultures'],
            'logits': np.array([4.0, 2.0, 1.5, 1.0, 0.5])
        },
        'The': {
            'tokens': ['pain', 'drug', 'channel', 'results', 'mice'],
            'logits': np.array([3.0, 2.5, 2.0, 1.5, 1.5])
        },
        'is': {
            'tokens': ['expressed', 'activated', 'essential', 'involved', 'a'],
            'logits': np.array([3.0, 2.5, 2.0, 2.0, 1.5])
        },
        'neurons': {
            'tokens': ['express', 'respond', 'in', 'are', 'show'],
            'logits': np.array([3.0, 2.5, 2.0, 2.0, 1.5])
        },
        'mutations': {
            'tokens': ['cause', 'in', 'lead', 'affect', 'alter'],
            'logits': np.array([4.0, 2.0, 2.0, 1.5, 1.0])
        },
        'cause': {
            'tokens': ['pain', 'erythromelalgia', 'hyperexcitability', 'changes', 'increased'],
            'logits': np.array([3.5, 3.0, 2.5, 1.0, 1.0])
        },
        'pain': {
            'tokens': ['.', 'in', 'through', 'signaling', 'sensitivity'],
            'logits': np.array([3.0, 2.5, 2.0, 1.5, 1.5])
        },
        'expressed': {
            'tokens': ['in', 'by', 'throughout', 'at', 'within'],
            'logits': np.array([4.0, 2.0, 1.5, 1.0, 0.5])
        },
        'in': {
            'tokens': ['DRG', 'nociceptors', 'pain', 'the', 'sensory'],
            'logits': np.array([3.0, 2.5, 2.0, 2.0, 1.5])
        },
        'nociceptors': {
            'tokens': ['.', 'and', 'where', 'that', ','],
            'logits': np.array([3.5, 2.0, 1.5, 1.0, 1.0])
        }
    }

    # Default for tokens not in our table
    default_transition = {
        'tokens': ['.'],
        'logits': np.array([5.0])
    }

    print("Mini language model loaded!")
    print(f"Vocabulary covers {len(transitions)} contexts")
    print(f"\nThis is a toy model — real LLMs have billions of parameters.")
    print(f"But the SAMPLING step works the same way.")
    return default_transition, transitions


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 1: Write a `generate_sentence` function

    Complete the function below that generates a sentence token by token, using the softmax function and temperature parameter we defined earlier.
    """)
    return


@app.cell
def _(default_transition, transitions):
    def generate_sentence(temperature=1.0, max_tokens=10):
        """Generate a sentence from our mini language model.
    
        Args:
            temperature: Controls randomness (0.1 = focused, 2.0 = random)
            max_tokens: Maximum number of tokens to generate
    
        Returns:
            A string containing the generated sentence.
        """
        generated = []
        current_context = '<START>'
    
        for _ in range(max_tokens):
            # Look up transition table for current context
            transition = transitions.get(current_context, default_transition)
        
            # YOUR CODE: Apply softmax with temperature to get probabilities
            # Hint: probs = softmax(transition['logits'], temperature=temperature)
        
            # YOUR CODE: Sample a token from the probability distribution
            # Hint: next_token = rng.choice(transition['tokens'], p=probs)
        
            # YOUR CODE: Append to generated list and update context
            # Stop if we hit a period
        
            pass  # Remove this line when you add your code
    
        return ' '.join(generated)

    # Test it (uncomment after implementing):
    # for temp in [0.1, 0.5, 1.0, 2.0]:
    #     print(f"\nTemperature = {temp}:")
    #     for i in range(3):
    #         print(f"  {generate_sentence(temperature=temp)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 2: Compare temperature effects

    Generate 10 sentences at each of 4 different temperatures (0.1, 0.5, 1.0, 2.0). What do you observe about:
    - How repetitive the outputs are at low temperature?
    - How varied (or nonsensical) they get at high temperature?
    - Which temperature seems best for generating "reasonable" pain biology sentences?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: loop over temperatures, generate 10 sentences each
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 3: Add top-p filtering to your generator

    Modify `generate_sentence` (or write a new version) that also supports a `top_p` parameter. Generate sentences with `temperature=1.0` and `top_p=0.5` vs `top_p=0.99`. How does the output change?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: after computing softmax probabilities, apply the top_p_filter function
    # from Section 4, then sample from the filtered distribution
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    | Concept | What it means for AI | Practical implication |
    |---------|---------------------|----------------------|
    | **Probability distribution** | LLM assigns probability to every possible next token | Outputs are sampled, not deterministic |
    | **Conditional probability** | Context (your prompt) changes the distribution | Better prompts → better distributions → better outputs |
    | **Temperature** | Reshapes distribution (peaked vs flat) | Low T for facts/code, high T for brainstorming |
    | **Top-p** | Cuts off unlikely token tail | Prevents very weird completions |
    | **Softmax** | Converts raw scores to probabilities | Amplifies differences between likely and unlikely tokens |
    | **Log probability** | How model confidence is measured | Lower perplexity = better model |

    ### The big picture

    You now understand the probability machinery that powers every interaction you have with Claude. This knowledge makes you a more effective AI user because:

    1. **You understand why prompting techniques work** — they shift conditional probability distributions
    2. **You can tune generation parameters intelligently** — temperature and top-p for different tasks
    3. **You understand why hallucinations happen** — flat distributions over plausible-sounding options
    4. **You can evaluate model claims** — understanding perplexity and loss in AI papers

    This is the math that separates an AI power user from a casual user.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Hypothesis Testing and P-values](02-hypothesis-testing-and-pvalues.py) | [Module Index](../README.md) | [Next: Your First API Call \u2192](../09-claude-api/01-your-first-api-call.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **[Think Stats](https://allendowney.github.io/ThinkStats/)** (Allen Downey) -- Free online textbook, same author and style as Think Python. Builds probability and statistics from data using Python. **Especially relevant chapters:**
      - [Chapter 5: Modeling Distributions](https://allendowney.github.io/ThinkStats/) -- fitting analytical distributions to data; directly connects to how LLM output distributions are shaped by temperature and top-p
      - [Chapter 6: Probability](https://allendowney.github.io/ThinkStats/) -- conditional probability, Bayes' theorem, and the probability rules that underpin token generation in LLMs
    - **[Anthropic API Docs: Messages (temperature, top_p)](https://docs.anthropic.com/en/api/messages)** -- Official documentation for the `temperature` and `top_p` parameters that control Claude's sampling behavior.
    - **[The Illustrated Transformer](https://jalammar.github.io/illustrated-transformer/)** (Jay Alammar) -- The best visual explanation of how transformer models (the architecture behind Claude, GPT, etc.) work.
    - **[Softmax Function (Wikipedia)](https://en.wikipedia.org/wiki/Softmax_function)** -- Mathematical reference for the softmax function that converts raw model scores (logits) into probabilities.
    - **[Visual Information Theory](https://colah.github.io/posts/2015-09-Visual-Information/)** (Chris Olah) -- An accessible, visual introduction to information theory concepts (entropy, cross-entropy, KL divergence) that underpin how language models are trained and evaluated.
    - **[The Illustrated Word2Vec](https://jalammar.github.io/illustrated-word2vec/)** (Jay Alammar) -- A gentler starting point that explains how words become numbers (embeddings).
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
    - 2026-03-25: QA pass — added "Why this matters" rationale blockquote
    - 2026-03-25: Added standardized callouts and decision frameworks
    """)
    return


if __name__ == "__main__":
    app.run()

