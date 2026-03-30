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
    # Module 6.1: Decomposition and Design

    ## How to Think About Building Tools for Your Research

    You're not becoming a software engineer. But when you ask Claude to build something for you — a screening pipeline, a data analysis tool, a literature monitor — you need to think clearly about **what** you want built and **how** the pieces fit together.

    This is exactly the same skill you already use in experimental design:

    | Lab Thinking | Software Thinking |
    |---|---|
    | What's the question? | What's the goal? |
    | What samples do I need? | What data goes in? |
    | What's the protocol? | What processing happens? |
    | What do I measure? | What comes out? |
    | What controls do I need? | How do I know it's correct? |

    This notebook teaches you to **decompose problems into components** so you can give Claude clear instructions and evaluate what it builds.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Setup & Best Practices for Claude Code](../05-mastering-claude-code/04-setup-and-best-practices.py) | [Module Index](../README.md) | [Next: Evaluating and Debugging Code \u2192](02-evaluating-and-debugging.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - When you ask Claude to "build me a screening pipeline for NaV1.7 binder candidates," the quality of the result depends entirely on how well you decompose the problem. Vague instructions produce vague code; structured decomposition produces working tools.
    > - Your binder design workflow has natural components (RFdiffusion, ProteinMPNN, AlphaFold validation, experimental filtering) -- decomposition is how you turn that into an automated pipeline instead of a series of manual steps.
    > - Every time you tell Claude "this isn't what I wanted," it's usually because you skipped the decomposition step. Spending 5 minutes defining inputs, outputs, and processing steps saves 30 minutes of back-and-forth.
    > - This is the same skill as experimental design -- you already decompose complex assays into steps with defined inputs and outputs. This notebook translates that instinct into software thinking.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Input -> Process -> Output

    Every piece of useful software — from a one-line script to a massive application — follows the same fundamental pattern:

    ```
    INPUT  -->  PROCESS  -->  OUTPUT
    ```

    This is identical to how you think about an assay:

    - **Calcium imaging**: cells on coverslip -> apply compound + image -> fluorescence traces
    - **RNA-seq**: tissue sample -> extract + sequence + align -> count matrix
    - **Behavioral assay**: mouse + stimulus -> measure response -> withdrawal latency

    When you're telling Claude what to build, always start by defining these three things.

    Let's see this in code:
    """)
    return


@app.cell
def _():
    # A simple Input -> Process -> Output example
    # Goal: convert calcium imaging fluorescence values to delta-F/F0

    import numpy as np

    # INPUT: raw fluorescence trace (simulated)
    np.random.seed(42)
    raw_fluorescence = 500 + np.random.normal(0, 10, 100)  # baseline ~500 AU
    # Simulate a calcium transient at frame 50
    raw_fluorescence[50:65] += np.array([20, 80, 150, 200, 180, 140, 100, 70, 45, 30, 20, 12, 8, 4, 2])

    # PROCESS: calculate delta-F/F0
    baseline_frames = raw_fluorescence[:20]  # first 20 frames as baseline
    f0 = np.mean(baseline_frames)
    delta_f_over_f0 = (raw_fluorescence - f0) / f0

    # OUTPUT: normalized trace
    print(f"Baseline F0: {f0:.1f} AU")
    print(f"Peak delta-F/F0: {delta_f_over_f0.max():.2f}")
    print(f"Output shape: {delta_f_over_f0.shape}")
    return (np,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice how even this tiny piece of code has clear Input, Process, and Output sections. When you ask Claude to build something, describe it in exactly these terms:

    > "I need a script that takes **raw calcium imaging CSV files** (input), **calculates delta-F/F0 using the first 20 frames as baseline** (process), and **produces a summary table with peak responses per cell** (output)."

    That's a clear specification. Compare it to:

    > "I need help analyzing my calcium imaging data."

    The first version will get you working code on the first try. The second will require 5 rounds of clarification.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** Decomposition quality determines Claude's output quality. When you give Claude a vague, monolithic request ("build me a screening pipeline"), you get generic, often wrong code. When you decompose the task into components with clear inputs and outputs, each component is small enough for Claude to get right on the first try. The 5 minutes you spend decomposing saves 30 minutes of debugging and back-and-forth.

    > **Tip:** For every component you define, think explicitly about its **input** and **output**. Write them down before asking Claude to build anything. "This function takes a DataFrame with columns [binder_id, sequence, kd_nM] and returns a DataFrame with an added column [composite_score]." That level of specificity is what turns a vague request into working code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Breaking Problems into Components

    Real research tasks are too complex to describe as a single Input -> Process -> Output. You need to **decompose** them.

    Think about how you design a multi-day experiment. You don't think of it as one thing — you break it into steps, where each step feeds into the next:

    ```
    Day 1: Culture DRG neurons
    Day 2: Transfect with binder constructs
    Day 3: Load calcium dye, run imaging
    Day 4: Analyze traces, generate figures
    ```

    Each step has its own inputs, process, and outputs. And critically, **the output of one step becomes the input of the next**.

    Software decomposition works the same way.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Decomposition Diagram: Research Pipeline as Components

    ```mermaid
    graph LR
        subgraph "Component 1"
            A1["INPUT<br>Raw data files"] --> A2["PROCESS<br>Load & validate"] --> A3["OUTPUT<br>Clean DataFrame"]
        end
        subgraph "Component 2"
            B1["INPUT<br>Clean DataFrame"] --> B2["PROCESS<br>Compute properties"] --> B3["OUTPUT<br>Enriched table"]
        end
        subgraph "Component 3"
            C1["INPUT<br>Enriched table"] --> C2["PROCESS<br>Filter & score"] --> C3["OUTPUT<br>Ranked hits"]
        end
        subgraph "Component 4"
            D1["INPUT<br>Ranked hits"] --> D2["PROCESS<br>Visualize & report"] --> D3["OUTPUT<br>Figures + report"]
        end

        A3 --> B1
        B3 --> C1
        C3 --> D1

        style A1 fill:#4878CF,color:#fff
        style A2 fill:#55A868,color:#fff
        style A3 fill:#FDB863,color:#000
        style B1 fill:#4878CF,color:#fff
        style B2 fill:#55A868,color:#fff
        style B3 fill:#FDB863,color:#000
        style C1 fill:#4878CF,color:#fff
        style C2 fill:#55A868,color:#fff
        style C3 fill:#FDB863,color:#000
        style D1 fill:#4878CF,color:#fff
        style D2 fill:#55A868,color:#fff
        style D3 fill:#FDB863,color:#000
    ```

    Each component is self-contained with defined inputs and outputs. The output of one component becomes the input of the next. This is the key principle: **if you can describe the input, process, and output of each component, you can build (or ask Claude to build) the whole pipeline one piece at a time.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Practical Example: Binder Candidate Screening Pipeline

    Let's decompose a real task: **"Screen 100 protein binder candidates for NaV1.7 and rank them."**

    If you just told Claude "build me a binder screening pipeline," you'd get something generic. Instead, let's think through the components:
    """)
    return


