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
    # 02: AI-Assisted Data Analysis Pipeline

    ## The real workflow

    You run an experiment. You get numbers. You need to:
    1. Clean and organize the data
    2. Filter and rank candidates
    3. Visualize key relationships
    4. Interpret results and plan next steps

    Steps 1-3 are [pandas](https://pandas.pydata.org/) + [matplotlib](https://matplotlib.org/) (Module 06). Step 4 is where Claude comes in — not replacing your expertise, but helping you think through the data systematically.

    This notebook builds two end-to-end pipelines:
    - **Pipeline A:** Binder screening data (your protein design work)
    - **Pipeline B:** Behavioral pain data (exercise — you build it)

    > **Prerequisites:** pandas and matplotlib from Module 06, Claude API from Module 05. For best practices on structuring computational research, see Wilson et al. (2017), "[Good Enough Practices in Scientific Computing](https://doi.org/10.1371/journal.pcbi.1005510)," *PLOS Computational Biology*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: AI-Assisted Literature Review](01-literature-review.py) | [Module Index](../README.md) | [Next: AI-Assisted Scientific Writing \u2192](03-writing-with-ai.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Your binder screening generates multi-dimensional data -- Kd, selectivity ratio, thermostability, expression yield -- for every candidate across multiple targets (NaV1.7, NaV1.8, KCNQ2/3). An automated pipeline means consistent analysis every time, not ad hoc Excel work that varies between experiments.
    > - Combining computational analysis with AI interpretation catches patterns you might miss: correlations between binder properties (tight binders expressing poorly), target-specific hit rate differences, or unexpected structure-activity relationships in your screening data.
    > - The same pipeline pattern works for behavioral data, calcium imaging, and RNA-seq -- define the analysis once, then re-run it on every new dataset with confidence that the processing is identical.
    > - This is also how you present results to collaborators and in lab meetings: reproducible figures generated from a pipeline, not one-off plots you can't recreate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### The AI-integrated data analysis pipeline

    """),
    mo.mermaid(
        """
        flowchart TD
            subgraph DATA["Your Experiment"]
                D1["Raw Data<br>(screening results,<br>behavioral scores,<br>calcium imaging)"]
            end
        
            subgraph PANDAS["pandas + matplotlib"]
                P1["Load & Inspect<br>pd.read_csv(), .describe()"]
                P2["Filter & Rank<br>apply hit criteria,<br>sort candidates"]
                P3["Visualize<br>scatter plots, bar charts,<br>time courses"]
                P4["Summarize<br>groupby stats,<br>hit rates, correlations"]
            end
        
            subgraph AI["Claude API"]
                A1["Structured Summary<br>(text with numbers,<br>not raw DataFrames)"]
                A2["Interpretation<br>patterns, tradeoffs,<br>biological context"]
                A3["Recommendations<br>next experiments,<br>design improvements"]
            end
        
            subgraph YOU["Your Expertise"]
                Y1["Scientific Judgment<br>validate claims,<br>plan next steps"]
            end
        
            D1 --> P1
            P1 --> P2
            P2 --> P3
            P3 --> P4
            P4 --> A1
            A1 --> A2
            A2 --> A3
            A3 --> Y1
            Y1 -->|"new experiment"| D1
        
            style D1 fill:#bdc3c7,color:#2c3e50
            style P1 fill:#3498db,color:#fff
            style P2 fill:#3498db,color:#fff
            style P3 fill:#3498db,color:#fff
            style P4 fill:#3498db,color:#fff
            style A1 fill:#8e44ad,color:#fff
            style A2 fill:#8e44ad,color:#fff
            style A3 fill:#8e44ad,color:#fff
            style Y1 fill:#e74c3c,color:#fff
        """
    ),
    mo.md(r"""

    Notice the loop: your judgment feeds back into new experiments. Claude accelerates the analysis-to-interpretation step, but you drive the science.
    """)
    ])
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
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    import json
    from IPython.display import display, Markdown

    client = anthropic.Anthropic()
    MODEL = "claude-sonnet-4-6"

    # Set a clean style for all plots
    sns.set_theme(style="whitegrid", palette="colorblind")
    plt.rcParams["figure.figsize"] = (10, 6)

    print("Ready.")
    return MODEL, Markdown, client, display, np, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Pipeline A: Binder screening results

    ### Step 1: Generate synthetic screening data

    Imagine you've run a screening campaign: 30 de novo protein binder candidates tested against NaV1.7, NaV1.8, and KCNQ2/3. For each candidate, you measured binding affinity (Kd), selectivity ratio, thermostability, and expression yield.
    """)
    return


