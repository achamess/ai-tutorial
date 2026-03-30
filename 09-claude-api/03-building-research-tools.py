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
    # 03: Building Research Tools

    You can now make API calls and get structured data back. This notebook puts it all together -- you'll build tools that process **batches** of data, handle **multi-turn conversations**, deal with **errors gracefully**, and combine Claude with **pandas** for real research workflows.

    By the end, you'll have a template for building any custom AI tool you need for your pain biology research.

    **Key references:** [Anthropic API: Rate Limits](https://docs.anthropic.com/en/api/rate-limits) | [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) | [Python `time` module](https://docs.python.org/3/library/time.html) | [Pandas DataFrame docs](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Structured Outputs](02-structured-outputs.py) | [Module Index](../README.md) | [Next: Pandas Basics for Research Data \u2192](../10-data-skills/01-pandas-basics.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - This notebook gives you the complete toolkit for building custom AI-powered research tools: batch processing, error handling, multi-turn conversations, and Claude + pandas integration.
    > - The batch processing pattern (loop over items, call Claude, collect structured results) is what you'll use to annotate gene lists from RNA-seq, classify screening compounds, and enrich experimental DataFrames with AI-generated context.
    > - Multi-turn conversations let you build interactive research assistants -- like the PaperQA tool that answers follow-up questions about a specific paper in context.
    > - The patterns here compose into any research tool you need. Once you have these building blocks, the bottleneck shifts from "can I build this?" to "what should I build?"
    """)
    return


@app.cell
def _():
    from anthropic import Anthropic
    import json
    import time
    import pandas as pd

    client = Anthropic()


    def parse_json_response(text):
        """Parse JSON from Claude's response, handling markdown code fences."""
        cleaned = text.strip()
        if cleaned.startswith("```"):
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:-1])
        return json.loads(cleaned)


    print("Ready.")
    return Anthropic, client, json, parse_json_response, pd, time


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Batch processing: running Claude over multiple inputs

    The most common pattern: you have a **list of items** and you want Claude to process each one. This could be gene names, paper abstracts, compound names, or anything else.

    Let's start with a realistic scenario: you have a list of ion channels from a DRG single-cell RNA-seq dataset and you want to classify each one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### Batch Processing Flow

    """),
    mo.mermaid(
        """
        flowchart TD
            INPUT["List of items<br>(genes, abstracts,<br>compounds)"] --> LOOP["For each item"]
            LOOP --> CALL["Call Claude API<br>with item + system prompt"]
            CALL --> PARSE{"Parse JSON<br>successful?"}
        
            PARSE -->|"Yes"| COLLECT["Add result<br>to list"]
            PARSE -->|"No"| RETRY{"Retries<br>left?"}
        
            RETRY -->|"Yes"| WAIT["Wait<br>(exponential backoff)"] --> CALL
            RETRY -->|"No"| SKIP["Log failure<br>append None"]
        
            COLLECT --> MORE{"More<br>items?"}
            SKIP --> MORE
            MORE -->|"Yes"| DELAY["Brief delay<br>(avoid rate limits)"] --> LOOP
            MORE -->|"No"| DF["pd.DataFrame(results)<br>Filter, analyze, save"]
        
            style INPUT fill:#4878CF,color:#fff
            style CALL fill:#E24A33,color:#fff
            style COLLECT fill:#55A868,color:#fff
            style DF fill:#55A868,color:#fff
            style SKIP fill:#FDB863,color:#000
            style WAIT fill:#FDB863,color:#000
        """
    ),
    mo.md(r"""

    This is the robust batch processing pattern you'll use for any task that processes multiple items through Claude. The key features are: (1) error handling with retries, (2) brief delays between calls to avoid rate limits, and (3) graceful failure -- one bad item doesn't crash the whole batch.
    """)
    ])
    return


@app.cell
def _(client, parse_json_response):
    # Ion channels detected in DRG neuron clusters
    channels = [
        "SCN9A",   # NaV1.7
        "SCN10A",  # NaV1.8
        "SCN11A",  # NaV1.9
        "KCNQ2",   # Kv7.2
        "KCNQ3",   # Kv7.3
        "TRPV1",   # capsaicin receptor
        "TRPA1",   # mustard oil receptor
        "TRPM8",   # cold receptor
        "CACNA1B", # CaV2.2 (N-type calcium)
        "P2RX3",   # purinergic receptor
    ]

    CLASSIFY_SYSTEM = """You are an ion channel classification tool for pain research.
    Given a gene name, return JSON (no other text, no code fences):
    {
        "gene": "gene symbol",
        "protein": "protein name",
        "ion_selectivity": "Na+|K+|Ca2+|non-selective cation|Cl-|other",
        "pain_role": "brief description",
        "therapeutic_target": true/false,
        "existing_drugs": ["list of known drugs targeting this channel, or empty list"]
    }"""


    def classify_channel(gene):
        """Classify an ion channel gene for pain research context."""
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            system=CLASSIFY_SYSTEM,
            messages=[{"role": "user", "content": f"Classify: {gene}"}]
        )
        return parse_json_response(message.content[0].text)

    return channels, classify_channel


@app.cell
def _(channels, classify_channel):
    # Process all channels
    results = []
    for gene in channels:
        print(f'  Classifying {gene}...', end=' ')
        try:
            _result = classify_channel(gene)
            results.append(_result)
            print(f"-> {_result['protein']} ({_result['ion_selectivity']})")
        except Exception as e:
            print(f'FAILED: {e}')
            results.append({'gene': gene, 'error': str(e)})
    print(f'\nProcessed {len(results)} channels.')
    return (results,)


@app.cell
def _(pd, results):
    # Convert to DataFrame for analysis
    df = pd.DataFrame(results)
    df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Rate limiting and error handling

    When processing batches, two things can go wrong:

    1. **Rate limits** — too many requests per minute. The API returns a 429 error.
    2. **Transient errors** — network issues, server hiccups. Usually resolved by retrying.

    Here's a robust batch processor that handles both.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Warning:** Rate limits and error handling are critical for batch processing. The Anthropic API has per-minute rate limits that vary by model and account tier. Without proper error handling, hitting a rate limit crashes your entire batch and you lose all progress. Always use the `batch_process` pattern below with exponential backoff (wait 5s, then 10s, then 20s on retries) and save intermediate results periodically so you can resume if something fails.

    > **Tip:** Exponential backoff is the standard pattern for handling rate limits. Instead of retrying immediately (which just hits the rate limit again), wait progressively longer: 5 seconds, then 10, then 20. The `batch_process` function below implements this. You'll use this pattern in every production pipeline.

    > **Decision point: Batch processing vs real-time vs streaming**
    >
    > | Approach | Latency | Cost efficiency | Complexity | Use when |
    > |----------|---------|----------------|------------|----------|
    > | **Batch processing** (loop over items) | High (minutes for large batches) | Best -- can use Haiku for volume | Low -- simple loop with error handling | Processing gene lists, annotating DataFrames, classifying screening hits |
    > | **Real-time** (single call, wait for response) | Low (1-5 seconds) | Moderate | Lowest | Interactive Q&A, one-off questions, live analysis |
    > | **Streaming** (tokens arrive incrementally) | Perceived low (first token fast) | Same as real-time | Medium -- need to handle partial responses | User-facing tools where perceived responsiveness matters |
    >
    > **For research pipelines:** Batch processing is almost always the right choice. You're processing data offline, so latency doesn't matter. Use the `batch_process` function with a small delay between calls (0.5s) to stay well under rate limits.
    """)
    return


