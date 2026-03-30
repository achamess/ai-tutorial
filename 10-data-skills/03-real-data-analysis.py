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
    # Module 6.3: Real Data Analysis Workflow

    **Goal:** Put it all together -- walk through a complete data analysis from raw data to biological interpretation, including using Claude to help interpret results.

    ---

    ## The scenario

    You've just received differential expression results from an RNA-seq experiment:
    - **Tissue:** Lumbar DRG neurons
    - **Comparison:** CFA-induced inflammatory pain (3 days) vs. vehicle control
    - **Question:** Which genes are differentially expressed, and what does this mean for your NaV1.7/NaV1.8 binder program?

    We'll generate a realistic synthetic dataset and analyze it end-to-end.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Data Visualization for Research](02-visualization.py) | [Module Index](../README.md) | [Next: Database Basics for Research Data \u2192](04-databases-basics.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - This is the payoff -- a complete analysis workflow from raw data to biological interpretation. This is what you'll actually do: load RNA-seq DE results from your DRG experiments, make a volcano plot, extract significant ion channel genes, and use Claude to interpret them in the context of your binder program.
    > - The pattern here (load, clean, visualize, analyze, interpret) applies to every dataset you'll encounter: binder screening campaigns, calcium imaging summaries, behavioral dose-response data, and pharmacokinetic curves.
    > - Combining pandas analysis with Claude API interpretation catches patterns you might miss -- for example, noticing that your top NaV1.7 binder hits cluster in a specific structural class, or that downregulated KCNQ2/3 expression correlates with pain sensitization timepoints.
    > - This workflow is also what makes your analysis reproducible and shareable. A notebook that goes from raw data to figures to AI-assisted interpretation is a complete, re-runnable scientific record.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### The complete analysis workflow

    This notebook follows this pipeline end-to-end:

    """),
    mo.mermaid(
        """
        flowchart TD
            A["Raw DE Results<br>2000 genes from DESeq2"] --> B["Inspect & QC<br>shape, dtypes, missing values,<br>expression distributions"]
            B --> C["Filter<br>Remove low-expression genes<br>(baseMean < 10)"]
            C --> D["Classify<br>Significance thresholds:<br>|log2FC| > 1, padj < 0.05"]
            D --> E["Visualize<br>Volcano plot, MA plot,<br>ion channel bar chart"]
            E --> F["Extract Insights<br>Top hits, ion channel focus,<br>pathway patterns"]
            F --> G["AI Interpretation<br>Send structured summary<br>to Claude API"]
            G --> H["Biological Conclusions<br>Implications for binder<br>program & next experiments"]
        
            style A fill:#bdc3c7,color:#2c3e50
            style B fill:#3498db,color:#fff
            style C fill:#f39c12,color:#fff
            style D fill:#e74c3c,color:#fff
            style E fill:#9b59b6,color:#fff
            style F fill:#2ecc71,color:#fff
            style G fill:#8e44ad,color:#fff
            style H fill:#1abc9c,color:#fff
        
            subgraph "YOUR EXPERTISE"
                direction LR
                H
            end
            subgraph "PANDAS + MATPLOTLIB"
                direction LR
                B
                C
                D
                E
                F
            end
            subgraph "CLAUDE API"
                direction LR
                G
            end
        """
    ),
    mo.md(r"""

    Each step below corresponds to a stage in this pipeline. By the end, you'll have a reusable template for any differential expression analysis.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** The complete analysis workflow -- load, clean, visualize, analyze, interpret -- is a pattern you'll use for every dataset. The specific plots and statistics change, but the structure is always the same. Internalizing this workflow means you can hand any new dataset to this template and have a systematic path from raw data to biological conclusions.

    > **Decision point: When to let Claude interpret vs interpret yourself**
    >
    > | Situation | Let Claude interpret | Interpret yourself | Why |
    > |-----------|---------------------|-------------------|-----|
    > | Pattern discovery in large gene lists | Yes -- Claude can spot pathway themes across hundreds of genes | Review Claude's interpretation | Claude excels at synthesizing across many items you can't hold in working memory |
    > | Statistical significance of YOUR key targets | No -- you know the biology | Use Claude to double-check | You know whether SCN9A upregulation makes biological sense in your model |
    > | Unexpected findings (a gene you don't recognize) | Yes -- ask Claude what it does and why it might be relevant | Verify with primary literature | Claude provides a quick starting point, but verify claims in papers |
    > | Final conclusions for a paper or grant | No -- this is your scientific judgment | Use Claude to pressure-test your reasoning | You're accountable for the claims; Claude is a sounding board |
    >
    > **Rule of thumb:** Use Claude for breadth (surveying many genes, suggesting pathways, generating hypotheses). Use your own expertise for depth (interpreting your specific targets, making claims, designing follow-up experiments).

    > **Warning:** P-hacking and cherry-picking are real risks in any analysis -- and AI tools can make them worse by helping you rapidly test many hypotheses. If you run 20 different comparisons and only report the one with p < 0.05, that's not a discovery -- it's noise. Define your analysis plan (which comparisons, which thresholds) before looking at the data. If you discover something unexpected during exploratory analysis, label it as hypothesis-generating and plan a confirmatory experiment.
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns

    sns.set_style('whitegrid')
    plt.rcParams['figure.dpi'] = 100
    return np, pd, plt


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 1: Generate Synthetic RNA-seq DE Results

    In real life, these come from [DESeq2](https://bioconductor.org/packages/release/bioc/html/DESeq2.html) or edgeR. DESeq2 (Love, M.I., Huber, W., Anders, S., 2014, "Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2," *Genome Biology* 15:550) is the standard tool for differential expression analysis from RNA-seq count data. Here we simulate realistic output with known biology baked in.
    """)
    return


@app.cell
def _(np, pd):
    np.random.seed(2025)

    n_genes = 2000

    # Gene names: mix of real pain-related genes and fake background genes
    pain_genes = {
        # Ion channels (your targets)
        'SCN9A': (1.8, 0.001),    # Nav1.7 - upregulated
        'SCN10A': (2.2, 0.0003),  # Nav1.8 - strongly upregulated
        'SCN11A': (1.5, 0.008),   # Nav1.9 - upregulated
        'TRPV1': (2.5, 0.0001),   # capsaicin receptor - strongly up
        'TRPA1': (1.9, 0.002),    # mustard oil receptor - up
        'KCNQ2': (-1.3, 0.01),   # Kv7.2 - downregulated (loss of M-current)
        'KCNQ3': (-1.1, 0.03),   # Kv7.3 - downregulated
        'KCNA2': (-1.8, 0.001),  # Kv1.2 - downregulated
        'PIEZO2': (0.8, 0.05),    # mechanosensor - modest change
        'P2RX3': (1.4, 0.005),    # purinergic - up
    
        # Neuropeptides & receptors
        'CALCA': (3.1, 0.00001),  # CGRP - strongly upregulated
        'TAC1': (2.8, 0.00005),   # Substance P - strongly up
        'CALCB': (2.4, 0.0002),   # CGRP-beta
        'NTRK1': (1.2, 0.02),     # TrkA (NGF receptor)
        'NGFR': (0.9, 0.06),      # p75NTR
    
        # Inflammatory mediators
        'IL6': (3.5, 0.000005),   # IL-6 - strongly up
        'TNF': (2.9, 0.00003),    # TNF-alpha
        'IL1B': (3.2, 0.00001),   # IL-1beta
        'PTGS2': (2.6, 0.0001),   # COX-2
        'CCL2': (3.8, 0.000001),  # MCP-1 chemokine
    
        # Transcription factors & signaling
        'ATF3': (4.2, 0.0000001), # injury marker
        'JUN': (2.0, 0.001),      # c-Jun
        'FOS': (1.6, 0.004),      # c-Fos
        'MAPK1': (0.6, 0.12),     # ERK2 - small change
        'STAT3': (1.3, 0.009),    # STAT3
    
        # Protein degradation related (for your PROTAC work)
        'UBB': (1.1, 0.025),      # ubiquitin
        'CRBN': (0.3, 0.4),       # cereblon (E3 ligase)
        'VHL': (-0.2, 0.6),       # VHL (E3 ligase)
    }

    # Generate background genes
    n_background = n_genes - len(pain_genes)
    bg_log2fc = np.random.normal(0, 0.5, n_background)
    bg_pvalues = np.random.beta(1, 1, n_background)  # uniform-ish p-values for null genes
    # Some background genes will be significant by chance
    bg_names = [f'GENE{i:04d}' for i in range(n_background)]

    # Build the full dataframe
    all_genes = list(pain_genes.keys()) + bg_names
    all_log2fc = [v[0] for v in pain_genes.values()] + list(bg_log2fc)
    all_pvals = [v[1] for v in pain_genes.values()] + list(bg_pvalues)

    de_results = pd.DataFrame({
        'gene': all_genes,
        'log2FoldChange': np.round(all_log2fc, 3),
        'pvalue': all_pvals,
        'baseMean': np.round(np.random.lognormal(5, 2, n_genes).clip(1), 1)
    })

    # Calculate adjusted p-values (Benjamini-Hochberg approximation)
    de_results = de_results.sort_values('pvalue')
    m = len(de_results)
    de_results['padj'] = np.minimum(
        de_results['pvalue'] * m / np.arange(1, m + 1),
        1.0
    )
    # Ensure padj is monotonically increasing from the bottom
    de_results['padj'] = de_results['padj'].iloc[::-1].cummin().iloc[::-1]
    de_results = de_results.sort_index()  # restore original order
    de_results['padj'] = de_results['padj'].round(6)
    de_results['pvalue'] = de_results['pvalue'].round(8)

    print(f"Generated DE results for {len(de_results)} genes")
    de_results.head(10)
    return (de_results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 2: Inspect and Clean the Data

    Always start by understanding what you have.
    """)
    return


@app.cell
def _(de_results):
    print("Dataset shape:", de_results.shape)
    print()
    print("Summary statistics:")
    de_results.describe()
    return


@app.cell
def _(de_results):
    # Check for issues
    print("Missing values:")
    print(de_results.isna().sum())
    print()
    print(f"Genes with baseMean < 10 (low expression, unreliable): {(de_results['baseMean'] < 10).sum()}")
    print(f"Genes with padj = NaN: {de_results['padj'].isna().sum()}")
    return


@app.cell
def _(de_results):
    # Filter out low-expression genes (standard practice)
    de_filtered = de_results[de_results['baseMean'] >= 10].copy()
    print(f"Before filter: {len(de_results)} genes")
    print(f"After filter (baseMean >= 10): {len(de_filtered)} genes")
    return (de_filtered,)


@app.cell
def _(de_filtered, plt):
    # Distribution of log2 fold changes
    _fig, axes = plt.subplots(1, 2, figsize=(12, 4))
    axes[0].hist(de_filtered['log2FoldChange'], bins=50, color='steelblue', edgecolor='white')
    axes[0].set_xlabel('log2 Fold Change')
    axes[0].set_ylabel('Number of genes')
    axes[0].set_title('Distribution of Fold Changes')
    axes[0].axvline(x=0, color='red', linestyle='--', alpha=0.5)
    axes[1].hist(de_filtered['pvalue'], bins=50, color='coral', edgecolor='white')
    axes[1].set_xlabel('P-value')
    # Distribution of p-values (should be uniform under null + spike near 0)
    axes[1].set_ylabel('Number of genes')
    axes[1].set_title('P-value Distribution')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 3: Volcano Plot

    The [volcano plot](https://en.wikipedia.org/wiki/Volcano_plot_(statistics)) is the signature visualization for differential expression. It shows fold change (x-axis) vs. statistical significance (y-axis). The convention of plotting -log10(p-value) vs. log2(fold change) makes it easy to spot genes that are both statistically significant and biologically meaningful (upper-left and upper-right corners).
    """)
    return


@app.cell
def _(de_filtered, np):
    # Add a column for significance classification
    def classify_gene(row, fc_cutoff=1.0, padj_cutoff=0.05):
        if _row['padj'] >= padj_cutoff:
            return 'Not significant'
        elif _row['log2FoldChange'] >= fc_cutoff:
            return 'Up'
        elif _row['log2FoldChange'] <= -fc_cutoff:
            return 'Down'
        else:
            return 'Not significant'
    de_filtered['significance'] = de_filtered.apply(classify_gene, axis=1)
    de_filtered['neg_log10_padj'] = -np.log10(de_filtered['padj'].clip(1e-50))
    print('Significance counts:')
    # Add -log10(padj) for plotting
    print(de_filtered['significance'].value_counts())
    return


@app.cell
def _(de_filtered, np, plt):
    # Volcano plot
    _fig, _ax = plt.subplots(figsize=(10, 7))
    colors = {'Not significant': '#bdc3c7', 'Up': '#e74c3c', 'Down': '#3498db'}
    for _sig_type, _color in colors.items():
        _subset = de_filtered[de_filtered['significance'] == _sig_type]
        _ax.scatter(_subset['log2FoldChange'], _subset['neg_log10_padj'], c=_color, alpha=0.5, s=15, label=f'{_sig_type} ({len(_subset)})')
    _ax.axhline(y=-np.log10(0.05), color='gray', linestyle='--', alpha=0.5)
    _ax.axvline(x=1, color='gray', linestyle='--', alpha=0.5)
    _ax.axvline(x=-1, color='gray', linestyle='--', alpha=0.5)
    genes_to_label = ['SCN9A', 'SCN10A', 'TRPV1', 'CALCA', 'ATF3', 'CCL2', 'IL6', 'KCNQ2', 'KCNA2', 'PTGS2', 'TAC1']
    # Significance thresholds
    for gene in genes_to_label:
        _row = de_filtered[de_filtered['gene'] == gene]
        if len(_row) > 0:
            _row = _row.iloc[0]
    # Label key genes
            _ax.annotate(gene, xy=(_row['log2FoldChange'], _row['neg_log10_padj']), xytext=(5, 5), textcoords='offset points', fontsize=8, fontweight='bold', arrowprops=dict(arrowstyle='-', color='black', lw=0.5))
    _ax.set_xlabel('log2 Fold Change (CFA vs. Vehicle)')
    _ax.set_ylabel('-log10(adjusted p-value)')
    _ax.set_title('Volcano Plot: DRG Gene Expression in Inflammatory Pain')
    _ax.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
    return (colors,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 4: Extract Significant Genes and Focus on Ion Channels
    """)
    return


@app.cell
def _(de_filtered):
    # Significant genes (padj < 0.05, |log2FC| > 1)
    sig_up = de_filtered[(de_filtered['significance'] == 'Up')].sort_values('log2FoldChange', ascending=False)
    sig_down = de_filtered[(de_filtered['significance'] == 'Down')].sort_values('log2FoldChange')

    print(f"Significantly upregulated: {len(sig_up)} genes")
    print(f"Significantly downregulated: {len(sig_down)} genes")
    print()

    print("=== Top 10 Upregulated ===")
    print(sig_up[['gene', 'log2FoldChange', 'padj', 'baseMean']].head(10).to_string(index=False))
    print()
    print("=== Top 10 Downregulated ===")
    print(sig_down[['gene', 'log2FoldChange', 'padj', 'baseMean']].head(10).to_string(index=False))
    return sig_down, sig_up


@app.cell
def _(de_filtered):
    # Focus on ion channels -- the proteins you're designing binders for
    ion_channel_genes = ['SCN9A', 'SCN10A', 'SCN11A', 'TRPV1', 'TRPA1',
                          'KCNQ2', 'KCNQ3', 'KCNA2', 'PIEZO2', 'P2RX3']

    channels = de_filtered[de_filtered['gene'].isin(ion_channel_genes)].sort_values('log2FoldChange', ascending=False)

    print("Ion channel expression changes:")
    channels[['gene', 'log2FoldChange', 'padj', 'significance']]
    return (channels,)


@app.cell
def _(channels, plt):
    # Visualize ion channel changes
    _fig, _ax = plt.subplots(figsize=(10, 5))
    colors_bar = ['#e74c3c' if fc > 0 else '#3498db' for fc in channels['log2FoldChange']]
    bars = _ax.barh(channels['gene'], channels['log2FoldChange'], color=colors_bar, edgecolor='white')
    for i, (_, _row) in enumerate(channels.iterrows()):
        if _row['padj'] < 0.001:
            stars = '***'
    # Add significance markers
        elif _row['padj'] < 0.01:
            stars = '**'
        elif _row['padj'] < 0.05:
            stars = '*'
        else:
            stars = 'ns'
        x_pos = _row['log2FoldChange'] + (0.1 if _row['log2FoldChange'] > 0 else -0.1)
        ha = 'left' if _row['log2FoldChange'] > 0 else 'right'
        _ax.text(x_pos, i, stars, va='center', ha=ha, fontsize=9)
    _ax.axvline(x=0, color='black', linewidth=0.8)
    _ax.set_xlabel('log2 Fold Change (CFA vs. Vehicle)')
    _ax.set_title('Ion Channel Expression Changes in Inflammatory Pain')
    plt.tight_layout()
    plt.show()
    print('\n* p<0.05, ** p<0.01, *** p<0.001, ns = not significant')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 5: Summary Statistics
    """)
    return


@app.cell
def _(de_filtered):
    # Categorize all significant genes by direction and magnitude
    sig_genes = de_filtered[de_filtered['significance'] != 'Not significant'].copy()

    def magnitude_bin(fc):
        afc = abs(fc)
        if afc >= 3:
            return 'Very strong (|FC| >= 3)'
        elif afc >= 2:
            return 'Strong (2 <= |FC| < 3)'
        else:
            return 'Moderate (1 <= |FC| < 2)'

    sig_genes['magnitude'] = sig_genes['log2FoldChange'].apply(magnitude_bin)

    print("Significant gene breakdown:")
    print(sig_genes.groupby(['significance', 'magnitude']).size().unstack(fill_value=0))
    return


@app.cell
def _(colors, de_filtered, np, plt):
    # MA plot (another standard QC visualization)
    _fig, _ax = plt.subplots(figsize=(10, 5))
    for _sig_type, _color in colors.items():
        _subset = de_filtered[de_filtered['significance'] == _sig_type]
        _ax.scatter(np.log10(_subset['baseMean']), _subset['log2FoldChange'], c=_color, alpha=0.4, s=10, label=_sig_type)
    _ax.axhline(y=0, color='black', linewidth=0.8)
    _ax.set_xlabel('log10(Mean Expression)')
    _ax.set_ylabel('log2 Fold Change')
    _ax.set_title('MA Plot: Expression Level vs. Fold Change')
    _ax.legend(loc='upper left')
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Step 6: Use Claude to Interpret Results

    This is where AI becomes a true research accelerator. Let's send our top hits to Claude and ask for biological interpretation relevant to your binder program.

    > **Note:** This requires your Anthropic API key. If you haven't set it up, review Module 05.
    """)
    return