@app.cell
def _(display, np, pd):
    np.random.seed(42)  # reproducible results

    n_candidates = 30
    targets = ["NaV1.7", "NaV1.8", "KCNQ2/3"]

    data = {
        "candidate_id": [f"DNB-{i+1:03d}" for i in range(n_candidates)],
        "target": np.random.choice(targets, n_candidates, p=[0.4, 0.35, 0.25]),
        "kd_nm": np.round(np.random.lognormal(mean=3.0, sigma=1.2, size=n_candidates), 1),
        "selectivity_ratio": np.round(np.random.lognormal(mean=3.5, sigma=1.5, size=n_candidates), 0),
        "tm_celsius": np.round(np.random.normal(loc=58, scale=12, size=n_candidates), 1),
        "expression_yield_mg_per_L": np.round(np.random.lognormal(mean=1.5, sigma=0.8, size=n_candidates), 1),
    }

    # Add some correlation: tighter binders tend to express less well (realistic)
    for i in range(n_candidates):
        if data["kd_nm"][i] < 10:
            data["expression_yield_mg_per_L"][i] *= 0.5

    df = pd.DataFrame(data)

    print(f"Screening data: {len(df)} candidates")
    display(df.head(10))
    return df, targets


@app.cell
def _(df, display):
    # Quick summary stats
    print("Summary statistics:\n")
    display(df.describe().round(1))

    print("\nCandidates per target:")
    print(df["target"].value_counts())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 2: Filter and rank candidates

    Not every candidate is worth advancing. Let's define criteria and filter — just like triage in any screening campaign.

    > 🔑 **Key concept:** Consistent pipeline = consistent results. By defining hit criteria as explicit variables (`KD_CUTOFF`, `SELECTIVITY_CUTOFF`, etc.) rather than ad hoc filtering, you guarantee that every screening round is analyzed identically. When you change criteria, the entire analysis updates — no risk of applying different thresholds to different datasets.

    > 💡 **Tip:** Save your hit criteria as a config dictionary or YAML file. When you present results in lab meeting, you can show exactly which criteria were applied. This also makes it trivial to re-run with relaxed or tightened criteria for sensitivity analysis.
    """)
    return


@app.cell
def _(df, display):
    # Define hit criteria
    KD_CUTOFF = 50           # nM — must bind tighter than this
    SELECTIVITY_CUTOFF = 10  # fold selectivity over closest off-target
    TM_CUTOFF = 50           # degrees C — must be stable enough for downstream assays
    EXPRESSION_CUTOFF = 1.0  # mg/L — must express enough to test

    # Apply filters
    hits = df[
        (df["kd_nm"] <= KD_CUTOFF) &
        (df["selectivity_ratio"] >= SELECTIVITY_CUTOFF) &
        (df["tm_celsius"] >= TM_CUTOFF) &
        (df["expression_yield_mg_per_L"] >= EXPRESSION_CUTOFF)
    ].copy()

    # Rank by Kd (tighter is better)
    hits = hits.sort_values("kd_nm")

    print(f"Hits passing all criteria: {len(hits)} / {len(df)} candidates")
    print(f"Hit rate: {100 * len(hits) / len(df):.0f}%\n")
    display(hits)
    return EXPRESSION_CUTOFF, KD_CUTOFF, SELECTIVITY_CUTOFF, TM_CUTOFF, hits


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 3: Visualize key relationships

    Three views that tell you the most about your screening campaign.
    """)
    return