@app.cell
def _(json, time):
    from anthropic import RateLimitError, APIError

    def batch_process(items, process_fn, delay=0.5, max_retries=3):
        """Process a list of items with Claude, handling rate limits and errors.
    
        Args:
            items: list of inputs to process
            process_fn: function that takes one item and returns a result
            delay: seconds to wait between calls (helps avoid rate limits)
            max_retries: number of retries for failed calls
    
        Returns:
            list of (item, result) tuples. result is None if all retries failed.
        """
        results = []
        for i, item in enumerate(items):
            print(f'  [{i + 1}/{len(items)}] Processing: {item}', end=' ')
            _result = None
            for attempt in range(max_retries):
                try:
                    _result = process_fn(item)
                    print('OK')
                    break
                except RateLimitError:
                    wait = 2 ** attempt * 5
                    print(f'rate limited, waiting {wait}s...', end=' ')
                    time.sleep(wait)
                except (json.JSONDecodeError, APIError) as e:  # exponential backoff: 5s, 10s, 20s
                    print(f'error ({e}), retrying...', end=' ')
                    time.sleep(1)
            if _result is None:
                print('FAILED after all retries')
            results.append((item, _result))
            if i < len(items) - 1:
                time.sleep(delay)
        succeeded = sum((1 for _, r in results if r is not None))
        print(f'\nDone: {succeeded}/{len(items)} succeeded.')
        return results
    print('batch_process() defined.')  # Small delay between calls to be a good API citizen
    return (batch_process,)


