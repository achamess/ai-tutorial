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
    # 02: Structured Outputs

    In the last notebook, Claude returned **free text** -- paragraphs you could read but couldn't easily process with code. In this notebook, you'll learn to get **structured data** back from Claude -- specifically JSON -- which you can parse, filter, store, and feed into downstream analysis.

    This is where the API becomes a real research tool: Claude reads unstructured text (papers, abstracts, notes) and produces structured data your code can work with.

    **Key references:** [Anthropic docs: Structured Outputs](https://docs.anthropic.com/en/docs/build-with-claude/structured-output) | [Python `json` module](https://docs.python.org/3/library/json.html) | [Think Python Ch 11: Dictionaries](https://allendowney.github.io/ThinkPython/chap11.html)

    **Local reference:** [resources/references/anthropic-tool-use-guide.md](../resources/references/anthropic-tool-use-guide.md)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Your First API Call](01-your-first-api-call.py) | [Module Index](../README.md) | [Next: Building Research Tools \u2192](03-building-research-tools.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Free text from Claude is useful for reading but useless for computation. Structured JSON output is what turns Claude into a data pipeline component -- you can filter, sort, and analyze the results with pandas.
    > - This is the pattern behind every research automation in this tutorial: extract structured fields from unstructured text (papers, notes, experimental descriptions) and build queryable datasets.
    > - For your binder program, structured extraction means you can process a batch of papers and instantly answer "which papers report NaV1.7 binding affinities below 10 nM?" without reading each one.
    > - The JSON parsing and error handling patterns here are essential for building robust pipelines that don't crash when one input produces unexpected output.
    """)
    return


@app.cell
def _():
    from anthropic import Anthropic
    import json

    client = Anthropic()  # reads ANTHROPIC_API_KEY from environment

    print("Ready.")
    return client, json


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Quick review: JSON and Python dictionaries

    JSON (JavaScript Object Notation) is the standard format for exchanging structured data. If you know Python dictionaries, you already know JSON — they look almost identical.

    ```json
    {
        "gene": "SCN9A",
        "protein": "NaV1.7",
        "role": "nociceptor excitability",
        "pain_disorders": ["erythromelalgia", "PEPD", "CIP"]
    }
    ```

    In Python:
    - `json.loads(text)` converts a JSON string into a Python dictionary
    - `json.dumps(data, indent=2)` converts a dictionary into a formatted JSON string

    > **Think Python reference:** Dictionaries (Chapter 11) and string methods. JSON is just a text representation of a dictionary.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Getting JSON from Claude

    The trick is simple: **tell Claude to respond in JSON** using the system prompt. Be specific about the exact fields you want.
    """)
    return


@app.cell
def _(client):
    _message = client.messages.create(model='claude-sonnet-4-6', max_tokens=1024, system='You are a pain biology expert. Respond ONLY with valid JSON, no other text. Do not wrap the JSON in markdown code fences.', messages=[{'role': 'user', 'content': 'Provide information about SCN9A in this exact JSON format:\n{"gene": "...", "protein": "...", "chromosome": "...", "expression_sites": ["..."], "pain_disorders": ["..."], "therapeutic_relevance": "..."}'}])
    raw_text = _message.content[0].text
    print('Raw response:')
    print(raw_text)
    return (raw_text,)


