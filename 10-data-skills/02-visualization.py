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
    # Module 6.2: Data Visualization for Research

    **Goal:** Learn to create clear, publication-quality figures using [matplotlib](https://matplotlib.org/) and [seaborn](https://seaborn.pydata.org/) with pain biology data.

    ---

    ## The plotting ecosystem

    - **[matplotlib](https://matplotlib.org/)** -- the foundational library. Verbose but gives you full control.
    - **[seaborn](https://seaborn.pydata.org/)** -- built on matplotlib, makes statistical plots easy and beautiful.

    We'll use both. The key mental model:
    - A **Figure** is the entire image (like a canvas)
    - An **Axes** is one individual plot within the figure
    - A figure can have multiple axes (subplots = multi-panel figures)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Pandas Basics for Research Data](01-pandas-basics.py) | [Module Index](../README.md) | [Next: Real Data Analysis Workflow \u2192](03-real-data-analysis.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Figures are how you communicate results -- in papers, grants, lab meetings, and collaborator emails. matplotlib and seaborn produce publication-quality figures that are fully reproducible, unlike manually arranged PowerPoint or GraphPad figures.
    > - When your binder screening data changes (new candidates, updated Kd measurements), you regenerate every figure instantly by re-running the code. No manual reformatting, no accidentally using last month's data.
    > - Reviewers increasingly expect reproducible figures. Code-generated plots with clear parameters (axis limits, color schemes, statistical annotations) are easier to defend and revise than point-and-click figures.
    > - Claude can write matplotlib code for you, but you need to read the output to know if the figure accurately represents your data -- axis scales, error bars, and color mappings all affect interpretation.
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    # Set a clean default style
    sns.set_style('whitegrid')
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['font.size'] = 11
    return np, pd, plt, sns


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Line Plots -- Calcium Imaging Traces

    Line plots are perfect for time-series data. Let's simulate calcium imaging traces from DRG neurons responding to capsaicin.
    """)
    return


@app.cell
def _(np):
    # Generate mock calcium imaging data
    np.random.seed(42)
    time = np.linspace(0, 60, 600)  # 60 seconds, 10 Hz sampling

    def simulate_calcium_trace(baseline, amplitude, onset, rise_tau, decay_tau, noise=0.02):
        """Simulate a calcium transient with exponential rise and decay."""
        trace = np.ones_like(time) * baseline
        mask = time >= onset
        t_shifted = time[mask] - onset
        response = amplitude * (1 - np.exp(-t_shifted / rise_tau)) * np.exp(-t_shifted / decay_tau)
        trace[mask] += response
        trace += np.random.normal(0, noise, len(time))
        return trace

    # Three neurons with different responses to capsaicin (applied at t=10s)
    neuron_1 = simulate_calcium_trace(1.0, 2.5, 10, 1.5, 15)   # strong responder
    neuron_2 = simulate_calcium_trace(1.0, 1.2, 10, 2.0, 10)   # moderate responder
    neuron_3 = simulate_calcium_trace(1.0, 0.1, 10, 1.0, 8, noise=0.02)  # non-responder

    print(f"Generated {len(time)} timepoints for 3 neurons")
    return neuron_1, neuron_2, neuron_3, time


@app.cell
def _(neuron_1, neuron_2, neuron_3, plt, time):
    # Basic line plot
    _fig, _ax = plt.subplots(figsize=(10, 4))
    _ax.plot(time, neuron_1, label='Neuron 1 (TRPV1+)', color='#e74c3c', linewidth=1.2)
    _ax.plot(time, neuron_2, label='Neuron 2 (TRPV1+)', color='#3498db', linewidth=1.2)
    _ax.plot(time, neuron_3, label='Neuron 3 (TRPV1-)', color='#95a5a6', linewidth=1.2)
    _ax.axvline(x=10, color='red', linestyle='--', alpha=0.5, label='Capsaicin (1 uM)')
    _ax.set_xlabel('Time (seconds)')
    # Mark capsaicin application
    _ax.set_ylabel('F/F0 (normalized fluorescence)')
    _ax.set_title('Calcium Imaging: DRG Neuron Responses to Capsaicin')
    _ax.legend(loc='upper right')
    _ax.set_xlim(0, 60)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Bar Charts -- Gene Expression Across Conditions

    Bar charts are the workhorse of molecular biology figures. Let's plot ion channel expression in DRG neurons under different pain conditions.
    """)
    return


@app.cell
def _(np, pd):
    # Mock gene expression data: fold change relative to naive control
    np.random.seed(123)

    genes = ['SCN9A\n(Nav1.7)', 'SCN10A\n(Nav1.8)', 'TRPV1', 'CALCA\n(CGRP)', 'KCNQ2\n(Kv7.2)']
    conditions = ['Naive', 'CFA (3d)', 'SNI (7d)']

    # Mean fold changes (CFA = inflammatory, SNI = neuropathic)
    means = {
        'Naive':    [1.0, 1.0, 1.0, 1.0, 1.0],
        'CFA (3d)': [1.8, 2.1, 2.5, 3.2, 0.6],
        'SNI (7d)': [2.3, 1.5, 1.9, 2.8, 0.4],
    }

    # Standard errors
    sems = {
        'Naive':    [0.1, 0.1, 0.1, 0.1, 0.1],
        'CFA (3d)': [0.3, 0.4, 0.5, 0.6, 0.1],
        'SNI (7d)': [0.4, 0.3, 0.3, 0.5, 0.08],
    }

    expr_df = pd.DataFrame({
        'gene': genes * 3,
        'condition': [c for c in conditions for _ in genes],
        'fold_change': means['Naive'] + means['CFA (3d)'] + means['SNI (7d)'],
        'sem': sems['Naive'] + sems['CFA (3d)'] + sems['SNI (7d)']
    })

    expr_df.head(10)
    return conditions, expr_df, genes


@app.cell
def _(conditions, expr_df, genes, np, plt):
    # Grouped bar chart
    _fig, _ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(genes))
    width = 0.25
    colors = ['#bdc3c7', '#e74c3c', '#8e44ad']
    for i, condition in enumerate(conditions):
        _subset = expr_df[expr_df['condition'] == condition]
        _ax.bar(x + i * width, _subset['fold_change'], width, yerr=_subset['sem'], capsize=3, label=condition, color=colors[i], edgecolor='white')
    _ax.set_xlabel('Gene')
    _ax.set_ylabel('Fold Change (vs. Naive)')
    _ax.set_title('Ion Channel Expression in DRG After Injury')
    _ax.set_xticks(x + width)
    _ax.set_xticklabels(genes)
    _ax.legend()
    _ax.axhline(y=1, color='gray', linestyle=':', alpha=0.5)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Scatter Plots -- Binding Affinity vs. Selectivity

    Scatter plots reveal relationships between two continuous variables. Perfect for screening data.
    """)
    return


@app.cell
def _(np, pd):
    # Mock binder screening data
    np.random.seed(99)
    _n = 50
    binder_data = pd.DataFrame({'name': [f'PB-{i + 1:03d}' for i in range(_n)], 'target': np.random.choice(['NaV1.7', 'NaV1.8', 'KCNQ2/3'], _n, p=[0.4, 0.35, 0.25]), 'Kd_nM': np.round(np.random.lognormal(3.5, 1.2, _n), 1), 'selectivity_fold': np.round(np.random.lognormal(2.5, 1.0, _n), 1), 'solubility_mg_ml': np.round(np.random.uniform(0.5, 20, _n), 1)})
    binder_data.head()
    return (binder_data,)


@app.cell
def _(binder_data, plt):
    # Scatter plot: Kd vs Selectivity, colored by target
    _fig, _ax = plt.subplots(figsize=(8, 6))
    target_colors = {'NaV1.7': '#e74c3c', 'NaV1.8': '#3498db', 'KCNQ2/3': '#2ecc71'}
    for target, color in target_colors.items():
        _subset = binder_data[binder_data['target'] == target]
        _ax.scatter(_subset['Kd_nM'], _subset['selectivity_fold'], s=_subset['solubility_mg_ml'] * 8, c=color, alpha=0.7, edgecolors='white', linewidth=0.5, label=target)
    _ax.axvspan(0, 50, alpha=0.05, color='green')
    _ax.axhspan(20, _ax.get_ylim()[1], alpha=0.05, color='green')
    _ax.set_xscale('log')  # size = solubility
    _ax.set_yscale('log')
    _ax.set_xlabel('Binding Affinity Kd (nM) -- lower is better')
    _ax.set_ylabel('Selectivity (fold over closest homolog)')
    # Mark the "sweet spot" region
    _ax.set_title('Protein Binder Screening: Affinity vs. Selectivity')
    _ax.legend(title='Target', loc='lower left')
    best_idx = binder_data['Kd_nM'].idxmin()
    best = binder_data.loc[best_idx]
    _ax.annotate(best['name'], xy=(best['Kd_nM'], best['selectivity_fold']), xytext=(best['Kd_nM'] * 3, best['selectivity_fold'] * 2), arrowprops=dict(arrowstyle='->', color='black'), fontsize=9, fontweight='bold')
    plt.tight_layout()
    # Annotate best candidate
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Reading this plot:** Each dot is a binder candidate. Position shows affinity (x) and selectivity (y). Dot size encodes solubility. The ideal candidates are in the upper-left: high affinity + high selectivity.

    ---

    ## 4. Box Plots -- Behavioral Assay Data

    Box plots show distributions and are standard for comparing treatment groups in behavioral studies.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Warning:** Misleading visualizations are easy to create accidentally (and sometimes intentionally). Watch for these common traps:
    > - **Truncated y-axis:** Starting the y-axis at 0.8 instead of 0 makes a 10% difference look like a 5x difference. Always consider whether your axis range honestly represents the data.
    > - **Wrong scale:** Linear scale for log-normal data (like Kd values) compresses most data points into a tiny region. Use log scale for binding affinities, gene expression, and concentrations.
    > - **Dual y-axes:** Two different y-axes on the same plot almost always mislead. The visual correlation between the two lines is meaningless because you can make any two lines appear correlated by adjusting the axis scales.
    > - **Bar charts for distributions:** A bar chart showing means hides the shape of your data. Always show individual data points (stripplot) or a box/violin plot when presenting group comparisons.

    > **Tip:** Use colorblind-safe palettes by default. About 8% of men have some form of color vision deficiency. Using red-green color schemes (the matplotlib default) means 1 in 12 viewers can't read your figure properly. Seaborn's `colorblind` palette or [ColorBrewer](https://colorbrewer2.org/) palettes are designed for universal accessibility. Set it once with `sns.set_palette('colorblind')` and never worry about it again.
    """)
    return