@app.cell
def _(batch_process, classify_channel, pd):
    # Test with a small batch
    test_genes = ['SCN9A', 'TRPV1', 'CALCA', 'NGF']
    results_1 = batch_process(test_genes, classify_channel, delay=0.2)
    successful = [r for _, r in results_1 if r is not None]
    # Extract just the successful results
    pd.DataFrame(successful)[['gene', 'protein', 'ion_selectivity', 'therapeutic_target']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Multi-turn conversations via the API

    In Claude chat, you have a back-and-forth conversation. You can do the same via the API by passing the **full message history** each time. This is essential for follow-up questions, clarifications, and iterative exploration.
    """)
    return


@app.cell
def _(Anthropic):
    class ResearchChat:
        """A multi-turn conversation with Claude for research Q&A."""
    
        def __init__(self, system=None, model="claude-sonnet-4-6"):
            self.client = Anthropic()
            self.model = model
            self.system = system or (
                "You are a knowledgeable pain biology research assistant. "
                "Give precise, technical answers. When discussing ion channels, "
                "include gene names, protein names, and relevant expression data. "
                "Be concise."
            )
            self.messages = []  # conversation history
    
        def ask(self, question):
            """Ask a question, maintaining conversation context."""
            # Add the new user message to history
            self.messages.append({"role": "user", "content": question})
        
            # Send the full conversation
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1024,
                system=self.system,
                messages=self.messages
            )
        
            answer = response.content[0].text
        
            # Add Claude's response to history (so the next call has full context)
            self.messages.append({"role": "assistant", "content": answer})
        
            return answer
    
        def reset(self):
            """Clear conversation history."""
            self.messages = []


    print("ResearchChat class defined.")
    return (ResearchChat,)


@app.cell
def _(ResearchChat):
    # Have a multi-turn conversation about a research topic
    chat = ResearchChat()

    # First question
    print("Q1: What are the main sodium channel subtypes expressed in DRG nociceptors?")
    print()
    answer1 = chat.ask("What are the main sodium channel subtypes expressed in DRG nociceptors?")
    print(answer1)
    return (chat,)


@app.cell
def _(chat):
    # Follow-up — Claude remembers the context
    print("Q2: Which of those would be the best target for a protein degrader, and why?")
    print()
    answer2 = chat.ask("Which of those would be the best target for a protein degrader approach, and why?")
    print(answer2)
    return


@app.cell
def _(chat):
    # Further follow-up
    print("Q3: What about selectivity — how similar are NaV1.7 and NaV1.8 structurally?")
    print()
    answer3 = chat.ask(
        "What about selectivity challenges — how similar are NaV1.7 and NaV1.8 "
        "structurally, and how would that affect binder design?"
    )
    print(answer3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Key insight:** Every time you call `chat.ask()`, the **entire conversation history** is sent to the API. This is how Claude maintains context. It also means longer conversations cost more tokens — the input grows with each turn. For long research sessions, consider starting fresh conversations for new topics.

    > **Think Python connection:** `ResearchChat` is a **class** — it bundles data (the message history) with functions (the `ask` method). If you haven't seen classes before, just think of it as a convenient container. The important thing is that `self.messages` accumulates the conversation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Combining Claude with pandas

    Here's a real-world scenario: you have a DataFrame of experimental results and you want to add AI-generated annotations. Let's simulate a calcium imaging dataset where you want Claude to help interpret the results.
    """)
    return


