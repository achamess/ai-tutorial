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
    # Module 6.1: Pandas Basics for Research Data

    **Goal:** Learn to organize, filter, and summarize tabular data using [pandas](https://pandas.pydata.org/) -- the most important Python library for working with research data.

    ---

    ## Why pandas?

    As a pain biologist, you work with tabular data constantly:
    - Gene expression tables from RNA-seq
    - Behavioral assay measurements (von Frey thresholds, tail-flick latencies)
    - Binding affinity data for your NaV1.7/NaV1.8 binder candidates
    - Calcium imaging trace summaries

    You probably manage this in Excel or GraphPad. Pandas lets you do the same things -- and much more -- in Python, which means:
    1. **Reproducibility** -- your analysis is code, not clicks
    2. **Scale** -- handle thousands of genes or hundreds of experiments effortlessly
    3. **Integration** -- feed data directly into plots, stats, or the Claude API

    > **Think Python connection:** This builds on data structures (lists, dictionaries) from Module 01. A DataFrame is essentially a dictionary of lists with superpowers. See [Think Python Chapter 11 (Dictionaries)](https://allendowney.github.io/ThinkPython/chap11.html) for the foundation.

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Building Research Tools](../09-claude-api/03-building-research-tools.py) | [Module Index](../README.md) | [Next: Data Visualization for Research \u2192](02-visualization.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - pandas is how Python handles tabular data -- the same kind of data you work with daily: gene expression tables from RNA-seq, binder screening results (Kd, selectivity, Tm, expression yield), behavioral assay scores, and calcium imaging summaries.
    > - This replaces manual Excel work with reproducible, scriptable analysis. When you re-run a screening campaign with 30 new candidates, the same pandas code processes them identically -- no copy-paste errors, no forgotten filter settings.
    > - pandas is also the bridge between your data and Claude. When you ask Claude to analyze your binder candidates, it will write pandas code. Understanding DataFrames means you can read, verify, and modify that code.
    > - Every data visualization and every AI-assisted analysis pipeline in the remaining modules depends on pandas. This is the foundation.
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np

    # Check versions
    print(f"pandas version: {pd.__version__}")
    print(f"numpy version: {np.__version__}")
    return np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Creating DataFrames

    A **DataFrame** is a table -- rows and columns, like a spreadsheet. The most common way to create one from scratch is from a Python dictionary, where each key becomes a column name.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** A DataFrame IS a spreadsheet you can program. If you know Excel, you already understand the core idea: rows of data, columns of variables, filtering, sorting, and summarizing. The difference is that pandas operations are written as code, which means they're reproducible, scalable, and composable. `df[df['Kd_nM'] < 100]` does the same thing as an Excel filter -- but you can re-run it on any dataset, embed it in a pipeline, and never accidentally clear it.

    > **Decision point: Excel vs pandas vs SQL**
    >
    > | Tool | Pros | Cons | Use when |
    > |------|------|------|----------|
    > | **Excel/Sheets** | Familiar, visual, quick for small datasets | Not reproducible, error-prone with copy-paste, breaks above ~100K rows | Quick look at a small dataset, sharing with non-coders, one-off calculations |
    > | **pandas** | Reproducible, scriptable, handles millions of rows, integrates with plotting and Claude API | Learning curve, no GUI for browsing data | Any analysis you want to reproduce, anything above ~1000 rows, feeding into pipelines |
    > | **SQL (SQLite)** | Handles relationships between tables, enforces data integrity, great for querying | Overkill for single-file analysis, separate query language | Multiple related tables, experiment tracking databases, data shared across tools |
    >
    > **Migration path:** Most researchers start in Excel, move to pandas for reproducibility, and add SQL when they need to manage related tables (e.g., linking binder candidates to assay results to structural predictions).

    > **Tip:** Method chaining makes pandas code readable. Instead of creating intermediate variables, chain operations: `df.query('Kd_nM < 100').sort_values('selectivity_fold', ascending=False).head(10)` reads like English: "from the data, take rows where Kd < 100, sort by selectivity descending, show top 10." This is much clearer than 3 separate lines with temporary variable names.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Anatomy of a DataFrame

    Before we create one, let's visualize what a DataFrame actually is:

    ```
                            COLUMNS (df.columns)
                     ┌──────────┬──────────┬──────────┐
                     │  gene    │ expr_tpm │cell_type │  ← column names (strings)
                     │  (str)   │ (float)  │  (str)   │  ← dtypes (per column)
        INDEX        ├──────────┼──────────┼──────────┤
      (df.index)   0 │  SCN9A   │   85.2   │nociceptor│  ← row 0
                   1 │  SCN10A  │  120.4   │nociceptor│  ← row 1
                   2 │  TRPV1   │   65.3   │nociceptor│  ← row 2
                   3 │  CALCA   │  210.8   │peptidergic│ ← row 3
                     └──────────┴──────────┴──────────┘
                            VALUES (df.values)
                         = the actual data (NumPy array)

      df.shape = (4, 3)     ← (rows, columns)
      df.dtypes              ← data type of each column
      df['gene']             ← select one column (→ Series)
      df.iloc[0]             ← select one row (→ Series)
    ```

    Think of it as: **a dictionary of columns** where each column is a list of the same length, plus a shared index that labels the rows.
    """)
    return


@app.cell
def _(pd):
    # Create a simple DataFrame: DRG neuron marker gene expression
    data = {
        'gene': ['SCN9A', 'SCN10A', 'TRPV1', 'CALCA', 'P2RX3', 'KCNQ2', 'KCNQ3', 'NTRK1'],
        'full_name': [
            'Nav1.7', 'Nav1.8', 'TRPV1 capsaicin receptor', 'CGRP',
            'P2X3 purinergic receptor', 'Kv7.2', 'Kv7.3', 'TrkA'
        ],
        'expression_tpm': [85.2, 120.4, 65.3, 210.8, 45.1, 38.7, 42.1, 95.6],
        'cell_type': [
            'nociceptor', 'nociceptor', 'nociceptor', 'peptidergic',
            'non-peptidergic', 'nociceptor', 'nociceptor', 'peptidergic'
        ],
        'is_ion_channel': [True, True, True, False, True, True, True, False]
    }

    df = pd.DataFrame(data)
    df
    return (df,)


@app.cell
def _(df):
    # Quick inspection methods you'll use constantly
    print("Shape (rows, columns):", df.shape)
    print()
    print("Column names:", list(df.columns))
    print()
    print("Data types:")
    print(df.dtypes)
    return


@app.cell
def _(df):
    # .head() and .tail() -- peek at the first/last rows
    print("First 3 rows:")
    df.head(3)
    return


@app.cell
def _(df):
    # .info() gives a compact summary
    df.info()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### The typical pandas workflow

    Most data analysis follows this pipeline (see the [pandas Getting Started tutorials](https://pandas.pydata.org/docs/getting_started/) for more detail on each step):

    """),
    mo.mermaid(
        """
        flowchart LR
            A["📂 Load<br>pd.read_csv()"] --> B["🔍 Inspect<br>.shape, .head(),<br>.info(), .describe()"]
            B --> C["🧹 Clean<br>.dropna(), .fillna(),<br>fix dtypes"]
            C --> D["🔎 Filter<br>df[df['col'] > val]<br>.isin(), .str.contains()"]
            D --> E["📊 Group & Aggregate<br>.groupby().mean()<br>.agg(), .value_counts()"]
            E --> F["💾 Save / Plot<br>.to_csv()<br>matplotlib"]
        
            style A fill:#3498db,color:#fff
            style B fill:#2ecc71,color:#fff
            style C fill:#f39c12,color:#fff
            style D fill:#e74c3c,color:#fff
            style E fill:#9b59b6,color:#fff
            style F fill:#1abc9c,color:#fff
        """
    ),
    mo.md(r"""

    This notebook walks through each step. By the end, you'll be comfortable with the whole pipeline.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Creating DataFrames from CSV strings

    In real life, you'll often read CSV files with `pd.read_csv('file.csv')`. Here we simulate that by creating a CSV in memory using `io.StringIO` -- this way the notebook stays self-contained.
    """)
    return


@app.cell
def _(pd):
    import io

    csv_text = """sample_id,condition,von_frey_threshold_g,paw_diameter_mm
    M01,vehicle,1.2,3.1
    M02,vehicle,1.4,3.0
    M03,vehicle,1.1,3.2
    M04,CFA,0.3,4.8
    M05,CFA,0.2,5.1
    M06,CFA,0.4,4.6
    M07,binder_A,0.9,3.4
    M08,binder_A,1.0,3.3
    M09,binder_A,0.8,3.5
    """

    behavior = pd.read_csv(io.StringIO(csv_text))
    behavior
    return (behavior,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Selecting Data

    ### Selecting columns
    """)
    return


@app.cell
def _(df):
    # Single column -- returns a Series (one-dimensional)
    df['gene']
    return


@app.cell
def _(df):
    # Multiple columns -- returns a DataFrame
    df[['gene', 'expression_tpm', 'cell_type']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Selecting rows by position with `.iloc[]`
    """)
    return


@app.cell
def _(df):
    # First row
    print("Row 0:")
    print(df.iloc[0])
    print()

    # Rows 2 through 4
    print("Rows 2-4:")
    df.iloc[2:5]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Filtering rows (the most useful operation)

    This is like applying a filter in Excel, but much more powerful.
    """)
    return


@app.cell
def _(df):
    # Filter: only ion channels
    ion_channels = df[df['is_ion_channel'] == True]
    print("Ion channels only:")
    ion_channels
    return


@app.cell
def _(df):
    # Filter: genes with expression > 80 TPM
    high_expr = df[df['expression_tpm'] > 80]
    print("Highly expressed genes (>80 TPM):")
    high_expr
    return


@app.cell
def _(df):
    # Combine conditions with & (and) or | (or)
    # Important: each condition must be in parentheses!

    # Ion channels expressed above 50 TPM
    result = df[(df['is_ion_channel'] == True) & (df['expression_tpm'] > 50)]
    print("Ion channels with expression > 50 TPM:")
    result
    return


@app.cell
def _(df):
    # Filter using .isin() -- like "WHERE gene IN (...)" in SQL
    _targets = ['SCN9A', 'SCN10A', 'KCNQ2', 'KCNQ3']
    df[df['gene'].isin(_targets)]
    return


@app.cell
def _(df):
    # String matching with .str.contains()
    df[df['gene'].str.contains('SCN')]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Sorting
    """)
    return