@app.cell
def _(KD_CUTOFF, SELECTIVITY_CUTOFF, df, plt, targets):
    # Plot 1: Kd vs selectivity, colored by target — the primary triage view
    _fig, _ax = plt.subplots(figsize=(10, 7))
    for _target in targets:
        subset = df[df['target'] == _target]
        _ax.scatter(subset['kd_nm'], subset['selectivity_ratio'], label=_target, s=80, alpha=0.7, edgecolors='black', linewidth=0.5)
    _ax.axvline(x=KD_CUTOFF, color='red', linestyle='--', alpha=0.5, label=f'Kd cutoff ({KD_CUTOFF} nM)')
    _ax.axhline(y=SELECTIVITY_CUTOFF, color='blue', linestyle='--', alpha=0.5, label=f'Selectivity cutoff ({SELECTIVITY_CUTOFF}x)')
    _ax.set_xlabel('Kd (nM)', fontsize=12)
    # Mark the hit zone
    _ax.set_ylabel('Selectivity ratio (fold)', fontsize=12)
    _ax.set_title('Binder Screening: Affinity vs Selectivity', fontsize=14)
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.legend()
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(EXPRESSION_CUTOFF, KD_CUTOFF, df, plt):
    # Plot 2: Kd vs Expression yield — the developability tradeoff
    _fig, _ax = plt.subplots(figsize=(10, 6))
    scatter = _ax.scatter(df['kd_nm'], df['expression_yield_mg_per_L'], c=df['tm_celsius'], cmap='RdYlGn', s=80, edgecolors='black', linewidth=0.5)
    _ax.axvline(x=KD_CUTOFF, color='red', linestyle='--', alpha=0.5)
    _ax.axhline(y=EXPRESSION_CUTOFF, color='blue', linestyle='--', alpha=0.5)
    plt.colorbar(scatter, label='Tm (°C)')
    _ax.set_xlabel('Kd (nM)', fontsize=12)
    _ax.set_ylabel('Expression yield (mg/L)', fontsize=12)
    _ax.set_title('Affinity vs Developability', fontsize=14)
    _ax.set_xscale('log')
    plt.tight_layout()
    plt.show()
    return