@app.cell
def _(pd):
    import numpy as np

    # Simulated calcium imaging data: compounds tested on DRG neurons
    np.random.seed(42)

    compounds_df = pd.DataFrame({
        "compound": [
            "capsaicin", "menthol", "mustard oil (AITC)", "ATP", 
            "bradykinin", "PGE2", "substance P", "NGF",
            "lidocaine", "carbamazepine"
        ],
        "concentration_uM": [1.0, 100, 50, 10, 1.0, 10, 1.0, 0.1, 100, 50],
        "pct_neurons_responding": [45, 32, 28, 55, 38, 22, 15, 8, 0, 5],
        "mean_delta_f_over_f": [2.8, 1.5, 2.1, 3.2, 1.8, 0.9, 0.6, 0.3, 0.0, 0.15],
        "response_type": [
            "transient", "sustained", "transient", "transient",
            "sustained", "sensitization", "slow_onset", "sensitization",
            "inhibition", "inhibition"
        ]
    })

    print("Simulated calcium imaging dataset:")
    compounds_df
    return (compounds_df,)


@app.cell
def _(client, compounds_df, parse_json_response):
    # Use Claude to annotate each compound with its receptor/target and mechanism
    COMPOUND_SYSTEM = """You annotate compounds used in DRG calcium imaging experiments.
    Return JSON only (no other text, no code fences):
    {
        "compound": "compound name",
        "primary_target": "receptor or channel name",
        "target_gene": "gene symbol",
        "mechanism": "agonist|antagonist|inhibitor|sensitizer|modulator",
        "expected_cell_type": "nociceptor|mechanoreceptor|all_drg|proprioceptor",
        "clinical_relevance": "brief note on clinical significance"
    }"""


    def annotate_compound(compound_name):
        """Get pain biology annotation for a compound."""
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=256,
            system=COMPOUND_SYSTEM,
            messages=[{"role": "user", "content": f"Annotate: {compound_name}"}]
        )
        return parse_json_response(message.content[0].text)


    # Process all compounds
    annotations = []
    for compound in compounds_df["compound"]:
        print(f"  Annotating {compound}...", end=" ")
        try:
            ann = annotate_compound(compound)
            annotations.append(ann)
            print(f"target={ann['primary_target']}")
        except Exception as e:
            print(f"FAILED: {e}")
            annotations.append({
                "compound": compound, "primary_target": "unknown",
                "target_gene": "unknown", "mechanism": "unknown",
                "expected_cell_type": "unknown", "clinical_relevance": "error"
            })

    print("Done.")
    return (annotations,)


@app.cell
def _(annotations, compounds_df, pd):
    # Merge annotations back into the original DataFrame
    ann_df = pd.DataFrame(annotations)

    # Join on compound name
    enriched_df = compounds_df.merge(ann_df, on="compound", how="left")

    # Show the enriched dataset
    enriched_df[["compound", "primary_target", "target_gene", "mechanism", 
                 "pct_neurons_responding", "mean_delta_f_over_f"]]
    return (enriched_df,)


