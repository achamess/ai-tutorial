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
    # 01: Your First Code

    ## How this works

    You're looking at a **marimo notebook**. It's made of **cells** — some are text (like this one), some are code (like the next one).

    ### The one shortcut you need right now

    **`Shift + Enter`** — runs the current cell and moves to the next one.

    Click on the code cell below and press `Shift + Enter`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Pre-Flight Check](../00-getting-started/02-preflight-check.py) | [Module Index](../README.md) | [Next: Working with Files \u2192](02-working-with-files.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Every Claude API call you'll write is Python. When you ask Claude to analyze your NaV1.7 binder screening data or automate a literature search, the code it generates — and that you'll need to read, trust, and modify — is Python.
    > - The data structures in this notebook (lists, dictionaries, loops) are exactly how you'll represent binder candidates, experimental results, and gene lists when building automated workflows.
    > - Understanding variables, types, and functions means you can verify what Claude Code produces instead of blindly trusting it. That's the difference between using AI effectively and using it dangerously.
    > - Python is the lingua franca of bioinformatics, structural biology tools (RFdiffusion, ProteinMPNN, AlphaFold2), and data science. This notebook is the entry point to all of them.
    """)
    return


@app.cell
def _():
    print("Hello from a DRG neuron")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You just ran Python. The output appears right below the cell. That's the whole workflow — write code, run it, see the result.

    > **VS Code tip:** If it asks you to select a kernel, choose **"ai-tutorial"** from the dropdown. That's the Python environment we set up for this project.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Variables: giving names to things

    A variable is just a name that points to a value. Think of it like labeling a tube in the lab.
    """)
    return


@app.cell
def _():
    # A string (text)
    channel = "NaV1.7"

    # A number (integer)
    num_drg_neurons = 45

    # A number with a decimal (float)
    firing_threshold_mv = -35.2

    # A boolean (True or False)
    is_nociceptor = True

    print(channel)
    print(num_drg_neurons)
    print(firing_threshold_mv)
    print(is_nociceptor)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Four types, and that's most of what you'll use:

    | Type | What it holds | Example |
    |------|--------------|--------|
    | `str` | Text | `"NaV1.7"` |
    | `int` | Whole numbers | `45` |
    | `float` | Decimals | `-35.2` |
    | `bool` | True/False | `True` |

    The `#` symbol starts a **comment** — Python ignores everything after it. Use comments to leave yourself notes.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph TD
        subgraph "Python's Core Data Types"
            STR["<b>str</b><br/>Text<br/><i>'NaV1.7'</i>"]
            INT["<b>int</b><br/>Whole numbers<br/><i>45</i>"]
            FLOAT["<b>float</b><br/>Decimals<br/><i>-35.2</i>"]
            BOOL["<b>bool</b><br/>True / False<br/><i>True</i>"]
        end

        subgraph "When to use each"
            STR --- S1["Names, labels, sequences<br/>Gene names, binder IDs, FASTA"]
            INT --- S2["Counts, indices<br/>Neuron counts, well numbers"]
            FLOAT --- S3["Measurements<br/>Kd values, voltage, temperature"]
            BOOL --- S4["Yes/No decisions<br/>Is it a nociceptor? Passed QC?"]
        end

        style STR fill:#4488cc,color:#fff
        style INT fill:#44aa88,color:#fff
        style FLOAT fill:#cc8844,color:#fff
        style BOOL fill:#aa44aa,color:#fff
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Lists: groups of things

    A list holds multiple values in order. Square brackets, comma-separated.
    """)
    return


@app.cell
def _():
    # Ion channels you're designing binders for
    target_channels = ["NaV1.7", "NaV1.8", "KCNQ2", "KCNQ3"]

    print(target_channels)
    print(f"Number of targets: {len(target_channels)}")
    return (target_channels,)


@app.cell
def _(target_channels):
    # Access items by position (counting starts at 0, not 1)
    print(target_channels[0])   # first item
    print(target_channels[-1])  # last item
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** Python counts from 0, not 1. The first item in a list is `target_channels[0]`, not `target_channels[1]`. This isn't arbitrary — it comes from how memory addresses work in computers. The index tells Python *how far to jump from the start*, so the first item is zero jumps away. You'll encounter zero-based indexing everywhere: list positions, DataFrame row numbers, and array indices in numpy. It feels weird for about a week, then it becomes second nature.
    """)
    return