@app.cell
def _(df, display, hits, pd, plt, targets):
    # Plot 3: Per-target hit rates — a bar chart for the team meeting
    target_stats = []
    for _target in targets:
        total = len(df[df['target'] == _target])
        hit_count = len(hits[hits['target'] == _target]) if len(hits) > 0 else 0
        target_stats.append({'target': _target, 'total_screened': total, 'hits': hit_count, 'hit_rate': 100 * hit_count / total if total > 0 else 0})
    stats_df = pd.DataFrame(target_stats)
    _fig, axes = plt.subplots(1, 2, figsize=(12, 5))
    _x = range(len(stats_df))
    axes[0].bar(_x, stats_df['total_screened'], label='Total screened', alpha=0.6)
    axes[0].bar(_x, stats_df['hits'], label='Hits', alpha=0.9)
    axes[0].set_xticks(_x)
    axes[0].set_xticklabels(stats_df['target'])
    axes[0].set_ylabel('Number of candidates')
    axes[0].set_title('Candidates per Target')
    axes[0].legend()
    # Counts
    axes[1].bar(_x, stats_df['hit_rate'], color='teal', alpha=0.8)
    axes[1].set_xticks(_x)
    axes[1].set_xticklabels(stats_df['target'])
    axes[1].set_ylabel('Hit rate (%)')
    axes[1].set_title('Hit Rate per Target')
    plt.tight_layout()
    plt.show()
    # Hit rates
    display(stats_df)
    return (stats_df,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 4: AI-assisted interpretation

    Here's where Claude adds value beyond what a plotting library can do. We send the summary statistics and hit information, and ask for scientific interpretation and next-step recommendations.

    This is the pattern from Module 03: give Claude the data in a structured format, then ask a specific analytical question.

    > ⚠️ **Warning:** Don't over-rely on AI interpretation without domain expertise. Claude can identify patterns in your screening data (e.g., "tight binders tend to express poorly"), but it cannot judge whether those patterns are biologically meaningful or artifacts of your expression system. **You bring the context:** Is the affinity-expression tradeoff a fundamental biophysical constraint, or is it because your E. coli system can't fold complex designs? Claude doesn't know — you do.

    > 🤔 **Decision point: When to automate vs do manually**
    >
    > | Analysis step | Automate? | Why |
    > |---------------|-----------|-----|
    > | Data loading and cleaning | Yes | Same every time, error-prone by hand |
    > | Hit filtering by cutoffs | Yes | Consistency, reproducibility |
    > | Standard visualizations | Yes | Saves time, enforces uniform style |
    > | Statistical tests | Yes (with verification) | Correct computation, but verify test choice |
    > | Biological interpretation | **No** | Requires your domain expertise |
    > | Deciding next experiments | **No** | AI can suggest, but you decide |
    > | Novel pattern discovery | Partial | AI can flag, you validate |
    >
    > **Diminishing returns:** Automating the first 80% of analysis (loading, filtering, plotting) saves hours. Automating interpretation saves minutes and adds risk. Invest your automation effort where the return is highest.
    """)
    return


@app.cell
def _(
    EXPRESSION_CUTOFF,
    KD_CUTOFF,
    SELECTIVITY_CUTOFF,
    TM_CUTOFF,
    df,
    hits,
    stats_df,
):
    # Build a structured summary for Claude
    summary_for_ai = f"""Binder Screening Campaign Summary
    ================================
    Total candidates screened: {len(df)}
    Targets: NaV1.7 ({len(df[df['target']=='NaV1.7'])}), NaV1.8 ({len(df[df['target']=='NaV1.8'])}), KCNQ2/3 ({len(df[df['target']=='KCNQ2/3'])})

    Hit criteria:
      - Kd <= {KD_CUTOFF} nM
      - Selectivity >= {SELECTIVITY_CUTOFF}-fold
      - Tm >= {TM_CUTOFF} C
      - Expression >= {EXPRESSION_CUTOFF} mg/L

    Results:
      - Total hits: {len(hits)} ({100*len(hits)/len(df):.0f}% hit rate)

    Per-target breakdown:
    {stats_df.to_string(index=False)}

    Overall statistics:
    {df.describe().round(1).to_string()}

    Top 5 hits (by Kd):
    {hits.head().to_string(index=False) if len(hits) > 0 else 'No hits found'}

    Key observation: Candidates with Kd < 10 nM tend to have lower expression yields 
    (mean {df[df['kd_nm'] < 10]['expression_yield_mg_per_L'].mean():.1f} mg/L) compared to 
    all candidates (mean {df['expression_yield_mg_per_L'].mean():.1f} mg/L).
    """

    print(summary_for_ai)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's the complete pipeline: **generate data → analyze → visualize → interpret with AI**.

    Notice how much better the interpretation is when you give Claude structured, quantitative data versus just asking "what do you think about my screening results?" This is the prompt engineering from Module 03 paying off.

    > **Pattern:** The AI doesn't see your plots — it reads the numbers. Build your summary text to capture what the visualizations show.

    <details><summary>Click to expand: Building reusable pipelines — from notebook to script</summary>

    Once your pipeline works in a notebook, consider extracting it to a Python script for reuse:

    1. **Functions in a `.py` file** — `filter_hits()`, `plot_screening_results()`, `build_ai_summary()`
    2. **Config file** — hit criteria, model choice, column names
    3. **CLI interface** — `python analyze_screen.py --input data.csv --kd-cutoff 50`

    This way, every new screening dataset gets the same analysis with one command. The notebook becomes your prototyping environment; the script becomes your production pipeline.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Pipeline B (Exercise): Behavioral pain data

    Now you build a similar pipeline for a different dataset: **behavioral pain scores** from an animal study.

    ### The experiment

    You're testing your top binder (DNB-017) as a pain therapeutic in the CFA inflammatory pain model:
    - 4 treatment groups: Vehicle, Low dose (1 mg/kg), High dose (10 mg/kg), Gabapentin (positive control)
    - Timepoints: Baseline, 2h, 6h, 24h, 48h post-dose
    - Measurement: Paw withdrawal threshold (grams) — higher = less pain
    - n = 8 per group

    ### Step 1: Generate the mock data
    """)
    return