@app.cell
def _(enriched_df):
    # Now you can do AI-informed analysis
    # Which agonists caused the strongest responses?
    agonists = enriched_df[enriched_df["mechanism"] == "agonist"].sort_values(
        "mean_delta_f_over_f", ascending=False
    )

    print("Agonist compounds ranked by response amplitude:")
    for _, row in agonists.iterrows():
        print(f"  {row['compound']} ({row['primary_target']}) — "
              f"dF/F={row['mean_delta_f_over_f']:.1f}, "
              f"{row['pct_neurons_responding']}% responding")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This pattern — **experimental data + AI annotation + analysis** — is incredibly powerful. You're not replacing your expertise; you're using Claude to automate the tedious literature-lookup step so you can focus on interpretation.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Building a literature Q&A tool

    Let's build a slightly more sophisticated tool: a literature Q&A system that takes a paper abstract and lets you ask questions about it. This uses multi-turn conversation with context.
    """)
    return


@app.cell
def _(Anthropic):
    class PaperQA:
        """Ask questions about a research paper (given its abstract)."""
    
        def __init__(self, title, abstract):
            self.client = Anthropic()
            self.title = title
            self.system = (
                f"You are a research assistant helping analyze this paper:\n\n"
                f"Title: {title}\n\nAbstract: {abstract}\n\n"
                f"Answer questions about this paper precisely. When you don't have enough "
                f"information from the abstract to answer, say so explicitly. Relate findings "
                f"to pain biology and ion channel research where relevant."
            )
            self.messages = []
    
        def ask(self, question):
            """Ask a question about the paper."""
            self.messages.append({"role": "user", "content": question})
        
            response = self.client.messages.create(
                model="claude-sonnet-4-6",
                max_tokens=1024,
                system=self.system,
                messages=self.messages
            )
        
            answer = response.content[0].text
            self.messages.append({"role": "assistant", "content": answer})
            return answer


    print("PaperQA class defined.")
    return (PaperQA,)


@app.cell
def _(PaperQA):
    # Load a paper
    paper = PaperQA(
        title="Targeted protein degradation of NaV1.7 for pain treatment",
        abstract="""Voltage-gated sodium channel NaV1.7 (encoded by SCN9A) is a genetically 
        validated pain target, yet selective small-molecule inhibitors have shown limited 
        clinical efficacy. Here we present a targeted protein degradation approach using 
        de novo designed protein binders conjugated to E3 ubiquitin ligase recruiters 
        (CRBN-based molecular glue degraders). Our lead degrader, DNB-Nav17-103, selectively 
        depletes NaV1.7 protein in DRG neurons with DC50 = 8.2 nM and achieves >90% 
        degradation within 6 hours. In a CFA-induced inflammatory pain model in mice, 
        intrathecal administration of DNB-Nav17-103 reversed mechanical and thermal 
        hypersensitivity for up to 72 hours without affecting motor function. Calcium imaging 
        of treated DRG neurons showed reduced excitability in TRPV1+ nociceptors with 
        preserved responses in TRPM8+ cold-sensing neurons. Whole-cell patch clamp confirmed 
        selective reduction of tetrodotoxin-sensitive sodium currents. These results 
        demonstrate that targeted degradation of NaV1.7 can achieve the analgesic efficacy 
        that has eluded traditional channel blockers."""
    )

    # Ask questions
    print("Q: What is the main therapeutic approach in this paper?")
    print(paper.ask("What is the main therapeutic approach?"))
    print()
    return (paper,)


@app.cell
def _(paper):
    print("Q: How selective is the degrader?")
    print(paper.ask("What evidence is there for selectivity of the degrader?"))
    print()
    return


@app.cell
def _(paper):
    print("Q: What follow-up experiments would you suggest?")
    print(paper.ask(
        "Based on this abstract, what follow-up experiments would you suggest "
        "to further validate the approach before moving to clinical development?"
    ))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Reading data from CSV files

    For the exercise below, let's create a sample CSV file and show how to load it. In practice, you'd use your own data files.
    """)
    return