@app.cell
def _(np, pd):
    # Mock von Frey threshold data from a binder efficacy study
    np.random.seed(77)
    groups = ['Vehicle', 'CFA only', 'CFA + PB-007\n(1 mg/kg)', 'CFA + PB-007\n(10 mg/kg)', 'CFA + Gabapentin']
    n_per_group = 10
    vf_data = []
    for _group, mean, sd in [('Vehicle', 1.2, 0.2), ('CFA only', 0.25, 0.1), ('CFA + PB-007\n(1 mg/kg)', 0.55, 0.15), ('CFA + PB-007\n(10 mg/kg)', 0.95, 0.2), ('CFA + Gabapentin', 0.7, 0.18)]:
    # Simulated von Frey thresholds (grams)
    # Vehicle = normal, CFA = sensitized, treatments = partial rescue
        _values = np.random.normal(mean, sd, n_per_group).clip(0.05)
        for _v in _values:
            vf_data.append({'group': _group, 'von_frey_g': round(_v, 3)})
    vf_df = pd.DataFrame(vf_data)
    print(f'{len(vf_df)} measurements across {len(groups)} groups')
    vf_df.groupby('group')['von_frey_g'].describe().round(3)  # thresholds can't be negative
    return (vf_df,)


@app.cell
def _(plt, sns, vf_df):
    # Box plot with individual data points (standard for behavioral data)
    _fig, _ax = plt.subplots(figsize=(9, 5))
    palette = ['#bdc3c7', '#e74c3c', '#f39c12', '#27ae60', '#3498db']
    sns.boxplot(data=vf_df, x='group', y='von_frey_g', palette=palette, width=0.5, fliersize=0, ax=_ax)
    sns.stripplot(data=vf_df, x='group', y='von_frey_g', color='black', size=5, alpha=0.6, jitter=True, ax=_ax)
    # Box plot
    _ax.set_xlabel('')
    _ax.set_ylabel('Von Frey Threshold (g)')
    _ax.set_title('Mechanical Allodynia: NaV1.7 Binder Dose-Response')
    # Overlay individual data points (strip plot)
    _ax.axhline(y=1.2, color='gray', linestyle=':', alpha=0.4, label='Naive baseline')
    _ax.legend(loc='upper left')
    plt.tight_layout()
    # Add a horizontal line for baseline reference
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Heatmaps -- Gene Expression Across Samples

    Heatmaps are essential for visualizing high-dimensional data like RNA-seq results across multiple samples.
    """)
    return


@app.cell
def _(np, pd):
    # Mock RNA-seq data: pain-related genes across DRG samples
    np.random.seed(2024)

    genes_hm = ['SCN9A', 'SCN10A', 'TRPV1', 'TRPA1', 'CALCA', 'TAC1',
                 'P2RX3', 'KCNQ2', 'KCNQ3', 'NTRK1', 'RET', 'PIEZO2']

    samples = ['Naive_1', 'Naive_2', 'Naive_3',
               'CFA_1', 'CFA_2', 'CFA_3',
               'SNI_1', 'SNI_2', 'SNI_3']

    # Base expression + condition effects
    base = np.random.normal(0, 0.5, (len(genes_hm), 3))  # naive

    # CFA (inflammatory) upregulates nociceptor genes
    cfa_effect = np.array([1.5, 1.8, 2.0, 1.2, 2.5, 1.8, 0.8, -0.8, -0.6, 1.0, 0.5, 0.3])
    cfa = base + cfa_effect[:, np.newaxis] + np.random.normal(0, 0.3, (len(genes_hm), 3))

    # SNI (neuropathic) has a different profile
    sni_effect = np.array([2.0, 0.8, 1.5, 2.2, 2.0, 2.5, 1.5, -1.2, -1.0, 0.3, -0.5, 1.8])
    sni = base + sni_effect[:, np.newaxis] + np.random.normal(0, 0.3, (len(genes_hm), 3))

    expression_matrix = pd.DataFrame(
        np.hstack([base, cfa, sni]),
        index=genes_hm,
        columns=samples
    ).round(2)

    expression_matrix
    return (expression_matrix,)


@app.cell
def _(expression_matrix, plt, sns):
    # Heatmap with clustering
    g = sns.clustermap(
        expression_matrix,
        cmap='RdBu_r',
        center=0,
        figsize=(8, 8),
        row_cluster=True,
        col_cluster=True,
        linewidths=0.5,
        linecolor='white',
        cbar_kws={'label': 'log2 fold change'},
        dendrogram_ratio=(0.15, 0.15)
    )

    g.fig.suptitle('Pain-Related Gene Expression in DRG', y=1.02, fontsize=14)
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Customization and Saving Figures

    > **Why you need this:** Journal-specific formatting requirements (font sizes, DPI, figure dimensions) are tedious to apply manually. Setting them in code means every figure in your paper is consistent, and switching from Nature to Cell format is a parameter change, not hours of reformatting. See the [Nature guide to preparing figures](https://www.nature.com/documents/nature-final-artwork.pdf) for specific requirements.
    """)
    return


