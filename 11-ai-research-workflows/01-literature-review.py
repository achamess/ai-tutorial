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
    # 01: AI-Assisted Literature Review

    ## The problem you already know

    You need to stay current on NaV1.7 inhibitors, novel PROTAC strategies, and DRG transcriptomics — but you're drowning in papers. Zotero captures them; now what?

    This notebook builds a **programmatic literature review pipeline**:
    1. Feed abstracts to Claude via the API
    2. Get structured extraction (not free-form summaries)
    3. Assemble a comparison table across papers
    4. Generate a synthesis paragraph grounded in the structured data

    By the end, you'll have a reusable pipeline you can point at any batch of papers.

    > **Prerequisites:** You should be comfortable with the Claude API basics from Module 05 and pandas from Module 06. We'll build on both.

    > **External APIs you could integrate:** [Semantic Scholar API](https://api.semanticscholar.org/) for programmatic paper search and citation data, and the [Zotero Web API](https://www.zotero.org/support/dev/web_api/v3/start) for pulling papers directly from your Zotero library. See also the [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) for examples of document processing with Claude.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    flowchart LR
        subgraph INPUT["Paper Sources"]
            Z1["Zotero<br>Export"]
            Z2["PubMed<br>Search"]
            Z3["Semantic<br>Scholar"]
        end

        subgraph EXTRACT["Structured Extraction"]
            E1["Claude API<br>(per paper)"]
            E2["JSON output:<br>target, methods,<br>key finding,<br>relevance score"]
        end

        subgraph ORGANIZE["Data Organization"]
            O1["pandas<br>DataFrame"]
            O2["Filter &<br>Sort"]
            O3["Comparison<br>Table"]
        end

        subgraph SYNTHESIZE["AI Synthesis"]
            S1["Send structured<br>data to Claude"]
            S2["Grant background<br>paragraph"]
            S3["Review section<br>draft"]
        end

        Z1 --> E1
        Z2 --> E1
        Z3 --> E1
        E1 --> E2
        E2 --> O1
        O1 --> O2
        O2 --> O3
        O3 --> S1
        S1 --> S2
        S1 --> S3

        style Z1 fill:#3498db,color:#fff
        style Z2 fill:#3498db,color:#fff
        style Z3 fill:#3498db,color:#fff
        style E1 fill:#8e44ad,color:#fff
        style E2 fill:#8e44ad,color:#fff
        style O1 fill:#f39c12,color:#fff
        style O2 fill:#f39c12,color:#fff
        style O3 fill:#f39c12,color:#fff
        style S1 fill:#2ecc71,color:#fff
        style S2 fill:#2ecc71,color:#fff
        style S3 fill:#2ecc71,color:#fff
    ```

    The pipeline above is what we build in this notebook -- from raw paper abstracts to structured data to synthesized narrative.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Database Basics for Research Data](../10-data-skills/04-databases-basics.py) | [Module Index](../README.md) | [Next: AI-Assisted Data Analysis Pipeline \u2192](02-data-analysis-pipeline.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - You track 13+ research topic clusters daily -- NaV1.7 inhibitors, PROTAC strategies, RFdiffusion methods, DRG transcriptomics, KCNQ modulators, and more. Manual literature review doesn't scale across all of these simultaneously.
    > - Programmatic extraction and synthesis lets you process dozens of papers in minutes instead of hours, with structured output you can query and compare. Instead of reading 20 abstracts to find which papers report NaV1.7 binding affinities, you extract that field automatically and sort by it.
    > - The structured extraction approach (JSON output, not free-form summaries) turns papers into data you can filter with pandas -- "show me all papers with Kd < 10 nM for sodium channel targets published after 2024."
    > - This pipeline also feeds directly into grant writing: the comparison tables and synthesis paragraphs it produces are first drafts of your background sections.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Setup
    """)
    return


@app.cell
def _():
    import anthropic
    import pandas as pd
    import json
    import os
    import textwrap
    from IPython.display import display, Markdown

    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY from environment

    MODEL = "claude-sonnet-4-6"
    print(f"Using model: {MODEL}")
    print("Ready.")
    return MODEL, Markdown, anthropic, client, display, json, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 1: Structured paper extraction

    The key insight: instead of asking Claude for a free-form summary, we ask for **structured JSON** with exactly the fields we want. This is the difference between a chatbot and a data pipeline.

    Recall from Module 03 (prompt engineering): structured output prompts work best when you specify the exact schema you want.

    > 🔑 **Key concept:** Structured extraction before synthesis. If you extract fields (target, methods, key finding, IC50) into a consistent schema first, your downstream synthesis is grounded in specific data rather than vague impressions. This is the difference between "several papers investigated NaV1.7" and "3 of 5 papers reported sub-10 nM IC50 values for NaV1.7."

    > 💡 **Tip:** Design your extraction schema around the questions you'll ask later. If you want to compare binding affinities across papers, make sure `quantitative_result` is a required field. If you want to sort by relevance, add a `relevance_score`. The schema IS the analysis plan.
    """)
    return


@app.cell
def _():
    # Mock paper metadata — not real citations. All authors, titles, and abstracts are fictional.
    # In practice, you'd pull these from Zotero, PubMed, or a CSV export.
    abstracts = [{'title': 'A selective NaV1.7 inhibitor reduces thermal hyperalgesia in a CFA model', 'authors': 'Author A, Author B, Author C, et al.', 'year': 2024, 'abstract': 'Voltage-gated sodium channel NaV1.7 is a genetically validated pain target. Loss-of-function mutations in SCN9A cause congenital insensitivity to pain, yet clinical NaV1.7 inhibitors have shown limited efficacy. Here we report compound XNV-442, a sulfonamide-based inhibitor with IC50 = 8 nM for NaV1.7 and >500-fold selectivity over NaV1.5 (cardiac). In rat DRG neurons, XNV-442 reduced action potential firing by 72% at 100 nM. In the CFA inflammatory pain model, oral dosing at 30 mg/kg reversed thermal hyperalgesia to baseline within 2 hours (p < 0.001 vs vehicle, n=12/group). No cardiac effects were observed at 10x the analgesic dose. These results suggest that high subtype selectivity may be key to translating NaV1.7 genetics into effective analgesics.'}, {'title': 'Targeted degradation of NaV1.8 via a PROTAC strategy in nociceptors', 'authors': 'Author D, Author E, Author F, et al.', 'year': 2025, 'abstract': 'NaV1.8, encoded by SCN10A, carries the majority of inward current during action potentials in nociceptive DRG neurons. Traditional small-molecule inhibitors face challenges with subtype selectivity. We developed PROTAC-Nav18, a heterobifunctional degrader linking a NaV1.8-binding warhead to a CRBN E3 ligase recruiter. In cultured DRG neurons, PROTAC-Nav18 achieved >90% degradation of NaV1.8 protein at 100 nM (DC50 = 15 nM) within 6 hours, with no effect on NaV1.7 or NaV1.5 levels. Calcium imaging showed a 65% reduction in capsaicin-evoked responses. In the SNI neuropathic pain model, daily dosing reduced mechanical allodynia by 58% at day 7 (p < 0.01). This demonstrates that targeted protein degradation can achieve selectivity unattainable by conventional channel blockers.'}, {'title': 'Single-cell RNA-seq reveals NaV1.7-expressing nociceptor subtypes in human DRG', 'authors': 'Author G, Author H, Author I, et al.', 'year': 2024, 'abstract': 'The cellular heterogeneity of human dorsal root ganglia remains poorly mapped. We performed single-cell RNA-seq on DRGs from 8 organ donors (4M/4F, ages 32-67). Unsupervised clustering identified 14 neuronal subtypes, including 4 nociceptor populations. SCN9A (NaV1.7) was broadly expressed across nociceptors but enriched 3.2-fold in a peptidergic CGRP+ subset co-expressing TRPV1 and SCN10A. SCN11A (NaV1.9) was restricted to a non-peptidergic IB4+ population. Differential expression analysis between NaV1.7-high and NaV1.7-low nociceptors identified 247 genes including NTRK1, CALCA, and P2RX3 as co-enriched. These data provide a cell-type-resolved atlas for rational targeting of sodium channels in pain circuits.'}, {'title': 'De novo protein binders for KCNQ2/3 channels modulate neuronal excitability', 'authors': 'Author J, Author K, Author L, et al.', 'year': 2025, 'abstract': 'KCNQ2/3 (Kv7.2/7.3) potassium channels generate the M-current that controls neuronal excitability. Dysfunction causes neonatal epilepsy and contributes to pain hypersensitivity. We used RFdiffusion to design de novo protein binders targeting the KCNQ2/3 heteromer interface. After screening 5,000 designs by AlphaFold2 confidence and Rosetta binding energy, 48 candidates were expressed and tested. The top binder, QB-12, showed Kd = 3.2 nM by SPR and enhanced M-current amplitude by 45% in DRG neurons via whole-cell patch clamp. In the formalin test, intrathecal QB-12 reduced Phase II pain behavior by 52% (p < 0.001). Cryo-EM at 3.1 A confirmed the designed binding mode. Computational protein design thus offers a route to ion channel modulators with programmable selectivity.'}, {'title': 'Inflammatory mediators remodel NaV expression in DRG neurons: a bulk RNA-seq time course', 'authors': 'Author M, Author N, Author O, et al.', 'year': 2024, 'abstract': 'Peripheral inflammation alters sodium channel expression in DRG neurons, but the temporal dynamics remain unclear. We performed bulk RNA-seq on mouse lumbar DRGs at 6h, 24h, 72h, and 7d after CFA injection (n=4/timepoint). SCN9A (NaV1.7) was upregulated 2.1-fold at 24h (padj < 0.001), peaking at 72h (3.4-fold). SCN10A (NaV1.8) showed delayed upregulation at 72h (1.8-fold). Unexpectedly, SCN11A (NaV1.9) was downregulated at all timepoints. Pathway analysis implicated NF-kB and JAK-STAT signaling. TNF-alpha treatment of cultured DRG neurons recapitulated the SCN9A upregulation (2.5-fold at 24h), which was blocked by NF-kB inhibitor BAY 11-7082. These findings map the transcriptional dynamics of sodium channel remodeling during inflammation and identify NF-kB as a driver of NaV1.7 upregulation.'}]
    print(f'Loaded {len(abstracts)} abstracts')
    for _i, a in enumerate(abstracts):
        print(f"  {_i + 1}. {a['title']} ({a['year']})")
    return (abstracts,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The extraction prompt

    We want Claude to return a JSON object with exactly these fields for each paper. This is the structured output technique from Module 03.
    """)
    return


@app.cell
def _():
    EXTRACTION_PROMPT = """\
    You are a pain biology research assistant. Given a paper's title, authors, year, 
    and abstract, extract structured information.

    Return ONLY valid JSON with these fields:
    {
      "title": "paper title",
      "authors": "author list",
      "year": 2024,
      "target": "primary molecular target (e.g., NaV1.7, NaV1.8, KCNQ2/3)",
      "approach": "experimental approach in 5-10 words",
      "key_finding": "most important result in one sentence",
      "methods": ["list", "of", "key", "techniques"],
      "model_system": "in vitro / in vivo model used",
      "quantitative_result": "the most important number (IC50, fold-change, etc.)",
      "relevance_to_binder_design": "one sentence on how this relates to de novo protein binder development for pain targets",
      "relevance_score": 8
    }

    For relevance_score, rate 1-10 how relevant this paper is to someone designing 
    de novo protein binders targeting ion channels (NaV1.7, NaV1.8, KCNQ2/3) for 
    pain therapeutics.

    Return ONLY the JSON object. No markdown formatting, no code fences, no commentary.
    """

    print("Extraction prompt ready.")
    print(f"Length: {len(EXTRACTION_PROMPT)} characters")
    return (EXTRACTION_PROMPT,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Extract one paper as a test

    Always test with a single item before looping.
    """)
    return


@app.cell
def _(EXTRACTION_PROMPT, MODEL, abstracts, client):
    # Test with the first abstract
    test_paper = abstracts[0]
    user_message = f"Title: {test_paper['title']}\nAuthors: {test_paper['authors']}\nYear: {test_paper['year']}\n\nAbstract:\n{test_paper['abstract']}"
    _response = client.messages.create(model=MODEL, max_tokens=1024, system=EXTRACTION_PROMPT, messages=[{'role': 'user', 'content': user_message}])
    raw_text = _response.content[0].text
    print('Raw response:')
    print(raw_text)
    return (raw_text,)


@app.cell
def _(json, raw_text):
    # Parse the JSON
    _extracted = json.loads(raw_text)
    # Pretty-print it
    print(json.dumps(_extracted, indent=2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 2: Processing multiple papers

    Now let's build the function and loop through all 5 abstracts. This is where programming beats chatting — you define the process once and run it on any number of papers.

    > 🤔 **Decision point: Manual vs AI-assisted literature review**
    >
    > | Factor | Manual review | AI-assisted pipeline |
    > |--------|--------------|---------------------|
    > | **Best for** | Small batches (< 10 papers), qualitative judgment | Large batches (10-200+ papers), structured comparison |
    > | **Strength** | Deep reading, nuance, catching subtle methodological issues | Consistency, speed, structured output for downstream analysis |
    > | **Weakness** | Doesn't scale, inconsistent extraction across papers | Misses nuance, may hallucinate fields, needs verification |
    > | **Time per paper** | 15-30 min | ~10 seconds + verification |
    > | **When to use** | Key papers in your subfield that need deep understanding | Scanning a broad literature for comparison tables, grant background |
    >
    > **The hybrid approach works best:** Use AI to extract structured data from many papers, then manually deep-read the 5-10 most relevant ones. The AI step is triage, not replacement.
    """)
    return


@app.cell
def _(EXTRACTION_PROMPT, MODEL, anthropic, json):
    def extract_paper_info(paper: dict, client: anthropic.Anthropic, model: str=MODEL) -> dict:
        """Send a paper abstract to Claude and get structured extraction."""
        user_message = f"Title: {paper['title']}\nAuthors: {paper['authors']}\nYear: {paper['year']}\n\nAbstract:\n{paper['abstract']}"
        _response = client.messages.create(model=model, max_tokens=1024, system=EXTRACTION_PROMPT, messages=[{'role': 'user', 'content': user_message}])
        raw_text = _response.content[0].text
        cleaned = raw_text.strip()
        if cleaned.startswith('```'):
            cleaned = cleaned.split('\n', 1)[1]
            cleaned = cleaned.rsplit('```', 1)[0]
        return json.loads(cleaned)
    print('Function defined.')  # Strip markdown code fences if Claude adds them despite instructions  # remove first line  # remove last fence
    return (extract_paper_info,)


@app.cell
def _(abstracts, client, extract_paper_info):
    # Process all abstracts
    results = []
    for _i, paper in enumerate(abstracts):
        print(f"Processing {_i + 1}/{len(abstracts)}: {paper['title'][:60]}...")
        _extracted = extract_paper_info(paper, client)
        results.append(_extracted)
    print(f'\nDone! Extracted info from {len(results)} papers.')
    return (results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 3: Building a comparison table

    Now the payoff: structured data goes straight into a pandas DataFrame. This is exactly what you'd want for comparing across a set of NaV1.7 studies or evaluating different therapeutic approaches.
    """)
    return


@app.cell
def _(display, pd, results):
    # Build a DataFrame from the extracted data
    df = pd.DataFrame(results)

    # Select the most useful columns for a comparison view
    comparison_cols = ["title", "year", "target", "approach", "key_finding", 
                       "quantitative_result", "relevance_score"]

    # Some columns might not exist if extraction varied — use what we have
    available_cols = [c for c in comparison_cols if c in df.columns]
    comparison = df[available_cols].copy()

    # Sort by relevance score
    comparison = comparison.sort_values("relevance_score", ascending=False)

    display(comparison)
    return (df,)


@app.cell
def _(df, display):
    # A more detailed view: methods and model systems
    methods_cols = ['title', 'target', 'methods', 'model_system']
    _available = [c for c in methods_cols if c in df.columns]
    methods_df = df[_available].copy()
    if 'methods' in methods_df.columns:
        methods_df['methods'] = methods_df['methods'].apply(lambda x: ', '.join(x) if isinstance(x, list) else str(x))
    # Convert methods lists to readable strings
    display(methods_df)
    return


@app.cell
def _(df):
    # Save the full extraction to CSV for your records
    output_df = df.copy()
    if "methods" in output_df.columns:
        output_df["methods"] = output_df["methods"].apply(
            lambda x: "; ".join(x) if isinstance(x, list) else str(x)
        )

    output_df.to_csv("literature_extraction.csv", index=False)
    print("Saved to literature_extraction.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 4: Generating a synthesis paragraph

    A comparison table is useful for scanning. But for a grant intro or a review section, you need **synthesis** — connecting the papers into a narrative.

    The trick: we send the structured data (not the raw abstracts) to Claude. This keeps the synthesis grounded in what we actually extracted.
    """)
    return


@app.cell
def _(results):
    # Build a structured summary to send to Claude for synthesis
    papers_summary = ''
    for _i, _row in enumerate(results):
        papers_summary += f"Paper {_i + 1}:\n  Title: {_row.get('title', 'N/A')}\n  Year: {_row.get('year', 'N/A')}\n  Target: {_row.get('target', 'N/A')}\n  Approach: {_row.get('approach', 'N/A')}\n  Key finding: {_row.get('key_finding', 'N/A')}\n  Quantitative result: {_row.get('quantitative_result', 'N/A')}\n  Relevance to binder design: {_row.get('relevance_to_binder_design', 'N/A')}\n\n"
    print(papers_summary)
    return (papers_summary,)


@app.cell
def _(MODEL, Markdown, client, display, papers_summary):
    synthesis_prompt = f'You are writing a paragraph for the background section of an R01 grant application \nfocused on developing de novo protein binders for ion channel targets (NaV1.7, \nNaV1.8, KCNQ2/3) as novel pain therapeutics.\n\nBased on these recent papers, write a concise synthesis paragraph (150-200 words) \nthat:\n1. Establishes the rationale for targeting these channels\n2. Highlights the limitations of current approaches\n3. Points to de novo protein binders and targeted degradation as promising alternatives\n4. Cites each paper by first author and year in parentheses\n\nUse a formal scientific writing style appropriate for an NIH grant.\n\nPapers:\n{papers_summary}'
    _response = client.messages.create(model=MODEL, max_tokens=1024, messages=[{'role': 'user', 'content': synthesis_prompt}])
    synthesis = _response.content[0].text
    display(Markdown(synthesis))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Look at that — a draft paragraph that cites all your papers and makes the argument for your approach. This isn't a final version (you'll revise it in Notebook 03 of this module), but it's a solid starting point that would have taken 30 minutes to draft from scratch.

    > **Key pattern:** structured extraction first, then synthesis. If you just dump abstracts into Claude and ask for a summary, you lose control over what gets emphasized. The extraction step forces Claude to identify the information you care about.

    > ⚠️ **Warning:** AI-extracted data needs verification. Claude may misinterpret quantitative results (confusing IC50 with Kd), invert directionalities (reporting upregulation as downregulation), or fill in plausible-sounding but incorrect values when the abstract is ambiguous. **Always spot-check at least 20% of extracted fields against the source abstracts** — especially numerical values, statistical claims, and model systems.

    <details><summary>Click to expand: Common extraction errors to watch for</summary>

    **Numerical confusion:**
    - IC50 vs Ki vs Kd — Claude may conflate these
    - Fold-change direction (2-fold up vs 2-fold down)
    - Units (nM vs uM is a 1000x difference)

    **Biological misattribution:**
    - Assigning findings to the wrong model system
    - Confusing in vitro and in vivo results
    - Misidentifying the molecular target (NaV1.7 vs NaV1.8)

    **Mitigation:** Include explicit field definitions in your extraction prompt ("IC50: the concentration that inhibits 50% of activity, in nM") and add a `confidence` field so Claude can flag uncertain extractions.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 5: Working with Zotero exports

    In real life, your papers live in Zotero. Here's how to bridge Zotero into this pipeline.

    Zotero can export your library (or a collection) as a CSV file via **File > Export Library > CSV**. Let's simulate that and show how to read it. For programmatic access, the [Zotero Web API v3](https://www.zotero.org/support/dev/web_api/v3/start) lets you pull library data directly from Python (see also the [`pyzotero`](https://github.com/urschrei/pyzotero) package).

    > **Think Python connection:** [Chapter 14 (Files)](https://allendowney.github.io/ThinkPython/chap14.html) covers reading and writing files, including CSV handling -- the same skills used to work with Zotero exports.
    """)
    return


@app.cell
def _(display, pd):
    # Simulate a Zotero CSV export (all data below is fictional mock data — not real papers or authors)
    # In real use, you'd do: File > Export Library > CSV in Zotero
    # The CSV has these standard columns (among others)

    zotero_data = {
        "Key": ["ABC123", "DEF456", "GHI789"],
        "Title": [
            "NaV1.7 as a therapeutic target: from genetics to drug design",
            "PROTAC approaches for membrane protein degradation",
            "Computational design of protein binders for ion channels"
        ],
        "Author": [
            "Author P; Author Q; Author R",
            "Author S; Author T",
            "Author U; Author V; Author W"
        ],
        "Publication Year": [2024, 2025, 2025],
        "Publication Title": ["Mock Review Journal", "Mock Chemistry Journal", "Mock Science Journal"],
        "DOI": ["10.xxxx/mock-doi-005", "10.xxxx/mock-doi-006", "10.xxxx/mock-doi-007"],
        "Abstract Note": [
            "NaV1.7 encoded by SCN9A is a validated pain target. This review covers genetic evidence, structural biology, and current inhibitor development challenges.",
            "Targeted protein degradation via PROTACs has been limited to soluble proteins. Here we extend the approach to transmembrane targets using novel E3 ligase recruiters.",
            "We demonstrate computational design of high-affinity protein binders for voltage-gated ion channels using RFdiffusion, achieving sub-nanomolar Kd values."
        ],
        "Manual Tags": ["pain; NaV1.7; review", "PROTAC; degradation; membrane", "protein design; ion channel; computational"]
    }

    zotero_df = pd.DataFrame(zotero_data)
    zotero_df.to_csv("mock_zotero_export.csv", index=False)
    print("Saved mock_zotero_export.csv")
    display(zotero_df)
    return


@app.cell
def _(pd):
    # Reading a Zotero CSV export — this is what you'd do with your real export
    zotero = pd.read_csv('mock_zotero_export.csv')
    print(f'Loaded {len(zotero)} papers from Zotero export')
    print(f'\nColumns available: {list(zotero.columns)}')
    print(f'\nPapers:')
    for _, _row in zotero.iterrows():
        print(f"  - {_row['Title']} ({_row['Publication Year']})")
    return (zotero,)


@app.cell
def _(pd, zotero):
    # Convert Zotero format to our pipeline's expected format
    def zotero_to_pipeline_format(zotero_df: pd.DataFrame) -> list[dict]:
        """Convert a Zotero CSV DataFrame into the format our extraction pipeline expects."""
        papers = []
        for _, _row in zotero_df.iterrows():
            abstract = _row.get('Abstract Note', '')
            if pd.isna(abstract) or not abstract.strip():
                continue  # skip papers without abstracts
            papers.append({'title': _row['Title'], 'authors': _row['Author'].replace(';', ',') if pd.notna(_row['Author']) else 'Unknown', 'year': int(_row['Publication Year']) if pd.notna(_row['Publication Year']) else 0, 'abstract': abstract})
        return papers
    pipeline_papers = zotero_to_pipeline_format(zotero)
    print(f'Converted {len(pipeline_papers)} papers for the extraction pipeline')
    for p in pipeline_papers:
        print(f"  - {p['title'][:60]}...")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now you can feed `pipeline_papers` into the same `extract_paper_info()` function we built above. The whole flow:

    ```
    Zotero collection → Export CSV → Read with pandas → Convert format →
    Extract with Claude API → Build comparison table → Generate synthesis
    ```

    That's a complete literature review pipeline.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Build your own mini-pipeline

    Put it all together. Using the 5 abstracts defined at the top of this notebook:

    1. Process all 5 through `extract_paper_info()`
    2. Build a DataFrame with columns: title, target, approach, key_finding, relevance_score
    3. Filter to only papers with relevance_score >= 7
    4. Generate a synthesis paragraph focused specifically on **targeted protein degradation** approaches

    Some of this code already exists above — the exercise is in assembling the pieces into a single, clean workflow.
    """)
    return


