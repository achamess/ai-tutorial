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
    # Module: Math You Actually Need -- 01: Descriptive Stats and Distributions

    **Goal:** Understand the basic numbers that summarize data -- means, medians, spread, and distributions -- so you can evaluate experimental results and understand how LLMs generate text.

    **References:** [NumPy Statistical Functions](https://numpy.org/doc/stable/reference/routines.statistics.html) | [SciPy Stats Module](https://docs.scipy.org/doc/scipy/reference/stats.html) | [Think Python Ch 7: Iteration](https://allendowney.github.io/ThinkPython/chap07.html) | [Think Stats](https://allendowney.github.io/ThinkStats/) (Allen Downey)

    > **Book companion:** This notebook covers the same territory as [Think Stats](https://allendowney.github.io/ThinkStats/) by Allen Downey (the same author as Think Python, same accessible style). Think Stats goes deeper on every topic here — if you want more after this notebook, it's the natural next step. Especially relevant: [Chapter 1 (Exploratory Data Analysis)](https://allendowney.github.io/ThinkStats/) and [Chapter 2 (Distributions)](https://allendowney.github.io/ThinkStats/).

    ---

    ## Why you need this
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Cloud Computing and When to Use What](../07-cloud-and-hpc/03-cloud-computing-and-when-to-use-what.py) | [Module Index](../README.md) | [Next: Hypothesis Testing and P-values \u2192](02-hypothesis-testing-and-pvalues.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - When a paper reports "von Frey threshold was 1.2 +/- 0.3 g," knowing whether that is SD or SEM changes your interpretation of the variability and reliability of the result. This notebook teaches you to spot the difference instantly.
    > - Your binder screening data (Kd values, selectivity ratios) follow lognormal distributions, not normal ones. Using the wrong summary statistic (mean vs median) on skewed data will mislead your hit-picking decisions.
    > - Understanding distributions is the foundation for the next two notebooks (hypothesis testing and AI math). Temperature in Claude's API literally reshapes a probability distribution over tokens -- the same math you learn here for binding affinities.
    > - Outlier detection protects your analyses from artifacts -- dead neurons in calcium imaging, failed injections in behavioral assays -- that would otherwise skew your results and waste follow-up experiments.
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy import stats

    # Nicer plots
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (8, 5)
    plt.rcParams['font.size'] = 12

    # Reproducibility
    rng = np.random.default_rng(42)

    print("Ready to go!")
    return np, pd, plt, rng, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Mean, Median, and Mode — When Each Matters

    ### Why you need this

    You record calcium transient amplitudes from 30 DRG neurons after capsaicin application. Some neurons fire huge responses, some don't respond at all. Which single number best summarizes your data? The answer depends on the *shape* of your data — and picking the wrong summary statistic can hide the biology.

    Let's create some realistic calcium imaging data and see why this matters.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** The choice between mean and median depends on data shape. For symmetric data (normal distribution), mean and median are nearly identical and either works. For skewed data -- which is extremely common in biology (binding affinities, gene expression levels, calcium transient amplitudes) -- the median is a more honest summary because it's not pulled by extreme values. When you report "average Kd = 500 nM" for a screen where most binders have Kd > 1000 nM but a few tight binders pull the mean down, you're giving a misleading picture of your typical candidate.

    > **Decision point: When to use mean vs median**
    >
    > | Data shape | Use | Why | Pain biology example |
    > |------------|-----|-----|---------------------|
    > | Symmetric (bell curve) | **Mean** | Mean = median, both are good summaries | Withdrawal latencies in a homogeneous group |
    > | Right-skewed (long tail of high values) | **Median** | Mean is inflated by outliers | Binding affinities (Kd) from a screening campaign |
    > | Left-skewed (long tail of low values) | **Median** | Mean is deflated by outliers | Time-to-response in fast-responding neuron populations |
    > | Bimodal (two peaks) | **Neither alone** -- report both peaks | Mean falls in the gap between peaks, misleading | Calcium imaging (responders vs non-responders) |
    > | Small n (< 10) | **Median** | Mean is unstable with few data points | Pilot behavioral experiments |

    > **Warning:** SEM (standard error of the mean) makes error bars look deceptively small. SEM = SD / sqrt(n), so it shrinks as you add more samples -- even if the underlying variability hasn't changed. A paper showing SEM error bars on n=50 will look much more precise than the same data with SD error bars. Always check whether a paper reports SD or SEM. For your own figures: use SD to show biological variability, SEM only when you're specifically estimating precision of the mean.
    """)
    return


@app.cell
def _(np, rng):
    # Simulate calcium imaging: DRG neurons responding to capsaicin
    # Reality: some neurons are TRPV1+ (respond strongly), others don't respond
    # This creates a BIMODAL distribution
    _n_neurons = 60
    n_responders = 35
    n_nonresponders = _n_neurons - n_responders  # ~58% of DRG neurons are TRPV1+
    responders = rng.normal(loc=2.5, scale=0.8, size=n_responders)
    responders = np.clip(responders, 0.5, None)
    # Responders: large calcium transients (delta F/F)
    nonresponders = rng.normal(loc=0.1, scale=0.15, size=n_nonresponders)
    nonresponders = np.clip(nonresponders, 0, None)  # minimum detectable response
    calcium_data = np.concatenate([responders, nonresponders])
    # Non-responders: just noise around baseline
    rng.shuffle(calcium_data)
    print(f'Recorded {_n_neurons} DRG neurons after 1 uM capsaicin')
    print(f'Raw values (delta F/F): {calcium_data[:8].round(2)} ...')  # mix them up like you'd see in an experiment
    return (calcium_data,)


@app.cell
def _(calcium_data, np):
    # Compare mean, median, and mode
    mean_val = np.mean(calcium_data)
    median_val = np.median(calcium_data)

    # For mode, we'll bin the data (continuous data doesn't have an exact mode)
    from scipy.stats import mode as scipy_mode

    print(f"Mean:   {mean_val:.2f} delta F/F")
    print(f"Median: {median_val:.2f} delta F/F")
    print()
    print("Which one is 'right'? Let's look at the distribution...")
    return mean_val, median_val


@app.cell
def _(calcium_data, mean_val, median_val, plt):
    _fig, _ax = plt.subplots(figsize=(10, 5))
    _ax.hist(calcium_data, bins=20, edgecolor='black', alpha=0.7, color='steelblue')
    _ax.axvline(mean_val, color='red', linewidth=2, linestyle='-', label=f'Mean = {mean_val:.2f}')
    _ax.axvline(median_val, color='orange', linewidth=2, linestyle='--', label=f'Median = {median_val:.2f}')
    _ax.set_xlabel('Calcium transient amplitude (delta F/F)')
    _ax.set_ylabel('Number of neurons')
    _ax.set_title('DRG neuron responses to 1 uM capsaicin')
    _ax.legend(fontsize=11)
    plt.tight_layout()
    plt.show()
    print('Neither the mean nor median captures the real story here:')
    print('There are TWO populations — responders and non-responders.')
    print('The mean falls in a region where almost NO neurons actually live.')
    print("This is a BIMODAL distribution — one number can't summarize it.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The lesson

    | Statistic | Best when... | Pain biology example |
    |-----------|-------------|---------------------|
    | **Mean** | Data is roughly symmetric, no extreme outliers | Paw withdrawal latency in a uniform group |
    | **Median** | Data is skewed or has outliers | Binding affinities (Kd values span orders of magnitude) |
    | **Mode** | Data has distinct peaks / categories | Neuron subtypes in calcium imaging (responder vs non-responder) |

    **Rule of thumb:** Always plot your data before picking a summary statistic. If it's skewed, use the median. If it's bimodal, report both peaks.

    For a deeper treatment of when to use each measure and how they behave with different distribution shapes, see [Think Stats, Chapter 2 (Distributions)](https://allendowney.github.io/ThinkStats/) — Downey uses real-world datasets to show how summary statistics can mislead.
    """)
    return


@app.cell
def _(np, plt, rng):
    # Visual comparison: mean vs median on skewed data
    # This drives home WHY the choice of summary statistic matters
    _fig, _axes = plt.subplots(1, 3, figsize=(16, 4.5))
    symmetric = rng.normal(loc=5, scale=1.5, size=500)
    _axes[0].hist(symmetric, bins=30, color='#4878CF', alpha=0.7, edgecolor='white')
    # 1. Symmetric (normal) -- mean and median agree
    _axes[0].axvline(np.mean(symmetric), color='red', lw=2.5, label=f'Mean = {np.mean(symmetric):.1f}')
    _axes[0].axvline(np.median(symmetric), color='orange', lw=2.5, ls='--', label=f'Median = {np.median(symmetric):.1f}')
    _axes[0].set_title('Symmetric (Normal)\nMean and median agree', fontsize=12)
    _axes[0].legend(fontsize=9)
    _axes[0].set_xlabel('Value')
    skewed = rng.lognormal(mean=1.5, sigma=0.8, size=500)
    _axes[1].hist(skewed, bins=40, color='#E24A33', alpha=0.7, edgecolor='white')
    _axes[1].axvline(np.mean(skewed), color='red', lw=2.5, label=f'Mean = {np.mean(skewed):.1f}')
    # 2. Right-skewed -- mean pulled toward tail
    _axes[1].axvline(np.median(skewed), color='orange', lw=2.5, ls='--', label=f'Median = {np.median(skewed):.1f}')
    _axes[1].set_title('Right-Skewed (Log-normal)\nMean pulled toward the tail', fontsize=12)
    _axes[1].legend(fontsize=9)
    _axes[1].set_xlabel('Value')
    _axes[1].annotate('Mean is misleading!\nMedian better represents\n"typical" value', xy=(np.mean(skewed), 0), fontsize=9, color='red', xytext=(np.mean(skewed) * 1.3, _axes[1].get_ylim()[1] * 0.6), arrowprops=dict(arrowstyle='->', color='red'))
    bimodal = np.concatenate([rng.normal(2, 0.5, 250), rng.normal(7, 0.8, 250)])
    _axes[2].hist(bimodal, bins=35, color='#55A868', alpha=0.7, edgecolor='white')
    _axes[2].axvline(np.mean(bimodal), color='red', lw=2.5, label=f'Mean = {np.mean(bimodal):.1f}')
    _axes[2].axvline(np.median(bimodal), color='orange', lw=2.5, ls='--', label=f'Median = {np.median(bimodal):.1f}')
    _axes[2].set_title('Bimodal\nNeither mean nor median\nis meaningful!', fontsize=12)
    _axes[2].legend(fontsize=9)
    _axes[2].set_xlabel('Value')
    # 3. Bimodal -- neither works well
    plt.suptitle('Mean vs Median: the shape of your data determines which is appropriate', fontsize=13, fontweight='bold', y=1.04)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Standard Deviation and SEM — What Spread Tells You

    ### Why you need this

    You read a paper that says "von Frey threshold was 0.4 ± 0.1 g." That ± could mean two completely different things:
    - **± SD (standard deviation):** How much individual mice vary. Tells you about biological variability.
    - **± SEM (standard error of the mean):** How precisely you've estimated the group average. Tells you about measurement precision.

    SEM is always smaller than SD (by a factor of sqrt(n)), so some papers use SEM to make error bars look smaller. This is not fraud, but it can be misleading if you don't know the difference.
    """)
    return


@app.cell
def _(rng):
    # Simulate von Frey threshold data: vehicle vs CFA (inflammatory pain model)
    n_per_group = 10

    vehicle = rng.normal(loc=1.2, scale=0.25, size=n_per_group)  # healthy mice
    cfa = rng.normal(loc=0.35, scale=0.12, size=n_per_group)     # CFA-treated (allodynia)

    print("Von Frey thresholds (grams):")
    print(f"  Vehicle: {vehicle.round(2)}")
    print(f"  CFA:     {cfa.round(2)}")
    return cfa, n_per_group, vehicle


@app.cell
def _(cfa, np, vehicle):
    # Compute SD and SEM for each group
    for name, data in [('Vehicle', vehicle), ('CFA', cfa)]:
        mean = np.mean(data)
        sd = np.std(data, ddof=1)    # ddof=1 for sample SD
        sem = sd / np.sqrt(len(data)) # SEM = SD / sqrt(n)
    
        print(f"{name}:")
        print(f"  Mean = {mean:.3f} g")
        print(f"  SD   = {sd:.3f} g  (individual variability)")
        print(f"  SEM  = {sem:.3f} g  (precision of the mean)")
        print(f"  Reported as: {mean:.2f} ± {sd:.2f} (SD) or {mean:.2f} ± {sem:.2f} (SEM)")
        print()
    return


@app.cell
def _(cfa, n_per_group, np, plt, vehicle):
    # Visual: bar plots with SD vs SEM error bars side by side
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 5), sharey=True)
    groups = ['Vehicle', 'CFA']
    means = [np.mean(vehicle), np.mean(cfa)]
    sds = [np.std(vehicle, ddof=1), np.std(cfa, ddof=1)]
    sems = [sds[0] / np.sqrt(n_per_group), sds[1] / np.sqrt(n_per_group)]
    _colors = ['#4878CF', '#E24A33']
    _axes[0].bar(groups, means, yerr=sds, capsize=8, color=_colors, alpha=0.7, edgecolor='black')
    _axes[0].set_title('Error bars = SD\n(biological variability)', fontsize=13)
    # SD error bars
    _axes[0].set_ylabel('Von Frey threshold (g)')
    _axes[1].bar(groups, means, yerr=sems, capsize=8, color=_colors, alpha=0.7, edgecolor='black')
    _axes[1].set_title('Error bars = SEM\n(precision of mean)', fontsize=13)
    for _ax in _axes:
    # SEM error bars
        _ax.set_ylim(0, 1.8)
    plt.suptitle(f'Same data, n={n_per_group} per group — different error bars tell different stories', fontsize=13, y=1.02)
    plt.tight_layout()
    plt.show()
    print('The SEM bars are smaller because SEM = SD / sqrt(n).')
    print(f'With n={n_per_group}, SEM is {1 / np.sqrt(n_per_group):.1%} the size of SD.')
    print('\nNeither is wrong — but they answer DIFFERENT questions.')
    print("SD:  'How much do individual mice vary?'")
    print("SEM: 'How precisely do I know the group mean?'")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Key insight for reading papers

    When you see `mean ± something` in a paper:
    1. **Check whether it's SD or SEM** (should be stated in methods)
    2. **If SEM, mentally multiply by sqrt(n)** to get SD and understand real variability
    3. **More mice → smaller SEM** (but SD stays roughly the same)

    When you ask Claude to interpret experimental results, you can now verify whether it's handling SD vs SEM correctly.
    """)
    return


