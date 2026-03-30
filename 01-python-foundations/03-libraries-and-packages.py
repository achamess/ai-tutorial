import marimo

__generated_with = "0.21.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import subprocess

    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 03: Libraries and Packages

    One of Python's superpowers is its ecosystem — tens of thousands of packages built by other people that you can use for free. Data analysis, plotting, statistics, machine learning, API calls — someone already wrote the hard parts.

    This notebook covers how to find, install, and use packages.

    > **References:**
    > - [Think Python — Chapter 15: Classes and Objects](https://allendowney.github.io/ThinkPython/chap15.html) (Objects and modules)
    > - [MIT Missing Semester — Lecture 4: Data Wrangling](https://missing.csail.mit.edu/2020/data-wrangling/) (Processing and transforming data with command-line and scripting tools)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Working with Files](02-working-with-files.py) | [Module Index](../README.md) | [Next: Data Structures in Practice \u2192](04-data-structures-in-practice.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - You don't write everything from scratch — and neither does Claude. When Claude generates analysis code, it uses libraries like pandas, numpy, and matplotlib. If you don't understand `import pandas as pd`, you can't read or trust what Claude produces.
    > - The `anthropic` package is how you'll call the Claude API from Python. Understanding how packages work means you can install and use any tool Claude suggests — from BioPython for sequence analysis to scipy for curve fitting your dose-response data.
    > - Every computational protein design tool in your pipeline (RFdiffusion, ProteinMPNN, AlphaFold2) is a Python package. Understanding imports and virtual environments is what lets you actually run them.
    > - numpy array operations are how calcium imaging traces, binding curves, and electrophysiology data get analyzed efficiently — one line instead of a hundred-iteration loop.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What are packages and why they matter

    A **package** (or **library**) is a bundle of pre-written Python code. Instead of writing everything from scratch, you import what you need.

    Analogy: You don't synthesize your own antibodies for every western blot. You buy validated ones from a supplier. Python packages work the same way — battle-tested tools you plug into your code.

    Here are the packages you'll use most in this tutorial:

    | Package | What it does | Your use case |
    |---------|-------------|---------------|
    | **pandas** | Tables and data manipulation | Analyzing screening results, RNA-seq data |
    | **numpy** | Fast math on arrays of numbers | Calcium imaging traces, numerical analysis |
    | **matplotlib** | Plotting and visualization | Dose-response curves, expression plots |
    | **seaborn** | Statistical plots (built on matplotlib) | Heatmaps, violin plots, pair plots |
    | **anthropic** | Claude API client | Sending prompts to Claude from Python |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Importing packages

    There are a few ways to import. Let's see them all.
    """)
    return


@app.cell
def _():
    # Style 1: Import the whole package
    import math

    print(math.sqrt(144))   # square root
    print(math.log10(1000)) # log base 10
    return


@app.cell
def _():
    # Style 2: Import specific things from a package
    from math import sqrt, pi

    print(sqrt(144))  # no need to write math.sqrt
    print(pi)
    return


@app.cell
def _():
    # Style 3: Import with an alias (nickname)
    # These aliases are universal conventions — everyone uses them
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt

    print(f"pandas version:  {pd.__version__}")
    print(f"numpy version:   {np.__version__}")
    return np, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Which style should you use?** For the big data science packages, always use the standard aliases:

    ```python
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    ```

    These are so universal that if you write `pd.read_csv()`, any Python user (or AI assistant) will immediately know what you mean.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 💡 **Tip:** Standard import aliases are a community convention — always use them. When you see `pd`, `np`, `plt`, or `sns` in code (whether from Claude, Stack Overflow, or a colleague), it always means `pandas`, `numpy`, `matplotlib.pyplot`, and `seaborn`. Using different aliases (like `import pandas as p`) will confuse every human and AI that reads your code. Memorize these four:
    > ```python
    > import pandas as pd
    > import numpy as np
    > import matplotlib.pyplot as plt
    > import seaborn as sns
    > ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph TB
        subgraph "How Python Imports Work"
            YOUR["YOUR CODE<br/><code>import pandas as pd</code>"]

            subgraph "Third-Party Packages (pip install)"
                PD["pandas"]
                NP["numpy"]
                PLT["matplotlib"]
                SNS["seaborn"]
                ANT["anthropic"]
            end

            subgraph "Standard Library (comes with Python)"
                CSV["csv"]
                JSON["json"]
                MATH["math"]
                PATH["pathlib"]
                OS["os"]
            end

            subgraph "Python Built-ins (always available)"
                PRINT["print()"]
                LEN["len()"]
                RANGE["range()"]
                TYPE["type()"]
            end

            YOUR --> PD
            YOUR --> NP
            YOUR --> CSV
            YOUR --> JSON
            YOUR --> PRINT
        end

        style YOUR fill:#cc4444,color:#fff
        style PD fill:#4488cc,color:#fff
        style NP fill:#4488cc,color:#fff
        style PLT fill:#4488cc,color:#fff
        style SNS fill:#4488cc,color:#fff
        style ANT fill:#4488cc,color:#fff
        style CSV fill:#44aa88,color:#fff
        style JSON fill:#44aa88,color:#fff
        style MATH fill:#44aa88,color:#fff
        style PATH fill:#44aa88,color:#fff
        style OS fill:#44aa88,color:#fff
        style PRINT fill:#cc8844,color:#fff
        style LEN fill:#cc8844,color:#fff
        style RANGE fill:#cc8844,color:#fff
        style TYPE fill:#cc8844,color:#fff
    ```

    Three layers of Python code you can use:
    - **Built-ins** (orange) -- always available, no import needed
    - **Standard library** (green) -- comes with Python, just `import` it
    - **Third-party packages** (blue) -- installed with `pip`, then `import`
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Quick tour: numpy — fast math on arrays

    NumPy is the foundation for all numerical computing in Python. Its core object is the **array** — like a Python list, but optimized for math.
    """)
    return


@app.cell
def _(np):
    trace = np.array([1.0, 1.02, 0.98, 1.01, 1.05, 1.8, 3.2, 4.1, 3.8, 2.9, 2.1, 1.6, 1.3, 1.1, 1.05, 1.02, 0.99, 1.01, 1.0, 0.98])
    print(f'Number of time points: {len(trace)}')
    # Calcium fluorescence ratios from a DRG neuron (mock data)
    # Each value is F/F0 at one time point during a calcium imaging experiment
    print(f'Baseline (mean of first 4): {trace[:4].mean():.3f}')
    print(f'Peak F/F0: {trace.max():.2f}')
    print(f'Peak time point: {trace.argmax()}')
    print(f'Mean: {trace.mean():.2f}')
    print(f'Std dev: {trace.std():.2f}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    NumPy lets you do math on entire arrays at once — no loops needed.

    - `trace.max()` — find the peak
    - `trace.argmax()` — find *where* the peak is
    - `trace[:4]` — grab the first 4 elements (slicing)
    - `trace[:4].mean()` — mean of those 4 elements
    """)
    return


@app.cell
def _(np):
    trace_1 = np.array([1.0, 1.02, 0.98, 1.01, 1.05, 1.8, 3.2, 4.1, 3.8, 2.9, 2.1, 1.6, 1.3, 1.1, 1.05, 1.02, 0.99, 1.01, 1.0, 0.98])
    baseline = trace_1[:4].mean()
    # Math on whole arrays — no loops
    delta_f = (trace_1 - baseline) / baseline
    print('Delta F/F0 values:')
    # Calculate delta F / F0 for every point at once
    print(np.round(delta_f, 3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use numpy vs. plain Python for math?
    >
    > | Option | Pros | Cons | Use when... |
    > |--------|------|------|-------------|
    > | **Plain Python** (`for` loops, `sum()`, `max()`) | No imports needed, readable, easy to debug | Slow for large arrays (100x-1000x slower), verbose for element-wise math | You have a few values, simple calculations, or non-numerical tasks |
    > | **NumPy** (`np.array`, vectorized operations) | Fast (C-optimized), concise array math (`trace - baseline`), built-in stats | Extra dependency, learning curve, less readable for non-array tasks | You have arrays of numbers: calcium traces, binding curves, time series, dose-response data, anything where you do the same math to every element |
    >
    > **Rule of thumb:** If you're doing math on a list of numbers longer than ~10 elements, use numpy. The `(trace - baseline) / baseline` syntax above would require a 5-line loop in plain Python.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That `(trace - baseline) / baseline` applied the formula to all 20 values simultaneously. In plain Python with lists, you'd need a loop. NumPy makes this kind of array math effortless.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Quick tour: matplotlib — plotting

    Matplotlib is Python's main plotting library. The syntax takes some getting used to, but once you know the basics, you can make any plot.
    """)
    return


@app.cell
def _(np, plt):
    time_s = np.arange(0, 20, 1)
    trace_2 = np.array([1.0, 1.02, 0.98, 1.01, 1.05, 1.8, 3.2, 4.1, 3.8, 2.9, 2.1, 1.6, 1.3, 1.1, 1.05, 1.02, 0.99, 1.01, 1.0, 0.98])
    plt.figure(figsize=(8, 4))
    # Mock calcium imaging data: time in seconds, F/F0 trace
    plt.plot(time_s, trace_2, color='#2563eb', linewidth=2)  # 0, 1, 2, ... 19 seconds
    plt.axhline(y=1.0, color='gray', linestyle='--', alpha=0.5, label='Baseline')
    plt.axvspan(4.5, 5.5, color='red', alpha=0.15, label='Capsaicin pulse')
    plt.xlabel('Time (s)')
    plt.ylabel('F / F₀')
    plt.title('DRG Neuron Calcium Response — TRPV1 Activation')
    plt.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The pattern is always:
    1. `plt.figure()` — create the canvas
    2. `plt.plot()` (or `.bar()`, `.scatter()`, etc.) — draw the data
    3. `plt.xlabel()`, `plt.ylabel()`, `plt.title()` — label things
    4. `plt.show()` — display the result

    You don't need to memorize every option. When you need to customize a plot, just describe what you want to Claude and it'll give you the code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Quick tour: pandas — data in tables

    We previewed pandas in the last notebook. Here's a bit more of what it can do.
    """)
    return


@app.cell
def _(pd):
    from pathlib import Path
    csv_file = Path.cwd() / '..' / '01-python-foundations' / 'sample_data' / 'binder_screening.csv'
    csv_file = Path.cwd() / 'sample_data' / 'binder_screening.csv'
    # Read the binder screening CSV
    df = pd.read_csv(csv_file)
    # If running from the same directory as notebook 02:
    print(f'Shape: {df.shape[0]} rows x {df.shape[1]} columns\n')
    print('Columns:', list(df.columns))
    print()
    df.head()
    return Path, df


@app.cell
def _(df):
    # Group by target and get average Kd
    summary = df.groupby("target")["predicted_kd_nm"].agg(["mean", "min", "count"])
    summary.columns = ["Mean Kd (nM)", "Best Kd (nM)", "# Candidates"]
    summary
    return


@app.cell
def _(df):
    # Sort by affinity (best first)
    df.sort_values("predicted_kd_nm").head(5)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    We'll go deep on pandas in Module 06 (Data Skills). For now, just notice how much you can do with very little code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## pip: installing packages

    Packages come from the **Python Package Index** ([PyPI](https://pypi.org), pronounced "pie-pee-eye"). You install them with `pip`.

    We already installed the core packages when setting up this tutorial, but here's how it works:

    ```bash
    # Install a single package
    pip install pandas

    # Install a specific version
    pip install pandas==2.2.0

    # Install multiple packages
    pip install pandas numpy matplotlib

    # See what's installed
    pip list

    # See what's installed and save it to a file (for reproducibility)
    pip freeze > requirements.txt
    ```

    > **Why virtual environments matter** ([MIT Missing Semester](https://missing.csail.mit.edu/2020/course-shell/) concept):
    > Different projects may need different package versions. A **virtual environment** ([`venv`](https://docs.python.org/3/library/venv.html)) is an isolated Python setup for each project. Our `ai-tutorial` kernel uses the `.venv/` directory — packages you install here won't affect any other Python projects on your machine. See [Python docs: `pip`](https://pip.pypa.io/en/stable/) for more on package management.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** Never run `pip install` outside a virtual environment. If you run `pip install pandas` without activating your venv, packages get installed into your system Python, which can break other tools or create version conflicts. Always check that your terminal shows `(.venv)` in the prompt, or verify with `which pip` — it should point to `.venv/bin/pip`, not `/usr/bin/pip` or `/usr/local/bin/pip`. If Claude Code suggests a `pip install` command, it will use the project's venv automatically, but in a raw terminal you need to activate it first with `source .venv/bin/activate`.
    """)
    return