@app.cell
def _(df):
    # Sort by expression level, highest first
    df.sort_values('expression_tpm', ascending=False)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Basic Calculations and Summaries
    """)
    return


@app.cell
def _(df):
    # Descriptive stats on a numeric column
    print(f"Mean expression: {df['expression_tpm'].mean():.1f} TPM")
    print(f"Median expression: {df['expression_tpm'].median():.1f} TPM")
    print(f"Std deviation: {df['expression_tpm'].std():.1f} TPM")
    print(f"Min: {df['expression_tpm'].min():.1f}, Max: {df['expression_tpm'].max():.1f}")
    return


@app.cell
def _(df):
    # .describe() gives you everything at once
    df['expression_tpm'].describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### GroupBy -- split-apply-combine

    This is one of the most powerful pandas operations. It works like a pivot table in Excel:
    1. **Split** the data into groups
    2. **Apply** a function to each group
    3. **Combine** the results
    """)
    return


@app.cell
def _(df):
    # Mean expression by cell type
    df.groupby('cell_type')['expression_tpm'].mean()
    return


@app.cell
def _(df):
    # Multiple summary stats at once
    df.groupby('cell_type')['expression_tpm'].agg(['mean', 'std', 'count'])
    return


@app.cell
def _(behavior):
    # GroupBy on the behavioral data
    print("Mean von Frey threshold by condition:")
    print(behavior.groupby('condition')['von_frey_threshold_g'].agg(['mean', 'std']))
    print()
    print("Mean paw diameter by condition:")
    print(behavior.groupby('condition')['paw_diameter_mm'].agg(['mean', 'std']))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Adding and Modifying Columns
    """)
    return


@app.cell
def _(df, np):
    # Add a new column: log2 of expression
    df['log2_expression'] = np.log2(df['expression_tpm'])
    df[['gene', 'expression_tpm', 'log2_expression']]
    return


@app.cell
def _(df, np):
    # Add a column based on a condition
    df['expression_category'] = np.where(
        df['expression_tpm'] > 80, 'high', 'moderate'
    )
    df[['gene', 'expression_tpm', 'expression_category']]
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Handling Missing Data

    > **Why you need this:** Real experimental data always has missing values -- a failed SPR run for one binder candidate, a mouse excluded from behavioral analysis, a gene below detection limit in one RNA-seq replicate. If you don't handle missing data explicitly, pandas will silently propagate NaN values through your calculations and produce misleading results.

    Real experimental data always has missing values -- a failed qPCR well, a mouse excluded from analysis, a gene below detection limit. Pandas uses `NaN` (Not a Number) to represent missing values.
    """)
    return


