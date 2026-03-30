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
    # 04: Data Structures in Practice

    You've learned variables, lists, dicts, loops, functions, files, and libraries. This notebook ties it all together with one key insight: **there are only about five shapes your data ever comes in**, and once you recognize them, everything else — APIs, DataFrames, JSON files, CSV exports — is just conversion between shapes.

    > **References:**
    > - [Think Python — Chapter 10: Lists](https://allendowney.github.io/ThinkPython/chap10.html)
    > - [Think Python — Chapter 11: Dictionaries](https://allendowney.github.io/ThinkPython/chap11.html)
    > - [Python `json` module documentation](https://docs.python.org/3/library/json.html)
    > - [pandas DataFrame documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Libraries and Packages](03-libraries-and-packages.py) | [Module Index](../README.md) | [Next: The Filesystem and the Shell \u2192](../02-your-computer/01-filesystem-and-shell.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Every tool in your pipeline speaks a different dialect of the same language. RFdiffusion outputs JSON configs. AlphaFold2 reads FASTA files. Your screening data lives in CSVs. The Claude API returns nested dictionaries. Pandas wants DataFrames. If you can recognize the underlying *shape* of the data, you can convert between any of these formats in a few lines of code.
    > - When you call the Claude API later in this tutorial, the response comes back as a deeply nested Python dictionary. If you can't navigate nested dicts, you can't extract the text Claude generated. This notebook teaches you exactly that skill.
    > - A list of dictionaries is the single most important data pattern in applied Python. It's how you'll represent your binder screening results, how pandas DataFrames are built, how JSON data is structured, and how API responses are organized. Master this one pattern and everything downstream clicks.
    > - Protein design generates *lots* of candidates. You need to move data fluidly between formats — from a JSON file of RFdiffusion outputs, to a pandas table for filtering, to a JSON payload for an API call. This notebook teaches the round-trip.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. The Five Shapes of Your Data

    Every piece of data you'll work with in Python — and in the Claude API, in pandas, in JSON files — fits into one of five shapes. Once you see this, the rest is just plumbing.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Shape 1: Single values (scalars)

    One piece of information. A gene name. A binding affinity. A filename.
    """)
    return


@app.cell
def _():
    # Single values — the atoms of your data
    gene = "SCN9A"           # NaV1.7 gene
    kd_nm = 8.3              # binding affinity in nanomolar
    is_selective = True       # passes selectivity screen?
    n_mutations = 4           # number of mutations from wild-type

    print(f"Gene: {gene}")
    print(f"Kd: {kd_nm} nM")
    print(f"Selective: {is_selective}")
    print(f"Type of kd_nm: {type(kd_nm)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Shape 2: Lists (ordered collections)

    Multiple values in a specific order. A gene list. Time-series measurements. Candidate IDs to test.
    """)
    return


@app.cell
def _():
    # Lists — ordered sequences of values
    target_genes = ["SCN9A", "SCN10A", "KCNQ2", "KCNQ3"]
    kd_values = [8.3, 15.1, 42.7, 38.9, 5.2, 67.0, 12.4]
    time_points = [0, 5, 10, 15, 30, 60, 120]  # minutes

    print(f"Targets: {target_genes}")
    print(f"Number of Kd measurements: {len(kd_values)}")
    print(f"Best Kd: {min(kd_values)} nM")
    print(f"First time point: {time_points[0]} min")
    print(f"Last time point: {time_points[-1]} min")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Shape 3: Dictionaries (labeled records)

    A single record with named fields. One binder candidate. One experiment. One paper.
    """)
    return


@app.cell
def _():
    # Dictionary — one labeled record
    binder = {
        "candidate_id": "DNB-Nav17-003",
        "target": "NaV1.7",
        "predicted_kd_nm": 8.3,
        "selectivity_ratio": 47.2,  # fold selectivity over NaV1.5
        "n_mutations": 4,
        "passes_filter": True,
        "designer": "RFdiffusion"
    }

    print(f"Candidate: {binder['candidate_id']}")
    print(f"Target: {binder['target']}")
    print(f"Kd: {binder['predicted_kd_nm']} nM")
    print(f"Number of fields: {len(binder)}")
    print(f"Field names: {list(binder.keys())}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Shape 4: Lists of dictionaries (tables as data)

    This is **the most important shape**. A list of dicts is a table — each dict is a row, each key is a column. This is how you'll represent screening results, paper metadata, API responses, and everything else.
    """)
    return


@app.cell
def _():
    # List of dictionaries — a table!
    screening_results = [
        {"candidate_id": "DNB-Nav17-001", "target": "NaV1.7", "predicted_kd_nm": 23.1, "passes_filter": False},
        {"candidate_id": "DNB-Nav17-002", "target": "NaV1.7", "predicted_kd_nm": 14.7, "passes_filter": True},
        {"candidate_id": "DNB-Nav17-003", "target": "NaV1.7", "predicted_kd_nm": 8.3,  "passes_filter": True},
        {"candidate_id": "DNB-Nav18-001", "target": "NaV1.8", "predicted_kd_nm": 42.7, "passes_filter": False},
        {"candidate_id": "DNB-Nav18-002", "target": "NaV1.8", "predicted_kd_nm": 15.1, "passes_filter": True},
        {"candidate_id": "DNB-KQ23-001", "target": "KCNQ2/3", "predicted_kd_nm": 5.2,  "passes_filter": True},
    ]

    print(f"Number of candidates: {len(screening_results)}")
    print(f"First candidate: {screening_results[0]}")
    print(f"Third candidate's Kd: {screening_results[2]['predicted_kd_nm']} nM")

    # Loop through like a table
    print("\nPassing candidates:")
    for row in screening_results:
        if row["passes_filter"]:
            print(f"  {row['candidate_id']} — {row['target']} — Kd = {row['predicted_kd_nm']} nM")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** A list of dictionaries IS a table. Each dict is a row, each key is a column header. This is the single most important data shape to internalize — it's how pandas DataFrames are created, how JSON APIs return results, and how Claude structures data when you ask it to extract information. When you see `[{"name": "DNB-001", "kd": 8.3}, {"name": "DNB-002", "kd": 15.1}]`, read it as a two-row spreadsheet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Shape 5: Nested structures (hierarchies)

    Dicts inside dicts, lists inside dicts, dicts inside lists inside dicts. This is what JSON looks like, what API responses look like, and what any hierarchical data (ontologies, file trees, experimental metadata) looks like.
    """)
    return


@app.cell
def _():
    # Nested structure — hierarchy of data
    experiment = {
        "experiment_id": "EXP-2026-042",
        "date": "2026-03-20",
        "researcher": "Alex",
        "target": {
            "gene": "SCN9A",
            "protein": "NaV1.7",
            "species": "human"
        },
        "binders_tested": [
            {"id": "DNB-Nav17-002", "kd_nm": 14.7, "blocks_current": True},
            {"id": "DNB-Nav17-003", "kd_nm": 8.3,  "blocks_current": True},
            {"id": "DNB-Nav17-007", "kd_nm": 51.2, "blocks_current": False}
        ],
        "assay": {
            "type": "patch_clamp",
            "cell_line": "HEK293-NaV1.7",
            "temperature_C": 22
        }
    }

    # Navigate the nesting
    print(f"Experiment: {experiment['experiment_id']}")
    print(f"Target protein: {experiment['target']['protein']}")
    print(f"Number of binders tested: {len(experiment['binders_tested'])}")
    print(f"Best binder: {experiment['binders_tested'][1]['id']}")
    print(f"Assay type: {experiment['assay']['type']}")
    print(f"Cell line: {experiment['assay']['cell_line']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How the five shapes relate

    ```
    Shape 1: SINGLE VALUE
        "SCN9A"                          ← a gene name
        8.3                              ← a Kd measurement

    Shape 2: LIST
        ["SCN9A", "SCN10A", "KCNQ2"]    ← a collection of single values

    Shape 3: DICTIONARY
        {"gene": "SCN9A", "kd": 8.3}    ← single values with labels

    Shape 4: LIST OF DICTIONARIES           ★ The key pattern ★
        [                                ← a table! each dict = one row
          {"gene": "SCN9A",  "kd": 8.3},
          {"gene": "SCN10A", "kd": 15.1},
        ]

    Shape 5: NESTED STRUCTURE
        {                                ← dicts inside dicts, lists inside dicts
          "experiment": "EXP-042",
          "target": {"gene": "SCN9A"},
          "results": [
            {"binder": "DNB-003", "kd": 8.3},
          ]
        }
    ```

    Everything nests: values go into lists, values go into dicts, dicts go into lists, and you get tables. Dicts go into dicts, and you get hierarchies. That's it. That's all there is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph TD
        V["Single Value<br/><code>'SCN9A'</code> or <code>8.3</code>"]
        L["List<br/><code>['SCN9A', 'SCN10A', ...]</code>"]
        D["Dictionary<br/><code>{'gene': 'SCN9A', 'kd': 8.3}</code>"]
        LD["List of Dicts<br/><code>[{'gene': ..., 'kd': ...}, ...]</code><br/>★ TABLE ★"]
        N["Nested Structure<br/><code>{'target': {'gene': ...}, 'results': [...]}</code>"]

        V -->|"collect into"| L
        V -->|"add labels"| D
        D -->|"collect into"| LD
        D -->|"nest deeper"| N
        L -->|"nest into dicts"| N
        LD -->|"nest into dicts"| N

        LD -.->|"pd.DataFrame()"| DF["pandas DataFrame"]
        LD -.->|"json.dumps()"| JSON["JSON string"]

        style V fill:#f59e0b,color:#000
        style L fill:#3b82f6,color:#fff
        style D fill:#10b981,color:#fff
        style LD fill:#ef4444,color:#fff
        style N fill:#8b5cf6,color:#fff
        style DF fill:#ec4899,color:#fff
        style JSON fill:#ec4899,color:#fff
    ```

    The red box — list of dicts — is the hub. It connects to DataFrames (pandas) and JSON (APIs and files). Master that shape and you can move data anywhere.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Lists of Dictionaries — The Gateway to Everything

    This section drives home the central insight: a list of dicts IS a table. It's the same thing as a DataFrame. It's the same thing as JSON. It's what the Claude API returns. Once you see this, you can move data between any format.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A list of dicts IS a table

    Let's start with binder screening data as a list of dicts, then show that it's the same thing in three different outfits.
    """)
    return


@app.cell
def _():
    # Binder screening data — as a list of dicts
    binders = [
        {"candidate_id": "DNB-Nav17-001", "target": "NaV1.7",  "predicted_kd_nm": 23.1, "designer": "RFdiffusion",  "passes_filter": False},
        {"candidate_id": "DNB-Nav17-002", "target": "NaV1.7",  "predicted_kd_nm": 14.7, "designer": "RFdiffusion",  "passes_filter": True},
        {"candidate_id": "DNB-Nav17-003", "target": "NaV1.7",  "predicted_kd_nm": 8.3,  "designer": "RFdiffusion",  "passes_filter": True},
        {"candidate_id": "DNB-Nav18-001", "target": "NaV1.8",  "predicted_kd_nm": 42.7, "designer": "ProteinMPNN",  "passes_filter": False},
        {"candidate_id": "DNB-Nav18-002", "target": "NaV1.8",  "predicted_kd_nm": 15.1, "designer": "RFdiffusion",  "passes_filter": True},
        {"candidate_id": "DNB-KQ23-001", "target": "KCNQ2/3",  "predicted_kd_nm": 5.2,  "designer": "ProteinMPNN",  "passes_filter": True},
        {"candidate_id": "DNB-KQ23-002", "target": "KCNQ2/3",  "predicted_kd_nm": 67.0, "designer": "RFdiffusion",  "passes_filter": False},
        {"candidate_id": "DNB-Nav17-004", "target": "NaV1.7",  "predicted_kd_nm": 12.4, "designer": "ProteinMPNN",  "passes_filter": True},
    ]

    # It's already a table — you can think of it row by row
    print(f"Number of rows: {len(binders)}")
    print(f"Columns: {list(binders[0].keys())}")
    print(f"\nRow 0: {binders[0]}")
    print(f"Row 2, Kd: {binders[2]['predicted_kd_nm']}")
    return (binders,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Same data as a pandas DataFrame
    """)
    return


@app.cell
def _(binders):
    import pandas as pd

    # One line: list of dicts → DataFrame
    df = pd.DataFrame(binders)
    df
    return df, pd


@app.cell
def _(df):
    # And back: DataFrame → list of dicts
    back_to_list = df.to_dict(orient="records")

    print("Type:", type(back_to_list))
    print("First record:", back_to_list[0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Same data as JSON
    """)
    return


@app.cell
def _(binders):
    import json

    # List of dicts → JSON string
    json_string = json.dumps(binders, indent=2)
    print(json_string[:500])  # first 500 characters
    return json, json_string


@app.cell
def _(json, json_string):
    # JSON string → list of dicts
    parsed_back = json.loads(json_string)

    print(f"Type: {type(parsed_back)}")
    print(f"Number of records: {len(parsed_back)}")
    print(f"First record: {parsed_back[0]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Same shape the Claude API returns

    When you call the Claude API (Module 05), the response is a nested dict. But inside it, structured data often comes back as — you guessed it — something that maps to a list of dicts.

    Here's a preview of what a Claude API response looks like:
    """)
    return


@app.cell
def _():
    # This is the SHAPE of a Claude API response (simplified)
    # You'll see the real thing in Module 05
    mock_api_response = {'id': 'msg_01ABC123', 'type': 'message', 'role': 'assistant', 'content': [{'type': 'text', 'text': 'Based on the screening data, DNB-KQ23-001 shows the best predicted affinity at 5.2 nM.'}], 'model': 'claude-sonnet-4-20250514', 'usage': {'input_tokens': 245, 'output_tokens': 38}}
    _text = mock_api_response['content'][0]['text']
    # To get the actual text Claude returned:
    # That's: dict → key "content" → first item in list → key "text"
    # Nested structure navigation — Shape 5 in action
    print(_text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The three representations are interchangeable

    ```
    List of Dicts  ←→  DataFrame  ←→  JSON
      (Python)          (pandas)       (text/files/APIs)

    List of Dicts → DataFrame:   pd.DataFrame(list_of_dicts)
    DataFrame → List of Dicts:   df.to_dict(orient="records")
    List of Dicts → JSON:        json.dumps(list_of_dicts)
    JSON → List of Dicts:        json.loads(json_string)
    ```

    These four conversions are all you need. Everything else is just applying them in sequence.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: Convert between all three representations

    Start with this list of dicts representing NaV1.7 binder candidates that passed selectivity screening. Convert it to:

    1. A pandas DataFrame
    2. A JSON string (with indentation)
    3. Back to a list of dicts from the JSON string
    4. Verify the round-trip: check that the first record matches the original
    """)
    return


@app.cell
def _():
    _selective_binders = [{'id': 'DNB-Nav17-003', 'kd_nm': 8.3, 'selectivity_vs_nav15': 47.2, 'n_mutations': 4}, {'id': 'DNB-Nav17-002', 'kd_nm': 14.7, 'selectivity_vs_nav15': 31.5, 'n_mutations': 6}, {'id': 'DNB-Nav17-004', 'kd_nm': 12.4, 'selectivity_vs_nav15': 28.9, 'n_mutations': 3}]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(json, pd):
    _selective_binders = [{'id': 'DNB-Nav17-003', 'kd_nm': 8.3, 'selectivity_vs_nav15': 47.2, 'n_mutations': 4}, {'id': 'DNB-Nav17-002', 'kd_nm': 14.7, 'selectivity_vs_nav15': 31.5, 'n_mutations': 6}, {'id': 'DNB-Nav17-004', 'kd_nm': 12.4, 'selectivity_vs_nav15': 28.9, 'n_mutations': 3}]
    df_1 = pd.DataFrame(_selective_binders)
    print('=== DataFrame ===')
    print(df_1)
    print()
    json_string_1 = json.dumps(_selective_binders, indent=2)
    print('=== JSON ===')
    print(json_string_1)
    print()
    round_tripped = json.loads(json_string_1)
    print('=== Round-tripped ===')
    print(f'Type: {type(round_tripped)}')
    print(f'First record: {round_tripped[0]}')
    print()
    print(f'Original first record:      {_selective_binders[0]}')
    print(f'Round-tripped first record: {round_tripped[0]}')
    print(f'Match: {_selective_binders[0] == round_tripped[0]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. JSON — The Language of APIs

    JSON (JavaScript Object Notation) is just a way of writing dicts and lists as text. It's the universal format for sending data between programs, storing configurations, and communicating with APIs.

    **Why you need to know JSON:**
    - The Claude API sends and receives JSON
    - RFdiffusion config files are JSON
    - Many bioinformatics databases (UniProt, PDB) offer JSON APIs
    - Zotero, Benchling, and other lab tools export JSON

    The good news: JSON maps directly to Python dicts and lists. If you know those, you already know JSON.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What JSON looks like

    ```json
    {
      "candidate_id": "DNB-Nav17-003",
      "target": "NaV1.7",
      "predicted_kd_nm": 8.3,
      "passes_filter": true,
      "mutations": ["A142G", "S198T", "L267V", "R301K"]
    }
    ```

    Looks familiar? It's almost identical to a Python dict. The only differences:
    - JSON uses `true`/`false` (lowercase) vs Python's `True`/`False`
    - JSON uses `null` vs Python's `None`
    - JSON keys must be strings in double quotes
    - No trailing commas allowed

    Python's `json` module handles all these conversions automatically.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use JSON vs. CSV vs. DataFrame?
    >
    > | Format | Pros | Cons | Use when... |
    > |--------|------|------|-------------|
    > | **JSON** | Handles nested/hierarchical data, universal API format, human-readable | Larger file size than CSV, harder to open in Excel | Saving experiment metadata, API responses, configs, or any data with nested structure (e.g., an experiment with multiple assays each containing multiple results) |
    > | **CSV** | Universal tabular format, opens in Excel/Google Sheets, compact | Flat only (no nesting), no type info (everything is strings), quoting issues with commas in data | Sharing flat tables with collaborators, exporting from instruments (plate readers, flow cytometers), archival data |
    > | **DataFrame** (pandas) | Fast filtering/grouping/stats, plotting integration, handles types | Only exists in Python memory (must save as CSV or JSON to disk), overkill for simple data | Active analysis — anytime you need to filter, sort, group, merge, or plot your data |
    >
    > **Common workflow:** Receive data as CSV or JSON, load into a DataFrame for analysis, save results back to CSV for sharing or JSON for pipelines.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Reading and writing JSON files
    """)
    return


@app.cell
def _(json):
    from pathlib import Path
    experiment_config = {'experiment_id': 'EXP-2026-042', 'date': '2026-03-20', 'target': 'NaV1.7', 'binders_tested': ['DNB-Nav17-002', 'DNB-Nav17-003', 'DNB-Nav17-004'], 'assay': {'type': 'calcium_imaging', 'stimulus': 'capsaicin', 'concentration_uM': 1.0, 'cell_type': 'mouse_DRG'}, 'notes': None}
    output_path = Path.cwd() / 'sample_data'
    output_path.mkdir(exist_ok=True)
    _json_file = output_path / 'experiment_config.json'
    with open(_json_file, 'w') as _f:
        json.dump(experiment_config, _f, indent=2)
    print(f'Saved to: {_json_file}')
    print(f'File size: {_json_file.stat().st_size} bytes')
    return (Path,)


@app.cell
def _(Path, json):
    _json_file = Path.cwd() / 'sample_data' / 'experiment_config.json'
    with open(_json_file, 'r') as _f:
        loaded = json.load(_f)
    print(f'Type: {type(loaded)}')
    print(f"Experiment: {loaded['experiment_id']}")
    print(f"Assay type: {loaded['assay']['type']}")
    print(f"Binders: {loaded['binders_tested']}")
    print(f"Notes: {loaded['notes']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Key functions:**

    | Function | What it does | Direction |
    |----------|-------------|-----------|
    | `json.dumps(data)` | Python → JSON **s**tring | Writing (to string) |
    | `json.dump(data, file)` | Python → JSON **f**ile | Writing (to file) |
    | `json.loads(string)` | JSON **s**tring → Python | Reading (from string) |
    | `json.load(file)` | JSON **f**ile → Python | Reading (from file) |

    The "s" at the end = "string". Without "s" = works with file objects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 💡 **Tip:** Use `json.dumps(data, indent=2)` whenever you need to inspect a complex data structure. Without `indent`, JSON is a single unreadable line. With `indent=2`, nested structures become clear. This is especially useful when debugging API responses or checking that your data transformations worked correctly. You can also use it as a quick "pretty print" for any dict or list.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Nested JSON: accessing data at depth

    API responses are typically nested several levels deep. The key skill is navigating to the data you need, one key/index at a time.
    """)
    return


@app.cell
def _():
    # A mock Claude API response — this is what you'll actually get back
    # when you call the Claude API in Module 05
    mock_claude_response = {
        "id": "msg_01XYZ789",
        "type": "message",
        "role": "assistant",
        "content": [
            {
                "type": "text",
                "text": "Here are the top 3 NaV1.7 binder candidates based on predicted affinity:\n\n1. DNB-Nav17-003 (Kd = 8.3 nM) — Best overall affinity\n2. DNB-Nav17-004 (Kd = 12.4 nM) — Fewest mutations (3)\n3. DNB-Nav17-002 (Kd = 14.7 nM) — Good selectivity ratio"
            }
        ],
        "model": "claude-sonnet-4-20250514",
        "stop_reason": "end_turn",
        "usage": {
            "input_tokens": 512,
            "output_tokens": 87
        }
    }

    # Step by step: navigate to the text
    print("Step 1 — top-level keys:")
    print(list(mock_claude_response.keys()))
    print()

    print("Step 2 — 'content' is a list:")
    print(type(mock_claude_response["content"]))
    print(f"Length: {len(mock_claude_response['content'])}")
    print()

    print("Step 3 — first item in 'content' is a dict:")
    print(mock_claude_response["content"][0].keys())
    print()

    print("Step 4 — the actual text:")
    print(mock_claude_response["content"][0]["text"])
    return (mock_claude_response,)


@app.cell
def _(mock_claude_response):
    # The one-liner you'll use every time:
    _text = mock_claude_response['content'][0]['text']
    input_tokens = mock_claude_response['usage']['input_tokens']
    # And you can also get usage info for cost tracking:
    output_tokens = mock_claude_response['usage']['output_tokens']
    print(f'Tokens used: {input_tokens} in + {output_tokens} out = {input_tokens + output_tokens} total')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: Parse a mock Claude API response

    The following mock response represents Claude analyzing your binder screening data and returning a structured recommendation. Extract:

    1. The text Claude generated
    2. The total number of tokens used (input + output)
    3. Which model was used
    4. The stop reason
    """)
    return


@app.cell
def _():
    # Extract the four pieces of information:
    # YOUR CODE HERE
    _api_response = {'id': 'msg_01DEF456', 'type': 'message', 'role': 'assistant', 'content': [{'type': 'text', 'text': 'Based on your screening data, I recommend prioritizing DNB-KQ23-001 for KCNQ2/3 (Kd = 5.2 nM, best affinity across all targets) and DNB-Nav17-003 for NaV1.7 (Kd = 8.3 nM, excellent selectivity over NaV1.5). For NaV1.8, DNB-Nav18-002 at 15.1 nM is your best option but may benefit from further optimization.'}], 'model': 'claude-sonnet-4-20250514', 'stop_reason': 'end_turn', 'usage': {'input_tokens': 1024, 'output_tokens': 93}}
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _():
    _api_response = {'id': 'msg_01DEF456', 'type': 'message', 'role': 'assistant', 'content': [{'type': 'text', 'text': 'Based on your screening data, I recommend prioritizing DNB-KQ23-001 for KCNQ2/3 (Kd = 5.2 nM, best affinity across all targets) and DNB-Nav17-003 for NaV1.7 (Kd = 8.3 nM, excellent selectivity over NaV1.5). For NaV1.8, DNB-Nav18-002 at 15.1 nM is your best option but may benefit from further optimization.'}], 'model': 'claude-sonnet-4-20250514', 'stop_reason': 'end_turn', 'usage': {'input_tokens': 1024, 'output_tokens': 93}}
    claude_text = _api_response['content'][0]['text']
    print("Claude's recommendation:")
    print(claude_text)
    print()
    total_tokens = _api_response['usage']['input_tokens'] + _api_response['usage']['output_tokens']
    print(f'Total tokens: {total_tokens}')
    print(f"Model: {_api_response['model']}")
    # 1. The text
    # 2. Total tokens
    # 3. Model
    # 4. Stop reason
    print(f"Stop reason: {_api_response['stop_reason']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. From Raw Data to DataFrame (and Back)

    In practice, your data often starts as JSON (from an API or a file), needs to become a DataFrame (for analysis), and then goes back to JSON (for sending to another API or saving). This section walks through the full pipeline.

    **The pipeline:**
    ```
    API response (JSON text)
        → json.loads() → Python dict/list
        → extract the data you need
        → pd.DataFrame() → DataFrame for analysis
        → df.to_dict(orient="records") → list of dicts
        → json.dumps() → JSON text
        → send to another API or save to file
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Demo: Full round-trip with binder data
    """)
    return