@app.cell
def _(pd):
    # Create a sample CSV of compounds for the exercise
    sample_data = pd.DataFrame({
        "compound_name": [
            "A-803467", "PF-05089771", "Funapide (TV-45070)",
            "Vixotrigine (BIIB074)", "ICA-121431", "ProTx-II",
            "Ziconotide", "Retigabine", "XEN1101", "GDC-0276"
        ],
        "status": [
            "preclinical", "phase_2", "phase_2",
            "phase_2", "preclinical", "research_tool",
            "approved", "withdrawn", "phase_2", "phase_1"
        ]
    })

    # Save to CSV
    csv_path = "/Users/alex/ai-tutorial/08-claude-api/sample_compounds.csv"
    sample_data.to_csv(csv_path, index=False)

    print(f"Saved {len(sample_data)} compounds to {csv_path}")
    print()
    print(sample_data)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Compound mechanism classifier

    Build a mini pipeline that:

    1. Reads the CSV file of compound names we just created
    2. For each compound, asks Claude to classify its **mechanism of action** with structured fields:
       - `compound` — the name
       - `primary_target` — the molecular target (e.g., "NaV1.7")
       - `target_gene` — gene symbol
       - `mechanism` — blocker, opener, degrader, antibody, peptide toxin, etc.
       - `selectivity` — selective for which subtypes
       - `pain_indication` — what type of pain it was developed for
    3. Saves the enriched data to a new CSV file

    Use the `batch_process` function or write your own loop.
    """)
    return


@app.cell
def _(pd):
    # Your code here

    # Step 1: Read the CSV
    compounds = pd.read_csv("/Users/alex/ai-tutorial/08-claude-api/sample_compounds.csv")
    print(f"Loaded {len(compounds)} compounds")
    print(compounds)
    return (compounds,)


@app.cell
def _(client, compounds, parse_json_response):
    # Step 2: Define the classification function
    MOA_SYSTEM = 'You classify pain therapeutics by mechanism of action.\nReturn JSON only (no other text, no code fences):\n{\n    "compound": "compound name",\n    "primary_target": "molecular target",\n    "target_gene": "gene symbol",\n    "mechanism": "blocker|opener|degrader|antibody|peptide_toxin|modulator|other",\n    "selectivity": "which subtypes it\'s selective for",\n    "pain_indication": "type of pain condition"\n}'

    def classify_moa(compound_name):
        """Classify mechanism of action for a pain compound."""
        message = client.messages.create(model='claude-sonnet-4-6', max_tokens=256, system=MOA_SYSTEM, messages=[{'role': 'user', 'content': f'Classify: {compound_name}'}])
        return parse_json_response(message.content[0].text)
    moa_results = []
    for name in compounds['compound_name']:
        print(f'  Classifying {name}...', end=' ')
        try:
            _result = classify_moa(name)
            moa_results.append(_result)
            print(f"-> {_result['mechanism']} targeting {_result['primary_target']}")
        except Exception as e:
            print(f'FAILED: {e}')
            moa_results.append({'compound': name, 'primary_target': 'error', 'target_gene': 'error', 'mechanism': 'error', 'selectivity': 'error', 'pain_indication': 'error'})
    # Step 3: Process all compounds
    print(f'\nClassified {len(moa_results)} compounds.')
    return (moa_results,)


@app.cell
def _(compounds, moa_results, pd):
    # Step 4: Merge and save
    moa_df = pd.DataFrame(moa_results)

    # Merge with original data (keeping the status column)
    enriched = compounds.merge(
        moa_df, 
        left_on="compound_name", 
        right_on="compound", 
        how="left"
    ).drop(columns=["compound"])  # drop duplicate name column

    # Save enriched data
    output_path = "/Users/alex/ai-tutorial/08-claude-api/compounds_classified.csv"
    enriched.to_csv(output_path, index=False)

    print(f"Saved enriched data to {output_path}")
    print()
    enriched
    return (enriched,)


@app.cell
def _(enriched):
    # Quick analysis: what are the most common mechanisms?
    print("Mechanism of action breakdown:")
    print(enriched["mechanism"].value_counts())
    print()

    print("Targets:")
    print(enriched["primary_target"].value_counts())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Capstone: Sketch your own research tool

    Now it's your turn to think about what tool would be most useful in your actual research. Here are some ideas:

    **For protein binder design:**
    - Input a list of protein regions (loops, termini, domains) and have Claude evaluate each as a binder target — considering accessibility, conservation, functional importance
    - Process RoseTTAFold or AlphaFold output annotations to prioritize binding interfaces

    **For literature:**
    - Batch-process abstracts from a PubMed search and extract: target, model, technique, key finding
    - Compare findings across papers: does compound X work better in model A or model B?

    **For data analysis:**
    - Take DRG RNA-seq DE gene lists and get Claude to group them by pathway/function
    - Annotate calcium imaging traces: given response parameters, classify neuron subtypes

    **For experimental planning:**
    - Input a target + approach and get Claude to suggest controls, potential pitfalls, and alternative strategies

    Pick one idea and sketch it out below. You don't need to build the whole thing — just:
    1. Define the input (what data do you start with?)
    2. Write the system prompt (what do you tell Claude?)
    3. Define the output schema (what JSON fields do you want back?)
    4. Write the function that ties it together
    """)
    return