@app.cell
def _(display, np, pd):
    np.random.seed(123)
    groups = ['Vehicle', 'Low dose (1 mg/kg)', 'High dose (10 mg/kg)', 'Gabapentin']
    timepoints = ['Baseline', '2h', '6h', '24h', '48h']
    n_per_group = 8
    true_means = {'Vehicle': [8.0, 2.5, 2.8, 3.0, 3.2], 'Low dose (1 mg/kg)': [8.0, 4.5, 5.0, 4.2, 3.5], 'High dose (10 mg/kg)': [8.0, 6.5, 7.2, 6.0, 4.8], 'Gabapentin': [8.0, 5.8, 6.0, 4.0, 3.3]}
    rows = []
    # Define the "true" mean paw withdrawal threshold for each group at each timepoint
    # Baseline is the same for all (pre-CFA), then CFA drops it, treatments help to varying degrees
    for _group in groups:
        for animal_id in range(n_per_group):  # CFA drops it, slow partial recovery
            for t_idx, timepoint in enumerate(timepoints):  # Modest effect, wears off
                mean_val = true_means[_group][t_idx]  # Strong effect, good duration
                value = np.round(np.random.normal(loc=mean_val, scale=0.8), 1)  # Known comparator, shorter duration
                value = max(0.5, value)
                rows.append({'animal_id': f'{_group[:3].upper()}-{animal_id + 1:02d}', 'group': _group, 'timepoint': timepoint, 'paw_withdrawal_g': value})
    behavior_df = pd.DataFrame(rows)
    print(f'Behavioral dataset: {len(behavior_df)} observations')
    print(f'  {len(groups)} groups x {n_per_group} animals x {len(timepoints)} timepoints')
    display(behavior_df.head(10))  # Add individual animal variability  # floor at 0.5g
    return behavior_df, groups, n_per_group, timepoints


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Your turn: Steps 2-4

    Build the rest of the pipeline. Here's what to do:

    **Step 2: Summarize the data**
    - Compute group means and standard deviations at each timepoint
    - Calculate the percent reversal from vehicle for each treatment group

    **Step 3: Visualize**
    - A time course plot (line plot, x = timepoint, y = mean paw withdrawal, one line per group, error bars = SEM)
    - A bar chart comparing groups at the 6h timepoint (peak effect)

    **Step 4: AI interpretation**
    - Send the summary statistics to Claude
    - Ask for: efficacy assessment, comparison to gabapentin, dose-response evaluation, and recommended follow-up experiments
    """)
    return


@app.cell
def _(behavior_df, display, np, pd, timepoints):
    # Step 2: Compute group summaries

    # Group means and SEM at each timepoint
    summary = behavior_df.groupby(["group", "timepoint"])["paw_withdrawal_g"].agg(
        ["mean", "std", "count"]
    ).reset_index()
    summary["sem"] = summary["std"] / np.sqrt(summary["count"])
    summary = summary.round(2)

    # Set timepoint order
    summary["timepoint"] = pd.Categorical(summary["timepoint"], categories=timepoints, ordered=True)
    summary = summary.sort_values(["group", "timepoint"])

    print("Group means by timepoint:")
    pivot = summary.pivot(index="group", columns="timepoint", values="mean")
    display(pivot)
    return pivot, summary


@app.cell
def _(groups, plt, summary, timepoints):
    # Step 3a: Time course plot
    _fig, _ax = plt.subplots(figsize=(10, 6))
    timepoint_positions = {tp: i for i, tp in enumerate(timepoints)}
    colors = {'Vehicle': 'gray', 'Low dose (1 mg/kg)': 'steelblue', 'High dose (10 mg/kg)': 'darkblue', 'Gabapentin': 'orange'}
    for _group in groups:
        grp = summary[summary['group'] == _group].sort_values('timepoint')
        _x = [timepoint_positions[tp] for tp in grp['timepoint']]
        _ax.errorbar(_x, grp['mean'], yerr=grp['sem'], marker='o', linewidth=2, capsize=4, label=_group, color=colors.get(_group, 'black'))
    _ax.set_xticks(range(len(timepoints)))
    _ax.set_xticklabels(timepoints)
    _ax.set_xlabel('Time post-dose', fontsize=12)
    _ax.set_ylabel('Paw withdrawal threshold (g)', fontsize=12)
    _ax.set_title('CFA Model: DNB-017 Efficacy Time Course', fontsize=14)
    _ax.legend(loc='lower right')
    _ax.set_ylim(0, 10)
    plt.tight_layout()
    plt.show()
    return (colors,)


@app.cell
def _(colors, plt, summary):
    # Step 3b: Bar chart at the 6h timepoint
    peak = summary[summary['timepoint'] == '6h'].copy()
    _fig, _ax = plt.subplots(figsize=(8, 5))
    bar_colors = [colors[g] for g in peak['group']]
    bars = _ax.bar(range(len(peak)), peak['mean'], yerr=peak['sem'], capsize=5, color=bar_colors, edgecolor='black', linewidth=0.5)
    _ax.set_xticks(range(len(peak)))
    _ax.set_xticklabels(peak['group'], rotation=15, ha='right')
    _ax.set_ylabel('Paw withdrawal threshold (g)', fontsize=12)
    _ax.set_title('6h Post-Dose: Peak Effect Comparison', fontsize=14)
    _ax.set_ylim(0, 10)
    _ax.axhline(y=8.0, color='green', linestyle='--', alpha=0.5, label='Pre-CFA baseline')
    _ax.legend()
    plt.tight_layout()
    # Add baseline reference line
    plt.show()
    return


@app.cell
def _(MODEL, Markdown, client, display, n_per_group, pivot):
    # Step 4: Send to Claude for interpretation

    # Build a structured summary
    behavior_summary = f"""CFA Inflammatory Pain Model — DNB-017 Efficacy Study
    =====================================================
    Design: 4 groups, n={n_per_group}/group, paw withdrawal threshold measured at 5 timepoints
    CFA injected at t=0, treatments dosed at t=0

    Group means (paw withdrawal threshold in grams, higher = less pain):
    {pivot.to_string()}

    Pre-CFA baseline (all groups): ~8.0 g
    Vehicle at 6h (peak inflammation): ~{pivot.loc['Vehicle', '6h']:.1f} g

    Percent reversal at 6h (vs vehicle):
      - Low dose: {100 * (pivot.loc['Low dose (1 mg/kg)', '6h'] - pivot.loc['Vehicle', '6h']) / (8.0 - pivot.loc['Vehicle', '6h']):.0f}%
      - High dose: {100 * (pivot.loc['High dose (10 mg/kg)', '6h'] - pivot.loc['Vehicle', '6h']) / (8.0 - pivot.loc['Vehicle', '6h']):.0f}%
      - Gabapentin: {100 * (pivot.loc['Gabapentin', '6h'] - pivot.loc['Vehicle', '6h']) / (8.0 - pivot.loc['Vehicle', '6h']):.0f}%

    Notable: High dose maintains efficacy at 24h while gabapentin effect has largely worn off.
    """

    behavior_prompt = f"""\
    You are a pain biology consultant reviewing preclinical efficacy data for a novel 
    de novo protein binder (DNB-017) targeting NaV1.7 for pain. The binder is being 
    compared to gabapentin in a CFA inflammatory pain model.

    Analyze these results and provide:

    1. **Efficacy assessment** (2-3 sentences): How effective is DNB-017? Is the effect 
       size meaningful for this model?

    2. **Head-to-head with gabapentin** (2-3 sentences): How does DNB-017 compare to 
       the positive control? Any advantages?

    3. **Dose-response** (2-3 sentences): What does the dose-response relationship tell you?

    4. **Duration of action** (2-3 sentences): Comment on the time course — when does 
       efficacy peak and how long does it last?

    5. **Recommended follow-up experiments** (numbered list of 4-5): What should be 
       done next to advance this candidate?

    Be specific. Reference actual numbers.

    Data:
    {behavior_summary}"""

    response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=[{"role": "user", "content": behavior_prompt}]
    )

    display(Markdown(response.content[0].text))
    return behavior_prompt, response


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Bonus: Asking follow-up questions

    One of the most useful patterns: after the initial interpretation, ask a targeted follow-up. Use a multi-turn conversation to dig deeper.
    """)
    return


