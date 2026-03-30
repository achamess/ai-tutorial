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
    # Module: Math You Actually Need -- 02: Hypothesis Testing and P-values

    **Goal:** Understand what p-values actually mean, when to use common statistical tests, and why multiple testing correction is essential for RNA-seq -- so you can evaluate papers, check Claude's statistical claims, and analyze your own data correctly.

    **References:** [SciPy `ttest_ind`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html) | [SciPy `f_oneway`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html) | [Think Stats](https://allendowney.github.io/ThinkStats/) (Allen Downey)

    > **Book companion:** This notebook pairs well with [Think Stats](https://allendowney.github.io/ThinkStats/) by Allen Downey. Think Stats covers hypothesis testing (Chapter 7), estimation (Chapter 8), and linear regression (Chapter 9) with the same code-first, accessible approach you've seen in Think Python. If you want to go deeper on any topic here — especially the mechanics of permutation tests and confidence intervals — Think Stats is the place.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Descriptive Stats and Distributions](01-descriptive-stats-and-distributions.py) | [Module Index](../README.md) | [Next: Probability and AI Math \u2192](03-probability-and-ai-math.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Every paper you read and every experiment you run involves p-values and statistical tests. Misunderstanding them leads to wrong conclusions about your NaV1.7 binder candidates -- declaring a drug "effective" when the result is noise, or missing a real effect because you used the wrong test.
    > - Multiple testing correction is non-negotiable for RNA-seq and other -omics analyses. Without it, testing 20,000 genes at p < 0.05 gives you ~1,000 false positives. This notebook teaches you the Benjamini-Hochberg correction used by DESeq2 and edgeR.
    > - Effect size (Cohen's d) answers the question p-values cannot: "Is the difference biologically meaningful?" A drug that raises von Frey threshold by 0.02 g can be statistically significant with enough mice but clinically useless.
    > - When Claude interprets statistical results for you, you need to verify it chose the right test, applied multiple testing correction where needed, and correctly interpreted the p-value. This notebook gives you that verification skill.
    """)
    return


@app.cell
def _():
    import numpy as np
    import pandas as pd
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy import stats

    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (8, 5)
    plt.rcParams['font.size'] = 12

    rng = np.random.default_rng(42)

    print("Ready to go!")
    return np, pd, plt, rng, stats


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. What a P-value Actually Is (and Isn't)

    ### Why you need this

    P-values are the most commonly misunderstood statistic in all of science. Even experienced researchers get this wrong. Getting it right means you can critically evaluate every statistical claim you encounter — in papers, in your own data, and in Claude's outputs.

    ### The definition

    **A p-value is the probability of seeing data at least as extreme as what you observed, IF the null hypothesis were true.**

    It is NOT:
    - The probability that the null hypothesis is true
    - The probability that your result is a fluke
    - A measure of effect size or biological importance

    For an accessible, simulation-based explanation of this distinction (with Python code you can run), see [Think Stats, Chapter 7 (Hypothesis Testing)](https://allendowney.github.io/ThinkStats/). Downey builds p-values from first principles using permutation tests, which makes the logic much clearer than the formula-based approach in most textbooks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Warning:** P-value misconceptions are everywhere -- even in published papers. Here are the three most dangerous:
    > - **"p < 0.05 means the result is true"** -- No. It means the data would be unlikely *if* the null hypothesis were true. It says nothing about the probability the drug works.
    > - **"p = 0.049 is significant, p = 0.051 is not"** -- This is an arbitrary line, not a cliff. These two p-values represent almost identical evidence. Never treat 0.05 as a magic boundary.
    > - **"Non-significant means no effect"** -- Absence of evidence is not evidence of absence. A non-significant result with n=3 might become significant with n=30.
    >
    > When Claude interprets statistical results, watch for these same errors. LLMs sometimes say "the drug had no effect (p = 0.08)" when the correct interpretation is "we did not find sufficient evidence for an effect at the 0.05 threshold."

    > **Tip:** Always check assumptions before running statistical tests. Every test has assumptions (normality, equal variances, independence). Violating them doesn't always invalidate results, but it can. Before any t-test, check: (1) Are the data approximately normal? (Shapiro-Wilk test or just look at a histogram.) (2) Are the variances similar? (Levene's test or eyeball the spread.) If either fails, use a non-parametric alternative (Mann-Whitney U instead of t-test).
    """)
    return


@app.cell
def _(np, rng, stats):
    # Coin-flip simulation: is a coin fair?
    # You flip a coin 20 times and get 14 heads. Is the coin biased?

    n_flips = 20
    observed_heads = 14

    # Null hypothesis: the coin is fair (p = 0.5)
    # P-value: if the coin IS fair, how often would we see 14 or more heads in 20 flips?

    # Simulate 100,000 experiments with a fair coin
    n_simulations = 100_000
    simulated_heads = rng.binomial(n=n_flips, p=0.5, size=n_simulations)

    # P-value = fraction of simulations as extreme or more extreme
    # Two-sided: as extreme in either direction
    p_value_sim = np.mean(np.abs(simulated_heads - 10) >= np.abs(observed_heads - 10))

    # Exact calculation using scipy
    p_value_exact = stats.binomtest(observed_heads, n_flips, 0.5).pvalue  # two-sided

    print(f"Observed: {observed_heads} heads in {n_flips} flips")
    print(f"Null hypothesis: coin is fair (50% heads)")
    print(f"P-value (simulated): {p_value_sim:.4f}")
    print(f"P-value (exact):     {p_value_exact:.4f}")
    print()
    print(f"Interpretation: If the coin IS fair, you'd see results this extreme")
    print(f"about {p_value_exact:.1%} of the time. That's not super rare — probably just luck.")
    return observed_heads, p_value_exact, simulated_heads


@app.cell
def _(np, observed_heads, p_value_exact, plt, simulated_heads):
    # Visualize: distribution of heads under the null hypothesis
    _fig, _ax = plt.subplots(figsize=(10, 5))
    bins = np.arange(-0.5, 21.5, 1)
    counts, _, patches = _ax.hist(simulated_heads, bins=bins, edgecolor='black', alpha=0.7, color='steelblue', density=True)
    for patch, left_edge in zip(patches, bins[:-1]):
        center = left_edge + 0.5
        if abs(center - 10) >= abs(observed_heads - 10):
    # Color the "extreme" regions
            patch.set_facecolor('#E24A33')
            patch.set_alpha(0.8)
    _ax.axvline(observed_heads, color='red', linewidth=2, linestyle='--', label=f'Observed: {observed_heads} heads')
    _ax.set_xlabel('Number of heads in 20 flips')
    _ax.set_ylabel('Probability')
    _ax.set_title(f'Distribution under null hypothesis (fair coin)\nRed region = results as extreme or more extreme (p = {p_value_exact:.3f})')
    _ax.legend(fontsize=12)
    _ax.set_xticks(range(0, 21, 2))
    plt.tight_layout()
    plt.show()
    print('The red bars show all outcomes as extreme or more extreme than what you observed.')
    print('The p-value is the total area of the red bars.')
    print('Small p-value = your result would be very unlikely if the null were true.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Common p-value thresholds

    | p-value | Convention | What it means |
    |---------|-----------|---------------|
    | p < 0.05 | "Significant" | Less than 5% chance of this result under the null |
    | p < 0.01 | "Highly significant" | Less than 1% chance |
    | p < 0.001 | "Very highly significant" | Less than 0.1% chance |

    **But remember:** these thresholds are arbitrary conventions, not laws of nature. A p-value of 0.049 is not fundamentally different from 0.051.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. T-tests: Comparing Two Groups

    ### Why you need this

    The most common statistical question in pain research: "Is group A different from group B?" Vehicle vs drug. Wild-type vs knockout. Baseline vs post-injury. The t-test is the workhorse for this comparison.
    """)
    return


@app.cell
def _(np, rng):
    # Scenario: testing a NaV1.7 binder in a von Frey assay
    # Vehicle vs binder-treated mice, both with CFA-induced inflammatory pain
    _n_per_group = 10
    vehicle_vf = rng.normal(loc=0.35, scale=0.12, size=_n_per_group)
    binder_vf = rng.normal(loc=0.75, scale=0.18, size=_n_per_group)
    vehicle_vf = np.clip(vehicle_vf, 0.04, None)  # CFA + vehicle
    binder_vf = np.clip(binder_vf, 0.04, None)  # CFA + NaV1.7 binder
    print('Von Frey thresholds (g) — CFA inflammatory pain model:')
    # Ensure non-negative
    print(f'  Vehicle (n={_n_per_group}):        {vehicle_vf.round(2)}')
    print(f'  NaV1.7 binder (n={_n_per_group}):  {binder_vf.round(2)}')
    print()
    print(f'  Vehicle mean:  {np.mean(vehicle_vf):.3f} ± {np.std(vehicle_vf, ddof=1):.3f} g (SD)')
    print(f'  Binder mean:   {np.mean(binder_vf):.3f} ± {np.std(binder_vf, ddof=1):.3f} g (SD)')
    return binder_vf, vehicle_vf


@app.cell
def _(binder_vf, stats, vehicle_vf):
    # Independent two-sample t-test
    t_stat, p_value = stats.ttest_ind(vehicle_vf, binder_vf)

    print(f"Two-sample t-test:")
    print(f"  t-statistic = {t_stat:.3f}")
    print(f"  p-value     = {p_value:.6f}")
    print()
    if p_value < 0.05:
        print(f"  Result: SIGNIFICANT at alpha=0.05")
        print(f"  The binder group has significantly different von Frey thresholds.")
    else:
        print(f"  Result: NOT significant at alpha=0.05")
    print()
    print("But wait — p-value alone doesn't tell you if the effect is MEANINGFUL...")
    return (p_value,)


@app.cell
def _(binder_vf, np, p_value, plt, vehicle_vf):
    # Visualize the two groups
    _fig, _axes = plt.subplots(1, 2, figsize=(12, 5))
    for _i, (_name, _data, _color) in enumerate([('Vehicle', vehicle_vf, '#E24A33'), ('NaV1.7 binder', binder_vf, '#4878CF')]):
    # Strip plot with means
        _axes[0].scatter(np.full_like(_data, _i), _data, s=80, alpha=0.7, color=_color, edgecolor='black', zorder=5)
        _axes[0].hlines(np.mean(_data), _i - 0.2, _i + 0.2, color='black', linewidth=2)
    _axes[0].set_xticks([0, 1])
    _axes[0].set_xticklabels(['Vehicle', 'NaV1.7 binder'])
    _axes[0].set_ylabel('Von Frey threshold (g)')
    _axes[0].set_title(f'CFA model: Vehicle vs NaV1.7 binder\np = {p_value:.4f}', fontsize=12)
    bp = _axes[1].boxplot([vehicle_vf, binder_vf], labels=['Vehicle', 'NaV1.7 binder'], patch_artist=True, widths=0.5)
    bp['boxes'][0].set_facecolor('#E24A33')
    bp['boxes'][1].set_facecolor('#4878CF')
    for box in bp['boxes']:
        box.set_alpha(0.5)
    _axes[1].set_ylabel('Von Frey threshold (g)')
    _axes[1].set_title('Box plot view', fontsize=12)
    # Box plot
    plt.suptitle('Always show individual data points — not just bar graphs', fontsize=13, y=1.02)
    plt.tight_layout()
    plt.show()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Which t-test to use?

    | Situation | Test | scipy function |
    |-----------|------|----------------|
    | Two independent groups (vehicle vs drug) | Independent t-test | `stats.ttest_ind()` |
    | Same subjects measured twice (before vs after) | Paired t-test | `stats.ttest_rel()` |
    | One group vs a known value | One-sample t-test | `stats.ttest_1samp()` |

    **Common mistake:** Using an independent t-test when you have paired data (e.g., baseline vs post-CFA in the same mice). The paired test is almost always more powerful because it accounts for individual variability.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Effect Size — Why Significance Isn't the Same as Importance

    ### Why you need this

    With enough mice, even a tiny difference becomes "statistically significant." A drug that raises von Frey threshold from 0.35 g to 0.37 g could have p < 0.001 with n=200 per group — but a 0.02 g change is biologically meaningless. **Effect size tells you whether the difference matters.**

    This is critical for evaluating papers AND for catching errors when Claude interprets statistical results.

    For a deeper discussion of how estimation and effect sizes complement hypothesis testing, see [Think Stats, Chapter 8 (Estimation)](https://allendowney.github.io/ThinkStats/). Downey argues convincingly that confidence intervals on effect sizes are often more informative than p-values alone — a perspective that's gaining traction in the biomedical statistics community.
    """)
    return


@app.cell
def _(np, rng, stats):
    # Demonstrate: same p-value, completely different effect sizes

    # Scenario A: Large effect, small sample
    n_a = 8
    group1_a = rng.normal(loc=0.35, scale=0.12, size=n_a)
    group2_a = rng.normal(loc=0.90, scale=0.15, size=n_a)

    # Scenario B: Tiny effect, large sample
    n_b = 200
    group1_b = rng.normal(loc=0.35, scale=0.12, size=n_b)
    group2_b = rng.normal(loc=0.39, scale=0.12, size=n_b)

    _, p_a = stats.ttest_ind(group1_a, group2_a)
    _, p_b = stats.ttest_ind(group1_b, group2_b)

    # Cohen's d: standardized effect size
    def cohens_d(group1, group2):
        """Compute Cohen's d effect size."""
        n1, n2 = len(group1), len(group2)
        var1, var2 = np.var(group1, ddof=1), np.var(group2, ddof=1)
        pooled_std = np.sqrt(((n1-1)*var1 + (n2-1)*var2) / (n1+n2-2))
        return abs(np.mean(group1) - np.mean(group2)) / pooled_std

    d_a = cohens_d(group1_a, group2_a)
    d_b = cohens_d(group1_b, group2_b)

    print("Scenario A: Large effect, small n")
    print(f"  n = {n_a} per group")
    print(f"  Difference in means: {abs(np.mean(group1_a) - np.mean(group2_a)):.3f} g")
    print(f"  p = {p_a:.4f}")
    print(f"  Cohen's d = {d_a:.2f} (LARGE effect)")
    print()
    print("Scenario B: Tiny effect, large n")
    print(f"  n = {n_b} per group")
    print(f"  Difference in means: {abs(np.mean(group1_b) - np.mean(group2_b)):.3f} g")
    print(f"  p = {p_b:.4f}")
    print(f"  Cohen's d = {d_b:.2f} (SMALL effect)")
    print()
    print("Both might be 'significant' — but only Scenario A is biologically meaningful.")
    return


@app.cell
def _():
    # Cohen's d interpretation guide
    print("=== Cohen's d effect size benchmarks ===")
    print()
    print("  d = 0.2  →  Small effect   (barely noticeable)")
    print("  d = 0.5  →  Medium effect   (clearly visible)")
    print("  d = 0.8  →  Large effect    (obvious difference)")
    print("  d > 1.0  →  Very large      (dramatic difference)")
    print()
    print("For pain research: if your drug has d < 0.3, it's probably not")
    print("clinically meaningful even if p < 0.05 with a big enough n.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Beyond T-tests: When You Have More Than 2 Groups

    ### Why you need this

    Real experiments rarely have just 2 groups. A dose-response study might have vehicle + 3 doses. A gene knockout study might compare WT, heterozygous, and knockout. **Running multiple t-tests inflates your false positive rate.** With 4 groups, you'd do 6 pairwise t-tests, and the chance of at least one false positive jumps from 5% to ~26%.

    The solution: ANOVA (Analysis of Variance) first, then post-hoc comparisons.
    """)
    return


@app.cell
def _(np, rng):
    # Scenario: NaV1.7 binder dose-response in CFA model
    _n_per_group = 8
    groups = {'Vehicle': rng.normal(loc=0.32, scale=0.1, size=_n_per_group), 'Low (1 mg/kg)': rng.normal(loc=0.45, scale=0.12, size=_n_per_group), 'Mid (3 mg/kg)': rng.normal(loc=0.72, scale=0.15, size=_n_per_group), 'High (10 mg/kg)': rng.normal(loc=1.05, scale=0.18, size=_n_per_group)}
    groups = {k: np.clip(v, 0.04, None) for k, v in groups.items()}
    print('Von Frey thresholds by dose group:')
    for _name, _data in groups.items():
    # Clip to non-negative
        print(f'  {_name:20s}: {np.mean(_data):.3f} ± {np.std(_data, ddof=1):.3f} g (n={len(_data)})')
    return (groups,)


@app.cell
def _(groups, stats):
    # WRONG approach: multiple t-tests
    print('=== WRONG: Multiple t-tests ===')
    group_names = list(groups.keys())
    group_data = list(groups.values())
    n_tests = 0
    for _i in range(len(group_names)):
        for _j in range(_i + 1, len(group_names)):
            _, p = stats.ttest_ind(group_data[_i], group_data[_j])
            n_tests += 1
            _sig = '*' if p < 0.05 else 'ns'
            print(f'  {group_names[_i]} vs {group_names[_j]}: p = {p:.4f} {_sig}')
    print(f'\nProblem: {n_tests} tests! Family-wise error rate up to ~{1 - 0.95 ** n_tests:.0%}')
    return group_data, group_names


@app.cell
def _(group_data, stats):
    # RIGHT approach: One-way ANOVA first
    f_stat, p_anova = stats.f_oneway(*group_data)

    print("=== RIGHT: One-way ANOVA ===")
    print(f"  F-statistic = {f_stat:.2f}")
    print(f"  p-value     = {p_anova:.6f}")
    print()
    if p_anova < 0.05:
        print("  ANOVA significant → proceed to post-hoc pairwise comparisons")
        print("  (with correction for multiple comparisons)")
    else:
        print("  ANOVA not significant → no evidence of difference between any groups")
        print("  Do NOT go fishing with individual t-tests!")
    return f_stat, p_anova


@app.cell
def _(group_data, group_names, stats):
    # Post-hoc: pairwise comparisons with Bonferroni correction
    # Bonferroni: multiply each p-value by the number of tests (or equivalently, divide alpha)
    from itertools import combinations
    print('=== Post-hoc pairwise comparisons (Bonferroni corrected) ===')
    print()
    pairs = list(combinations(range(len(group_names)), 2))
    n_comparisons = len(pairs)
    for _i, _j in pairs:
        _, p_raw = stats.ttest_ind(group_data[_i], group_data[_j])
        p_corrected = min(p_raw * n_comparisons, 1.0)
        _sig = '*' if p_corrected < 0.05 else 'ns'
        print(f'  {group_names[_i]:20s} vs {group_names[_j]:20s}: p_raw={p_raw:.4f}, p_corrected={p_corrected:.4f} {_sig}')
    print(f'\nBonferroni correction: multiply each p by {n_comparisons} (number of comparisons)')  # Bonferroni correction
    print('This is conservative but simple. More powerful methods exist (Tukey HSD, etc.)')
    return


@app.cell
def _(f_stat, group_data, group_names, np, p_anova, plt, rng):
    # Visualize the dose-response
    _fig, _ax = plt.subplots(figsize=(10, 6))
    colors = ['#E24A33', '#FDB863', '#4878CF', '#55A868']
    positions = range(len(group_names))
    for pos, (_name, _data, _color) in enumerate(zip(group_names, group_data, colors)):
        jitter = rng.uniform(-0.1, 0.1, size=len(_data))
        _ax.scatter(np.full_like(_data, pos) + jitter, _data, s=70, alpha=0.7, color=_color, edgecolor='black', zorder=5)
        _ax.hlines(np.mean(_data), pos - 0.2, pos + 0.2, color='black', linewidth=2.5)
        sem = np.std(_data, ddof=1) / np.sqrt(len(_data))
        _ax.vlines(pos, np.mean(_data) - sem, np.mean(_data) + sem, color='black', linewidth=2)
    _ax.set_xticks(positions)
    _ax.set_xticklabels(group_names, fontsize=11)  # SEM error bars
    _ax.set_ylabel('Von Frey threshold (g)', fontsize=12)
    _ax.set_title(f'NaV1.7 binder dose-response (CFA model)\nOne-way ANOVA: F={f_stat:.1f}, p={p_anova:.4f}', fontsize=13)
    plt.tight_layout()
    plt.show()
    print('Bars = mean ± SEM. Individual data points shown.')
    print('This is how most behavioral pharmacology data should be presented.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Decision tree: which test to use

    ```
    How many groups are you comparing?
    │
    ├── 2 groups
    │   ├── Same subjects measured twice? → Paired t-test
    │   └── Different subjects?           → Independent t-test
    │
    ├── 3+ groups
    │   ├── One factor (e.g., dose)?      → One-way ANOVA + post-hoc
    │   └── Two factors (dose × time)?    → Two-way ANOVA
    │
    └── Data not normally distributed?
        ├── 2 groups  → Mann-Whitney U (independent) or Wilcoxon (paired)
        └── 3+ groups → Kruskal-Wallis
    ```

    **Pro tip:** When asking Claude to help choose a statistical test, provide: (1) number of groups, (2) whether measurements are paired or independent, (3) whether data looks normally distributed. Claude is quite good at test selection when given this information.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Visual Decision Tree: Which Statistical Test to Use

    ```mermaid
    flowchart TD
        START["What kind of data<br>do you have?"] --> CONT{"Continuous<br>(measurements)?"}
        START --> CAT{"Categorical<br>(counts/proportions)?"}

        CONT --> NGROUPS{"How many<br>groups?"}
        NGROUPS -->|"2 groups"| PAIRED{"Same subjects<br>measured twice?"}
        NGROUPS -->|"3+ groups"| NORMAL2{"Data roughly<br>normal?"}

        PAIRED -->|"Yes<br>(before/after)"| PT["Paired t-test<br>stats.ttest_rel()"]
        PAIRED -->|"No<br>(different subjects)"| NORMAL1{"Data roughly<br>normal?"}

        NORMAL1 -->|"Yes"| TT["Independent t-test<br>stats.ttest_ind()"]
        NORMAL1 -->|"No / n<10"| MW["Mann-Whitney U<br>stats.mannwhitneyu()"]

        NORMAL2 -->|"Yes"| ANOVA["One-way ANOVA<br>stats.f_oneway()<br>+ post-hoc Tukey"]
        NORMAL2 -->|"No / n<10"| KW["Kruskal-Wallis<br>stats.kruskal()<br>+ post-hoc Dunn"]

        CAT --> CHI["Chi-squared test<br>stats.chi2_contingency()<br>or Fisher's exact test"]

        style START fill:#4878CF,color:#fff
        style PT fill:#55A868,color:#fff
        style TT fill:#55A868,color:#fff
        style MW fill:#FDB863,color:#000
        style ANOVA fill:#55A868,color:#fff
        style KW fill:#FDB863,color:#000
        style CHI fill:#8172B2,color:#fff
    ```

    **Green boxes** = parametric tests (assume roughly normal data). **Yellow boxes** = non-parametric alternatives (safer for small samples or non-normal data). When in doubt, the non-parametric option is the safer choice.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Multiple Testing: The RNA-seq Problem

    ### Why you need this

    This is possibly the most practically important section for your genomics work. When you run an RNA-seq experiment, you're testing ~20,000 genes simultaneously. At p < 0.05, you expect **1,000 false positives by pure chance.** If you don't correct for this, your "significant" gene list is mostly noise.

    **This directly affects your work:** when you look at differential expression results for NaV1.7/1.8 pathway genes after CFA, you need to know whether a "significant" result survives multiple testing correction or is just one of a thousand false positives.

    For a code-driven walkthrough of how regression interacts with multiple testing (and when to use regression instead of many separate tests), see [Think Stats, Chapter 9 (Linear Regression)](https://allendowney.github.io/ThinkStats/).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** Multiple testing is the silent killer of genomics results. If you test 20,000 genes at p < 0.05, you expect ~1,000 false positives by chance alone. This is why adjusted p-values (FDR/Benjamini-Hochberg) are mandatory for any experiment with more than a handful of comparisons. The raw p-value tells you about one test; the adjusted p-value tells you about your entire experiment.

    > **Decision point: Which statistical test for which scenario**
    >
    > | Scenario | Test | Assumptions | Pain biology example |
    > |----------|------|-------------|---------------------|
    > | 2 groups, normal data | **Unpaired t-test** | Normality, equal variance | Vehicle vs drug withdrawal latency |
    > | 2 groups, non-normal or small n | **Mann-Whitney U** | None (non-parametric) | Von Frey thresholds (ordinal-like data) |
    > | 2 groups, paired measurements | **Paired t-test** | Normal differences | Before vs after drug in same animal |
    > | 3+ groups, normal data | **One-way ANOVA + post-hoc** | Normality, equal variance | Vehicle vs low-dose vs high-dose |
    > | 3+ groups, non-normal | **Kruskal-Wallis + Dunn's** | None | Multiple pain models compared |
    > | 2 groups x 2 timepoints | **Two-way ANOVA** | Normality | Drug x time interaction in behavioral study |
    > | 20,000 genes | **DESeq2/edgeR** (built-in FDR correction) | Negative binomial distribution | RNA-seq differential expression |
    > | Correlation between 2 variables | **Pearson** (normal) or **Spearman** (any) | Pearson: linearity, normality | Kd vs selectivity correlation |
    >
    > **When in doubt:** Use the non-parametric version. It's slightly less powerful but never wrong due to violated assumptions.
    """)
    return


@app.cell
def _(np, rng):
    # Simulate the multiple testing problem
    # Test 20,000 genes, where only 500 are truly differentially expressed

    n_genes = 20000
    n_true_de = 500       # truly differentially expressed genes
    n_null = n_genes - n_true_de  # genes with no real change

    # Generate p-values
    # Null genes: p-values uniformly distributed between 0 and 1
    p_null = rng.uniform(0, 1, size=n_null)

    # True DE genes: p-values concentrated near 0 (small)
    p_true = rng.beta(a=0.3, b=5, size=n_true_de)  # small p-values

    all_pvalues = np.concatenate([p_null, p_true])
    is_truly_de = np.concatenate([np.zeros(n_null), np.ones(n_true_de)]).astype(bool)

    # Apply naive threshold p < 0.05
    naive_significant = all_pvalues < 0.05

    print(f"=== Naive approach: p < 0.05 ===")
    print(f"Total genes tested: {n_genes:,}")
    print(f"Truly DE genes: {n_true_de}")
    print(f"Called significant: {naive_significant.sum():,}")
    print(f"  True positives:  {(naive_significant & is_truly_de).sum()}")
    print(f"  FALSE positives: {(naive_significant & ~is_truly_de).sum()}")
    print(f"  False discovery rate: {(naive_significant & ~is_truly_de).sum() / naive_significant.sum():.1%}")
    print()
    print("Without correction, about HALF of your 'significant' genes are false positives!")
    return all_pvalues, is_truly_de, n_genes, naive_significant


@app.cell
def _(plt):
    # Visual explanation of the multiple testing / FDR problem
    # The "20,000 genes" problem made concrete
    _fig, _axes = plt.subplots(1, 3, figsize=(18, 5))
    categories = ['Total genes\ntested', 'Truly DE\ngenes', 'Truly null\ngenes']
    values = [20000, 500, 19500]
    # Panel 1: The scale of the problem
    colors_bar = ['#4878CF', '#55A868', '#E24A33']
    _axes[0].bar(categories, values, color=colors_bar, edgecolor='black', alpha=0.8)
    _axes[0].set_ylabel('Number of genes')
    _axes[0].set_title('The scale of RNA-seq testing', fontsize=12, fontweight='bold')
    for _i, v in enumerate(values):
        _axes[0].text(_i, v + 300, f'{v:,}', ha='center', fontsize=11, fontweight='bold')
    true_positives = 400
    false_positives = 975
    false_negatives = 100
    # Panel 2: What happens at p < 0.05 without correction
    # 5% of 19,500 null genes = 975 false positives!
    true_negatives = 18525  # ~80% of 500 truly DE genes detected
    sig_categories = ['True\npositives', 'FALSE\nPOSITIVES', 'False\nnegatives', 'True\nnegatives']  # 5% of 19,500 null genes
    sig_values = [true_positives, false_positives, false_negatives, true_negatives]  # 20% of 500 truly DE missed
    sig_colors = ['#55A868', '#E24A33', '#FDB863', '#cccccc']
    bars = _axes[1].bar(sig_categories, sig_values, color=sig_colors, edgecolor='black', alpha=0.8)
    _axes[1].set_ylabel('Number of genes')
    _axes[1].set_title('Without correction (p < 0.05)\n975 false discoveries!', fontsize=12, fontweight='bold')
    for _i, v in enumerate(sig_values):
        _axes[1].text(_i, v + 200, f'{v:,}', ha='center', fontsize=10, fontweight='bold')
    _axes[1].annotate(f'FDR = {false_positives}/{true_positives + false_positives} = {false_positives / (true_positives + false_positives):.0%}', xy=(0.5, 0.85), xycoords='axes fraction', fontsize=13, fontweight='bold', color='#E24A33', ha='center', bbox=dict(boxstyle='round', facecolor='lightyellow', edgecolor='#E24A33'))
    tp_corrected = 350
    fp_corrected = 25
    fn_corrected = 150
    tn_corrected = 19475
    corr_categories = ['True\npositives', 'FALSE\nPOSITIVES', 'False\nnegatives', 'True\nnegatives']
    corr_values = [tp_corrected, fp_corrected, fn_corrected, tn_corrected]
    _axes[2].bar(corr_categories, corr_values, color=sig_colors, edgecolor='black', alpha=0.8)
    _axes[2].set_ylabel('Number of genes')
    # Panel 3: After BH-FDR correction
    _axes[2].set_title('With BH-FDR correction (q < 0.05)\nOnly ~25 false discoveries', fontsize=12, fontweight='bold')
    for _i, v in enumerate(corr_values):
        _axes[2].text(_i, v + 200, f'{v:,}', ha='center', fontsize=10, fontweight='bold')
    _axes[2].annotate(f'FDR = {fp_corrected}/{tp_corrected + fp_corrected} = {fp_corrected / (tp_corrected + fp_corrected):.0%}', xy=(0.5, 0.85), xycoords='axes fraction', fontsize=13, fontweight='bold', color='#55A868', ha='center', bbox=dict(boxstyle='round', facecolor='lightgreen', edgecolor='#55A868'))
    plt.suptitle('Why multiple testing correction is essential for RNA-seq', fontsize=14, fontweight='bold', y=1.03)
    plt.tight_layout()
    plt.show()
    print("Without correction: 71% of your 'significant' genes are FALSE POSITIVES.")
    print('With BH-FDR correction: only ~7% are false positives -- a manageable rate.')
    print("\nThis is why DESeq2 reports 'padj' (adjusted p-values), not raw p-values.")
    return


@app.cell
def _(all_pvalues, is_truly_de, np):
    # Benjamini-Hochberg FDR correction
    # This is what DESeq2/edgeR use for RNA-seq analysis

    def benjamini_hochberg(pvalues):
        """Apply Benjamini-Hochberg FDR correction.
        Returns adjusted p-values (q-values)."""
        n = len(pvalues)
        # Sort p-values and track original indices
        sorted_indices = np.argsort(pvalues)
        sorted_pvalues = pvalues[sorted_indices]
    
        # BH adjustment: p_adj[i] = p[i] * n / rank[i]
        ranks = np.arange(1, n + 1)
        adjusted = sorted_pvalues * n / ranks
    
        # Ensure monotonicity (each adjusted p >= previous)
        adjusted = np.minimum.accumulate(adjusted[::-1])[::-1]
        adjusted = np.clip(adjusted, 0, 1)
    
        # Put back in original order
        result = np.empty(n)
        result[sorted_indices] = adjusted
        return result

    padj = benjamini_hochberg(all_pvalues)

    # Apply FDR threshold of 0.05
    fdr_significant = padj < 0.05

    print(f"=== Benjamini-Hochberg FDR correction (padj < 0.05) ===")
    print(f"Called significant: {fdr_significant.sum()}")
    print(f"  True positives:  {(fdr_significant & is_truly_de).sum()}")
    print(f"  FALSE positives: {(fdr_significant & ~is_truly_de).sum()}")
    if fdr_significant.sum() > 0:
        print(f"  False discovery rate: {(fdr_significant & ~is_truly_de).sum() / fdr_significant.sum():.1%}")
    print()
    print("FDR correction dramatically reduces false positives while keeping most true positives.")
    print("This is why RNA-seq papers report 'padj' or 'q-value', not raw p-values.")
    return fdr_significant, padj


@app.cell
def _(all_pvalues, fdr_significant, n_genes, naive_significant, padj, plt):
    # Visualize: p-value distribution before and after correction
    _fig, _axes = plt.subplots(1, 2, figsize=(14, 5))
    _axes[0].hist(all_pvalues, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    # Raw p-values
    _axes[0].axvline(0.05, color='red', linewidth=2, linestyle='--', label='p = 0.05 threshold')
    _axes[0].set_xlabel('Raw p-value')
    _axes[0].set_ylabel('Number of genes')
    _axes[0].set_title(f'Raw p-values ({n_genes:,} genes)\n{naive_significant.sum():,} genes below threshold', fontsize=12)
    _axes[0].legend()
    _axes[0].annotate('True DE genes\n(spike near 0)', xy=(0.02, 1200), fontsize=10, arrowprops=dict(arrowstyle='->', color='black'), xytext=(0.25, 1500))
    _axes[0].annotate('Null genes\n(flat distribution)', xy=(0.5, 400), fontsize=10, xytext=(0.55, 800))
    _axes[1].hist(padj[padj < 1], bins=50, edgecolor='black', alpha=0.7, color='#55A868')
    # Note: the spike near 0 is the true DE genes; the flat part is the null genes
    _axes[1].axvline(0.05, color='red', linewidth=2, linestyle='--', label='padj = 0.05 threshold')
    _axes[1].set_xlabel('Adjusted p-value (BH)')
    _axes[1].set_ylabel('Number of genes')
    _axes[1].set_title(f'BH-adjusted p-values\n{fdr_significant.sum()} genes below threshold', fontsize=12)
    _axes[1].legend()
    plt.suptitle('Multiple testing correction in RNA-seq', fontsize=14, y=1.02)
    # Adjusted p-values
    plt.tight_layout()
    plt.show()
    print('Key insight: under the null hypothesis, p-values are UNIFORMLY distributed.')
    print('The spike near 0 in the left plot = truly differentially expressed genes.')
    print('The flat part = null genes, ~5% of which fall below p=0.05 by chance.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Multiple testing correction methods

    | Method | Controls | Used in | How it works |
    |--------|----------|---------|-------------|
    | **Bonferroni** | Family-wise error rate | Post-hoc pairwise tests | Multiply p by number of tests. Very conservative. |
    | **Benjamini-Hochberg** | False discovery rate (FDR) | RNA-seq (DESeq2, edgeR) | Ranks p-values, adjusts by rank. Less conservative. |
    | **Storey q-value** | FDR | Some proteomics | Estimates proportion of true nulls. Even less conservative. |

    The Benjamini-Hochberg procedure was introduced in: Benjamini, Y. & Hochberg, Y. (1995). "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing." *Journal of the Royal Statistical Society: Series B*, 57(1), 289-300. [doi:10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x) -- This is one of the most cited statistics papers ever and the foundation of FDR correction used in virtually all modern genomics analyses.

    **For your RNA-seq work:** Always use the `padj` column from DESeq2/edgeR, which applies BH correction. Never filter on raw p-values for genome-wide analyses. See [statsmodels `multipletests`](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html) for applying these corrections in Python.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Why This Matters for AI

    ### Why you need this

    When you ask Claude to analyze data or interpret statistical results, you need to verify its reasoning. LLMs are particularly prone to:
    - Confusing statistical significance with practical importance
    - Not mentioning multiple testing correction when it's needed
    - Misinterpreting p-values (saying "95% probability the drug works")
    - Suggesting inappropriate tests for the experimental design

    Now you have the knowledge to catch these errors.
    """)
    return


@app.cell
def _():
    # Example: what to check when Claude gives you statistical advice

    checklist = """
    === Statistical Claim Checklist ===

    When Claude (or a paper) makes a statistical claim, ask:

    1. WHAT TEST was used?
       - Is it appropriate for the number of groups?
       - Is it appropriate for paired vs independent data?
       - Does the data meet the test's assumptions (normality, equal variance)?

    2. WHAT IS THE P-VALUE?
       - Is it raw or adjusted for multiple comparisons?
       - If multiple tests were run, was any correction applied?

    3. WHAT IS THE EFFECT SIZE?
       - A small p-value with a tiny effect size = probably not meaningful
       - Report Cohen's d or mean difference, not just p

    4. WHAT IS THE SAMPLE SIZE?
       - n=3 per group is common in pain research but gives very low power
       - With small n, a non-significant result doesn't mean no effect

    5. IS THE INTERPRETATION CORRECT?
       - "p = 0.03" does NOT mean "97% probability the drug works"
       - "Not significant" does NOT mean "no difference exists"
    """
    print(checklist)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Simulated Behavioral Experiment

    You're testing a KCNQ2/3 channel opener (retigabine analog) in a neuropathic pain model. You have 4 groups:
    - Vehicle
    - Low dose (1 mg/kg)
    - Mid dose (3 mg/kg)
    - High dose (10 mg/kg)

    Each group has n=8 mice, measured on von Frey and tail-flick assays.

    **Step 1:** Run the cell below to generate the dataset.
    """)
    return


@app.cell
def _(np, pd, rng):
    # Generate behavioral dataset
    n_mice = 8
    group_labels = ['Vehicle', 'Low (1 mg/kg)', 'Mid (3 mg/kg)', 'High (10 mg/kg)']
    vf_means = [0.3, 0.38, 0.65, 0.95]
    # Von Frey: KCNQ opener should increase threshold (reduce allodynia)
    vf_sds = [0.1, 0.11, 0.15, 0.2]  # dose-dependent increase
    tf_means = [4.2, 4.5, 5.0, 5.3]
    tf_sds = [0.8, 0.9, 1.0, 1.1]
    # Tail-flick: KCNQ opener has modest effect on thermal pain
    experiment_data = []  # modest dose-dependent increase
    for _i, label in enumerate(group_labels):
        vf = np.clip(rng.normal(loc=vf_means[_i], scale=vf_sds[_i], size=n_mice), 0.04, None)
        tf = np.clip(rng.normal(loc=tf_means[_i], scale=tf_sds[_i], size=n_mice), 1.0, None)
        for _j in range(n_mice):
            experiment_data.append({'mouse_id': f'{label[:3]}_{_j + 1}', 'group': label, 'von_frey_g': round(vf[_j], 3), 'tail_flick_s': round(tf[_j], 2)})
    exp_df = pd.DataFrame(experiment_data)
    print(f'Behavioral experiment: {len(exp_df)} mice, {len(group_labels)} groups')
    print()
    print(exp_df.groupby('group')[['von_frey_g', 'tail_flick_s']].agg(['mean', 'std']).round(3))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 1: Run a one-way ANOVA on von Frey thresholds

    Is there a significant overall effect of dose on von Frey threshold?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: extract each group's data, then stats.f_oneway(group1, group2, group3, group4)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 2: Run post-hoc pairwise comparisons with Bonferroni correction

    Which specific dose groups are significantly different from vehicle?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: compare each dose group to vehicle using t-tests
    # Then multiply p-values by the number of comparisons (3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 3: Compute effect sizes (Cohen's d) for each dose vs vehicle

    Are the significant results also biologically meaningful?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: use the cohens_d function defined earlier in this notebook
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 4: Repeat the analysis for tail-flick latency

    Is the drug effective on thermal pain (tail-flick) as well as mechanical pain (von Frey)? Run ANOVA + post-hoc tests.
    """)
    return


@app.cell
def _():
    # Your code here
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Task 5: Visualize both assays

    Create a two-panel figure showing individual data points + means for both von Frey and tail-flick assays.
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    | Concept | Key insight | When you need it |
    |---------|------------|------------------|
    | **P-value** | Probability of data under null hypothesis — NOT probability null is true | Reading any paper, interpreting any result |
    | **T-test** | Compare 2 groups | Vehicle vs drug, WT vs KO |
    | **ANOVA** | Compare 3+ groups (avoids multiple testing inflation) | Dose-response, multi-group experiments |
    | **Effect size** | Is the difference meaningful, not just significant? | Evaluating drug efficacy |
    | **FDR correction** | Control false positives when testing many hypotheses | RNA-seq, proteomics, any -omics |

    **AI connection:** You can now evaluate statistical claims from Claude (or papers) with confidence. Ask: right test? corrected for multiple comparisons? meaningful effect size? correct interpretation of p-value?

    **Next up:** Probability and AI math — how probability distributions power LLMs and why understanding them makes you a better prompt engineer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Descriptive Stats and Distributions](01-descriptive-stats-and-distributions.py) | [Module Index](../README.md) | [Next: Probability and AI Math \u2192](03-probability-and-ai-math.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **[Think Stats](https://allendowney.github.io/ThinkStats/)** (Allen Downey) -- Free online textbook, same author and style as Think Python. Code-first approach to statistics with real datasets. **Especially relevant chapters:**
      - [Chapter 7: Hypothesis Testing](https://allendowney.github.io/ThinkStats/) -- builds p-values from scratch using permutation tests; the clearest explanation of what a p-value actually means
      - [Chapter 8: Estimation](https://allendowney.github.io/ThinkStats/) -- confidence intervals, standard errors, and why effect sizes matter more than p-values
      - [Chapter 9: Linear Regression](https://allendowney.github.io/ThinkStats/) -- regression as a framework for testing relationships, connecting to ANOVA and multiple testing
    - **[SciPy: `ttest_ind`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.ttest_ind.html)** -- Independent two-sample t-test. The workhorse for comparing two groups.
    - **[SciPy: `f_oneway`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.f_oneway.html)** -- One-way ANOVA for comparing three or more groups.
    - **[Statsmodels: `multipletests`](https://www.statsmodels.org/stable/generated/statsmodels.stats.multitest.multipletests.html)** -- Bonferroni, Benjamini-Hochberg, and other multiple testing corrections in Python.
    - **Benjamini, Y. & Hochberg, Y. (1995). "Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing." *J. Royal Statistical Society B*, 57(1), 289-300.** [doi:10.1111/j.2517-6161.1995.tb02031.x](https://doi.org/10.1111/j.2517-6161.1995.tb02031.x) -- The original FDR paper.
    - **James, G., Witten, D., Hastie, T., & Tibshirani, R. *An Introduction to Statistical Learning* (ISLR).** [Free online](https://www.statlearning.com/) -- Accessible textbook covering statistical tests, regression, and machine learning.
    - **[Khan Academy: Hypothesis Testing](https://www.khanacademy.org/math/statistics-probability/significance-tests-one-sample)** -- Visual, step-by-step introduction to p-values and hypothesis testing.
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
    - 2026-03-25: QA pass — added "Why this matters" rationale blockquote; replaced deprecated `stats.binom_test()` with `stats.binomtest().pvalue`
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