@app.cell
def _():
    # Let's map out the binder screening pipeline as components
    # Each component is a dictionary with input, process, output
    pipeline_components = [{'name': '1. Load Candidates', 'input': 'CSV file with 100 binder sequences and metadata', 'process': 'Read file, validate sequences, check for duplicates', 'output': 'Clean list of unique binder candidates'}, {'name': '2. Compute Properties', 'input': 'Clean list of binder candidates', 'process': 'Calculate MW, pI, hydrophobicity, predicted solubility', 'output': 'Table of candidates with computed properties'}, {'name': '3. Filter by Criteria', 'input': 'Table with computed properties', 'process': 'Remove candidates outside acceptable ranges (MW, solubility, etc.)', 'output': 'Filtered table of viable candidates'}, {'name': '4. Score and Rank', 'input': 'Filtered candidates with properties', 'process': 'Apply weighted scoring (binding affinity prediction, selectivity, druglikeness)', 'output': 'Ranked list with composite scores'}, {'name': '5. Generate Report', 'input': 'Ranked list with scores', 'process': 'Create summary stats, visualizations, top-10 detail cards', 'output': 'PDF/HTML report with figures and recommendations'}]
    for _comp in pipeline_components:
        print(f"{'=' * 60}")
        print(f"  {_comp['name']}")
        print(f"  IN:  {_comp['input']}")
        print(f"  DO:  {_comp['process']}")
        print(f"  OUT: {_comp['output']}")
    # Print the pipeline
    print(f"{'=' * 60}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Data Flow Diagram: Binder Screening Pipeline

    ```mermaid
    flowchart TD
        CSV["CSV file<br>100 binder sequences<br>+ metadata"] --> LOAD["Load Candidates<br>Read, validate,<br>remove duplicates"]
        LOAD --> CLEAN["Clean list<br>95 unique candidates<br>(DataFrame)"]
        CLEAN --> PROPS["Compute Properties<br>MW, pI, hydrophobicity,<br>predicted solubility"]
        PROPS --> ENRICHED["Enriched table<br>95 rows x 8 columns"]
        ENRICHED --> FILTER["Filter by Criteria<br>Kd < 100nM<br>Solubility > 0.3<br>Selectivity > 5x"]
        FILTER --> VIABLE["Viable candidates<br>~20 remaining"]
        VIABLE --> SCORE["Score & Rank<br>Weighted composite:<br>40% affinity<br>35% selectivity<br>25% druglikeness"]
        SCORE --> RANKED["Ranked list<br>with composite scores"]
        RANKED --> REPORT["Generate Report<br>Summary stats<br>Visualizations<br>Top-10 detail cards"]
        REPORT --> OUTPUT["PDF/HTML report<br>+ figures/"]

        style CSV fill:#4878CF,color:#fff
        style CLEAN fill:#FDB863,color:#000
        style ENRICHED fill:#FDB863,color:#000
        style VIABLE fill:#FDB863,color:#000
        style RANKED fill:#FDB863,color:#000
        style OUTPUT fill:#55A868,color:#fff
        style LOAD fill:#eee,color:#000
        style PROPS fill:#eee,color:#000
        style FILTER fill:#eee,color:#000
        style SCORE fill:#eee,color:#000
        style REPORT fill:#eee,color:#000
    ```

    Notice how the data transforms at each step: CSV file becomes a DataFrame, which gets enriched with new columns, then filtered down to fewer rows, then scored and ranked. Tracking these transformations is how you debug pipelines -- if the output of step 3 looks wrong, you inspect the data at the boundary between steps 2 and 3.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Why Decomposition Matters When Working with Claude

    When you decompose a task like this, you can:

    1. **Ask Claude to build one component at a time** — each one is small enough to get right
    2. **Test each component independently** — if step 3 gives wrong results, you know where to look
    3. **Swap out components** — want a different scoring method? Replace step 4 without touching anything else
    4. **Explain what you need clearly** — "Build me step 2: it takes a pandas DataFrame with a 'sequence' column and adds columns for MW, pI, and hydrophobicity"

    This is exactly how you think about modular experimental protocols — you can swap out the calcium dye without changing your analysis pipeline.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Data Flow: How Information Moves Through a Pipeline

    Once you have components, you need to understand how data flows between them. This is like tracking your samples through a protocol — at each step, you need to know what you have and what format it's in.

    Let's build a small working pipeline to see data flow in action:
    """)
    return


@app.cell
def _(np):
    import pandas as pd
    np.random.seed(42)
    n_candidates = 20
    # Simulate binder candidate data
    candidates = pd.DataFrame({'binder_id': [f'NaV17-B{i:03d}' for i in range(1, n_candidates + 1)], 'sequence_length': np.random.randint(80, 200, n_candidates), 'predicted_kd_nm': np.random.lognormal(mean=3, sigma=1.5, size=n_candidates).round(1), 'predicted_solubility': np.random.uniform(0.1, 1.0, n_candidates).round(3), 'nav17_selectivity_ratio': np.random.uniform(0.5, 50, n_candidates).round(1)})
    print('STEP 1 OUTPUT — Raw candidate data:')
    print(f'Shape: {candidates.shape}')
    print(candidates.head())
    return candidates, pd


@app.cell
def _(candidates):
    # STEP 2: Filter candidates
    # INPUT: candidates DataFrame from step 1

    # Define criteria
    MAX_KD = 100  # nm — we want tight binders
    MIN_SOLUBILITY = 0.3  # arbitrary scale
    MIN_SELECTIVITY = 5.0  # at least 5x selective for NaV1.7 over other NaV subtypes

    filtered = candidates[
        (candidates["predicted_kd_nm"] <= MAX_KD) &
        (candidates["predicted_solubility"] >= MIN_SOLUBILITY) &
        (candidates["nav17_selectivity_ratio"] >= MIN_SELECTIVITY)
    ].copy()

    print(f"STEP 2 OUTPUT — After filtering:")
    print(f"Started with {len(candidates)} candidates, kept {len(filtered)}")
    print(f"Removed {len(candidates) - len(filtered)} candidates that didn't meet criteria")
    print()
    print(filtered)
    return (filtered,)


@app.cell
def _(filtered, pd):
    # STEP 3: Score and rank
    # INPUT: filtered DataFrame from step 2

    # Normalize each property to 0-1 scale, then combine with weights
    def normalize(series, lower_is_better=False):
        """Scale values to 0-1. If lower_is_better, invert."""
        min_val, max_val = series.min(), series.max()
        if max_val == min_val:
            return pd.Series(0.5, index=series.index)
        normed = (series - min_val) / (max_val - min_val)
        return 1 - normed if lower_is_better else normed

    # Apply scoring weights
    weights = {
        "affinity_score": 0.4,      # binding affinity matters most
        "selectivity_score": 0.35,  # selectivity is critical for NaV1.7
        "solubility_score": 0.25,   # practical but less important
    }

    filtered["affinity_score"] = normalize(filtered["predicted_kd_nm"], lower_is_better=True)
    filtered["selectivity_score"] = normalize(filtered["nav17_selectivity_ratio"])
    filtered["solubility_score"] = normalize(filtered["predicted_solubility"])

    filtered["composite_score"] = (
        weights["affinity_score"] * filtered["affinity_score"] +
        weights["selectivity_score"] * filtered["selectivity_score"] +
        weights["solubility_score"] * filtered["solubility_score"]
    ).round(3)

    ranked = filtered.sort_values("composite_score", ascending=False).reset_index(drop=True)
    ranked.index += 1  # rank starting at 1
    ranked.index.name = "rank"

    print("STEP 3 OUTPUT — Ranked candidates:")
    print(ranked[["binder_id", "predicted_kd_nm", "nav17_selectivity_ratio", 
                  "predicted_solubility", "composite_score"]])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice how each step:
    - Takes a **clearly defined input** (a DataFrame with known columns)
    - Performs a **specific transformation**
    - Produces a **clearly defined output** that feeds into the next step

    This is **data flow**. When something goes wrong, you can inspect the data at each step boundary to find where things broke — just like checking your samples at each stage of a protocol.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. What Makes Code "Good" (Even If You Didn't Write It)

    When Claude generates code for you, you need to evaluate it before trusting it with your research data. Here's what to look for — think of it like evaluating a protocol from another lab.

    ### The Key Qualities

    1. **Readability** — Can you follow what it does? (Like a well-written methods section)
    2. **Single responsibility** — Does each piece do ONE thing? (Like each step in a protocol)
    3. **Clear naming** — Are variables and functions named for what they represent? (Like labeling your tubes)
    4. **No magic numbers** — Are thresholds and parameters explained, not just hardcoded?

    Let's see the difference:
    """)
    return