@app.cell
def _(subprocess):
    # You can run pip from inside a notebook using the ! prefix (runs a shell command)
    # Let's see what packages are installed in our environment
    #! pip list --format=columns 2>/dev/null | head -20
    subprocess.call(['pip', 'list', '--format=columns', '2>/dev/null', '|', 'head', '-20'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## How to find and learn packages

    When you need to do something in Python, the workflow is:

    1. **Ask Claude:** "What's the best Python package for [task]?" — this is the fastest way
    2. **Search PyPI:** https://pypi.org — the official package repository
    3. **Check the docs:** Every good package has documentation with examples

    You can also explore a package from within Python:
    """)
    return


@app.cell
def _(np):
    # See what functions are available
    # (This prints a lot — just scan it to get a feel)
    print([x for x in dir(np) if not x.startswith('_')][:30])  # first 30 public names
    return


@app.cell
def _(np):
    # Get help on a specific function
    help(np.mean)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Honestly? You'll rarely read docs line-by-line. The real workflow is:
    1. Know the package exists
    2. Know roughly what it does
    3. Ask Claude (or search) for the specific function you need

    That's a legitimate professional workflow, not cheating.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Quick tour: seaborn — beautiful statistical plots

    Seaborn builds on matplotlib and makes statistical visualizations easy. Let's build up a realistic example.
    """)
    return


@app.cell
def _(np, pd):
    import seaborn as sns
    np.random.seed(42)
    concentrations = [0, 1, 10, 100, 1000]
    n_replicates = 4
    rows = []
    # Generate mock calcium imaging data: % of DRG neurons responding
    # across different binder concentrations
    for conc in concentrations:  # makes random numbers reproducible
        for rep in range(n_replicates):
            if conc == 0:  # nM
                pct_responding = np.random.normal(78, 5)
            else:
                inhibition = 65 * (conc / (conc + 50))
                pct_responding = np.random.normal(78 - inhibition, 4)
            rows.append({'concentration_nM': conc, 'replicate': rep + 1, 'pct_responding': max(0, min(100, pct_responding))})
    dose_response = pd.DataFrame(rows)  # Simulate a dose-response: more binder → more neurons inhibited
    dose_response.head(10)  # baseline ~78% respond to capsaicin  # Dose-dependent inhibition with some noise  # Hill-ish curve, EC50 ~50 nM  # clamp to 0-100
    return (sns,)


@app.cell
def _(np, pd, plt, sns):
    np.random.seed(42)
    concentrations_1 = [0, 1, 10, 100, 1000]
    rows_1 = []
    for conc_1 in concentrations_1:
        for rep_1 in range(4):
    # Recreate the data (notebook is self-contained)
            if conc_1 == 0:
                pct = np.random.normal(78, 5)
            else:
                inhibition_1 = 65 * (conc_1 / (conc_1 + 50))
                pct = np.random.normal(78 - inhibition_1, 4)
            rows_1.append({'concentration_nM': conc_1, 'pct_responding': max(0, min(100, pct))})
    dose_response_1 = pd.DataFrame(rows_1)
    fig, ax = plt.subplots(figsize=(8, 5))
    dose_response_1['conc_label'] = dose_response_1['concentration_nM'].apply(lambda x: str(int(x)) if x > 0 else 'Vehicle')
    order = ['Vehicle', '1', '10', '100', '1000']
    sns.barplot(data=dose_response_1, x='conc_label', y='pct_responding', order=order, color='#93c5fd', edgecolor='#1e40af', alpha=0.7, ax=ax)
    sns.stripplot(data=dose_response_1, x='conc_label', y='pct_responding', order=order, color='#1e40af', size=6, alpha=0.8, ax=ax)
    ax.set_xlabel('DNB-Nav17-003 Concentration (nM)')
    # Plot: dose-response with individual data points
    ax.set_ylabel('% DRG Neurons Responding to Capsaicin')
    ax.set_title('Binder Dose-Response: Inhibition of Capsaicin-Evoked Calcium Transients')
    # Use log scale for concentration (add small offset for 0 nM)
    ax.set_ylim(0, 100)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's a publication-quality dose-response figure in about 15 lines of code. Let's break down what happened:

    - `sns.barplot()` — draws the bars (means with confidence intervals)
    - `sns.stripplot()` — overlays individual data points
    - `ax.set_xlabel()`, etc. — labels and formatting

    The key insight: **seaborn works directly with pandas DataFrames**. You say "x is this column, y is that column" and it figures out the rest.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Combining packages: a mini-analysis

    Let's put it all together. Here's a realistic scenario: you have calcium imaging traces from multiple neurons and want to identify responders.
    """)
    return


@app.cell
def _(np, plt):
    np.random.seed(123)
    time_s_1 = np.arange(0, 30, 1)
    n_neurons = 6
    traces = {}
    # Simulate calcium traces for 6 DRG neurons
    # 30 time points, 1 second each. Stimulus at t=10s.
    for i in range(n_neurons):
        baseline_1 = 1.0 + np.random.normal(0, 0.03, 30)
        is_responder = i in [0, 2, 4, 5]
        if is_responder:
            peak_height = np.random.uniform(2.0, 5.0)
            response = np.zeros(30)
            for t in range(10, 30):  # Baseline with noise
                response[t] = peak_height * np.exp(-(t - 11) / 5)
            baseline_1 = baseline_1 + response
        traces[f'Neuron {i + 1}'] = baseline_1  # Some neurons respond (peak at t=12), some don't
    fig_1, axes = plt.subplots(2, 3, figsize=(12, 6), sharex=True, sharey=True)  # 4 of 6 respond
    for idx, (name, trace_3) in enumerate(traces.items()):
        ax_1 = axes[idx // 3][idx % 3]
        ax_1.plot(time_s_1, trace_3, color='#2563eb', linewidth=1.5)  # Simple response shape: rapid rise, exponential decay
        ax_1.axvline(x=10, color='red', linestyle='--', alpha=0.5)
        ax_1.set_title(name, fontsize=11)
        ax_1.set_ylim(0.5, 6)
        baseline_mean = trace_3[:10].mean()
        baseline_std = trace_3[:10].std()
        peak = trace_3[10:].max()
        if peak > baseline_mean + 3 * baseline_std:
    # Plot all traces
            ax_1.text(0.95, 0.95, 'Responder', transform=ax_1.transAxes, ha='right', va='top', fontsize=9, color='green', fontweight='bold')
        else:
            ax_1.text(0.95, 0.95, 'Non-responder', transform=ax_1.transAxes, ha='right', va='top', fontsize=9, color='gray')
    fig_1.supxlabel('Time (s)')
    fig_1.supylabel('F / F₀')
    fig_1.suptitle('Calcium Imaging — DRG Neurons + 100 nM Capsaicin (red dashed = stimulus)', fontsize=12, y=1.02)
    plt.tight_layout()
    plt.show()  # Check if it's a responder: peak after stimulus > 2x baseline std
    return (traces,)


@app.cell
def _(traces):
    n_responders = 0
    n_total = len(traces)
    # Quantify: what fraction responded?
    print('Neuron-by-neuron analysis:')
    print('-' * 50)
    for name_1, trace_4 in traces.items():
        baseline_mean_1 = trace_4[:10].mean()
        baseline_std_1 = trace_4[:10].std()
        peak_1 = trace_4[10:].max()
        peak_time = trace_4[10:].argmax() + 10
        delta_f_1 = (peak_1 - baseline_mean_1) / baseline_mean_1
        is_resp = peak_1 > baseline_mean_1 + 3 * baseline_std_1
        if is_resp:
            n_responders = n_responders + 1  # offset by 10 since we sliced
        status = 'RESPONDER' if is_resp else '---'
        print(f'  {name_1}:  peak F/F0 = {peak_1:.2f}  ΔF/F0 = {delta_f_1:.2f}  peak at {peak_time}s  [{status}]')
    print(f'\nResponders: {n_responders}/{n_total} ({100 * n_responders / n_total:.0f}%)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is a realistic analysis workflow: generate or load data (numpy/pandas), visualize it (matplotlib), and quantify results. You just did calcium imaging analysis in Python.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Create a bar plot of binder affinities

    Using the binder screening CSV from the previous notebook:

    1. Read `sample_data/binder_screening.csv` with pandas
    2. Create a horizontal bar chart showing each candidate's predicted Kd
    3. Color the bars based on whether Kd < 20 nM (good) or >= 20 nM (needs work)
    4. Add a vertical dashed line at 20 nM as a threshold marker

    **Hints:**
    - `plt.barh()` makes horizontal bars
    - You can pass a list of colors, one per bar
    - `plt.axvline(x=20, ...)` draws a vertical line
    """)
    return