@app.cell
def _(target_channels):
    # Add to a list
    target_channels.append("CaV2.2")
    print(target_channels)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why dictionaries?** When Claude generates code to process your binder screening data, it almost always represents each candidate as a dictionary — `{"name": "DNB-001", "target": "NaV1.7", "kd_nm": 8.3}`. Recognizing this pattern means you can read and modify Claude's output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Dictionaries: labeled data

    A dictionary maps **keys** to **values**. Think of it as a structured record — like metadata for an experiment.
    """)
    return


@app.cell
def _():
    experiment = {
        "target": "NaV1.8",
        "region": "C-terminus",
        "approach": "de novo binder + E3 ligase",
        "goal": "targeted degradation",
        "num_candidates": 12
    }

    print(experiment)
    return (experiment,)


@app.cell
def _(experiment):
    # Access a single value by its key
    print(experiment["target"])
    print(experiment["num_candidates"])
    return


@app.cell
def _(experiment):
    # Add new information
    experiment["status"] = "in silico screening"

    print(experiment)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph LR
        subgraph "Lists — Ordered Collections"
            L["[ 'NaV1.7', 'NaV1.8', 'KCNQ2' ]"]
            L --- L1["Access by position: list[0]"]
            L --- L2["Ordered: first, second, third..."]
            L --- L3["Use for: channels, measurements, gene lists"]
        end

        subgraph "Dictionaries — Labeled Records"
            D["{ 'target': 'NaV1.8', 'Kd': 12.7 }"]
            D --- D1["Access by key: dict['target']"]
            D --- D2["Labeled: each value has a name"]
            D --- D3["Use for: experiments, candidates, metadata"]
        end

        style L fill:#4488cc,color:#fff
        style D fill:#44aa88,color:#fff
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use a list vs. a dictionary?
    >
    > | Option | Pros | Cons | Use when... |
    > |--------|------|------|-------------|
    > | **List** `[]` | Ordered, easy to loop through, supports slicing | Access by position only — `items[2]` doesn't tell you what's there | You have a collection of similar things: gene names, Kd values, time points, channel targets |
    > | **Dictionary** `{}` | Named access (`experiment["target"]`), self-documenting, great for records | No inherent order (though insertion order is preserved in modern Python), can't slice | You have a single record with labeled fields: one experiment, one binder candidate, one paper's metadata |
    > | **List of dicts** `[{}, {}]` | Combines both: a table of labeled records you can loop through | More verbose than a simple list | You have multiple records — this is the gateway to pandas DataFrames and JSON (covered in notebook 04) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Lists are for **ordered collections** (a set of channels, a sequence of measurements).
    Dictionaries are for **labeled records** (an experiment, a protein, a paper's metadata).

    You'll use both constantly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## f-strings: putting variables into text

    The `f` before the quotes lets you embed variables directly in text using `{curly braces}`.
    """)
    return


@app.cell
def _():
    channel_1 = 'NaV1.7'
    gene = 'SCN9A'
    location = 'DRG nociceptors'
    summary = f'{channel_1} (encoded by {gene}) is expressed in {location}'
    print(summary)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 💡 **Tip:** f-string quoting rules — this is where Alex hit a real bug (see exercise below). Inside an f-string, the quotes around dictionary keys must differ from the outer quotes. If your f-string uses double quotes (`f"..."`), use single quotes for dict keys inside braces (`{candidate['name']}`). Mixing them up causes a `SyntaxError` that's hard to spot. When in doubt, use single quotes inside and double quotes outside.
    """)
    return


@app.cell
def _():
    # You can do math inside the braces
    num_binders = 48
    passed_filter = 7

    print(f"{passed_filter} of {num_binders} candidates passed ({100 * passed_filter / num_binders:.1f}%)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `:.1f` is a format code — it means "one decimal place." You don't need to memorize these; just know they exist and ask when you need one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Loops: doing something to every item

    A `for` loop walks through a list one item at a time.
    """)
    return


@app.cell
def _():
    channels = ["NaV1.7", "NaV1.8", "NaV1.5", "KCNQ2"]

    for ch in channels:
        print(f"Designing binder for {ch}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Critical Python rule:** the indented block under the `for` line is what gets repeated. Indentation isn't cosmetic in Python — it's how the language knows what's inside the loop.

    VS Code will auto-indent for you after a colon (`:`), so this usually just works.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** Mutable default arguments are a classic Python trap. Never write `def process_data(results=[])`. If you use a list or dict as a default argument, Python creates it *once* and reuses it across all calls — so data from one call leaks into the next. Instead, use `None` and create the list inside the function:
    > ```python
    > def process_data(results=None):
    >     if results is None:
    >         results = []
    > ```
    > This won't bite you today, but it will the first time Claude generates a function with a mutable default. Now you'll catch it.
    """)
    return


@app.cell
def _():
    # Combine loops with conditionals
    channels_1 = ['NaV1.7', 'NaV1.8', 'NaV1.5', 'KCNQ2', 'KCNQ3']
    nav_channels = []
    for ch_1 in channels_1:
        if ch_1.startswith('NaV'):
            nav_channels.append(ch_1)
    print(f'Sodium channels: {nav_channels}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Read that code out loud: *"For each channel in channels, if it starts with 'NaV', add it to the nav_channels list."*

    Good Python reads almost like English.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Functions: reusable recipes

    A function packages up code so you can reuse it. Like a protocol — define it once, run it many times.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why functions?** Every reusable analysis — calculating dF/F from a calcium trace, filtering binder candidates by affinity, formatting a screening report — becomes a function. When Claude writes code for you, it structures it as functions. Understanding `def` and `return` means you can read, test, and trust that code.
    """)
    return