@app.cell
def _(channels, de_filtered, sig_down, sig_up):
    # Prepare a summary of results for Claude
    top_up = sig_up[['gene', 'log2FoldChange', 'padj']].head(15)
    top_down = sig_down[['gene', 'log2FoldChange', 'padj']].head(10)

    results_text = f"""RNA-seq Differential Expression Results: DRG neurons, CFA inflammatory pain (3d) vs vehicle

    Total genes tested: {len(de_filtered)}
    Significantly upregulated (log2FC > 1, padj < 0.05): {len(sig_up)}
    Significantly downregulated (log2FC < -1, padj < 0.05): {len(sig_down)}

    TOP UPREGULATED GENES:
    {top_up.to_string(index=False)}

    TOP DOWNREGULATED GENES:
    {top_down.to_string(index=False)}

    ION CHANNEL CHANGES:
    {channels[['gene', 'log2FoldChange', 'padj']].to_string(index=False)}
    """

    print(results_text)
    return


@app.cell
def _():
    # Send to Claude for interpretation
    # Uncomment and run when you have your API key set up

    # import anthropic
    # 
    # client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from environment
    # 
    # message = client.messages.create(
    #     model="claude-sonnet-4-20250514",
    #     max_tokens=1500,
    #     messages=[{
    #         "role": "user",
    #         "content": f"""You are a pain neurobiology expert. I'm developing de novo protein binders 
    # targeting NaV1.7 (SCN9A) and NaV1.8 (SCN10A) for pain treatment, and also working on 
    # KCNQ2/3 channel modulators.
    # 
    # Please interpret these RNA-seq results from DRG neurons in an inflammatory pain model:
    # 
    # {results_text}
    # 
    # Specifically:
    # 1. What biological pathways are activated?
    # 2. How do the ion channel changes relate to pain sensitization?
    # 3. What implications do these results have for my NaV1.7/NaV1.8 binder program?
    # 4. Are there any surprising findings or genes worth following up on?
    # """
    #     }]
    # )
    # 
    # print(message.content[0].text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Calcium Imaging Analysis

    Now it's your turn. Analyze a mock calcium imaging dataset where DRG neurons were exposed to capsaicin (1 uM) across three conditions:
    - **Vehicle:** normal neurons
    - **PGE2:** sensitized with prostaglandin E2 (inflammatory mediator)
    - **PGE2 + PB-007:** sensitized, then treated with your NaV1.7 binder

    **Step 1:** Run the cell below to generate the dataset.
    """)
    return


@app.cell
def _(np, pd):
    np.random.seed(42)

    n_neurons = 60  # 20 per condition
    conditions_ca = ['Vehicle'] * 20 + ['PGE2'] * 20 + ['PGE2 + PB-007'] * 20

    calcium_data = pd.DataFrame({
        'neuron_id': [f'N{i+1:03d}' for i in range(n_neurons)],
        'condition': conditions_ca,
        'baseline_F': np.round(np.random.normal(1.0, 0.05, n_neurons), 3),
        'peak_response': np.round(
            np.concatenate([
                np.random.normal(2.5, 0.6, 20),   # vehicle: moderate response
                np.random.normal(4.2, 0.8, 20),   # PGE2: sensitized, bigger response
                np.random.normal(2.8, 0.5, 20),   # PGE2 + PB-007: rescued
            ]), 3),
        'time_to_peak_s': np.round(
            np.concatenate([
                np.random.normal(8.0, 1.5, 20),
                np.random.normal(5.5, 1.2, 20),   # faster in sensitized
                np.random.normal(7.5, 1.5, 20),
            ]), 2),
        'decay_tau_s': np.round(
            np.concatenate([
                np.random.normal(12.0, 2.0, 20),
                np.random.normal(18.0, 3.0, 20),  # slower decay when sensitized
                np.random.normal(13.0, 2.5, 20),
            ]), 2),
        'is_responder': np.concatenate([
            np.random.choice([True, False], 20, p=[0.6, 0.4]),   # 60% respond
            np.random.choice([True, False], 20, p=[0.85, 0.15]), # 85% respond when sensitized
            np.random.choice([True, False], 20, p=[0.55, 0.45]), # rescue reduces responders
        ])
    })

    print(f"Calcium imaging dataset: {len(calcium_data)} neurons")
    calcium_data.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Your tasks:

    1. **Inspect** the data: shape, data types, summary statistics
    2. **Calculate** the response amplitude (peak_response - baseline_F) as a new column
    3. **Summarize** by condition: mean and SEM for amplitude, time_to_peak, and decay_tau
    4. **Filter** to only responders, then re-calculate the summaries
    5. **Visualize**:
       - Box plot of response amplitudes by condition (responders only)
       - Bar chart of % responders by condition
    6. **Interpret**: What do these results tell you about PB-007's efficacy?
    """)
    return