@app.cell
def _():
    # YOUR CODE HERE

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### Solution
    """)
    return


@app.cell
def _(Path, pd, plt):
    csv_file_1 = Path.cwd() / 'sample_data' / 'binder_screening.csv'
    df_1 = pd.read_csv(csv_file_1)
    df_1 = df_1.sort_values('predicted_kd_nm', ascending=True)
    colors = ['#22c55e' if kd < 20 else '#f97316' for kd in df_1['predicted_kd_nm']]
    labels = [f"{row['candidate_id']} ({row['target']})" for _, row in df_1.iterrows()]
    fig_2, ax_2 = plt.subplots(figsize=(9, 5))
    ax_2.barh(labels, df_1['predicted_kd_nm'], color=colors, edgecolor='#374151', alpha=0.85)
    # Sort by Kd for a cleaner plot
    ax_2.axvline(x=20, color='#dc2626', linestyle='--', linewidth=1.5, label='20 nM threshold')
    ax_2.set_xlabel('Predicted Kd (nM)')
    # Color each bar: green if Kd < 20, orange otherwise
    ax_2.set_title('De Novo Binder Screening — Predicted Binding Affinity')
    ax_2.legend()
    # Build labels: candidate ID + target
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Multi-neuron calcium trace heatmap

    Seaborn can make heatmaps. Create one showing calcium traces for 10 simulated neurons over 30 seconds.

    1. Use numpy to generate mock traces (similar to the example above)
    2. Put them into a pandas DataFrame (rows = neurons, columns = time points)
    3. Use `sns.heatmap()` to visualize

    **Hints:**
    - `sns.heatmap(df, cmap="YlOrRd")` — the `cmap` argument sets the color scheme
    - `YlOrRd` (yellow-orange-red) is good for fluorescence intensity
    """)
    return