@app.cell
def _(np):
    # === THE MESSY VERSION ===
    # Would you trust this with your data?
    def proc(d):
        x = d[:20]
        m = np.mean(x)
        r = (d - m) / m
        p = []
        for i in range(len(r)):
            if r[i] > 0.15:
                if i > 0 and r[i - 1] <= 0.15:
                    p.append(i)
        return (r, p)
    # What does this do? What is 0.15? What are p and r?
    # If this gives wrong results, where do you start looking?
    print("Messy version defined (don't use this)")
    return


@app.cell
def _(np):
    # === THE CLEAN VERSION ===
    # Same functionality, but you can actually understand and trust it
    BASELINE_FRAMES = 20
    RESPONSE_THRESHOLD = 0.15

    # Configuration — easy to find and change
    def calculate_delta_f_over_f0(raw_trace, n_baseline_frames=BASELINE_FRAMES):  # Number of frames to use for F0 calculation
        """Convert raw fluorescence trace to delta-F/F0.  # delta-F/F0 threshold for calling a calcium transient
    
        Uses the mean of the first n_baseline_frames as F0.
        Returns normalized trace where 0 = baseline and 1.0 = 100% increase.
        """
        baseline = raw_trace[:n_baseline_frames]
        f0 = np.mean(baseline)
        delta_f_f0 = (raw_trace - f0) / f0
        return delta_f_f0

    def find_transient_onsets(delta_f_trace, threshold=RESPONSE_THRESHOLD):
        """Find frames where calcium transients begin.
    
        A transient onset is where the trace crosses above threshold
        (previous frame below, current frame at or above).
        """
        onset_frames = []
        for frame in range(1, len(delta_f_trace)):
            crossed_threshold = delta_f_trace[frame] > threshold and delta_f_trace[frame - 1] <= threshold
            if crossed_threshold:
                onset_frames.append(frame)
        return onset_frames
    np.random.seed(42)
    raw_trace = 500 + np.random.normal(0, 10, 100)
    raw_trace[50:65] += np.array([20, 80, 150, 200, 180, 140, 100, 70, 45, 30, 20, 12, 8, 4, 2])
    normalized = calculate_delta_f_over_f0(raw_trace)
    onsets = find_transient_onsets(normalized)
    print(f'Found {len(onsets)} calcium transient(s)')
    print(f'Onset frame(s): {onsets}')
    # Use it
    print(f'Peak delta-F/F0: {normalized.max():.3f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Functions: The Building Blocks

    Functions are how you package "one step" of a pipeline. Think of a function like a protocol step: it has defined inputs, does one thing, and produces a defined output.

    **Reference**: See [*Think Python*, Chapter 3: Functions](https://allendowney.github.io/ThinkPython/chap03.html) for a deeper introduction to writing and using functions, and [Chapter 4: Program Development](https://allendowney.github.io/ThinkPython/chap04.html) for how to plan and build programs incrementally.

    You don't need to become an expert at writing functions -- Claude will write them for you. But you need to understand enough to:
    - Tell Claude what functions to create
    - Read the functions Claude gives you
    - Know when a function is doing too much
    """)
    return


@app.cell
def _(np, pd):
    # Good function: does ONE thing, clear name, clear inputs/outputs

    def filter_responsive_cells(traces_df, threshold=0.15, min_duration_frames=3):
        """
        Identify cells that show a calcium response above threshold.
    
        Parameters:
            traces_df: DataFrame where each column is a cell's delta-F/F0 trace
            threshold: minimum delta-F/F0 to count as responsive
            min_duration_frames: response must exceed threshold for this many consecutive frames
    
        Returns:
            List of column names (cell IDs) that are responsive
        """
        responsive_cells = []
    
        for cell_id in traces_df.columns:
            trace = traces_df[cell_id].values
            above_threshold = trace > threshold
        
            # Check for consecutive frames above threshold
            consecutive_count = 0
            for is_above in above_threshold:
                if is_above:
                    consecutive_count += 1
                    if consecutive_count >= min_duration_frames:
                        responsive_cells.append(cell_id)
                        break
                else:
                    consecutive_count = 0
    
        return responsive_cells


    # Test it with simulated data
    np.random.seed(42)
    n_frames = 100
    n_cells = 10

    # Create simulated traces (some responsive, some not)
    traces = pd.DataFrame({
        f"cell_{i}": np.random.normal(0, 0.05, n_frames) 
        for i in range(n_cells)
    })

    # Make cells 2, 5, and 7 responsive (add transients)
    for cell_idx in [2, 5, 7]:
        traces.iloc[50:58, cell_idx] += 0.3

    responsive = filter_responsive_cells(traces)
    print(f"Responsive cells: {responsive}")
    print(f"Response rate: {len(responsive)}/{n_cells} = {len(responsive)/n_cells:.0%}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Decision point: Notebook vs script vs command-line tool**
    >
    > | Format | Pros | Cons | Use when |
    > |--------|------|------|----------|
    > | **marimo Notebook** (`.py`) | Shows your work, great for exploration, inline plots, mixes explanation with code, reactive execution, git-friendly | Newer tool with smaller ecosystem than Jupyter | One-off exploration, generating figures, documenting an analysis for yourself or a collaborator |
    > | **Python Script** (`.py`) | Repeatable, can run from terminal, easy to version control, can take arguments | No inline visualization, harder to iterate interactively | Anything you'll run more than twice: batch processing, data pipelines, regular analyses |
    > | **Command-line Tool** (`.py` with argparse) | Reusable by others, configurable via flags, can be scheduled | More setup, overkill for simple tasks | Lab-wide tools, automated pipelines, anything with variable inputs (different files, thresholds, targets) |
    >
    > **Rule of thumb:** Start in a notebook to explore and prototype. Once the analysis works, ask Claude to "turn this into a script I can run from the command line." If multiple people need it or inputs vary, add command-line arguments.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. When to Use a Notebook vs. a Script vs. a Tool

    This is a practical decision you'll make frequently. Here's a simple guide:

    ### marimo Notebook (`.py`)
    **Use for**: Exploration, one-off analyses, generating figures, documenting your thought process

    - Like a lab notebook entry -- shows your work
    - Great for: "Let me look at this RNA-seq dataset and figure out what's interesting"
    - Not great for: Things you'll run repeatedly or on a schedule

    ### Python Script (`.py`)
    **Use for**: Repeatable analyses, batch processing, anything you'll run more than twice

    - Like a finalized protocol -- reliable, repeatable
    - Great for: "Process all 50 calcium imaging files from this week's experiments"
    - Can be run from the command line: `python analyze_traces.py data/experiment_001/`

    ### Command-Line Tool
    **Use for**: Something you or your lab will use routinely, with different inputs each time

    - Like a piece of lab equipment -- standardized, with knobs to adjust
    - Great for: "Score any set of binder candidates against NaV1.7"
    - Has options/flags: `python score_binders.py --target NaV1.7 --input candidates.csv --output ranked.csv`

    **References**: See [Missing Semester Lecture 4: Data Wrangling](https://missing.csail.mit.edu/2020/data-wrangling/) for using shell tools to process data, and Lectures 1-2 for running scripts and building command-line tools. For deeper thinking about software organization, John Ousterhout's *A Philosophy of Software Design* (Yaknyam Press, 2018) is an excellent resource on managing complexity -- its core idea that "complexity is anything related to the structure of a software system that makes it hard to understand" applies directly to research pipelines.

    ### Decision Flowchart

    ```
    Will you run this more than twice?
      NO  --> Notebook
      YES --> Will different people use it, or will you use it with different inputs?
                NO  --> Script
                YES --> Command-line tool
    ```
    """)
    return


@app.cell
def _(pd):
    # Here's what a transition from notebook exploration to a script might look like.
    # In a notebook, you'd explore interactively:
    import matplotlib.pyplot as plt

    def identify_pain_related_degs(counts_df, condition_col, control_label, treatment_label, fold_change_threshold=2.0, pvalue_threshold=0.05):
        """
    # Simulate: you explored RNA-seq data in a notebook and found interesting genes
    # Now you want to package the analysis as a reusable function
        Identify differentially expressed genes from a count matrix.
        This is a simplified demonstration — real DEG analysis uses DESeq2 or similar.
    
        Parameters:
            counts_df: DataFrame with genes as rows, samples as columns
            condition_col: which column in sample metadata indicates condition
            control_label: label for control condition
            treatment_label: label for treatment condition  
            fold_change_threshold: minimum fold change to call as DE
            pvalue_threshold: maximum p-value (simplified — use proper stats in practice)
    
        Returns:
            DataFrame of differentially expressed genes with fold changes
        """
        print(f'Would analyze {counts_df.shape[0]} genes across conditions:')
        print(f'  Control: {control_label}')
        print(f'  Treatment: {treatment_label}')
        print(f'  FC threshold: {fold_change_threshold}')
        print(f'  P-value threshold: {pvalue_threshold}')  # This is a simplified placeholder to illustrate the concept
        return pd.DataFrame()  # Real analysis would use proper statistical methods
    # In a notebook, you'd call this interactively and examine results.
    # Once you're happy with the logic, you'd ask Claude:
    # "Turn this into a script I can run from the command line on any count matrix."
    print('Function defined — ready to be extracted into a script')  # placeholder
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. Exercise: Decompose a Research Workflow

    Now it's your turn. Let's decompose a realistic research workflow into components.

    ### The Task: Daily Literature Digest

    You want a tool that:
    - Checks for new papers relevant to your research (NaV1.7/1.8 binders, KCNQ2/3, targeted protein degradation)
    - Filters out irrelevant ones
    - Summarizes the key findings
    - Sends you a daily email or saves a report

    **Your job**: Fill in the components below. For each one, describe:
    1. What goes **in** (input)
    2. What it **does** (process)
    3. What comes **out** (output)
    """)
    return


@app.cell
def _():
    # EXERCISE: Fill in the blanks for each component
    # Think about what data flows between each step
    literature_digest_pipeline = [{'name': '1. Fetch New Papers', 'input': '___', 'process': '___', 'output': '___'}, {'name': '2. Filter Relevant Papers', 'input': '___', 'process': '___', 'output': '___'}, {'name': '3. Summarize Papers', 'input': '___', 'process': '___', 'output': '___'}, {'name': '4. Format and Deliver Report', 'input': '___', 'process': '___', 'output': '___'}]
    print('My Literature Digest Pipeline')
    print('=' * 50)
    for _comp in literature_digest_pipeline:
        print(f"\n{_comp['name']}")  # What does this step need to start? (hint: search terms, date range, API)
        print(f"  IN:  {_comp['input']}")  # What does it do? (hint: query a database)
        print(f"  DO:  {_comp['process']}")  # What does it produce? (hint: list of...)
    # Print your pipeline design
        print(f"  OUT: {_comp['output']}")  # What comes from step 1?  # How do you decide what's relevant?  # What's left after filtering?  # What does the summarizer need?  # How are summaries generated?  # What format is the summary in?  # What needs to be formatted?  # How is it formatted and sent?  # What's the final deliverable?
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Bonus Questions to Think About

    After filling in the pipeline above, consider:

    1. **What could go wrong at each step?** (e.g., the paper database API is down, a paper has no abstract)
    2. **Which step would you build first?** (hint: start with the one that has the simplest input)
    3. **How would you test each step?** (hint: use known papers to verify step 1 works)
    4. **Where would you use an LLM?** (hint: which step benefits from language understanding?)

    When you're ready to actually build this, you could tell Claude:

    > "I want to build a daily literature digest tool. Here are the components I've identified: [paste your pipeline]. Let's start with component 1: fetching new papers from PubMed. It should take a list of search terms and a date range, query the PubMed API, and return a list of papers with title, authors, abstract, and DOI."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Key Takeaways

    1. **Always think Input -> Process -> Output** before asking Claude to build anything
    2. **Decompose big tasks into small components** — each one should be describable in one sentence
    3. **Data flows between components** — know what format data is in at each step
    4. **Good code is readable code** — ask Claude for clear names, docstrings, and named constants
    5. **Choose the right format** — notebook for exploration, script for repetition, tool for sharing

    ### What to Say to Claude

    Instead of: *"Build me a binder screening tool"*

    Say: *"I need a binder screening pipeline with these components: (1) load candidates from CSV, (2) compute molecular properties, (3) filter by solubility > 0.3 and Kd < 100nM, (4) rank by weighted score, (5) generate a report. Let's start with component 1."*

    The decomposition IS the specification.
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
    - 2026-03-25: QA pass — removed duplicate Section 5 (Functions) and Section 6 (Notebook vs Script) cells
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **[Think Python, Chapter 3: Functions](https://allendowney.github.io/ThinkPython/chap03.html)** -- Defining, calling, and composing functions in Python.
    - **[Think Python, Chapter 4: Program Development](https://allendowney.github.io/ThinkPython/chap04.html)** -- Incremental development, planning, and building programs step by step.
    - **[Missing Semester Lecture 4: Data Wrangling](https://missing.csail.mit.edu/2020/data-wrangling/)** -- Shell-based data processing, piping, and transforming data between formats.
    - **Ousterhout, J. (2018). *A Philosophy of Software Design.* Yaknyam Press.** -- A concise book on managing complexity in software. Its principles (deep modules, information hiding, reducing cognitive load) apply directly to designing research pipelines.
    - **[Python Official Tutorial: Defining Functions](https://docs.python.org/3/tutorial/controlflow.html#defining-functions)** -- The standard reference for function syntax, arguments, and return values.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [← Previous: Setup & Best Practices for Claude Code](../05-mastering-claude-code/04-setup-and-best-practices.py) | [Module Index](../README.md) | [Next: Evaluating and Debugging Code →](02-evaluating-and-debugging.py)
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
    - 2026-03-25: QA pass — removed duplicate Section 5 (Functions) and Section 6 (Notebook vs Script) cells
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