@app.cell
def _(np, pd):
    # Create a dataset with missing values (common in real experiments)
    qpcr_data = pd.DataFrame({
        'gene': ['SCN9A', 'SCN10A', 'TRPV1', 'CALCA', 'SCN9A', 'SCN10A', 'TRPV1', 'CALCA'],
        'sample': ['DRG_1', 'DRG_1', 'DRG_1', 'DRG_1', 'DRG_2', 'DRG_2', 'DRG_2', 'DRG_2'],
        'ct_value': [22.1, 19.8, 24.5, np.nan, 21.8, np.nan, 25.1, 18.2],
        'delta_ct': [3.2, 0.9, 5.6, np.nan, 2.9, np.nan, 6.2, -0.7]
    })

    print("Dataset with missing values:")
    qpcr_data
    return (qpcr_data,)


@app.cell
def _(qpcr_data):
    # Check for missing values
    print("Missing values per column:")
    print(qpcr_data.isna().sum())
    print()
    print("Total missing values:", qpcr_data.isna().sum().sum())
    return


@app.cell
def _(qpcr_data):
    # Drop rows with any missing values
    clean = qpcr_data.dropna()
    print(f"Before: {len(qpcr_data)} rows, After dropna: {len(clean)} rows")
    clean
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **When to drop vs. fill missing data** is a scientific judgment call. For gene expression below detection limit, you might fill with 0 or a minimum value. For a failed technical replicate, you probably want to drop it. Pandas gives you the tools -- you make the decision.

    ---

    ## 6. Combining DataFrames

    > **Why you need this:** Your binder data lives in multiple places -- binding affinities from SPR in one spreadsheet, expression yields from purification in another, structural predictions from AlphaFold in a third. Merging DataFrames is how you bring all of that into a single table for integrated analysis.

    Often you need to merge data from different sources -- for example, combining gene expression data with gene annotation info.
    """)
    return


@app.cell
def _(pd):
    # Gene expression data
    expression = pd.DataFrame({
        'gene': ['SCN9A', 'SCN10A', 'TRPV1', 'KCNQ2'],
        'log2FC': [2.1, 1.8, 3.2, -0.5],
        'padj': [0.001, 0.003, 0.0001, 0.45]
    })

    # Gene annotation info (from a different source)
    annotations = pd.DataFrame({
        'gene': ['SCN9A', 'SCN10A', 'TRPV1', 'KCNQ2', 'KCNQ3'],
        'protein': ['Nav1.7', 'Nav1.8', 'TRPV1', 'Kv7.2', 'Kv7.3'],
        'type': ['sodium channel', 'sodium channel', 'TRP channel', 'potassium channel', 'potassium channel']
    })

    # Merge on the 'gene' column
    merged = pd.merge(expression, annotations, on='gene', how='left')
    merged
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Protein Binder Candidates

    You've designed a panel of de novo protein binders targeting NaV1.7, NaV1.8, and KCNQ2/3. Create a DataFrame and answer the questions below.

    **Step 1:** Run the cell below to create the mock dataset.
    """)
    return