@app.cell
def _(MODEL, Markdown, behavior_prompt, client, display, response):
    # Multi-turn: ask a follow-up about the expression yield problem from Pipeline A
    followup_messages = [
        {
            "role": "user", 
            "content": behavior_prompt  # original screening analysis request
        },
        {
            "role": "assistant",
            "content": response.content[0].text  # Claude's previous interpretation
        },
        {
            "role": "user",
            "content": (
                "Good analysis. I want to focus on the affinity-expression tradeoff. "
                "We're using RFdiffusion for design and E. coli for expression. "
                "Can you suggest specific computational strategies during the design "
                "phase that might improve expression of tight binders? Also, would "
                "switching to a mammalian expression system help for these particular "
                "targets (transmembrane ion channels)?"
            )
        }
    ]

    followup_response = client.messages.create(
        model=MODEL,
        max_tokens=1500,
        messages=followup_messages
    )

    display(Markdown(followup_response.content[0].text))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **Data analysis methodology:**
    - Wilson, G. et al. (2017). "Good Enough Practices in Scientific Computing." *PLOS Computational Biology* 13(6): e1005510. [DOI: 10.1371/journal.pcbi.1005510](https://doi.org/10.1371/journal.pcbi.1005510) -- practical guidelines for organizing data, writing code, and making research reproducible. Directly applicable to the pipeline pattern used in this notebook.

    **pandas and visualization:**
    - [pandas documentation: analysis methods](https://pandas.pydata.org/docs/user_guide/index.html) -- comprehensive guide to filtering, grouping, and aggregating data
    - [Matplotlib tutorials](https://matplotlib.org/stable/tutorials/) -- official tutorials for all plot types used in this notebook
    - [Seaborn tutorial](https://seaborn.pydata.org/tutorial.html) -- statistical visualization built on matplotlib

    **Anthropic / Claude:**
    - [Anthropic API Documentation](https://docs.anthropic.com/) -- reference for the Claude API, including message formatting and model selection
    - [Anthropic documentation on structured outputs](https://docs.anthropic.com/en/docs/build-with-claude/structured-output) -- how to get JSON and other structured formats from Claude (used in the interpretation step)
    - [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) -- practical examples of data analysis and interpretation with Claude

    **Reproducible research:**
    - [marimo documentation](https://docs.marimo.io/) -- tips for making notebooks reproducible and shareable
    - *Python for Data Analysis* (3rd ed.) by Wes McKinney -- the pandas creator's book covers the full analysis pipeline from data loading to visualization
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
    - 2026-03-25: QA pass — removed duplicate markdown-in-code cell, removed duplicate Edit Log, fixed undefined interpretation_prompt variable
    - 2026-03-25: Added callout boxes — key concept (consistent pipeline), decision point (automate vs manual with diminishing returns table), warning (AI interpretation without domain expertise), tip (config files), collapsible deep-dive (notebook to script)
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: AI-Assisted Literature Review](01-literature-review.py) | [Module Index](../README.md) | [Next: AI-Assisted Scientific Writing \u2192](03-writing-with-ai.py)
    """)
    return


if __name__ == "__main__":
    app.run()