@app.cell
def _(np, plt, stats):
    # Side-by-side distribution shapes with labeled features
    # Reference card: what each shape looks like and what to watch for
    _fig, _axes = plt.subplots(1, 4, figsize=(18, 4.5))
    x = np.linspace(-4, 4, 200)
    y_normal = stats.norm.pdf(x, 0, 1)
    _axes[0].fill_between(x, y_normal, alpha=0.4, color='#4878CF')
    _axes[0].plot(x, y_normal, color='#4878CF', lw=2)
    # 1. Normal (symmetric, bell-shaped)
    _axes[0].axvline(0, color='red', lw=1.5, ls='--', label='Mean = Median')
    _axes[0].annotate('Symmetric\ntails', xy=(-2, 0.05), fontsize=9, ha='center', color='#4878CF')
    _axes[0].annotate('Symmetric\ntails', xy=(2, 0.05), fontsize=9, ha='center', color='#4878CF')
    _axes[0].set_title('Normal\n(e.g., tail-flick latencies)', fontsize=11, fontweight='bold')
    _axes[0].legend(fontsize=9)
    _axes[0].set_yticks([])
    x_sk = np.linspace(0, 10, 200)
    y_skew = stats.lognorm.pdf(x_sk, s=0.8, scale=1.5)
    _axes[1].fill_between(x_sk, y_skew, alpha=0.4, color='#E24A33')
    _axes[1].plot(x_sk, y_skew, color='#E24A33', lw=2)
    # 2. Right-skewed
    mean_sk = np.exp(np.log(1.5) + 0.8 ** 2 / 2)
    med_sk = 1.5
    _axes[1].axvline(mean_sk, color='red', lw=1.5, ls='-', label=f'Mean')
    _axes[1].axvline(med_sk, color='orange', lw=1.5, ls='--', label=f'Median')
    _axes[1].annotate('Long right\ntail', xy=(6, 0.02), fontsize=9, ha='center', color='#E24A33')
    _axes[1].set_title('Right-Skewed\n(e.g., Kd values)', fontsize=11, fontweight='bold')
    _axes[1].legend(fontsize=9)
    _axes[1].set_yticks([])
    x_ls = np.linspace(0, 10, 200)
    y_lskew = stats.lognorm.pdf(10 - x_ls, s=0.8, scale=1.5)
    _axes[2].fill_between(x_ls, y_lskew, alpha=0.4, color='#55A868')
    _axes[2].plot(x_ls, y_lskew, color='#55A868', lw=2)
    _axes[2].annotate('Long left\ntail', xy=(2, 0.02), fontsize=9, ha='center', color='#55A868')
    # 3. Left-skewed
    _axes[2].set_title('Left-Skewed\n(e.g., % cell viability)', fontsize=11, fontweight='bold')
    _axes[2].set_yticks([])
    x_bi = np.linspace(-5, 10, 200)
    y_bi = 0.45 * stats.norm.pdf(x_bi, 0.5, 0.8) + 0.55 * stats.norm.pdf(x_bi, 5, 1.2)
    _axes[3].fill_between(x_bi, y_bi, alpha=0.4, color='#8172B2')
    _axes[3].plot(x_bi, y_bi, color='#8172B2', lw=2)
    _axes[3].annotate('Population 1\n(non-responders)', xy=(0.5, 0.23), fontsize=8, ha='center')
    _axes[3].annotate('Population 2\n(responders)', xy=(5, 0.2), fontsize=8, ha='center')
    # 4. Bimodal
    _axes[3].set_title('Bimodal\n(e.g., calcium imaging)', fontsize=11, fontweight='bold')
    _axes[3].set_yticks([])
    for _ax in _axes:
        _ax.set_xlabel('Value', fontsize=10)
        _ax.spines['top'].set_visible(False)
        _ax.spines['right'].set_visible(False)
    plt.suptitle('Distribution shapes you need to recognize', fontsize=13, fontweight='bold', y=1.04)
    plt.tight_layout()
    plt.show()
    print('Before computing ANY summary statistic, plot a histogram.')
    print('The shape tells you which statistic to use and which tests are valid.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Distributions: Normal, Skewed, and Bimodal

    ### Why you need this

    The *shape* of your data determines which statistical tests are valid, which summary statistics are meaningful, and how to interpret results. Many biological measurements are NOT normally distributed:
    - Binding affinities (Kd) span orders of magnitude → **log-normal**
    - Neuron firing rates often have many zeros → **skewed right**
    - Mixed cell populations → **bimodal** (as we saw above with calcium imaging)

    And critically, **LLMs generate text by sampling from probability distributions** — understanding distribution shapes prepares you for Module 03 (probability and AI math).

    For a thorough, code-driven exploration of PMFs (probability mass functions) and CDFs (cumulative distribution functions), see [Think Stats, Chapter 3 (PMFs)](https://allendowney.github.io/ThinkStats/) and [Chapter 4 (CDFs)](https://allendowney.github.io/ThinkStats/). CDFs are especially useful for comparing distributions — they make it immediately obvious whether one group is shifted relative to another.
    """)
    return


@app.cell
def _(np, plt, rng):
    # Generate examples of each distribution shape from pain biology
    _fig, _axes = plt.subplots(2, 2, figsize=(12, 9))
    normal_data = rng.normal(loc=8.5, scale=1.2, size=500)
    # 1. Normal: tail-flick latencies in a homogeneous group
    _axes[0, 0].hist(normal_data, bins=30, edgecolor='black', alpha=0.7, color='#4878CF')
    _axes[0, 0].set_title('Normal Distribution\nTail-flick latencies (seconds)', fontsize=12)
    _axes[0, 0].set_xlabel('Latency (s)')
    _axes[0, 0].axvline(np.mean(normal_data), color='red', linewidth=2, label='Mean')
    _axes[0, 0].legend()
    skewed_data = rng.lognormal(mean=3.0, sigma=1.2, size=500)
    _axes[0, 1].hist(skewed_data, bins=40, edgecolor='black', alpha=0.7, color='#E24A33')
    # 2. Right-skewed: Kd values for a binder screen
    _axes[0, 1].set_title('Right-Skewed (Log-normal)\nBinding Kd values (nM)', fontsize=12)
    _axes[0, 1].set_xlabel('Kd (nM)')
    _axes[0, 1].axvline(np.mean(skewed_data), color='red', linewidth=2, label=f'Mean={np.mean(skewed_data):.0f}')
    _axes[0, 1].axvline(np.median(skewed_data), color='orange', linewidth=2, linestyle='--', label=f'Median={np.median(skewed_data):.0f}')
    _axes[0, 1].legend()
    bimodal_data = np.concatenate([rng.normal(loc=0.2, scale=0.15, size=250), rng.normal(loc=2.8, scale=0.6, size=250)])
    bimodal_data = np.clip(bimodal_data, 0, None)
    _axes[1, 0].hist(bimodal_data, bins=35, edgecolor='black', alpha=0.7, color='#55A868')
    _axes[1, 0].set_title('Bimodal Distribution\nCalcium responses (TRPV1+ vs TRPV1-)', fontsize=12)
    # 3. Bimodal: calcium imaging (as above)
    _axes[1, 0].set_xlabel('Delta F/F')
    _axes[1, 0].axvline(np.mean(bimodal_data), color='red', linewidth=2, label=f'Mean={np.mean(bimodal_data):.1f}')
    _axes[1, 0].legend()
    uniform_data = rng.uniform(low=0.1, high=100, size=500)
    _axes[1, 1].hist(uniform_data, bins=30, edgecolor='black', alpha=0.7, color='#8172B2')
    _axes[1, 1].set_title('Uniform Distribution\n(for comparison)', fontsize=12)
    _axes[1, 1].set_xlabel('Value')
    plt.suptitle('Distribution shapes you encounter in pain research', fontsize=14, y=1.01)
    plt.tight_layout()
    plt.show()
    print('Key takeaway: ALWAYS visualize your data before computing summary statistics.')
    # 4. Uniform: randomized drug concentrations in a dose-response
    print('A mean is meaningless for bimodal data. A mean is misleading for skewed data.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Why distributions matter for AI

    When an LLM generates text, at each step it produces a **probability distribution** over all possible next tokens (~100,000 words/word-pieces). The `temperature` parameter reshapes this distribution:

    - **temperature=0** → all probability on the single most likely token (deterministic)
    - **temperature=1** → the model's "natural" distribution
    - **temperature>1** → flatter distribution (more random/creative)

    We'll explore this in detail in notebook 03, but the key idea is: **probability distributions aren't abstract math — they're the mechanism by which Claude generates every word.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Log Transformations — Why Everything is Log-Scale

    ### Why you need this

    Three specific scenarios from your daily work:
    1. **RNA-seq results** report log2 fold changes. A log2FC of 3 means 2^3 = 8-fold increase. You need to go between log and linear scales fluently.
    2. **Binding affinities** are reported as pKd (negative log10) because Kd values range from picomolar to millimolar — 9 orders of magnitude.
    3. **LLM loss functions** use logarithms (cross-entropy loss). When you see "perplexity" in an AI paper, it's an exponentiated average log-probability.

    Log transformations are everywhere because **biology operates on multiplicative scales**, not additive ones.
    """)
    return


@app.cell
def _(np, pd):
    # Demonstrate: why RNA-seq uses log2 fold changes

    # Simulated differential expression results
    genes = ['SCN9A', 'SCN10A', 'TRPV1', 'CALCA', 'P2RX3', 'KCNQ2', 'KCNQ3', 'NTRK1', 'IL6', 'TNF']

    # Expression in TPM: control vs CFA-treated DRG
    control_expr = np.array([85, 120, 65, 210, 45, 39, 42, 96, 5, 8])
    cfa_expr = np.array([340, 60, 520, 1680, 22, 10, 11, 96, 160, 320])

    # Raw fold change vs log2 fold change
    fold_change = cfa_expr / control_expr
    log2_fc = np.log2(fold_change)

    df_expr = pd.DataFrame({
        'gene': genes,
        'control_TPM': control_expr,
        'CFA_TPM': cfa_expr,
        'fold_change': fold_change.round(2),
        'log2FC': log2_fc.round(2)
    })

    print("Differential expression: DRG after CFA injection")
    print(df_expr.to_string(index=False))
    return fold_change, genes, log2_fc


@app.cell
def _(fold_change, genes, log2_fc, plt):
    # Visual: why log scale is better for fold changes
    _fig, _axes = plt.subplots(1, 2, figsize=(14, 5))
    _colors = ['#E24A33' if fc > 0 else '#4878CF' for fc in log2_fc]
    _axes[0].barh(genes, fold_change, color=_colors, edgecolor='black', alpha=0.7)
    _axes[0].set_xlabel('Fold change (CFA / control)')
    # Linear fold change — hard to compare up vs down
    _axes[0].set_title('Linear fold change\n(misleading!)', fontsize=13)
    _axes[0].axvline(1, color='black', linewidth=1, linestyle=':')
    _axes[1].barh(genes, log2_fc, color=_colors, edgecolor='black', alpha=0.7)
    _axes[1].set_xlabel('log2 fold change')
    _axes[1].set_title('log2 fold change\n(standard in RNA-seq)', fontsize=13)
    # Log2 fold change — symmetric, easy to compare
    _axes[1].axvline(0, color='black', linewidth=1, linestyle=':')
    plt.suptitle('The same data — log scale makes up- and down-regulation symmetric', fontsize=13, y=1.02)
    plt.tight_layout()
    plt.show()
    print('On linear scale: 8-fold UP looks huge, 0.25-fold DOWN looks like nothing.')
    print('On log2 scale:   log2(8) = 3 and log2(0.25) = -2 are clearly comparable.')
    print('\nThis is why every volcano plot uses log2 fold change on the x-axis.')
    return


@app.cell
def _(np):
    # Quick reference: converting between log and linear

    print("=== Log2 fold change cheat sheet ===")
    print()
    for log2fc in [-3, -2, -1, 0, 1, 2, 3]:
        fc = 2**log2fc
        direction = 'UP' if log2fc > 0 else ('DOWN' if log2fc < 0 else 'no change')
        print(f"  log2FC = {log2fc:+d}  →  {fc:.3g}-fold  ({direction})")

    print()
    print("=== Kd to pKd (binding affinity) ===")
    print()
    for kd_nm in [0.1, 1, 10, 100, 1000, 10000]:
        kd_m = kd_nm * 1e-9
        pkd = -np.log10(kd_m)
        print(f"  Kd = {kd_nm:>8.1f} nM  →  pKd = {pkd:.1f}")
    return


@app.cell
def _(np, plt, rng):
    # Demonstrate: log transform makes skewed data normal-ish
    # This is why many statistical tests work better on log-transformed data
    kd_values = rng.lognormal(mean=4, sigma=1.5, size=1000)
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 4.5))  # simulated Kd screen
    _axes[0].hist(kd_values, bins=50, edgecolor='black', alpha=0.7, color='#E24A33')
    _axes[0].set_xlabel('Kd (nM)')
    _axes[0].set_ylabel('Count')
    _axes[0].set_title('Raw Kd values\n(wildly skewed — hard to analyze)', fontsize=12)
    _axes[1].hist(np.log10(kd_values), bins=50, edgecolor='black', alpha=0.7, color='#4878CF')
    _axes[1].set_xlabel('log10(Kd)')
    _axes[1].set_ylabel('Count')
    _axes[1].set_title('log10-transformed Kd\n(approximately normal — ready for statistics)', fontsize=12)
    plt.tight_layout()
    plt.show()
    print('Log transformation turns multiplicative processes into additive ones.')
    print('Most biological assays have multiplicative noise, which is why log scales are so common.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Identifying Outliers

    ### Why you need this

    Outliers in behavioral data can mean a dead mouse, a failed injection, a recording artifact — or genuinely unusual biology. You need systematic ways to flag them, rather than eyeballing.

    Two common approaches:
    - **Z-score method:** flag points more than 2-3 standard deviations from the mean
    - **IQR method:** flag points beyond 1.5x the interquartile range (what box plots use)
    """)
    return


@app.cell
def _(np, rng):
    # Simulate von Frey data with a couple of outliers
    vf_data = rng.normal(loc=1.2, scale=0.25, size=20)

    # Inject some outliers (e.g., mouse didn't respond, or measurement error)
    vf_data[3] = 3.8   # suspiciously high
    vf_data[15] = 0.01  # suspiciously low

    # Z-score method
    z_scores = (vf_data - np.mean(vf_data)) / np.std(vf_data, ddof=1)
    z_outliers = np.abs(z_scores) > 2

    # IQR method
    q1, q3 = np.percentile(vf_data, [25, 75])
    iqr = q3 - q1
    iqr_outliers = (vf_data < q1 - 1.5*iqr) | (vf_data > q3 + 1.5*iqr)

    print("Von Frey thresholds (g):")
    for i, val in enumerate(vf_data):
        flags = []
        if z_outliers[i]: flags.append('Z-score')
        if iqr_outliers[i]: flags.append('IQR')
        flag_str = f"  <-- OUTLIER ({', '.join(flags)})" if flags else ''
        print(f"  Mouse {i+1:2d}: {val:.2f}{flag_str}")
    return iqr_outliers, vf_data


@app.cell
def _(iqr_outliers, np, plt, vf_data):
    # Visualize with a box plot (which uses the IQR method internally)
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 5))
    _axes[0].scatter(np.zeros_like(vf_data), vf_data, s=60, alpha=0.7, color=['red' if o else 'steelblue' for o in iqr_outliers], edgecolor='black', zorder=5)
    # Strip plot showing every point
    _axes[0].set_xlim(-0.5, 0.5)
    _axes[0].set_xticks([])
    _axes[0].set_ylabel('Von Frey threshold (g)')
    _axes[0].set_title('Individual data points\n(red = IQR outliers)', fontsize=12)
    bp = _axes[1].boxplot(vf_data, vert=True, widths=0.5)
    _axes[1].set_ylabel('Von Frey threshold (g)')
    _axes[1].set_title('Box plot\n(diamonds = outliers by IQR rule)', fontsize=12)
    _axes[1].set_xticklabels(['Vehicle'])
    # Box plot
    plt.suptitle('Outlier detection in behavioral data', fontsize=13, y=1.02)
    plt.tight_layout()
    plt.show()
    print("Important: flagging an outlier doesn't mean you should remove it.")
    print('You need a biological or technical reason (failed injection, equipment error, etc.).')
    print('Document your exclusion criteria BEFORE looking at the data.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: DRG Calcium Imaging Analysis

    You've performed calcium imaging on DRG neurons from a CFA-treated mouse. Each neuron was exposed to three stimuli in sequence: capsaicin (TRPV1 agonist), ATP (P2X agonist), and high K+ (depolarization control).

    Your tasks:
    1. Generate synthetic data and compute descriptive statistics
    2. Visualize the distributions
    3. Identify which summary statistics are appropriate for each stimulus
    4. Find outlier neurons

    **Step 1:** Run the cell below to generate the dataset.
    """)
    return