@app.cell
def _(plt, sns, vf_df):
    # Publication-ready style settings
    pub_params = {'font.size': 10, 'axes.titlesize': 12, 'axes.labelsize': 11, 'xtick.labelsize': 9, 'ytick.labelsize': 9, 'legend.fontsize': 9, 'figure.dpi': 150, 'savefig.dpi': 300, 'font.family': 'sans-serif'}
    with plt.rc_context(pub_params):
        _fig, _ax = plt.subplots(figsize=(4, 3))
        _subset = vf_df[vf_df['group'].isin(['Vehicle', 'CFA only', 'CFA + PB-007\n(10 mg/kg)'])]
        sns.boxplot(data=_subset, x='group', y='von_frey_g', palette=['#bdc3c7', '#e74c3c', '#27ae60'], width=0.5, fliersize=0, ax=_ax)
        sns.stripplot(data=_subset, x='group', y='von_frey_g', color='black', size=4, alpha=0.5, jitter=True, ax=_ax)
        _ax.set_xlabel('')
        _ax.set_ylabel('Von Frey Threshold (g)')
        _ax.set_title('PB-007 Reverses Mechanical Allodynia')
        _ax.set_xticklabels(['Vehicle', 'CFA', 'CFA +\nPB-007'], rotation=0)
        plt.tight_layout()
        plt.show()
    print('\nTip: Use PDF for journal submissions (vector), PNG for slides/posters.')  # Nature single-column width  # Uncomment to save:  # fig.savefig('figure_1a.pdf', bbox_inches='tight')  # vector for publication  # fig.savefig('figure_1a.png', bbox_inches='tight')  # raster for presentations
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Multi-Panel Behavioral Figure

    Create a publication-style figure with 4 panels (2x2) showing results from a binder efficacy study. The mock data is generated below.

    **Your figure should have:**
    - Panel A: Von Frey thresholds (box plot) across time points
    - Panel B: Paw withdrawal latency to heat (bar chart with error bars)
    - Panel C: Paw edema over time (line plot, mean +/- SEM)
    - Panel D: Conditioned place aversion scores (bar chart)

    **Step 1:** Run the cell below to generate mock data.
    """)
    return


@app.cell
def _(np, pd):
    np.random.seed(2025)
    _n = 8  # mice per group
    timepoints = ['Baseline', 'Day 1', 'Day 3', 'Day 7']
    # ---- Panel A data: Von Frey at multiple time points ----
    panel_a_rows = []
    for tp, veh_mean, cfa_mean, treat_mean in [('Baseline', 1.2, 1.2, 1.2), ('Day 1', 1.15, 0.25, 0.28), ('Day 3', 1.18, 0.2, 0.6), ('Day 7', 1.2, 0.22, 0.9)]:
        for _group, mean_val in [('Vehicle', veh_mean), ('CFA', cfa_mean), ('CFA + PB-007', treat_mean)]:
            _values = np.random.normal(mean_val, mean_val * 0.15, _n).clip(0.05)
            for _v in _values:
                panel_a_rows.append({'timepoint': tp, 'group': _group, 'von_frey_g': round(_v, 3)})
    panel_a_df = pd.DataFrame(panel_a_rows)
    panel_b = pd.DataFrame({'group': ['Vehicle', 'CFA', 'CFA + PB-007'], 'latency_s': [11.2, 4.8, 8.5], 'sem': [0.8, 0.5, 0.7]})
    days = np.array([0, 1, 2, 3, 5, 7])
    edema_vehicle = np.array([3.0, 3.05, 3.02, 3.01, 3.0, 3.0])
    edema_cfa = np.array([3.0, 4.8, 4.5, 4.2, 3.9, 3.6])
    edema_treat = np.array([3.0, 4.7, 4.1, 3.6, 3.3, 3.1])
    edema_sem = np.array([0.1, 0.2, 0.2, 0.15, 0.15, 0.1])
    panel_d_rows = []
    # ---- Panel B data: Hargreaves (paw withdrawal latency) ----
    for _group, mean_val in [('Vehicle', 5.2), ('CFA', -120.5), ('CFA + PB-007', -35.8)]:
        _values = np.random.normal(mean_val, abs(mean_val) * 0.3 + 10, _n)
        for _v in _values:
            panel_d_rows.append({'group': _group, 'cpa_score': round(_v, 1)})
    panel_d_df = pd.DataFrame(panel_d_rows)
    print('Mock behavioral data generated successfully!')
    # ---- Panel C data: Paw edema time course ----
    print(f'  Panel A: {len(panel_a_df)} measurements')
    print(f'  Panel B: {len(panel_b)} group means')
    print(f'  Panel C: {len(days)} time points x 3 groups')
    # ---- Panel D data: Conditioned place aversion ----
    print(f'  Panel D: {len(panel_d_df)} measurements')
    return


@app.cell
def _():
    # YOUR CODE HERE: Create a 2x2 multi-panel figure
    # 
    # Hints:
    #   fig, axes = plt.subplots(2, 2, figsize=(10, 8))
    #   ax_a = axes[0, 0]   # top-left
    #   ax_b = axes[0, 1]   # top-right
    #   ax_c = axes[1, 0]   # bottom-left
    #   ax_d = axes[1, 1]   # bottom-right
    #
    # For Panel A: use sns.boxplot with x='timepoint', y='von_frey_g', hue='group'
    # For Panel B: use ax.bar() with yerr for error bars
    # For Panel C: use ax.plot() with ax.fill_between() for SEM shading
    # For Panel D: use sns.boxplot or sns.barplot
    #
    # Don't forget: labels, titles, and plt.tight_layout()
    # Add panel labels with ax.text(-0.15, 1.05, 'A', transform=ax.transAxes, fontsize=14, fontweight='bold')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary: Choosing the Right Plot

    | Data type | Plot | Example |
    |---|---|---|
    | Time series | Line plot | Calcium traces, edema over time |
    | Categories vs. values | Bar chart | Gene expression by condition |
    | Two continuous variables | Scatter plot | Kd vs. selectivity |
    | Distributions by group | Box/violin plot | Behavioral scores by treatment |
    | Matrix data | Heatmap | Gene expression across samples |

    **Key matplotlib/seaborn pattern:**
    ```python
    fig, ax = plt.subplots(figsize=(width, height))  # create canvas
    # ... plot commands using ax ...
    ax.set_xlabel('X label')
    ax.set_ylabel('Y label')
    ax.set_title('Title')
    plt.tight_layout()
    plt.show()
    ```

    **Next up:** Module 6.3 -- Real Data Analysis, where we combine pandas + plotting into a complete analysis workflow.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Decision point: Which plot type for which data (expanded guide)**
    >
    > | Data scenario | Best plot | Why | Avoid |
    > |---------------|-----------|-----|-------|
    > | Time series (calcium traces, edema) | **Line plot** | Shows temporal trends clearly | Bar chart (loses temporal information) |
    > | 2 groups, few measurements per group (n < 20) | **Box plot + strip plot** | Shows distribution AND individual points | Bar chart with error bars (hides distribution shape) |
    > | 2 groups, many measurements (n > 50) | **Violin plot** | Shows full distribution shape | Strip plot alone (too many overlapping points) |
    > | 3+ groups with means and error | **Grouped bar chart** | Compact comparison of means | Individual bar charts per group (hard to compare) |
    > | Relationship between 2 continuous variables | **Scatter plot** | Reveals correlations, clusters, outliers | Line plot (implies ordered sequence) |
    > | High-dimensional data (genes x samples) | **Heatmap / clustermap** | Pattern discovery across many variables | Multiple scatter plots (too many to interpret) |
    > | Distribution of one variable | **Histogram** or **KDE plot** | Shows shape: normal, skewed, bimodal | Summary statistics alone (loses shape information) |
    > | Proportions or composition | **Stacked bar** or **pie chart** (if few categories) | Shows parts of a whole | Regular bar chart (doesn't communicate "part of whole") |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### Visual decision guide: which plot for which data?

    Use this flowchart when you're not sure which plot type to use:

    """),
    mo.mermaid(
        """
        flowchart TD
            Q["What kind of data<br>are you plotting?"]
            Q --> TS["Time series?<br>(measurements over time)"]
            Q --> CAT["Categories vs. numbers?<br>(groups with measurements)"]
            Q --> REL["Relationship between<br>two numeric variables?"]
            Q --> DIST["Distribution of<br>a single variable?"]
            Q --> MAT["Matrix / many variables<br>across many samples?"]
        
            TS --> LINE["LINE PLOT<br>ax.plot()<br><br>e.g., calcium traces,<br>edema over time"]
        
            CAT --> FEW{"Few data<br>points per<br>group?"}
            FEW -->|"< 20"| BOX["BOX / VIOLIN PLOT<br>sns.boxplot()<br><br>e.g., von Frey thresholds<br>by treatment"]
            FEW -->|"means only"| BAR["BAR CHART<br>ax.bar() + yerr<br><br>e.g., gene expression<br>fold change"]
        
            REL --> SCAT["SCATTER PLOT<br>ax.scatter()<br><br>e.g., Kd vs. selectivity,<br>affinity vs. expression"]
        
            DIST --> HIST["HISTOGRAM<br>ax.hist()<br><br>e.g., fold-change<br>distribution"]
        
            MAT --> HEAT["HEATMAP<br>sns.clustermap()<br><br>e.g., RNA-seq across<br>samples"]
        
            style LINE fill:#3498db,color:#fff
            style BOX fill:#e74c3c,color:#fff
            style BAR fill:#f39c12,color:#fff
            style SCAT fill:#2ecc71,color:#fff
            style HIST fill:#9b59b6,color:#fff
            style HEAT fill:#1abc9c,color:#fff
        """
    ),
    mo.md(r"""

    > **Rule of thumb:** When in doubt, show individual data points (stripplot or swarmplot overlaid on a box plot). Reviewers want to see your n.
    """)
    ])
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
    - 2026-03-25: QA pass — removed duplicate section 6 cell
    - 2026-03-25: Added standardized callouts and decision frameworks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Pandas Basics for Research Data](01-pandas-basics.py) | [Module Index](../README.md) | [Next: Real Data Analysis Workflow \u2192](03-real-data-analysis.py)
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
    - 2026-03-25: QA pass — removed duplicate section 6 cell
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