@app.cell
def _(np, pd):
    # Mock binder candidate data
    np.random.seed(42)  # for reproducibility
    n_binders = 20
    _targets = np.random.choice(['NaV1.7', 'NaV1.8', 'KCNQ2', 'KCNQ3'], n_binders)
    binders = pd.DataFrame({'name': [f'PB-{i + 1:03d}' for i in range(n_binders)], 'target': _targets, 'Kd_nM': np.round(np.random.lognormal(mean=3, sigma=1.5, size=n_binders), 1), 'selectivity_fold': np.round(np.random.lognormal(mean=2, sigma=1, size=n_binders), 1), 'solubility_mg_ml': np.round(np.random.uniform(0.1, 15, size=n_binders), 1), 'thermal_stability_C': np.round(np.random.normal(65, 8, size=n_binders), 1)})
    print(f'Generated {len(binders)} binder candidates')
    binders.head(10)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Step 2:** Answer these questions using pandas operations. Write your code in the cells below.

    ### Q1: How many binders target each ion channel?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: use .value_counts() or .groupby()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2: Which binder has the best (lowest) Kd?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: sort by Kd_nM and look at the first row
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3: What is the average Kd for each target?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: groupby target, then .mean() on Kd_nM
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4: Find "lead candidates" -- binders with Kd < 50 nM AND selectivity > 10-fold AND solubility > 5 mg/mL
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: combine three conditions with &
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5: For NaV1.7 binders only, what's the correlation between Kd and solubility?
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: filter for NaV1.7, then use .corr() on two columns
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    You now know the core pandas operations that cover ~80% of what you'll need for research data:

    | Operation | Code |
    |---|---|
    | Create DataFrame | `pd.DataFrame({'col': [values]})` |
    | Read CSV | `pd.read_csv('file.csv')` |
    | Inspect | `.shape`, `.head()`, `.info()`, `.describe()` |
    | Select columns | `df['col']` or `df[['col1', 'col2']]` |
    | Filter rows | `df[df['col'] > value]` |
    | Sort | `df.sort_values('col')` |
    | Group & summarize | `df.groupby('col')['val'].mean()` |
    | Add column | `df['new'] = ...` |
    | Handle missing | `.isna()`, `.dropna()`, `.fillna()` |
    | Merge tables | `pd.merge(df1, df2, on='key')` |

    **Next up:** Module 6.2 -- Visualization, where we'll turn these DataFrames into publication-quality figures.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **Official documentation:**
    - [pandas Getting Started](https://pandas.pydata.org/docs/getting_started/) -- installation, overview, and introductory tutorials from the pandas team
    - [10 Minutes to pandas](https://pandas.pydata.org/docs/user_guide/10min.html) -- a concise walkthrough of the most common pandas operations (recommended as a quick refresher)
    - [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html) -- comprehensive reference for all pandas functionality

    **Books:**
    - *Python for Data Analysis* (3rd ed.) by Wes McKinney -- the definitive book on pandas, written by the creator of the library. Covers everything from basic DataFrames to advanced time-series and groupby operations.
    - [Think Python, Chapter 11: Dictionaries](https://allendowney.github.io/ThinkPython/chap11.html) -- the Python data structure that underlies DataFrames. Understanding dictionaries makes pandas intuitive.

    **Tutorials and guides:**
    - [Kaggle pandas course](https://www.kaggle.com/learn/pandas) -- free, interactive, with exercises (good for extra practice)
    - [Real Python: pandas DataFrames 101](https://realpython.com/pandas-dataframe/) -- thorough tutorial with practical examples
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
    - 2026-03-25: QA pass — removed duplicate section 5 and 6 cells
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
    - 2026-03-25: QA pass — removed duplicate section 5 and 6 cells
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