@app.cell
def _(display, pd, results):
    # Step 1: Process all abstracts (we already did this — reuse the results)
    # If you want to re-run, uncomment these lines:
    # results = []
    # for paper in abstracts:
    #     extracted = extract_paper_info(paper, client)
    #     results.append(extracted)
    exercise_df = pd.DataFrame(results)
    # Step 2: Build a focused DataFrame
    focus_cols = ['title', 'target', 'approach', 'key_finding', 'relevance_score']
    _available = [c for c in focus_cols if c in exercise_df.columns]
    exercise_df = exercise_df[_available]
    print('All papers:')
    display(exercise_df)
    if 'relevance_score' in exercise_df.columns:
        high_relevance = exercise_df[exercise_df['relevance_score'] >= 7].copy()
        print(f'\nHigh-relevance papers (score >= 7): {len(high_relevance)}')
    # Step 3: Filter by relevance
        display(high_relevance)
    return


@app.cell
def _(MODEL, Markdown, client, display, results):
    # Step 4: Generate a synthesis focused on targeted degradation
    filtered_results = [r for r in results if r.get('relevance_score', 0) >= 7]
    # Build the summary from high-relevance papers
    summary_text = ''
    for _i, _row in enumerate(filtered_results):
        summary_text += f"Paper {_i + 1}:\n  Title: {_row.get('title', 'N/A')}\n  Target: {_row.get('target', 'N/A')}\n  Approach: {_row.get('approach', 'N/A')}\n  Key finding: {_row.get('key_finding', 'N/A')}\n  Quantitative result: {_row.get('quantitative_result', 'N/A')}\n\n"
    degradation_prompt = f'Write a 150-word synthesis paragraph for a grant background section about \ntargeted protein degradation (PROTACs) as a strategy for pain therapeutics. \nFocus on how this approach overcomes the selectivity challenges faced by \ntraditional small-molecule ion channel inhibitors.\n\nCite each paper by first author and year.\n\nPapers:\n{summary_text}'
    _response = client.messages.create(model=MODEL, max_tokens=1024, messages=[{'role': 'user', 'content': degradation_prompt}])
    display(Markdown('### Synthesis: Targeted Degradation for Pain\n\n' + _response.content[0].text))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **APIs for literature search:**
    - [Semantic Scholar API](https://api.semanticscholar.org/) -- free API for searching papers, retrieving citations, and getting paper metadata. The `/paper/search` endpoint is particularly useful for programmatic literature discovery. Rate limit: 100 requests/5 minutes without an API key.
    - [Zotero Web API v3](https://www.zotero.org/support/dev/web_api/v3/start) -- access your Zotero library programmatically. The [`pyzotero`](https://github.com/urschrei/pyzotero) Python package wraps this API.
    - [PubMed E-utilities](https://www.ncbi.nlm.nih.gov/books/NBK25501/) -- NCBI's programmatic interface to PubMed; useful for searching biomedical literature by MeSH terms.

    **Claude and document processing:**
    - [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) -- official examples of using the Claude API for document processing, structured extraction, and multi-step workflows
    - [Anthropic API Documentation](https://docs.anthropic.com/) -- reference for all API features including structured output with tool use

    **Think Python:**
    - [Chapter 14: Files](https://allendowney.github.io/ThinkPython/chap14.html) -- reading and writing files (CSV, text), which underpins the Zotero export workflow in Part 5

    **Books and methodology:**
    - *Writing Science* by Joshua Schimel -- excellent guide to structuring scientific narratives, from individual paragraphs to full papers. The "OCAR" framework (Opening, Challenge, Action, Resolution) applies directly to grant writing and literature synthesis.
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
    - 2026-03-25: QA pass — removed duplicate Edit Log section
    - 2026-03-25: Added callout boxes — decision point (manual vs AI-assisted review), warning (AI-extracted data verification), tip (schema design), key concept (structured extraction), collapsible deep-dive (common extraction errors)
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Database Basics for Research Data](../10-data-skills/04-databases-basics.py) | [Module Index](../README.md) | [Next: AI-Assisted Data Analysis Pipeline \u2192](02-data-analysis-pipeline.py)
    """)
    return


if __name__ == "__main__":
    app.run()

