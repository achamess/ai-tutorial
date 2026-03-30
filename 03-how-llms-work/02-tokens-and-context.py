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
    # 02: Tokens and Context Windows

    In the last notebook, we saw that LLMs predict the next **token**. But what exactly is a token? And why does it matter for your work?

    Understanding tokens is practical knowledge that directly affects:
    - How much text you can feed Claude in one go
    - How much your API calls cost
    - How fast you get a response
    - Whether Claude can read your entire RNA-seq results table or just part of it

    > **References:**
    > - **Think Python, Chapter 8**: [Strings](https://allendowney.github.io/ThinkPython/chap08.html) — string operations like `split()` and `len()` used throughout this notebook
    > - [Anthropic Models and Pricing](https://docs.anthropic.com/en/docs/about-claude/models) — current model specifications, context windows, and pricing
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: What Is an LLM?](01-what-is-an-llm.py) | [Module Index](../README.md) | [Next: How Claude "Thinks" \u2192](03-how-claude-thinks.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Token limits directly determine whether you can paste your entire R01 draft plus three supporting papers into one Claude conversation, or whether you need to split them up. Knowing the math means you plan effectively instead of hitting truncation mid-analysis.
    > - Scientific text (protein sequences, gene names like "prostaglandin E2 receptor") uses more tokens per word than plain English. Understanding this explains why your RNA-seq table eats context faster than you'd expect, and helps you estimate costs before running expensive API calls.
    > - Token count controls API cost. A batch analysis of 50 binder candidates costs pennies if you structure it right, or dollars if you waste tokens on redundant context. This notebook gives you the numbers to make informed decisions.
    > - Context window strategy — what to include, what to leave out, where to put key instructions — is a practical skill that directly improves Claude's output quality for literature reviews, grant drafts, and data analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What are tokens?

    A **token** is the basic unit that an LLM reads and generates. Tokens are *not* the same as words.

    LLMs use a process called **tokenization** to break text into chunks. Common words usually become one token. Uncommon words, scientific terms, and long words get split into multiple tokens.

    **Pain biology analogy:** Think of it like how a mass spectrometer fragments proteins into peptides. The spectrometer doesn't work with whole proteins or individual amino acids — it works with peptide fragments of varying length. Similarly, an LLM doesn't work with whole sentences or individual characters — it works with tokens of varying length.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exploring tokenization

    Let's see how text gets broken into tokens. We'll start with a simple word-splitting approach, then look at how real tokenizers work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That gives us 10 words. But real LLM tokenizers work differently — they use a technique called **Byte-Pair Encoding (BPE)** or similar algorithms that break text into subword pieces.

    The general pattern is:
    - Common English words ("the", "is", "in") = 1 token each
    - Common longer words ("expressed", "neurons") = 1 token each
    - Technical/rare terms ("nociceptors", "NaV1.7") = multiple tokens
    - Punctuation and whitespace = often separate tokens

    **Rule of thumb: 1 token is roughly 3/4 of a word in English, or about 4 characters.** So 100 words is about 130 tokens.
    """)
    return


@app.cell
def _():
    import numpy as np

    def estimate_tokens(text):
        """Rough token estimate: ~1.3 tokens per word for English text.
        Scientific text with technical terms runs higher (~1.5 tokens/word).
        """
        _word_count = len(text.split())
        return int(_word_count * 1.4)  # Scientific text tends to have more multi-token words
    samples = {'Plain English': 'The quick brown fox jumps over the lazy dog near the river', 'Pain biology': 'TRPV1-expressing nociceptors in the dorsal root ganglion exhibit sensitization following exposure to inflammatory mediators such as prostaglandin E2 and bradykinin', 'Protein sequence': 'MANLGCWMLVATALHPSPEGKDVPGDTDPFCKEIIVNDPKFIDNYTSGLFSVL', 'Python code': 'df = pd.read_csv("calcium_traces.csv")\npeak = df.groupby("neuron_id")["dF_F"].max()'}
    print(f"{'Type':<20} {'Words':>6} {'Est. tokens':>12} {'Chars':>6}  {'Ratio':>6}")
    # Let's test with different types of text
    print('-' * 60)
    for _label, text in samples.items():
        words = len(text.split())
        est_tok = estimate_tokens(text)
        chars = len(text)
        ratio = est_tok / max(words, 1)
        print(f'{_label:<20} {words:>6} {est_tok:>12} {chars:>6}  {ratio:>5.1f}x')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice that the protein sequence is just one "word" by whitespace splitting, but a tokenizer would break it into many tokens (roughly one per 3-4 characters). Technical terms like "prostaglandin" and "bradykinin" also tend to consume more tokens than common English words.

    **Practical impact:** When you paste a long protein sequence or a huge data table into Claude, it uses more tokens than you might expect.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why token count matters

    Tokens affect three things you care about:

    ### 1. Cost (API usage)
    When you use the Claude API, you pay per token — both for your input (prompt) and Claude's output (response). Current pricing is roughly:

    | Model | Input (per 1M tokens) | Output (per 1M tokens) |
    |-------|----------------------|----------------------|
    | Claude 3.5 Sonnet | $3.00 | $15.00 |
    | Claude 3.5 Haiku | $0.80 | $4.00 |

    *(Prices as of early 2025 — check Anthropic's pricing page for current rates.)*

    ### 2. Context window limits
    Each model has a maximum number of tokens it can handle in one conversation. If your input + output exceeds this limit, the API call fails.

    ### 3. Speed
    More output tokens = longer wait time. Claude generates tokens one at a time (remember autoregressive generation from notebook 01), so a 2,000-token response takes longer than a 200-token response.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** Context window limits affect output quality, not just whether your request fits. Even though Claude's 200K context window can hold 20+ papers, stuffing it to capacity can dilute attention. Claude pays slightly more attention to text at the beginning and end of the context, and less to material buried in the middle. For critical tasks, curate your context — give Claude only the relevant papers rather than dumping everything in. And always put your most important instructions at the top of the prompt.

    > 💡 **Tip:** Estimate token count before sending expensive API calls. A quick formula: multiply your word count by 1.4 for scientific text (technical terms use more tokens). A 6,000-word paper is roughly 8,400 tokens, which costs about $0.025 to process as input on Sonnet. Before running a batch job on 100 papers, do the math: 100 papers x 8,400 tokens = 840K tokens = ~$2.50 in input costs plus output costs. That's affordable, but knowing the number upfront prevents surprises.
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    documents = {'A short prompt': 50, 'Research abstract\n(~300 words)': 400, 'Grant specific aims\n(~1 page)': 1000, 'Methods section\n(~3 pages)': 3000, 'Full research paper\n(~8 pages)': 8000, 'R01 grant\n(~12 pages)': 16000, 'RNA-seq table\n(20k genes)': 120000}
    # Let's estimate what common research documents cost to process
    labels = list(documents.keys())
    tokens = list(documents.values())
    costs = [t * 3.0 / 1000000 for t in tokens]
    _fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    bars1 = ax1.barh(labels, tokens, color='steelblue')
    ax1.set_xscale('log')
    ax1.set_xlabel('Estimated tokens (log scale)')
    ax1.set_title('Token counts for research documents')
    ax1.invert_yaxis()
    for bar, t in zip(bars1, tokens):
        _label = f'{t:,}'
        ax1.text(bar.get_width() * 1.3, bar.get_y() + bar.get_height() / 2, _label, va='center', fontsize=9)
    bars2 = ax2.barh(labels, costs, color='coral')
    ax2.set_xlabel('Input cost (USD, Sonnet pricing)')
    # Cost at Claude 3.5 Sonnet input pricing ($3/1M tokens)
    ax2.set_title('Cost to send to Claude (input only)')
    ax2.invert_yaxis()
    for bar, c in zip(bars2, costs):
        _label = f'${c:.4f}' if c < 0.01 else f'${c:.3f}' if c < 1 else f'${c:.2f}'
    # Token counts
        ax2.text(bar.get_width() + max(costs) * 0.02, bar.get_y() + bar.get_height() / 2, _label, va='center', fontsize=9)
    plt.tight_layout()
    plt.show()
    print('Key insight: even a full research paper costs less than a penny to process.')
    # Costs
    print('Large data tables are where costs add up — but still very affordable.')
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** Which model should you use based on context needs and cost?
    >
    > | Model | Context window | Input cost (per 1M tokens) | Output cost (per 1M tokens) | Use when... |
    > |-------|---------------|---------------------------|----------------------------|-------------|
    > | **Claude 3.5 Haiku** | 200K tokens | $0.80 | $4.00 | High-volume tasks where speed and cost matter more than depth: batch data extraction, simple classification, parsing screening results |
    > | **Claude 3.5 Sonnet** | 200K tokens | $3.00 | $15.00 | The workhorse: grant writing, paper synthesis, code generation, experimental design — best balance of quality and cost |
    > | **Claude 3 Opus** | 200K tokens | $15.00 | $75.00 | When you need maximum reasoning depth: complex multi-paper synthesis, subtle scientific arguments, challenging code architecture |
    >
    > **Rule of thumb:** Start with Sonnet. Drop to Haiku for batch/repetitive tasks. Upgrade to Opus only when Sonnet's output isn't good enough for a specific task. Most research tasks hit the sweet spot with Sonnet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Context windows: what fits, what doesn't

    The **context window** is the total amount of text (input + output) that a model can handle in one conversation. Think of it as the model's working memory.

    | Model | Context window |
    |-------|---------------|
    | Claude 3.5 Sonnet | 200,000 tokens |
    | Claude 3.5 Haiku | 200,000 tokens |
    | GPT-4o | 128,000 tokens |

    200,000 tokens is roughly 150,000 words, or about **500 pages** of text. That's a lot — you can fit an entire dissertation in one conversation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph TD
        subgraph CTX ["Context Window — 200,000 tokens"]
            direction TB
            SYS["<b>System Prompt</b><br/>~200 tokens<br/>Sets Claude's role & rules"]
            CONTENT["<b>Your Content</b><br/>Papers, data, code<br/>(variable size)"]
            PROMPT["<b>Your Instruction</b><br/>~100-500 tokens<br/>What to do with the content"]
            RESPONSE["<b>Claude's Response</b><br/>~200-5,000 tokens<br/>The generated output"]
            FREE["<b>Unused Capacity</b>"]

            SYS ~~~ CONTENT
            CONTENT ~~~ PROMPT
            PROMPT ~~~ RESPONSE
            RESPONSE ~~~ FREE
        end

        subgraph COST ["Token Costs at a Glance"]
            C1["Research abstract<br/>~400 tokens"]
            C2["Full paper<br/>~8,000 tokens"]
            C3["R01 grant<br/>~16,000 tokens"]
            C4["RNA-seq table (20k genes)<br/>~120,000 tokens"]
        end

        style SYS fill:#aa44aa,color:#fff
        style CONTENT fill:#cc8844,color:#fff
        style PROMPT fill:#4488cc,color:#fff
        style RESPONSE fill:#44aa88,color:#fff
        style FREE fill:#e8e8e8,color:#666
    ```

    **Key insight:** Even a full R01 grant application uses less than 10% of Claude's context window. You can fit your grant + 10 supporting papers in a single conversation.
    """)
    return


@app.cell
def _():
    # How much research content fits in Claude's 200K context window?
    _context_window = 200000
    research_items = {'Research abstracts (~400 tok each)': (400, 'abstracts'), 'Full papers (~8,000 tok each)': (8000, 'papers'), 'R01 grant pages (~1,300 tok each)': (1300, 'pages'), 'Gene rows in RNA-seq table (~6 tok each)': (6, 'genes'), 'Protein sequences (~200 tok each, ~500 residues)': (200, 'sequences')}  # tokens
    print("What fits in Claude's 200K context window:")
    print('=' * 55)
    usable = _context_window - 20000
    print(f"(Reserving ~20K tokens for your prompt and Claude's response)\n")
    for _desc, (tok_per_item, unit) in research_items.items():
        count = usable // tok_per_item
        print(f'  {count:>6,} {unit:<12}  ({_desc})')
    print(f'\nYou could paste ~22 full papers into a single conversation.')
    print(f'Or ~30,000 genes from an RNA-seq table.')
    # Reserve 20K tokens for the prompt and response
    print(f"That's powerful for literature review and data analysis.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Practical exercise: Estimate tokens in your research

    Let's estimate how many tokens are in some real research text. Below are representative samples — replace them with your own text when you're experimenting.
    """)
    return


@app.cell
def _():
    # Sample research abstract (NaV1.7 related)
    abstract = "\nVoltage-gated sodium channel NaV1.7 (encoded by SCN9A) is a critical determinant \nof pain signaling in the peripheral nervous system. Gain-of-function mutations in \nSCN9A cause inherited erythromelalgia and paroxysmal extreme pain disorder, while \nloss-of-function mutations result in congenital insensitivity to pain. These human \ngenetic findings have validated NaV1.7 as a high-priority target for novel analgesic \ndevelopment. However, achieving selective pharmacological blockade of NaV1.7 over \nother NaV subtypes, particularly NaV1.5 (cardiac) and NaV1.6 (CNS), remains a \nsignificant challenge. Here we report the design and characterization of de novo \nprotein binders targeting the voltage-sensing domain of NaV1.7 with subnanomolar \naffinity and >1000-fold selectivity over NaV1.5. Lead candidates were validated in \nDRG neuron cultures using calcium imaging and whole-cell patch clamp electrophysiology, \ndemonstrating potent inhibition of NaV1.7-mediated currents without affecting action \npotential firing in NaV1.8-expressing nociceptors. In vivo testing in a complete \nFreund's adjuvant model of inflammatory pain showed dose-dependent analgesia with \nno observed cardiac or motor side effects.\n".strip()
    _word_count = len(abstract.split())
    char_count = len(abstract)
    est_by_words = int(_word_count * 1.4)
    est_by_chars = int(char_count / 3.5)
    print('Research Abstract Analysis')
    print('=' * 40)
    print(f'Word count:              {_word_count}')
    print(f'Character count:         {char_count}')
    print(f'Estimated tokens (word): ~{est_by_words}')
    print(f'Estimated tokens (char): ~{est_by_chars}')
    print(f'Average estimate:        ~{(est_by_words + est_by_chars) // 2}')
    print()
    print(f'Cost to send as input (Sonnet): ${est_by_words * 3.0 / 1000000:.5f}')
    # Count basic stats
    # Estimate tokens using different methods
    print(f"That's about {est_by_words / 200000 * 100:.3f}% of the context window.")  # scientific text multiplier  # character-based estimate
    return


@app.cell
def _():
    # Now let's estimate for a whole grant section
    specific_aims = '\nSpecific Aims\n\nChronic pain affects over 50 million adults in the United States, with current \ntreatments limited by poor efficacy, addiction liability, and off-target effects. \nThe voltage-gated sodium channel NaV1.7 represents one of the most genetically \nvalidated analgesic targets, yet decades of effort to develop selective small-molecule \ninhibitors have yielded disappointing clinical results. We propose a fundamentally \ndifferent approach: engineered protein binders that achieve selectivity through \nmulti-point contacts with NaV1.7-specific epitopes, coupled with targeted protein \ndegradation to achieve sustained functional knockdown.\n\nAim 1: Design and optimize de novo protein binders targeting the NaV1.7 \nvoltage-sensing domain (VSD-IV) using computational protein design.\nWe will use RFdiffusion and ProteinMPNN to generate candidate binders targeting \nthe S1-S2 and S3-S4 loops of VSD-IV, where NaV1.7 diverges most from NaV1.5. \nCandidates will be screened by AlphaFold2 confidence metrics and validated by \nyeast surface display. We expect to identify >5 binders with Kd <50 nM and \n>100-fold selectivity over NaV1.5.\n\nAim 2: Engineer binder-E3 ligase chimeras for targeted degradation of NaV1.7 \nin DRG neurons.\nLead binders from Aim 1 will be fused to CRBN-recruiting modules to create \nbifunctional degraders (protein-based PROTACs). We will characterize degradation \nefficiency, selectivity, and kinetics in heterologous cells and cultured DRG \nneurons using Western blot, immunocytochemistry, and functional assays (calcium \nimaging, multi-electrode arrays).\n\nAim 3: Evaluate lead degrader candidates in preclinical models of inflammatory \nand neuropathic pain.\nTop candidates will be tested in CFA inflammatory pain and spared nerve injury \nneuropathic pain models. Primary endpoints include von Frey mechanical sensitivity, \nHargreaves thermal sensitivity, and conditioned place preference. Safety will be \nassessed by cardiac electrophysiology (ECG), motor function (rotarod), and \nhistopathology of DRG and peripheral nerves.\n\nImpact: This project will establish a new therapeutic modality — protein-based \ntargeted degradation — for the treatment of chronic pain, with a pipeline \napplicable to other ion channel targets including NaV1.8 and KCNQ2/3.\n'.strip()
    _word_count = len(specific_aims.split())
    _est_tokens = int(_word_count * 1.4)
    print('Specific Aims Page Analysis')
    print('=' * 40)
    print(f'Word count:        {_word_count}')
    print(f'Estimated tokens:  ~{_est_tokens}')
    print(f'Context usage:     {_est_tokens / 200000 * 100:.2f}%')
    print()
    print("Even a full specific aims page is a tiny fraction of Claude's context window.")
    print("You could include your entire grant application AND the papers you're citing.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Simulating a tokenizer

    Real tokenizers (like the ones used by Claude) use BPE — Byte-Pair Encoding. Here's a simplified version to build intuition. The key idea: common sequences of characters get merged into single tokens.
    """)
    return


@app.cell
def _():
    # Simplified tokenization demo
    # This shows the PRINCIPLE, not the exact algorithm

    def simple_tokenize(text):
        """A simplified tokenizer that mimics BPE behavior.
        Common words stay whole; rare/technical words get split.
        This is illustrative, not a real tokenizer.
        """
        # Common words that would be single tokens
        common_words = {
            "the", "is", "in", "of", "and", "a", "to", "for", "with", "that",
            "are", "by", "from", "an", "as", "it", "was", "which", "or", "be",
            "this", "not", "have", "has", "but", "can", "on", "at", "we", "our",
            "pain", "neurons", "channel", "expression",  # common in training data
        }
    
        tokens = []
        for word in text.split():
            word_lower = word.lower().strip(".,;:()")
            if word_lower in common_words:
                tokens.append(word)
            elif len(word) <= 5:
                tokens.append(word)
            else:
                # Split longer uncommon words into chunks (simulating subword tokenization)
                # Real BPE is more sophisticated, but this shows the principle
                i = 0
                parts = []
                while i < len(word):
                    chunk_size = min(4, len(word) - i)
                    if i == 0:
                        chunk_size = min(5, len(word))
                    parts.append(word[i:i + chunk_size])
                    i += chunk_size
                tokens.extend(parts)
    
        return tokens

    # Compare plain English vs. scientific text
    plain = "The dog is in the park and the sun is warm"
    scientific = "TRPV1-expressing nociceptors exhibit sensitization following prostaglandin E2 exposure"

    plain_tokens = simple_tokenize(plain)
    sci_tokens = simple_tokenize(scientific)

    print("Plain English:")
    print(f"  Text:   '{plain}'")
    print(f"  Tokens: {plain_tokens}")
    print(f"  Count:  {len(plain_tokens)} tokens for {len(plain.split())} words")
    print()
    print("Scientific text:")
    print(f"  Text:   '{scientific}'")
    print(f"  Tokens: {sci_tokens}")
    print(f"  Count:  {len(sci_tokens)} tokens for {len(scientific.split())} words")
    print()
    print("Scientific text uses more tokens per word because technical terms")
    print("get split into subword pieces.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## How context affects output quality

    The context window isn't just about *fitting* text — it's about **quality**. More context generally means better output. Here's why:

    ### The "needle in a haystack" effect
    Claude can use information from anywhere in its context window. If you paste a 50-page paper and ask about a detail on page 43, Claude can find it. But there are practical limits:

    - **Beginning and end bias**: Models tend to pay slightly more attention to text at the beginning and end of the context. Put your most important instructions at the top.
    - **Relevance dilution**: If you dump 20 papers into a conversation, Claude has to figure out which parts matter. Curating your context (giving only relevant papers) produces better results.
    - **Instruction following**: The longer the context, the more important it is to be clear about what you want.

    ### Context strategies for research

    | Task | Strategy |
    |------|----------|
    | Summarize a paper | Paste the full text — Claude works best with the complete source |
    | Compare papers | Paste 2-3 relevant papers with a clear comparison question |
    | Draft grant text | Provide your aims, relevant background papers, and style examples |
    | Debug code | Include the full error traceback and the relevant code file |
    | Analyze data | Paste a representative sample if the full dataset is too large |
    """)
    return


@app.cell
def _(plt):
    import matplotlib.patches as mpatches
    _fig, ax = plt.subplots(figsize=(12, 6))
    _context_window = 200000
    workflows = [{'name': 'Quick question', 'parts': [('Prompt', 100, '#4488cc'), ('Response', 500, '#44aa88'), ('Free', _context_window - 600, '#e8e8e8')]}, {'name': 'Summarize paper', 'parts': [('Paper text', 8000, '#cc8844'), ('Prompt', 200, '#4488cc'), ('Response', 2000, '#44aa88'), ('Free', _context_window - 10200, '#e8e8e8')]}, {'name': 'Literature review\n(5 papers)', 'parts': [('Papers', 40000, '#cc8844'), ('Prompt', 500, '#4488cc'), ('Response', 5000, '#44aa88'), ('Free', _context_window - 45500, '#e8e8e8')]}, {'name': 'RNA-seq analysis\n(full DEG table)', 'parts': [('Data table', 120000, '#cc8844'), ('Prompt', 500, '#4488cc'), ('Response', 3000, '#44aa88'), ('Free', _context_window - 123500, '#e8e8e8')]}, {'name': 'Grant draft\n(full application)', 'parts': [('Draft + refs', 80000, '#cc8844'), ('Prompt', 1000, '#4488cc'), ('Response', 10000, '#44aa88'), ('Free', _context_window - 91000, '#e8e8e8')]}]
    y_positions = range(len(workflows))
    for i, wf in enumerate(workflows):
        left = 0
        for part_name, size, color in wf['parts']:
            ax.barh(i, size, left=left, color=color, edgecolor='white', linewidth=0.5, height=0.6)
            if size > _context_window * 0.05:
                ax.text(left + size / 2, i, f'{size:,}', ha='center', va='center', fontsize=7)
            left += size
    ax.set_yticks(y_positions)
    ax.set_yticklabels([wf['name'] for wf in workflows])
    ax.set_xlabel('Tokens')
    ax.set_title('Context window usage for different research workflows (200K window)')
    ax.set_xlim(0, _context_window)
    legend_patches = [mpatches.Patch(color='#cc8844', label='Content (papers, data)'), mpatches.Patch(color='#4488cc', label='Your prompt'), mpatches.Patch(color='#44aa88', label="Claude's response"), mpatches.Patch(color='#e8e8e8', label='Unused capacity')]
    ax.legend(handles=legend_patches, loc='upper right', fontsize=9)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Token budget planning

    You want to use Claude to help review and compare three papers about NaV1.7 binder design. Estimate whether everything will fit in a single conversation, and what it will cost.
    """)
    return


@app.cell
def _():
    # YOUR TURN: Fill in the estimates
    paper_1_words = 6500
    # Typical paper lengths (in words)
    paper_2_words = 4200  # Research article
    paper_3_words = 8100  # Short communication
    prompt_words = 150  # Review article
    response_words = 1500
    # Your prompt
    multiplier = 1.4  # "Compare these three papers focusing on..."
    paper_tokens = int((paper_1_words + paper_2_words + paper_3_words) * multiplier)
    # Expected response length
    prompt_tokens = int(prompt_words * 1.3)  # A detailed comparison
    response_tokens = int(response_words * 1.3)
    # ---- Calculate ----
    # Use the 1.4x multiplier for scientific text
    total_tokens = paper_tokens + prompt_tokens + response_tokens
    _context_window = 200000
    print('Token Budget Estimate')
    print('=' * 40)  # prompts are usually more plain English
    print(f'Three papers:    ~{paper_tokens:,} tokens')
    print(f'Your prompt:     ~{prompt_tokens:,} tokens')
    print(f'Expected output: ~{response_tokens:,} tokens')
    print(f'Total:           ~{total_tokens:,} tokens')
    print()
    print(f'Context window:  {_context_window:,} tokens')
    print(f'Usage:           {total_tokens / _context_window * 100:.1f}%')
    print(f"Fits?            {('Yes!' if total_tokens < _context_window else 'No — need to trim.')}")
    print()
    input_cost = (paper_tokens + prompt_tokens) * 3.0 / 1000000
    output_cost = response_tokens * 15.0 / 1000000
    total_cost = input_cost + output_cost
    print(f'Estimated cost (Sonnet):')
    print(f'  Input:  ${input_cost:.4f}')
    print(f'  Output: ${output_cost:.4f}')
    print(f'  Total:  ${total_cost:.4f}')
    # Cost estimate (Sonnet pricing)
    print(f"\nThat's about {total_cost * 100:.2f} cents for a detailed comparison of 3 papers.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: What fits in the context window?

    For each scenario, estimate whether it fits in a single 200K-token conversation. Modify the code below to check your intuition.
    """)
    return


@app.cell
def _():
    # Check whether various research tasks fit in a 200K context window
    context_limit = 200000
    scenarios = [('Your entire R01 grant application (12 pages)', 16000), ('10 papers for literature review', 80000), ('Full RNA-seq DEG table (20,000 genes x 6 columns)', 120000), ('A 500-page PhD thesis', 650000), ('All abstracts from a PubMed search (200 results)', 80000), ('Your lab notebook for one month', 30000), ('The human SCN9A gene sequence (full mRNA, ~6kb)', 8000), ('Calcium imaging data: 100 neurons x 1000 timepoints (CSV)', 400000)]
    reserved = 20000
    available = context_limit - reserved
    print(f'Context window: {context_limit:,} tokens')
    print(f'Reserved for prompt/response: {reserved:,} tokens')
    print(f'Available for content: {available:,} tokens')
    print('=' * 70)
    for _desc, _est_tokens in scenarios:
        fits = _est_tokens <= available
        pct = _est_tokens / context_limit * 100
        status = 'FITS' if fits else 'TOO BIG'
        print(f'  [{status:>7}] {_desc}')
        print(f'           ~{_est_tokens:>8,} tokens ({pct:.1f}% of window)')
    # Reserve space for prompt and response
        if not fits:
            print(f'           Suggestion: split into {_est_tokens // available + 1} chunks')
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Tips for managing tokens in practice

    1. **Give Claude the full source when possible.** Pasting a complete paper is better than paraphrasing it — Claude can find the details it needs.

    2. **For large datasets, send a representative sample.** If your RNA-seq table has 20,000 genes, send the top 500 differentially expressed genes plus a description of the full dataset.

    3. **Start a new conversation when context gets stale.** Long conversations accumulate context. If you've been going back and forth for 20 exchanges about different topics, start fresh rather than continuing.

    4. **Put key instructions at the top.** Due to how attention works, instructions at the beginning and end of the context are most reliably followed.

    5. **Be concise in your prompts.** You don't need to write a paragraph when a sentence will do. But be *specific* — brevity isn't the same as vagueness.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Key takeaways

    1. **Tokens are subword pieces** — common words = 1 token, technical terms = multiple tokens. Roughly 1 token per 3/4 of a word.
    2. **Token count determines cost, speed, and fit.** More tokens = higher cost, slower response, but also richer context.
    3. **Context windows are generous.** 200K tokens fits 20+ papers or an entire grant application.
    4. **More context = better output** — but curate for relevance rather than dumping everything in.
    5. **Scientific text uses more tokens per word** than plain English, because of technical vocabulary.

    Next up: [03-how-claude-thinks.py](./03-how-claude-thinks.py) — we'll explore how Claude processes your messages and how to get better outputs by understanding the conversation structure.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [← Previous: What Is an LLM?](01-what-is-an-llm.py) | [Module Index](../README.md) | [Next: How Claude "Thinks" →](03-how-claude-thinks.py)
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
    - 2026-03-25: QA pass — removed code cell containing markdown text (duplicate of adjacent markdown cell)
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Think Python, Chapter 8**: [Strings](https://allendowney.github.io/ThinkPython/chap08.html) — Python string operations (`.split()`, `.len()`, slicing) used for text manipulation throughout this notebook
    - [Anthropic Models and Pricing](https://docs.anthropic.com/en/docs/about-claude/models) — official documentation on Claude model specifications, context window sizes, and current per-token pricing
    - [OpenAI Tokenizer Tool](https://platform.openai.com/tokenizer) — an interactive tool for visualizing how text gets broken into tokens; useful for building intuition even though Claude uses a different tokenizer
    - [Anthropic: Counting Tokens](https://docs.anthropic.com/en/docs/build-with-claude/token-counting) — Anthropic's documentation on token counting for the Claude API, including how to estimate costs
    - [Byte-Pair Encoding (Hugging Face)](https://huggingface.co/learn/nlp-course/chapter6/5) — a clear explanation of the BPE tokenization algorithm that most modern LLMs use
    - [Anthropic API Reference: Messages](https://docs.anthropic.com/en/api/messages) — the API endpoint documentation showing how `input_tokens` and `output_tokens` are reported in responses
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
    - 2026-03-25: QA pass — removed code cell containing markdown text (duplicate of adjacent markdown cell)
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