@app.cell
def _(np, pd, rng):
    # Generate synthetic calcium imaging data
    _n_neurons = 80
    trpv1_pos = int(_n_neurons * 0.45)
    # Capsaicin: bimodal (TRPV1+ and TRPV1- neurons)
    capsaicin_response = np.concatenate([rng.normal(loc=3.0, scale=0.9, size=trpv1_pos), rng.normal(loc=0.15, scale=0.1, size=_n_neurons - trpv1_pos)])  # ~45% are TRPV1+
    capsaicin_response = np.clip(capsaicin_response, 0, None)
    atp_response = rng.lognormal(mean=0.3, sigma=0.8, size=_n_neurons)  # responders
    highk_response = rng.normal(loc=4.5, scale=1.0, size=_n_neurons)  # non-responders
    highk_response = np.clip(highk_response, 0.5, None)
    imaging_df = pd.DataFrame({'neuron_id': [f'N{i + 1:03d}' for i in range(_n_neurons)], 'capsaicin_dFF': capsaicin_response.round(3), 'atp_dFF': atp_response.round(3), 'highK_dFF': highk_response.round(3)})
    print(f'Generated calcium imaging data for {_n_neurons} DRG neurons')
    # ATP: right-skewed (most respond weakly, some respond strongly)
    print(f'Columns: {list(imaging_df.columns)}')
    # High K+: normal-ish (most neurons depolarize similarly)
    imaging_df.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 1: Compute descriptive statistics for each stimulus

    For each of the three responses (capsaicin, ATP, high K+), compute: mean, median, SD, SEM, min, max.
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: imaging_df[['capsaicin_dFF', 'atp_dFF', 'highK_dFF']].describe() gets you most of it
    # For SEM, you'll need to compute it manually: SD / sqrt(n)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 2: Visualize all three distributions

    Create a figure with three histograms (one per stimulus). Mark the mean and median on each.
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    # Then axes[0].hist(...), axes[1].hist(...), axes[2].hist(...)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 3: Which summary statistic is appropriate for each?

    After looking at the histograms, answer these questions in the markdown cell below:
    - For capsaicin responses: should you report mean or median? Why?
    - For ATP responses: should you report mean or median? Why?
    - For high K+ responses: does it matter? Why?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    *Your answers here:*

    - Capsaicin: ...
    - ATP: ...
    - High K+: ...
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 4: Identify outlier neurons in the high K+ response

    Use both Z-score (threshold=2.5) and IQR methods. How many outliers does each method find?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: follow the pattern from Section 5 above
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    | Concept | What it tells you | Pain biology example |
    |---------|------------------|---------------------|
    | **Mean** | Center of symmetric data | Average tail-flick latency |
    | **Median** | Center of skewed data | Typical binding Kd in a screen |
    | **SD** | How much individuals vary | Variability in von Frey thresholds |
    | **SEM** | How precisely you know the mean | Error bars on a bar graph |
    | **Distribution shape** | What kind of data you have | Normal, skewed, bimodal |
    | **Log transform** | Makes multiplicative data additive | RNA-seq log2FC, pKd |
    | **Outlier detection** | Flags unusual observations | Failed recordings in calcium imaging |

    **AI connection preview:** In notebook 03, we'll see how probability distributions are the foundation of LLM text generation — temperature, top-p sampling, and softmax all manipulate distributions over tokens.

    **Next up:** Hypothesis testing and p-values — the statistics you encounter in every paper and every RNA-seq analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Cloud Computing and When to Use What](../07-cloud-and-hpc/03-cloud-computing-and-when-to-use-what.py) | [Module Index](../README.md) | [Next: Hypothesis Testing and P-values \u2192](02-hypothesis-testing-and-pvalues.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **[Think Stats](https://allendowney.github.io/ThinkStats/)** (Allen Downey) -- Free online textbook by the same author as Think Python. Covers exploratory data analysis, distributions, PMFs, CDFs, and statistical thinking with Python code throughout. **Especially relevant chapters:**
      - [Chapter 1: Exploratory Data Analysis](https://allendowney.github.io/ThinkStats/) -- first look at a dataset, summary statistics, histograms
      - [Chapter 2: Distributions](https://allendowney.github.io/ThinkStats/) -- representing distributions, comparing distributions, outliers
      - [Chapter 3: Probability Mass Functions](https://allendowney.github.io/ThinkStats/) -- PMFs for comparing groups, visualizing discrete distributions
      - [Chapter 4: Cumulative Distribution Functions](https://allendowney.github.io/ThinkStats/) -- CDFs as the most useful way to compare distributions
    - **[Think Python, Chapter 7: Iteration](https://allendowney.github.io/ThinkPython/chap07.html)** -- Loops and iteration in Python, which underpin computing statistics over datasets.
    - **[NumPy: Statistical Functions](https://numpy.org/doc/stable/reference/routines.statistics.html)** -- Official reference for `np.mean()`, `np.median()`, `np.std()`, `np.percentile()`, and other statistical functions used throughout this notebook.
    - **[SciPy: Statistical Functions (`scipy.stats`)](https://docs.scipy.org/doc/scipy/reference/stats.html)** -- Comprehensive library for probability distributions, statistical tests, and descriptive statistics.
    - **[Khan Academy: Statistics and Probability](https://www.khanacademy.org/math/statistics-probability)** -- A gentler, visual introduction to the same concepts covered here (mean, median, standard deviation, distributions).
    - **[Matplotlib: Histogram Tutorial](https://matplotlib.org/stable/gallery/statistics/hist.html)** -- How to create and customize histograms for visualizing distributions.
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
    - 2026-03-25: QA pass — added "Why this matters" rationale blockquote
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