@app.cell
def _():
    # YOUR CODE HERE

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### Solution
    """)
    return


@app.cell
def _(np, pd, plt, sns):
    np.random.seed(99)
    n_neurons_1 = 10
    n_timepoints = 30
    all_traces = np.ones((n_neurons_1, n_timepoints))
    for i_1 in range(n_neurons_1):
        all_traces[i_1] = all_traces[i_1] + np.random.normal(0, 0.02, n_timepoints)
        if np.random.random() < 0.6:
            peak_2 = np.random.uniform(1.5, 4.5)
            onset = np.random.randint(10, 13)
    # Generate traces
            for t_1 in range(onset, n_timepoints):  # start at baseline = 1.0
                all_traces[i_1, t_1] = all_traces[i_1, t_1] + peak_2 * np.exp(-(t_1 - onset) / np.random.uniform(3, 7))
    neuron_labels = [f'Neuron {i + 1}' for i in range(n_neurons_1)]
    time_labels = [f'{t}s' for t in range(n_timepoints)]  # Add baseline noise
    df_traces = pd.DataFrame(all_traces, index=neuron_labels, columns=time_labels)
    fig_3, ax_3 = plt.subplots(figsize=(12, 5))
    sns.heatmap(df_traces, cmap='YlOrRd', ax=ax_3, xticklabels=5, cbar_kws={'label': 'F / F₀'})  # ~60% of neurons respond (like a capsaicin challenge on DRG culture)
    ax_3.axvline(x=10, color='white', linewidth=2, linestyle='--')
    ax_3.set_xlabel('Time')
    ax_3.set_ylabel('')  # slight variation in response onset
    ax_3.set_title('Calcium Imaging Heatmap — DRG Culture + Capsaicin (white dashed = stimulus)')
    plt.tight_layout()
    # Build DataFrame
    # Plot heatmap
    plt.show()  # show every 5th time label
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
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Working with Files](02-working-with-files.py) | [Module Index](../README.md) | [Next: Data Structures in Practice \u2192](04-data-structures-in-practice.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Think Python, Chapter 15**: [Classes and Objects](https://allendowney.github.io/ThinkPython/chap15.html) — introduces Python objects and modules, the foundation for understanding how packages like pandas and numpy are structured
    - **Missing Semester, Lecture 4**: [Data Wrangling](https://missing.csail.mit.edu/2020/data-wrangling/) — processing and transforming data with command-line tools and scripts; complements the pandas/numpy approach in this notebook
    - [Python docs: `venv`](https://docs.python.org/3/library/venv.html) — official documentation for creating and managing virtual environments
    - [Python docs: `pip`](https://pip.pypa.io/en/stable/) — the package installer for Python; covers installation, requirements files, and version management
    - [NumPy Quickstart Tutorial](https://numpy.org/doc/stable/user/quickstart.html) — the official gentle introduction to NumPy arrays, which we used for calcium trace analysis in this notebook
    - [Pandas Getting Started](https://pandas.pydata.org/docs/getting_started/index.html) — the official entry point for learning pandas, starting from reading CSVs through groupby operations
    - [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html) — official tutorials covering basic to advanced plotting; start with "Pyplot tutorial" for the `plt.plot()` style used here
    - [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html) — guide to statistical visualization with seaborn, covering the bar plots and heatmaps from this notebook
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
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