@app.cell
def _(json, raw_text):
    # Parse the JSON string into a Python dictionary
    _data = json.loads(raw_text)
    print(f"Gene: {_data['gene']}")
    # Now you can access fields programmatically
    print(f"Protein: {_data['protein']}")
    print(f"Expression sites: {', '.join(_data['expression_sites'])}")
    print(f"Number of associated pain disorders: {len(_data['pain_disorders'])}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's the core pattern: **prompt for JSON** -> **get text back** -> **parse with `json.loads()`** -> **use as a Python dictionary**.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** Structured output turns Claude from a chatbot into a data pipeline component. Free text is useful for reading but useless for computation. When Claude returns JSON with defined fields, you can filter, sort, aggregate, and feed the results into pandas -- turning unstructured knowledge into queryable data. This is the foundation of every research automation tool you'll build.

    > **Decision point: JSON vs markdown vs plain text output format**
    >
    > | Format | Pros | Cons | Use when |
    > |--------|------|------|----------|
    > | **JSON** | Machine-parseable, feeds into pandas/code, consistent structure | Requires parsing logic, error handling for malformed responses | Building pipelines, batch processing, any time the output feeds into more code |
    > | **Markdown** | Human-readable, supports formatting (tables, headers, bold) | Hard to parse programmatically, inconsistent structure | Reports, summaries, anything a human will read directly |
    > | **Plain text** | Simplest, no parsing needed | No structure, hard to extract specific fields | Quick one-off questions, brainstorming, when you just need a sentence or two |
    >
    > **Rule of thumb:** If the output will be processed by code, use JSON. If the output will be read by a human, use markdown. If you're just asking a quick question, plain text is fine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Structured Output Pipeline

    ```mermaid
    graph LR
        A["Unstructured Input<br>(text, abstract,<br>notes)"] --> B["System Prompt<br>Defines JSON schema<br>+ extraction rules"]
        B --> C["Claude API<br>Extracts structured<br>data from text"]
        C --> D["Raw JSON String<br>'{\"gene\": \"SCN9A\", ...}'"]
        D --> E["json.loads()<br>Parse to Python"]
        E --> F["Python Dict<br>{'gene': 'SCN9A', ...}"]
        F --> G["pd.DataFrame()<br>Tabular analysis"]

        style A fill:#E24A33,color:#fff
        style B fill:#FDB863,color:#000
        style C fill:#4878CF,color:#fff
        style D fill:#eee,color:#000
        style E fill:#eee,color:#000
        style F fill:#55A868,color:#fff
        style G fill:#55A868,color:#fff
    ```

    This is the core pattern for turning unstructured text into structured data. The system prompt is your schema definition -- it tells Claude exactly what fields to extract and what format to use. The parsed dictionary can then be combined with other results into a pandas DataFrame for analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Robust JSON parsing

    Sometimes Claude wraps JSON in markdown code fences (` ```json ... ``` `) even when you ask it not to. Let's write a helper that handles this reliably.
    """)
    return


@app.cell
def _(json):
    def parse_json_response(text):
        """Parse JSON from Claude's response, handling markdown code fences."""
        # Strip markdown code fences if present
        cleaned = text.strip()
        if cleaned.startswith("```"):
            # Remove first line (```json) and last line (```)
            lines = cleaned.split("\n")
            cleaned = "\n".join(lines[1:-1])
    
        return json.loads(cleaned)


    # Test with a response that has code fences
    test_with_fences = '```json\n{"gene": "TRPV1", "role": "heat sensing"}\n```'
    test_without = '{"gene": "TRPV1", "role": "heat sensing"}'

    print(parse_json_response(test_with_fences))
    print(parse_json_response(test_without))
    return (parse_json_response,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## System prompts for structured output

    The system prompt is where you define the output schema. Here are patterns that work well:

    ### Pattern 1: Give an example in the system prompt
    """)
    return


@app.cell
def _(client, json, parse_json_response):
    EXTRACTION_SYSTEM = 'You are a research data extraction assistant. \nGiven information about an ion channel, extract structured data.\n\nRespond ONLY with valid JSON in this exact format (no other text, no code fences):\n{\n    "channel_name": "common name (e.g., NaV1.7)",\n    "gene": "gene symbol",\n    "channel_type": "sodium|potassium|calcium|chloride|TRP|other",\n    "primary_expression": ["list of tissues/cell types"],\n    "pain_relevant": true or false,\n    "mechanism_in_pain": "brief description or null if not pain-relevant",\n    "druggable": true or false\n}'
    _message = client.messages.create(model='claude-sonnet-4-6', max_tokens=512, system=EXTRACTION_SYSTEM, messages=[{'role': 'user', 'content': 'Tell me about KCNQ2 (Kv7.2)'}])
    channel_data = parse_json_response(_message.content[0].text)
    print(json.dumps(channel_data, indent=2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Pattern 2: Use prefilling to guarantee JSON

    A powerful technique: put the opening `{` as an **assistant message**, so Claude is forced to continue the JSON object.
    """)
    return


@app.cell
def _(client, json):
    _message = client.messages.create(model='claude-sonnet-4-6', max_tokens=512, system='Extract ion channel information as JSON with fields: channel_name, gene, channel_type, pain_relevant (bool), key_function.', messages=[{'role': 'user', 'content': 'Extract info about TRPV1.'}, {'role': 'assistant', 'content': '{'}])
    raw = '{' + _message.content[0].text
    _data = json.loads(raw)
    # Since we prefilled with "{", we need to add it back
    print(json.dumps(_data, indent=2))  # prefill forces JSON output
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The prefilling technique is useful when you absolutely need clean JSON with no preamble. For most cases, a clear system prompt is enough.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Building a pipeline: text in, structured data out

    Now let's combine everything into a real function. Imagine you have a DRG RNA-seq experiment and you want to quickly annotate a list of differentially expressed genes.
    """)
    return


@app.cell
def _(client, json, parse_json_response):
    def annotate_gene(gene_name):
        """Use Claude to annotate a gene with pain biology context."""
        system = 'You are a pain biology annotation tool. Given a gene name, return JSON with:\n{\n    "gene": "gene symbol",\n    "protein": "protein name",\n    "category": "ion_channel|receptor|kinase|transcription_factor|neuropeptide|cytokine|other",\n    "pain_relevant": true/false,\n    "pain_role": "brief description or null",\n    "expression_in_drg": "high|moderate|low|absent|unknown"\n}\nRespond ONLY with valid JSON, no other text, no code fences.'
        _message = client.messages.create(model='claude-sonnet-4-6', max_tokens=256, system=system, messages=[{'role': 'user', 'content': f'Annotate: {gene_name}'}])
        return parse_json_response(_message.content[0].text)
    _result = annotate_gene('CALCA')
    # Test with a single gene
    print(json.dumps(_result, indent=2))
    return (annotate_gene,)


@app.cell
def _(annotate_gene):
    # Now annotate several genes from a hypothetical DRG RNA-seq DE list
    de_genes = ["SCN9A", "TRPV1", "CALCA", "IL6", "NGF", "NTRK1"]

    annotations = []
    for gene in de_genes:
        print(f"Annotating {gene}...", end=" ")
        ann = annotate_gene(gene)
        annotations.append(ann)
        print(f"-> {ann['category']}, pain_relevant={ann['pain_relevant']}")

    print(f"\nAnnotated {len(annotations)} genes.")
    return (annotations,)


@app.cell
def _(annotations):
    # Filter: which of these are pain-relevant ion channels or receptors?
    pain_hits = [
        a for a in annotations 
        if a["pain_relevant"] and a["category"] in ("ion_channel", "receptor")
    ]

    print("Pain-relevant ion channels/receptors in DE gene list:")
    for hit in pain_hits:
        print(f"  {hit['gene']} ({hit['protein']}) — {hit['pain_role']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is the basic pipeline: **list of inputs** -> **Claude annotates each** -> **filter/analyze the structured results**. You'll build more sophisticated versions of this in the next notebook.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Warning:** JSON parsing can fail silently if you don't validate the structure. Claude might return valid JSON that's missing a field you expected, or a field might have the wrong type (string instead of boolean). Always check that critical fields exist before using them: `if 'pain_relevant' in result and isinstance(result['pain_relevant'], bool)`. For batch processing, the `safe_annotate_gene` pattern above with `try/except` is essential -- one malformed response shouldn't crash a 500-item batch.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Handling parsing errors gracefully

    Sometimes Claude's JSON isn't perfect. Always wrap parsing in a try/except so one bad response doesn't crash your whole pipeline.
    """)
    return