@app.cell
def _():
    raw_json = '{\n  "status": "success",\n  "pipeline": "RFdiffusion_v2",\n  "timestamp": "2026-03-20T14:30:00Z",\n  "results": [\n    {"candidate_id": "DNB-Nav17-010", "target": "NaV1.7", "kd_nm": 6.1, "plddt": 92.3, "rmsd": 0.8},\n    {"candidate_id": "DNB-Nav17-011", "target": "NaV1.7", "kd_nm": 18.4, "plddt": 87.1, "rmsd": 1.2},\n    {"candidate_id": "DNB-Nav17-012", "target": "NaV1.7", "kd_nm": 11.7, "plddt": 90.5, "rmsd": 0.9},\n    {"candidate_id": "DNB-Nav17-013", "target": "NaV1.7", "kd_nm": 45.3, "plddt": 78.2, "rmsd": 2.1},\n    {"candidate_id": "DNB-Nav17-014", "target": "NaV1.7", "kd_nm": 9.8, "plddt": 91.0, "rmsd": 0.7}\n  ]\n}'
    print('STEP 1: Raw JSON received')
    print(f'Type: {type(raw_json)}')
    # STEP 1: Simulate receiving JSON from an API
    # (In real life, this would come from requests.get() or the anthropic library)
    print(f'Length: {len(raw_json)} characters')
    return (raw_json,)