@app.cell
def _():
    # Sketch your research tool here
    #
    # Example skeleton:
    #
    # TOOL_SYSTEM = """You are a [specialized role].
    # Given [input type], return JSON:
    # {
    #     "field1": "...",
    #     "field2": "...",
    #     "field3": ["..."],
    # }
    # Respond ONLY with valid JSON."""
    #
    #
    # def my_research_tool(input_data):
    #     """Describe what this tool does."""
    #     message = client.messages.create(
    #         model="claude-sonnet-4-6",
    #         max_tokens=512,
    #         system=TOOL_SYSTEM,
    #         messages=[{"role": "user", "content": f"Process: {input_data}"}]
    #     )
    #     return parse_json_response(message.content[0].text)
    #
    #
    # # Test it
    # result = my_research_tool("your test input")
    # print(json.dumps(result, indent=2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - **Batch processing** — loop over items, call Claude for each, collect structured results
    - **Error handling** — `try/except` with retries and exponential backoff for rate limits
    - **Multi-turn conversations** — maintain message history for follow-up questions
    - **Claude + pandas** — annotate DataFrames with AI-generated fields, then filter and analyze
    - **CSV workflows** — read data, enrich with Claude, save enriched data
    - **Research tool patterns** — system prompt + JSON schema + processing function = custom tool

    ### The patterns you now have

    | Pattern | When to use |
    |---------|------------|
    | `ask_claude(prompt)` | One-off questions |
    | `parse_json_response(text)` | Any time you need structured output |
    | `batch_process(items, fn)` | Processing lists of things |
    | `ResearchChat` / `PaperQA` | Multi-turn exploration |
    | DataFrame + annotate function | Enriching experimental data |

    These building blocks compose into any research tool you need. In the next modules, you'll use them to build full data analysis workflows and see how Claude fits into the broader AI landscape.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Structured Outputs](02-structured-outputs.py) | [Module Index](../README.md) | [Next: Pandas Basics for Research Data \u2192](../10-data-skills/01-pandas-basics.py)
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
    - 2026-03-25: QA pass — removed duplicate markdown-in-code cells, fixed CSV paths (05-claude-api -> 08-claude-api), fixed undefined interpretation_prompt variable
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
    - 2026-03-25: QA pass — removed duplicate markdown-in-code cells, fixed CSV paths (05-claude-api → 08-claude-api), fixed undefined interpretation_prompt variable
    - 2026-03-25: QA pass — added "Why this matters" rationale section
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