@app.cell
def _(annotate_gene, json):
    def safe_annotate_gene(gene_name):
        """Annotate a gene, returning None if parsing fails."""
        try:
            return annotate_gene(gene_name)
        except json.JSONDecodeError as e:
            print(f'  WARNING: Failed to parse JSON for {gene_name}: {e}')
            return None
        except Exception as e:
            print(f'  WARNING: API error for {gene_name}: {e}')
            return None
    _result = safe_annotate_gene('SCN10A')
    if _result:
    # This version won't crash if one gene fails
        print(json.dumps(_result, indent=2))
    else:
        print('Failed — would skip this gene and continue.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Putting structured data into a pandas DataFrame

    Since you'll often want to analyze results in a table, here's how to go from a list of JSON responses to a DataFrame.
    """)
    return


@app.cell
def _(annotations):
    import pandas as pd

    # We already have the annotations list from above
    df = pd.DataFrame(annotations)
    df
    return df, pd


@app.cell
def _(df):
    # Now you can use standard pandas operations
    print("Pain-relevant genes:")
    print(df[df["pain_relevant"] == True][["gene", "protein", "category", "pain_role"]])

    print(f"\nCategory counts:")
    print(df["category"].value_counts())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Paper abstract extractor

    Build a function called `extract_paper_info` that takes a paper **title** and **abstract** and returns a dictionary with these fields:

    - `target` — the molecular target studied (gene or protein name)
    - `mechanism` — the biological mechanism investigated
    - `model_organism` — the species or model system used
    - `pain_type` — type of pain studied (inflammatory, neuropathic, acute, etc.)
    - `key_finding` — one-sentence summary of the main result
    - `techniques` — list of experimental techniques used

    Test it with the example abstracts provided below.
    """)
    return