@app.cell
def _(json, raw_json):
    # STEP 2: Parse JSON into Python
    data = json.loads(raw_json)

    print("STEP 2: Parsed into Python")
    print(f"Type: {type(data)}")
    print(f"Top-level keys: {list(data.keys())}")
    print(f"Pipeline: {data['pipeline']}")
    print(f"Number of results: {len(data['results'])}")
    return (data,)


@app.cell
def _(data, pd):
    # STEP 3: Extract the results and make a DataFrame
    results = data['results']  # this is the list of dicts
    df_2 = pd.DataFrame(results)
    print('STEP 3: DataFrame')
    print(df_2)
    print(f"\nBest candidate: {df_2.loc[df_2['kd_nm'].idxmin(), 'candidate_id']} (Kd = {df_2['kd_nm'].min()} nM)")
    return (df_2,)


@app.cell
def _(df_2):
    # STEP 4: Filter in pandas — keep only high-confidence candidates
    good_candidates = df_2[(df_2['kd_nm'] < 15) & (df_2['plddt'] > 89)].copy()
    print('STEP 4: Filtered DataFrame')
    print(good_candidates)
    print(f'\n{len(good_candidates)} of {len(df_2)} candidates passed filters')
    return (good_candidates,)


@app.cell
def _(data, good_candidates, json):
    # STEP 5: Convert back to JSON (e.g., to send to another API or save)
    filtered_records = good_candidates.to_dict(orient='records')
    _output = {'source_pipeline': data['pipeline'], 'filter_criteria': 'kd_nm < 15 AND plddt > 89', 'n_passed': len(filtered_records), 'candidates': filtered_records}
    output_json = json.dumps(_output, indent=2)
    print('STEP 5: Back to JSON')
    print(output_json)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's the full pipeline:
    1. **Receive** JSON from an API or file
    2. **Parse** it into a Python dict (`json.loads`)
    3. **Extract** the list of dicts you care about
    4. **Convert** to DataFrame for analysis (`pd.DataFrame`)
    5. **Filter/transform** in pandas
    6. **Convert back** to dicts (`df.to_dict(orient="records")`)
    7. **Serialize** to JSON (`json.dumps`) to save or send

    You'll use this exact pipeline in Module 05 with real Claude API calls.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise: Build the full round-trip

    Below is a JSON string representing binder screening output. Your task:

    1. Parse the JSON
    2. Extract the `"candidates"` list
    3. Convert to a DataFrame
    4. Add a new column `"priority"` that is `"high"` if `kd_nm < 10` and `solubility_score > 0.8`, otherwise `"standard"`
    5. Filter to only high-priority candidates
    6. Convert the filtered results back to a JSON string and print it
    """)
    return


@app.cell
def _():
    _screening_json = '{\n  "screen_id": "SCREEN-2026-008",\n  "target": "NaV1.7",\n  "candidates": [\n    {"id": "DNB-101", "kd_nm": 5.4,  "solubility_score": 0.92, "thermal_stability_C": 68.1},\n    {"id": "DNB-102", "kd_nm": 22.1, "solubility_score": 0.85, "thermal_stability_C": 71.3},\n    {"id": "DNB-103", "kd_nm": 8.7,  "solubility_score": 0.88, "thermal_stability_C": 65.9},\n    {"id": "DNB-104", "kd_nm": 7.2,  "solubility_score": 0.71, "thermal_stability_C": 62.4},\n    {"id": "DNB-105", "kd_nm": 3.1,  "solubility_score": 0.95, "thermal_stability_C": 72.8},\n    {"id": "DNB-106", "kd_nm": 41.6, "solubility_score": 0.93, "thermal_stability_C": 74.1},\n    {"id": "DNB-107", "kd_nm": 9.9,  "solubility_score": 0.82, "thermal_stability_C": 67.5}\n  ]\n}'
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Solution
    """)
    return