@app.cell
def _():
    # Task 1: Inspect the data
    return


@app.cell
def _():
    # Task 2: Calculate response amplitude
    return


@app.cell
def _():
    # Task 3: Summarize by condition
    return


@app.cell
def _():
    # Task 4: Filter to responders and re-summarize
    return


@app.cell
def _():
    # Task 5: Visualizations
    return


@app.cell
def _():
    # Task 6 (bonus): Send results to Claude for interpretation
    # Build a summary string and use the API like in Step 6 above
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    In this notebook you completed a full analysis workflow:

    1. **Load & inspect** data (shape, dtypes, head, describe)
    2. **Clean & filter** (remove low-quality data)
    3. **Visualize** (volcano plot, bar charts, MA plot)
    4. **Extract insights** (significant genes, ion channel focus)
    5. **Summarize** with statistics (groupby, counts)
    6. **Interpret** with Claude API (AI-assisted biology)

    This pattern -- load, clean, visualize, analyze, interpret -- applies to almost any biological dataset you'll encounter. The specific plots and statistics change, but the workflow is the same.

    **You now have the core data skills to:**
    - Wrangle any tabular dataset with pandas
    - Create publication-quality figures
    - Run a complete analysis pipeline
    - Use Claude as a research interpretation partner
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **Differential expression analysis:**
    - Love, M.I., Huber, W., Anders, S. (2014). "Moderated estimation of fold change and dispersion for RNA-seq data with DESeq2." *Genome Biology* 15:550. [DOI: 10.1186/s13059-014-0550-8](https://doi.org/10.1186/s13059-014-0550-8) -- the original DESeq2 paper; essential reading if you run DE analysis
    - [DESeq2 vignette](https://bioconductor.org/packages/release/bioc/vignettes/DESeq2/inst/doc/DESeq2.html) -- the official tutorial for running DESeq2 in R

    **Volcano plots and visualization conventions:**
    - [Volcano plot (Wikipedia)](https://en.wikipedia.org/wiki/Volcano_plot_(statistics)) -- overview of the visualization and its conventions
    - Standard thresholds: |log2FC| > 1 and padj < 0.05 are common but arbitrary; adjust based on your dataset and biological question

    **pandas for data analysis:**
    - [pandas `merge` documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.merge.html) -- reference for joining DataFrames (used in Step 4 for combining expression data with annotations)
    - [pandas `groupby` documentation](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.groupby.html) -- reference for split-apply-combine operations
    - [NumPy random module](https://numpy.org/doc/stable/reference/random/index.html) -- reference for the random number generation used to create synthetic data in this notebook

    **Books:**
    - *Python for Data Analysis* (3rd ed.) by Wes McKinney -- Chapters 7-10 cover data cleaning, joining, and aggregation in detail
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
    - 2026-03-25: Added standardized callouts and decision frameworks
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
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