@app.cell
def _(client, parse_json_response):
    # Your code here
    def extract_paper_info(title, abstract):
        """Extract structured information from a paper title and abstract."""
        system = 'You are a pain biology literature extraction tool. Given a paper title and\nabstract, extract structured data. Respond ONLY with valid JSON (no other text, no code fences):\n{\n    "target": "molecular target (gene or protein)",\n    "mechanism": "biological mechanism investigated",\n    "model_organism": "species or model system",\n    "pain_type": "inflammatory|neuropathic|acute|cancer|visceral|other",\n    "key_finding": "one-sentence summary of main result",\n    "techniques": ["list", "of", "techniques"]\n}\nIf a field cannot be determined from the abstract, use null.'
        _message = client.messages.create(model='claude-sonnet-4-6', max_tokens=512, system=system, messages=[{'role': 'user', 'content': f'Title: {title}\n\nAbstract: {abstract}'}])
        return parse_json_response(_message.content[0].text)

    return (extract_paper_info,)


@app.cell
def _(extract_paper_info, json):
    # Test abstract 1
    title1 = "NaV1.7 gain-of-function mutations in idiopathic small fiber neuropathy"
    abstract1 = """Small fiber neuropathy (SFN) often remains idiopathic despite extensive 
    evaluation. We hypothesized that gain-of-function mutations in sodium channel NaV1.7 
    might be present in patients with idiopathic SFN. We sequenced SCN9A in 28 patients 
    with biopsy-confirmed idiopathic SFN and identified mutations in 8 patients (28.6%). 
    Functional analysis using voltage-clamp recordings in DRG neurons transfected with 
    mutant channels showed gain-of-function changes including hyperpolarized activation 
    and enhanced ramp currents. These mutations rendered DRG neurons hyperexcitable as 
    demonstrated by current-clamp recordings showing reduced current threshold and 
    increased firing frequency. Our results suggest that gain-of-function mutations in 
    NaV1.7 are a common cause of SFN and may provide targets for pain treatment."""

    result1 = extract_paper_info(title1, abstract1)
    print(json.dumps(result1, indent=2))
    return (result1,)


@app.cell
def _(extract_paper_info, json):
    # Test abstract 2
    title2 = "CGRP receptor antagonism in migraine treatment"
    abstract2 = """Calcitonin gene-related peptide (CGRP) plays a critical role in migraine 
    pathophysiology. We conducted a randomized, double-blind, placebo-controlled trial of 
    a monoclonal antibody targeting the CGRP receptor in 955 patients with episodic migraine. 
    Patients receiving the active treatment showed a mean reduction of 4.2 migraine days per 
    month compared to 2.1 for placebo (P<0.001). Adverse events were similar between groups. 
    Calcium imaging of trigeminal neurons in a mouse model confirmed reduced neuronal 
    activation following CGRP receptor blockade."""

    result2 = extract_paper_info(title2, abstract2)
    print(json.dumps(result2, indent=2))
    return (result2,)


@app.cell
def _(pd, result1, result2):
    # Combine results into a DataFrame for comparison
    papers_df = pd.DataFrame([result1, result2])
    papers_df
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Try it with your own abstracts

    Copy-paste a real abstract from a paper relevant to your work and run it through `extract_paper_info`. How well does it capture the key information?
    """)
    return


@app.cell
def _():
    # Paste your own abstract here and test
    # my_title = "..."
    # my_abstract = "..."
    # result = extract_paper_info(my_title, my_abstract)
    # print(json.dumps(result, indent=2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - **JSON from Claude** — use system prompts to request specific JSON schemas
    - **Parsing** — `json.loads()` converts text to Python dictionaries, with `parse_json_response()` handling markdown fences
    - **Prefilling** — put `{` as an assistant message to force clean JSON
    - **Pipelines** — input -> Claude -> structured data -> analysis
    - **Error handling** — `try/except` around parsing so one failure doesn't crash a batch
    - **DataFrames** — `pd.DataFrame(list_of_dicts)` for instant tabular analysis

    Next up: **building research tools** — batch processing, multi-turn conversations, and combining Claude with pandas for real data workflows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Your First API Call](01-your-first-api-call.py) | [Module Index](../README.md) | [Next: Building Research Tools \u2192](03-building-research-tools.py)
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
    - 2026-03-25: QA pass — removed duplicate "Quick review" section, added missing import cell (json, anthropic)
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
    - 2026-03-25: QA pass — removed duplicate "Quick review" section, added missing import cell (json, anthropic)
    - 2026-03-25: QA pass — added "Why this matters" rationale section
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