@app.cell
def _(json, pd):
    _screening_json = '{\n  "screen_id": "SCREEN-2026-008",\n  "target": "NaV1.7",\n  "candidates": [\n    {"id": "DNB-101", "kd_nm": 5.4,  "solubility_score": 0.92, "thermal_stability_C": 68.1},\n    {"id": "DNB-102", "kd_nm": 22.1, "solubility_score": 0.85, "thermal_stability_C": 71.3},\n    {"id": "DNB-103", "kd_nm": 8.7,  "solubility_score": 0.88, "thermal_stability_C": 65.9},\n    {"id": "DNB-104", "kd_nm": 7.2,  "solubility_score": 0.71, "thermal_stability_C": 62.4},\n    {"id": "DNB-105", "kd_nm": 3.1,  "solubility_score": 0.95, "thermal_stability_C": 72.8},\n    {"id": "DNB-106", "kd_nm": 41.6, "solubility_score": 0.93, "thermal_stability_C": 74.1},\n    {"id": "DNB-107", "kd_nm": 9.9,  "solubility_score": 0.82, "thermal_stability_C": 67.5}\n  ]\n}'
    data_1 = json.loads(_screening_json)
    print(f"Screen: {data_1['screen_id']}, Target: {data_1['target']}")
    candidates = data_1['candidates']
    df_3 = pd.DataFrame(candidates)
    print(f'\nAll candidates ({len(df_3)}):')
    print(df_3)
    df_3['priority'] = 'standard'
    df_3.loc[(df_3['kd_nm'] < 10) & (df_3['solubility_score'] > 0.8), 'priority'] = 'high'
    print(f'\nWith priority:')
    print(df_3[['id', 'kd_nm', 'solubility_score', 'priority']])
    high_priority = df_3[df_3['priority'] == 'high']
    print(f'\nHigh-priority candidates: {len(high_priority)}')
    _output = {'screen_id': data_1['screen_id'], 'filter': 'kd_nm < 10 AND solubility_score > 0.8', 'high_priority_candidates': high_priority.drop(columns='priority').to_dict(orient='records')}
    print(f'\nJSON output:')
    print(json.dumps(_output, indent=2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Recognizing Shapes in the Wild

    Now that you know the five shapes, let's see where they appear in real tools and workflows. The point isn't to memorize every format — it's to develop the reflex: "What shape is this data? How do I convert it to what I need?"
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### CSV files → list of dicts / DataFrame

    CSV is the simplest tabular format. Each row is a record, each column has a header. It maps directly to a list of dicts.
    """)
    return


@app.cell
def _(Path, pd):
    import csv
    csv_file = Path.cwd() / 'sample_data' / 'binder_screening.csv'
    if csv_file.exists():
        with open(csv_file, 'r') as _f:
            reader = csv.DictReader(_f)
            rows = list(reader)
        print(f'csv.DictReader → list of dicts: {len(rows)} rows')
        print(f'First row: {rows[0]}')
        print()
        df_4 = pd.read_csv(csv_file)
        print(f'pd.read_csv → DataFrame: {df_4.shape[0]} rows x {df_4.shape[1]} columns')
        print(df_4.head(3))
    else:
        print(f'Note: {csv_file} not found — this is OK if running standalone.')
        print('The point is: csv.DictReader gives you a list of dicts, pd.read_csv gives you a DataFrame.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Zotero / reference manager exports → list of dicts

    When you export your Zotero library to JSON, each paper is a dict, and the whole export is a list of dicts.
    """)
    return


@app.cell
def _(pd):
    # What a Zotero JSON export looks like (simplified)
    zotero_papers = [{'title': 'NaV1.7 as a target for pain therapeutics', 'authors': ['Bhatt DK', 'Bhatt SP'], 'year': 2024, 'journal': 'Pain', 'doi': '10.1097/j.pain.0000000000003123', 'tags': ['NaV1.7', 'pain', 'therapeutics']}, {'title': 'De novo protein binder design with RFdiffusion', 'authors': ['Watson JL', 'Juergens D', 'Bennett NR'], 'year': 2023, 'journal': 'Nature', 'doi': '10.1038/s41586-023-06415-8', 'tags': ['protein design', 'RFdiffusion', 'binders']}]
    print(f'Papers in library: {len(zotero_papers)}')
    print(f"First paper: {zotero_papers[0]['title']}")
    print(f"First paper authors: {', '.join(zotero_papers[0]['authors'])}")
    df_papers = pd.DataFrame(zotero_papers)
    print(f'\nAs DataFrame:')
    # It's a list of dicts — you already know how to work with this!
    # Convert to DataFrame for filtering
    print(df_papers[['title', 'year', 'journal']])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Claude API responses → nested dicts

    You've already seen this above. The pattern is always:

    ```python
    response["content"][0]["text"]   # the text Claude generated
    response["usage"]["input_tokens"] # how many tokens you sent
    response["usage"]["output_tokens"] # how many tokens Claude returned
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Gene ontology / hierarchies → nested dicts

    Ontologies and taxonomies are trees. In Python, trees are nested dicts.
    """)
    return


@app.cell
def _():
    # A simplified pain-related ontology
    pain_ontology = {
        "term": "pain",
        "id": "HP:0012531",
        "children": [
            {
                "term": "neuropathic pain",
                "id": "HP:0011096",
                "children": [
                    {"term": "burning pain", "id": "HP:0012762", "children": []},
                    {"term": "allodynia", "id": "HP:0012534", "children": []},
                ]
            },
            {
                "term": "inflammatory pain",
                "id": "HP:0012532",
                "children": [
                    {"term": "joint pain", "id": "HP:0002829", "children": []},
                ]
            }
        ]
    }

    # Navigate the tree
    print(f"Root: {pain_ontology['term']}")
    print(f"Children: {[c['term'] for c in pain_ontology['children']]}")
    print(f"Grandchildren of neuropathic pain: {[c['term'] for c in pain_ontology['children'][0]['children']]}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Your filesystem → tree (nested dicts)

    Even your file system is a tree — folders contain folders contain files. Same shape.
    """)
    return


@app.cell
def _():
    # Your project structure is also a nested dict / tree
    project_tree = {
        "ai-tutorial": {
            "01-python-foundations": [
                "01-your-first-code.py",
                "02-working-with-files.py",
                "03-libraries-and-packages.py",
                "04-data-structures-in-practice.py",
            ],
            "02-how-llms-work": [],
            "05-claude-api": [],
            "resources": ["cheat-sheets"],
        }
    }

    # Same navigation pattern
    notebooks = project_tree["ai-tutorial"]["01-python-foundations"]
    print(f"Module 01 notebooks: {len(notebooks)}")
    for nb in notebooks:
        print(f"  - {nb}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quick reference: "I have X, I want Y, use Z"

    | I have... | I want... | Use... |
    |-----------|-----------|--------|
    | List of dicts | DataFrame | `pd.DataFrame(list_of_dicts)` |
    | DataFrame | List of dicts | `df.to_dict(orient="records")` |
    | List of dicts | JSON string | `json.dumps(list_of_dicts)` |
    | JSON string | List of dicts | `json.loads(json_string)` |
    | JSON file | Python object | `json.load(open(path))` |
    | Python object | JSON file | `json.dump(obj, open(path, "w"))` |
    | CSV file | DataFrame | `pd.read_csv(path)` |
    | DataFrame | CSV file | `df.to_csv(path, index=False)` |
    | CSV file | List of dicts | `list(csv.DictReader(open(path)))` |
    | DataFrame | JSON string | `df.to_json(orient="records")` |
    | Nested dict | Value at depth | Chain keys: `d["a"]["b"][0]["c"]` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - **Five data shapes** — single values, lists, dicts, lists of dicts, and nested structures. That's all there is.
    - **Lists of dicts = tables** — this is the key pattern. A list of dicts IS a DataFrame IS JSON. They're the same data in different outfits.
    - **JSON is just text** — it maps directly to Python dicts and lists. `json.dumps` writes it, `json.loads` reads it.
    - **The full pipeline** — JSON → Python dict → list of dicts → DataFrame → analysis → dicts → JSON. You can go in either direction.
    - **Shape recognition** — once you can identify which of the five shapes you're looking at, you know exactly which conversion function to use.

    This is the foundation for everything that follows:
    - Module 05 (Claude API): the API returns nested dicts, you extract what you need
    - Module 06 (Data Skills): DataFrames are just lists of dicts with superpowers
    - Module 07 (Research Workflows): you'll chain API calls, parsing, and analysis together
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Think Python, Chapter 10: Lists** — covers list operations, slicing, and list methods in depth. Good for solidifying the fundamentals if any of the list operations above felt unfamiliar. [https://allendowney.github.io/ThinkPython/chap10.html](https://allendowney.github.io/ThinkPython/chap10.html)

    - **Think Python, Chapter 11: Dictionaries** — covers dict operations, looping over dicts, and using dicts to count things. The section on "dictionaries as a collection of counters" is particularly useful for bioinformatics work. [https://allendowney.github.io/ThinkPython/chap11.html](https://allendowney.github.io/ThinkPython/chap11.html)

    - **Python `json` module documentation** — the official reference for `json.load`, `json.dump`, `json.loads`, and `json.dumps`. The examples section at the top is the most useful part. [https://docs.python.org/3/library/json.html](https://docs.python.org/3/library/json.html)

    - **pandas `DataFrame` documentation** — the reference page for DataFrame construction, including creating DataFrames from dicts, lists of dicts, and other sources. You don't need to read this end-to-end; use it as a lookup when you need a specific method. [https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Libraries and Packages](03-libraries-and-packages.py) | [Module Index](../README.md) | [Next: The Filesystem and the Shell \u2192](../02-your-computer/01-filesystem-and-shell.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created notebook — five data shapes, list-of-dicts as gateway pattern, JSON/DataFrame round-trip exercises
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