@app.cell
def _():
    def describe_target(channel, gene, region):
        """Generate a one-line description of a binder target."""
        return f"{channel} ({gene}) — targeting {region}"

    # Use it
    print(describe_target("NaV1.7", "SCN9A", "C-terminus"))
    print(describe_target("NaV1.8", "SCN10A", "interdomain loop I-II"))
    print(describe_target("KCNQ2", "KCNQ2", "N-terminus"))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `def` keyword defines the function. The `return` keyword sends a value back. The triple-quoted string is a **docstring** — a built-in way to document what the function does.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 🧪 Exercise: Build a binder candidate record

    Your turn. In the cell below:

    1. Create a dictionary called `candidate` with these keys:
       - `"name"` — make up a binder name (e.g., `"DNB-Nav17-001"`)
       - `"target_channel"` — which channel it targets
       - `"binding_region"` — where on the channel (C-terminus, extracellular loop, etc.)
       - `"effector"` — what payload it carries (E3 ligase, deubiquitinase, etc.)
       - `"predicted_kd_nm"` — a made-up binding affinity in nanomolar

    2. Print a formatted summary using an f-string, something like:
       `"DNB-Nav17-001 targets NaV1.7 C-terminus with E3 ligase payload (predicted Kd: 12.5 nM)"`

    Don't overthink it — just get something that runs.
    """)
    return


@app.cell
def _():
    # Alex's first attempt (kept for reference):
    # print(f"{candidate['name'] targets {candidate['target_channel']} at the {candidate["binding_region"]}}")
    #
    # Two bugs:
    #   1. Missing closing } after candidate['name']
    #   2. Double quotes around "binding_region" clash with the outer f-string quotes

    candidate = {
        "name": "DNB001",
        "target_channel": "NaV1.7",
        "binding_region": "C-terminal",
        "effector": "CRBN",
        "predicted_kd_nm": 5.0   # note: a number, not a string — so we can do math with it later
    }

    print(f"{candidate['name']} targets {candidate['target_channel']} at the {candidate['binding_region']} with {candidate['effector']} payload (predicted Kd: {candidate['predicted_kd_nm']} nM)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 🧪 Exercise: Filter a list of candidates

    Here's a list of candidates with their predicted affinities. Write a loop that prints only the ones with Kd below 20 nM.
    """)
    return


app._unparsable_cell(
    r"""
    ---

    ## Edit Log

    - 2026-03-24: Created notebook with initial content
    - 2026-03-25: Fixed exercise 1 f-string bugs, added corrected version with Alex's attempt preserved
    - 2026-03-25: Fixed exercise 2 loop bugs, added corrected version with Alex's attempt preserved
    - 2026-03-25: Added "Why this matters" rationale section
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: Added standardized callouts and decision frameworks
    """,
    name="_"
)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - **Variables** — store values with meaningful names ([Python docs: Data Types](https://docs.python.org/3/library/stdtypes.html))
    - **Types** — strings, numbers, booleans
    - **Lists** — ordered collections (`[]`) ([Python docs: Lists](https://docs.python.org/3/tutorial/introduction.html#lists))
    - **Dictionaries** — labeled records (`{}`) ([Python docs: Dictionaries](https://docs.python.org/3/tutorial/datastructures.html#dictionaries))
    - **f-strings** — embed variables in text ([Python docs: Formatted String Literals](https://docs.python.org/3/tutorial/inputoutput.html#formatted-string-literals))
    - **Loops** — do something for every item
    - **Conditionals** — `if` to make decisions
    - **Functions** — reusable code with `def`

    That's a real foundation. Next notebook, we'll use these building blocks to read and work with actual files — the kind of data you deal with every day.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Think Python, Chapter 1**: [The Way of the Program](https://allendowney.github.io/ThinkPython/chap01.html) — introduces what programming is and how to think about it; covers running your first Python code
    - **Think Python, Chapter 2**: [Variables and Statements](https://allendowney.github.io/ThinkPython/chap02.html) — variables, assignment, types, and expressions in depth
    - **Think Python, Chapter 5**: [Conditionals and Recursion](https://allendowney.github.io/ThinkPython/chap05.html) — `if`/`else` logic and boolean expressions
    - **Think Python, Chapter 6**: [Return Values](https://allendowney.github.io/ThinkPython/chap06.html) — how functions return values and why that matters
    - **Think Python, Chapter 7**: [Iteration](https://allendowney.github.io/ThinkPython/chap07.html) — `for` and `while` loops in detail
    - [Python Official Tutorial — Sections 3-5](https://docs.python.org/3/tutorial/introduction.html) — the official introduction to Python data types, control flow, and data structures
    - [Python Built-in Functions Reference](https://docs.python.org/3/library/functions.html) — documentation for `print()`, `len()`, `type()`, `range()`, and all other built-ins used in this notebook
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Pre-Flight Check](../00-getting-started/02-preflight-check.py) | [Module Index](../README.md) | [Next: Working with Files \u2192](02-working-with-files.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-24: Created notebook with initial content
    - 2026-03-25: Fixed exercise 1 f-string bugs, added corrected version with Alex's attempt preserved
    - 2026-03-25: Fixed exercise 2 loop bugs, added corrected version with Alex's attempt preserved
    - 2026-03-25: Added "Why this matters" rationale section
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

