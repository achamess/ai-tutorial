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
    # Module 9.4: Database Basics for Research Data

    **Goal:** Learn what databases are, when you need one instead of a CSV, and how to use SQLite from Python -- so you can evaluate database code that Claude builds for you.

    ---

    ## Why this matters

    When your binder screening grows beyond one CSV -- multiple rounds, different assays, cross-referencing with literature -- you need a database. Also, many bioinformatics data sources use SQL, and Claude can write SQL for you if you understand the concepts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Real Data Analysis Workflow](03-real-data-analysis.py) | [Module Index](../README.md) | [Next: AI-Assisted Literature Review \u2192](../11-ai-research-workflows/01-literature-review.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - You're designing de novo protein binders for NaV1.7, NaV1.8, and KCNQ2/3. Each screening round generates binding data (Kd from SPR), expression yields, thermal stability measurements, and selectivity panels. That data accumulates across rounds and assay types.
    > - Right now one CSV might work. But when you have 200 binder candidates across 5 screening rounds, with electrophysiology data for some, behavioral data for a subset, and you want to ask "show me all NaV1.7 binders with Kd < 10 nM that also passed the selectivity panel" -- you need structured relationships between tables, not VLOOKUP chains in Excel.
    > - Many bioinformatics resources (UniProt, PDB, ChEMBL, GEO) store data in relational databases and expose SQL-based query interfaces. Understanding the concepts lets you ask Claude to write queries against these resources.
    > - You don't need to become a database administrator. You need to know enough to (1) recognize when a CSV is no longer sufficient, (2) understand the SQL that Claude writes for you, and (3) verify that joins and queries are correct before trusting the results.
    """)
    return


@app.cell
def _():
    import sqlite3
    import pandas as pd
    import numpy as np

    print(f"sqlite3 version: {sqlite3.sqlite_version}")
    print(f"pandas version: {pd.__version__}")
    print(f"numpy version: {np.__version__}")
    return np, pd, sqlite3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. What Is a Database (and Why Not Just Use CSVs)?

    > **Why this section matters:** You already know CSVs and DataFrames. Understanding *when* they stop being sufficient saves you from building fragile multi-spreadsheet systems that break when your project scales.

    A **database** is a structured system for storing, organizing, and querying data. The kind we'll use is a **relational database** -- data lives in tables (like spreadsheets), but tables can be *linked together* through shared columns.

    ### CSV/Spreadsheet vs. Database

    | Feature | CSV / Spreadsheet | Database |
    |---|---|---|
    | **Storage** | One flat file per table | Multiple related tables in one file |
    | **Querying** | Load entire file, filter in pandas | Ask for exactly what you need with SQL |
    | **Relationships** | Manual VLOOKUP / merge | Built-in JOINs between tables |
    | **Data integrity** | No enforcement | Can enforce types, required fields, valid references |
    | **Concurrent access** | Dangerous (file corruption) | Safe (built-in locking) |
    | **Size** | Slows down above ~100K rows | Handles millions of rows efficiently |

    ### When to switch from CSV to a database

    You probably need a database when:
    - You have **multiple related tables** (candidates, assays, results, targets)
    - You find yourself doing **repeated merges** between the same DataFrames
    - Your data is **growing across rounds** and you keep appending to CSVs
    - You want to **enforce rules** (e.g., every result must reference a valid candidate)
    - Multiple people need to **read/write the same data**

    A CSV is fine when:
    - You have a single, flat table
    - The data fits comfortably in memory
    - You're doing one-off analysis, not building a persistent record
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. SQLite -- A Database in a Single File

    > **Why this section matters:** SQLite is the easiest database to start with -- no server, no installation, it's built into Python via the [`sqlite3` standard library module](https://docs.python.org/3/library/sqlite3.html). The [SQLite project](https://sqlite.org/docs.html) is the most widely deployed database in the world (it's in your phone, your browser, and your operating system).
    """)
    return


@app.cell
def _(sqlite3):
    # Create an in-memory database (disappears when we close the connection)
    # For a persistent database, use: sqlite3.connect('screening.db')
    conn = sqlite3.connect(':memory:')

    # A cursor executes SQL commands
    cursor = conn.cursor()

    print("Connected to in-memory SQLite database")
    print(f"SQLite version: {sqlite3.sqlite_version}")
    return conn, cursor


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Creating Tables

    > **Why this section matters:** When you ask Claude to build a screening tracker or analysis pipeline, it may create database tables. You need to read the table definitions to verify they capture your data correctly -- wrong column types or missing fields mean wrong results downstream.

    Tables are defined with SQL's `CREATE TABLE` statement. You specify:
    - Column names
    - Data types (TEXT, INTEGER, REAL, etc.)
    - Constraints (PRIMARY KEY, NOT NULL, etc.)

    Let's model a binder screening campaign with three related tables.
    """)
    return


@app.cell
def _(conn, cursor):
    # Table 1: Targets -- the ion channels we're designing binders for
    cursor.execute('''
        CREATE TABLE targets (
            target_id   INTEGER PRIMARY KEY,
            gene_name   TEXT NOT NULL,
            protein     TEXT NOT NULL,
            family      TEXT,
            role_in_pain TEXT
        )
    ''')

    # Table 2: Binder candidates
    cursor.execute('''
        CREATE TABLE binder_candidates (
            candidate_id    INTEGER PRIMARY KEY,
            name            TEXT NOT NULL UNIQUE,
            target_id       INTEGER NOT NULL,
            design_round    INTEGER,
            scaffold_type   TEXT,
            sequence_length INTEGER,
            FOREIGN KEY (target_id) REFERENCES targets(target_id)
        )
    ''')

    # Table 3: Screening results (multiple assays per candidate)
    cursor.execute('''
        CREATE TABLE screening_results (
            result_id       INTEGER PRIMARY KEY,
            candidate_id    INTEGER NOT NULL,
            assay_type      TEXT NOT NULL,
            value           REAL,
            unit            TEXT,
            date_measured   TEXT,
            notes           TEXT,
            FOREIGN KEY (candidate_id) REFERENCES binder_candidates(candidate_id)
        )
    ''')

    conn.commit()
    print("Created 3 tables: targets, binder_candidates, screening_results")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Understanding the schema

    Notice the structure:

    ```
    targets (1) ──── (many) binder_candidates (1) ──── (many) screening_results
    ```

    - Each **target** (NaV1.7, NaV1.8, etc.) can have many **binder candidates**
    - Each **binder candidate** can have many **screening results** (Kd, Tm, expression yield, etc.)
    - The `FOREIGN KEY` constraints enforce these relationships -- you can't add a result for a candidate that doesn't exist

    This is the power of a relational database: data is normalized (stored once, referenced everywhere) rather than duplicated across flat files.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Inserting Data

    > **Why this section matters:** You'll either insert data manually for small datasets or have Claude write insertion scripts that pull from CSVs or instrument output files. Either way, understanding INSERT tells you how data gets into the system.
    """)
    return


@app.cell
def _(cursor):
    # Insert targets
    targets_data = [
        (1, 'SCN9A',  'NaV1.7', 'sodium channel', 'Primary pain signaling in nociceptors'),
        (2, 'SCN10A', 'NaV1.8', 'sodium channel', 'Action potential propagation in nociceptors'),
        (3, 'KCNQ2',  'Kv7.2',  'potassium channel', 'Neuronal excitability modulation'),
        (4, 'KCNQ3',  'Kv7.3',  'potassium channel', 'M-current regulation in DRG neurons'),
    ]

    cursor.executemany('INSERT INTO targets VALUES (?, ?, ?, ?, ?)', targets_data)
    print(f"Inserted {len(targets_data)} targets")
    return


@app.cell
def _(cursor):
    # Insert binder candidates
    candidates_data = [
        (1,  'PB-001', 1, 1, 'miniprotein', 58),
        (2,  'PB-002', 1, 1, 'miniprotein', 62),
        (3,  'PB-003', 1, 2, 'designed_repeat', 95),
        (4,  'PB-004', 2, 1, 'miniprotein', 55),
        (5,  'PB-005', 2, 1, 'helical_bundle', 72),
        (6,  'PB-006', 2, 2, 'miniprotein', 60),
        (7,  'PB-007', 3, 1, 'designed_repeat', 88),
        (8,  'PB-008', 3, 1, 'miniprotein', 52),
        (9,  'PB-009', 4, 1, 'helical_bundle', 70),
        (10, 'PB-010', 4, 2, 'miniprotein', 63),
    ]

    cursor.executemany('INSERT INTO binder_candidates VALUES (?, ?, ?, ?, ?, ?)', candidates_data)
    print(f"Inserted {len(candidates_data)} binder candidates")
    return


@app.cell
def _(conn, cursor, np):
    # Insert screening results -- multiple assay types per candidate
    # This is where the database shines: one candidate, many measurements
    np.random.seed(42)
    results_data = []
    result_id = 1
    for cand_id in range(1, 11):
        _kd = round(np.random.lognormal(mean=2.5, sigma=1.2), 1)
        results_data.append((result_id, cand_id, 'SPR_Kd', _kd, 'nM', '2026-01-15', None))
        result_id += 1  # SPR binding affinity (Kd in nM)
        _tm = round(np.random.normal(65, 8), 1)
        results_data.append((result_id, cand_id, 'thermal_Tm', _tm, 'C', '2026-01-18', None))
        result_id += 1
        expr = round(np.random.lognormal(mean=1.5, sigma=0.8), 1)
        results_data.append((result_id, cand_id, 'expression_yield', expr, 'mg/L', '2026-01-12', None))  # Thermal stability (Tm in Celsius)
        result_id += 1
    for cand_id in [3, 6, 10]:
        sel = round(np.random.lognormal(mean=2.5, sigma=0.8), 1)
        results_data.append((result_id, cand_id, 'selectivity_fold', sel, 'fold', '2026-02-05', 'vs closest off-target'))
        result_id += 1  # Expression yield (mg/L)
    cursor.executemany('INSERT INTO screening_results VALUES (?, ?, ?, ?, ?, ?, ?)', results_data)
    conn.commit()
    print(f'Inserted {len(results_data)} screening results')
    # Add selectivity data for a subset (round 2 candidates only)
    print(f'Assay types: SPR_Kd, thermal_Tm, expression_yield, selectivity_fold')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Basic SQL Queries: SELECT, WHERE, ORDER BY

    > **Why this section matters:** SQL is the language you use to ask questions of a database. When Claude writes a query against your screening data or a bioinformatics resource, you need to read it and confirm it's asking the right question. These four operations cover ~90% of what you'll encounter.

    **SQL** (Structured Query Language) is how you talk to a database. The most important statement is `SELECT` -- it retrieves data.
    """)
    return


@app.cell
def _(cursor):
    # SELECT all columns (*) from a table
    cursor.execute('SELECT * FROM targets')
    _rows = cursor.fetchall()
    print('All targets:')
    for _row in _rows:
        print(f'  {_row}')
    return


@app.cell
def _(cursor):
    # SELECT specific columns
    cursor.execute('SELECT gene_name, protein FROM targets')
    for _row in cursor.fetchall():
        print(f'  {_row[0]} -> {_row[1]}')
    return


@app.cell
def _(cursor):
    # WHERE -- filter rows (like pandas boolean indexing)
    cursor.execute('\n    SELECT name, scaffold_type, sequence_length\n    FROM binder_candidates\n    WHERE target_id = 1\n')
    print('Binders targeting NaV1.7 (target_id=1):')
    for _row in cursor.fetchall():
        print(f'  {_row[0]}: {_row[1]}, {_row[2]} residues')
    return


@app.cell
def _(cursor):
    # WHERE with multiple conditions
    cursor.execute("\n    SELECT name, design_round, scaffold_type\n    FROM binder_candidates\n    WHERE design_round = 2 AND scaffold_type = 'miniprotein'\n")
    print('Round 2 miniprotein candidates:')
    for _row in cursor.fetchall():
        print(f'  {_row[0]}: round {_row[1]}, {_row[2]}')
    return


@app.cell
def _(cursor):
    # ORDER BY -- sort results
    cursor.execute("\n    SELECT candidate_id, assay_type, value, unit\n    FROM screening_results\n    WHERE assay_type = 'SPR_Kd'\n    ORDER BY value ASC\n")
    print('Binders ranked by Kd (best first):')
    for _row in cursor.fetchall():
        print(f'  Candidate {_row[0]}: Kd = {_row[2]} {_row[3]}')
    return


@app.cell
def _(cursor):
    # LIMIT -- get only the top N results
    cursor.execute("\n    SELECT candidate_id, value\n    FROM screening_results\n    WHERE assay_type = 'SPR_Kd'\n    ORDER BY value ASC\n    LIMIT 3\n")
    print('Top 3 binders by affinity:')
    for _row in cursor.fetchall():
        print(f'  Candidate {_row[0]}: Kd = {_row[1]} nM')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SQL vs. pandas comparison

    If you already know pandas, SQL will feel familiar:

    | pandas | SQL | What it does |
    |---|---|---|
    | `df[['col1', 'col2']]` | `SELECT col1, col2 FROM table` | Pick columns |
    | `df[df['col'] > 10]` | `WHERE col > 10` | Filter rows |
    | `df.sort_values('col')` | `ORDER BY col` | Sort |
    | `df.head(5)` | `LIMIT 5` | First N rows |
    | `df.groupby('col').mean()` | `GROUP BY col` + `AVG(col)` | Aggregate |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. JOIN -- The Key Database Superpower

    > **Why this section matters:** JOINs are the reason databases exist. When you want to ask "show me the Kd values for all NaV1.7 binders from round 2," the answer requires combining data from three tables: targets, binder_candidates, and screening_results. In a CSV world, this means chaining `pd.merge()` calls and praying the keys align. In SQL, it's one query.

    A **JOIN** combines rows from two or more tables based on a shared column. This is the database equivalent of `pd.merge()` in pandas.
    """)
    return


@app.cell
def _(cursor):
    # JOIN binder_candidates with targets to see which protein each binder targets
    cursor.execute('\n    SELECT bc.name, t.protein, bc.scaffold_type, bc.design_round\n    FROM binder_candidates bc\n    JOIN targets t ON bc.target_id = t.target_id\n    ORDER BY t.protein, bc.name\n')
    print(f"{'Binder':<10} {'Target':<10} {'Scaffold':<18} {'Round'}")
    print('-' * 48)
    for _row in cursor.fetchall():
        print(f'{_row[0]:<10} {_row[1]:<10} {_row[2]:<18} {_row[3]}')
    return


@app.cell
def _(cursor):
    # Three-table JOIN: get Kd values with target names and candidate names
    cursor.execute("\n    SELECT bc.name, t.protein, sr.value AS kd_nM, bc.design_round\n    FROM screening_results sr\n    JOIN binder_candidates bc ON sr.candidate_id = bc.candidate_id\n    JOIN targets t ON bc.target_id = t.target_id\n    WHERE sr.assay_type = 'SPR_Kd'\n    ORDER BY sr.value ASC\n")
    print('All binders with their Kd values and target proteins:')
    print(f"{'Binder':<10} {'Target':<10} {'Kd (nM)':<10} {'Round'}")
    print('-' * 40)
    for _row in cursor.fetchall():
        print(f'{_row[0]:<10} {_row[1]:<10} {_row[2]:<10} {_row[3]}')
    return


@app.cell
def _(cursor):
    # The real power: a complex question answered in one query
    # "What's the average Kd for each target, and how many binders were tested?"
    cursor.execute("\n    SELECT t.protein,\n           COUNT(*) AS n_binders,\n           ROUND(AVG(sr.value), 1) AS avg_kd_nM,\n           ROUND(MIN(sr.value), 1) AS best_kd_nM\n    FROM screening_results sr\n    JOIN binder_candidates bc ON sr.candidate_id = bc.candidate_id\n    JOIN targets t ON bc.target_id = t.target_id\n    WHERE sr.assay_type = 'SPR_Kd'\n    GROUP BY t.protein\n    ORDER BY avg_kd_nM ASC\n")
    print('Screening summary by target:')
    print(f"{'Target':<10} {'N tested':<10} {'Avg Kd':<10} {'Best Kd'}")
    print('-' * 40)
    for _row in cursor.fetchall():
        print(f'{_row[0]:<10} {_row[1]:<10} {_row[2]:<10} {_row[3]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. Python's sqlite3 Module -- Connecting, Querying, Getting Results

    > **Why this section matters:** You've been using `cursor.execute()` and `fetchall()` already -- now let's formalize the pattern. This is the Python code that wraps around SQL, and it's what Claude will generate when building database tools for you.

    The `sqlite3` module is part of Python's standard library. The basic workflow is:

    ```python
    import sqlite3

    # 1. Connect to a database (creates file if it doesn't exist)
    conn = sqlite3.connect('my_data.db')   # or ':memory:' for temporary

    # 2. Create a cursor to execute SQL
    cursor = conn.cursor()

    # 3. Execute SQL
    cursor.execute('SELECT * FROM my_table WHERE ...')

    # 4. Fetch results
    rows = cursor.fetchall()  # list of tuples

    # 5. Close when done
    conn.close()
    ```
    """)
    return


@app.cell
def _(cursor):
    # Getting results as tuples (default)
    cursor.execute('SELECT name, scaffold_type FROM binder_candidates LIMIT 3')
    _rows = cursor.fetchall()
    print('Results as tuples (default):')
    for _row in _rows:
        print(f'  {_row}  -- access by index: row[0] = {_row[0]}')
    return


@app.cell
def _(conn, sqlite3):
    # Getting results as dictionaries (more readable)
    # Set row_factory to access columns by name
    conn.row_factory = sqlite3.Row
    dict_cursor = conn.cursor()
    dict_cursor.execute('SELECT name, scaffold_type, sequence_length FROM binder_candidates LIMIT 3')
    _rows = dict_cursor.fetchall()
    print('Results as Row objects (access by name):')
    for _row in _rows:
        print(f"  {_row['name']}: {_row['scaffold_type']}, {_row['sequence_length']} residues")
    # Reset row_factory for subsequent cells
    conn.row_factory = None
    return


@app.cell
def _(cursor):
    # IMPORTANT: Use parameterized queries to avoid SQL injection
    # Never build SQL strings with f-strings or string concatenation!

    # BAD (never do this):
    # target_name = "NaV1.7"
    # cursor.execute(f"SELECT * FROM targets WHERE protein = '{target_name}'")

    # GOOD (use ? placeholders):
    target_name = "NaV1.7"
    cursor.execute('SELECT * FROM targets WHERE protein = ?', (target_name,))
    result = cursor.fetchone()
    print(f"Found target: {result}")

    # This matters because if the value comes from user input or a file,
    # string concatenation could allow malicious SQL to run.
    # Always use ? placeholders -- Claude should write it this way too.
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 8. Pandas Integration: pd.read_sql()

    > **Why this section matters:** This is the bridge between databases and everything you already know in pandas. One function call turns any SQL query into a DataFrame, so you can use all your pandas and plotting skills on database-sourced data. In practice, you'll use this constantly.
    """)
    return


@app.cell
def _(conn, pd):
    # pd.read_sql() runs a SQL query and returns a DataFrame
    df_targets = pd.read_sql('SELECT * FROM targets', conn)
    df_targets
    return


@app.cell
def _(conn, pd):
    # Complex queries become DataFrames just as easily
    df_screening = pd.read_sql('''
        SELECT bc.name AS binder,
               t.protein AS target,
               sr.assay_type,
               sr.value,
               sr.unit,
               bc.design_round
        FROM screening_results sr
        JOIN binder_candidates bc ON sr.candidate_id = bc.candidate_id
        JOIN targets t ON bc.target_id = t.target_id
        ORDER BY bc.name, sr.assay_type
    ''', conn)

    print(f"Shape: {df_screening.shape}")
    df_screening.head(10)
    return (df_screening,)


@app.cell
def _(df_screening):
    # Now use regular pandas operations on the result
    # Pivot: one row per binder, columns for each assay type
    df_kd = df_screening[df_screening['assay_type'] == 'SPR_Kd']

    print("Average Kd by target (from database -> pandas):")
    print(df_kd.groupby('target')['value'].agg(['mean', 'min', 'count']).round(1))
    return


@app.cell
def _(conn, pd):
    # Going the other direction: DataFrame -> database table
    # Useful for importing CSV data into a database

    # Simulate a CSV of behavioral data
    behavioral_data = pd.DataFrame({
        'mouse_id': ['M01', 'M02', 'M03', 'M04', 'M05', 'M06'],
        'treatment': ['vehicle', 'vehicle', 'PB-003', 'PB-003', 'PB-006', 'PB-006'],
        'von_frey_g': [1.2, 1.4, 0.9, 0.85, 0.7, 0.65],
        'paw_diameter_mm': [3.1, 3.0, 3.3, 3.4, 3.2, 3.3]
    })

    # Write DataFrame to a new database table
    behavioral_data.to_sql('behavioral_results', conn, if_exists='replace', index=False)

    # Verify it's there
    df_check = pd.read_sql('SELECT * FROM behavioral_results', conn)
    print("Behavioral data stored in database:")
    df_check
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The typical workflow

    In practice, the database-pandas workflow looks like this:

    1. **Store** your structured data in SQLite tables (with relationships)
    2. **Query** the specific subset you need with SQL
    3. **Analyze** the result as a pandas DataFrame
    4. **Plot** with matplotlib/seaborn

    The database handles storage and relationships. Pandas handles analysis and plotting. Each tool does what it's best at.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 9. Decision Guide: Database vs. CSV vs. Pandas

    > **Why this section matters:** The most common mistake is using the wrong tool. A single CSV is fine for a small experiment. A database for a one-off analysis is overkill. This guide helps you choose correctly.

    | Scenario | Best tool | Why |
    |---|---|---|
    | One-off analysis of a single data file | **pandas** (read CSV) | Simple, fast, no setup |
    | Sharing a dataset with a collaborator | **CSV** | Universal, no special software needed |
    | Tracking 200+ binders across 5 screening rounds with multiple assays | **SQLite database** | Relationships, integrity, complex queries |
    | Quick exploration of RNA-seq results | **pandas** (read CSV) | Interactive, good for EDA |
    | Building a lab inventory system | **SQLite database** | Persistent, multi-table, queryable |
    | Feeding data into a plot or statistical test | **pandas DataFrame** | Integration with matplotlib, scipy |
    | Querying a public bioinformatics resource | **SQL** (their interface) | Many resources use SQL-based APIs |
    | Archiving raw instrument output | **CSV files** | Simple, future-proof, version-controllable |

    ### Rules of thumb

    - **1 table, < 100K rows, one-time analysis** -> CSV + pandas
    - **Multiple related tables OR growing dataset OR repeated queries** -> SQLite
    - **Multiple users writing simultaneously OR web application** -> PostgreSQL (ask Claude to set it up)
    - **Highly connected data (protein interaction networks, pathways)** -> Graph database (just be aware these exist)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Decision point: CSV vs SQLite vs pandas (when to upgrade)**
    >
    > | Scenario | Best tool | Why | Upgrade trigger |
    > |----------|-----------|-----|-----------------|
    > | Single data file, < 10,000 rows | **CSV + pandas** | Simple, portable, no setup | You're fine -- don't over-engineer |
    > | Multiple related tables (binders + assays + structures) | **SQLite** | Enforces relationships, prevents orphaned records | When you find yourself doing lots of `pd.merge()` across files |
    > | Shared data across multiple scripts/notebooks | **SQLite** | Single source of truth, concurrent reads | When two scripts read different versions of the same CSV |
    > | Very large data (> 1M rows) | **SQLite** or PostgreSQL | Query without loading everything into memory | When `pd.read_csv()` is slow or uses too much RAM |
    > | Simple analysis on one DataFrame | **pandas alone** | Fast, flexible, great for exploration | Don't use a database for this -- it's overkill |
    >
    > **Migration path:** Start with CSVs. When you have 3+ related files that you merge frequently, create a SQLite database. You can always export back to CSV with `df.to_csv()`.

    > **Tip:** Use parameterized queries for security and correctness. Never build SQL queries with f-strings or string concatenation (`f"SELECT * FROM binders WHERE target = '{user_input}'"`) -- this is vulnerable to SQL injection. Always use parameterized queries: `cursor.execute("SELECT * FROM binders WHERE target = ?", (user_input,))`. This is safer and handles special characters correctly.

    > **Warning:** SQL injection is a real security risk, even in local research databases. If your database tool ever accepts user input (a gene name, a binder ID), always use parameterized queries with `?` placeholders. This isn't just a web security issue -- a malformed input like `'; DROP TABLE binders; --` in a string-concatenated query could destroy your data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 10. What's Beyond SQLite (Awareness Only)

    > **Why this section matters:** You don't need to learn these, but you should know they exist so you can have an informed conversation with Claude or a computational collaborator about the right tool for a project.

    | Database | What it is | When you'd encounter it |
    |---|---|---|
    | **PostgreSQL** | Full-featured relational database with a server | Lab-wide data systems, web applications, shared databases |
    | **MySQL / MariaDB** | Another server-based relational database | Many bioinformatics web resources (Ensembl, UCSC Genome Browser) run on MySQL |
    | **MongoDB** | Document database (stores JSON-like objects) | Flexible schemas, when data structure varies between records |
    | **Neo4j** | Graph database (nodes and relationships) | Protein interaction networks, pathway analysis, knowledge graphs |
    | **DuckDB** | Analytical database optimized for data science | Like SQLite but faster for analytical queries on large datasets; growing in bioinformatics |

    For your binder screening work, SQLite will likely be sufficient for years. If you ever need to scale up, Claude can help you migrate.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Build an Experiment Tracking Database

    Build a small SQLite database to track experimental results across multiple assay types for your binder candidates. This simulates what you'd actually build to manage a screening campaign.

    ### Setup

    Run the cell below to create a fresh database and populate it with data.
    """)
    return


@app.cell
def _(np, sqlite3):
    # Create a fresh database for the exercise
    ex_conn = sqlite3.connect(':memory:')
    ex_cursor = ex_conn.cursor()
    ex_cursor.executescript("\n    CREATE TABLE experiments (\n        experiment_id   INTEGER PRIMARY KEY,\n        name            TEXT NOT NULL,\n        assay_type      TEXT NOT NULL,\n        date_performed  TEXT,\n        operator        TEXT\n    );\n\n    CREATE TABLE compounds (\n        compound_id     INTEGER PRIMARY KEY,\n        name            TEXT NOT NULL UNIQUE,\n        target          TEXT NOT NULL,\n        design_method   TEXT,\n        molecular_weight_kda REAL\n    );\n\n    CREATE TABLE measurements (\n        measurement_id  INTEGER PRIMARY KEY,\n        experiment_id   INTEGER NOT NULL,\n        compound_id     INTEGER NOT NULL,\n        value           REAL,\n        unit            TEXT,\n        replicate       INTEGER DEFAULT 1,\n        quality_flag    TEXT DEFAULT 'OK',\n        FOREIGN KEY (experiment_id) REFERENCES experiments(experiment_id),\n        FOREIGN KEY (compound_id) REFERENCES compounds(compound_id)\n    );\n")
    # Create tables
    experiments = [(1, 'SPR_round1', 'SPR', '2026-01-10', 'Alex'), (2, 'SPR_round2', 'SPR', '2026-02-14', 'Alex'), (3, 'DSF_stability', 'DSF', '2026-01-20', 'Alex'), (4, 'Ephys_Nav17', 'electrophysiology', '2026-03-01', 'Sarah'), (5, 'VonFrey_pilot', 'behavioral', '2026-03-10', 'Alex')]
    ex_cursor.executemany('INSERT INTO experiments VALUES (?, ?, ?, ?, ?)', experiments)
    compounds = [(1, 'NB-101', 'NaV1.7', 'RFdiffusion', 12.3), (2, 'NB-102', 'NaV1.7', 'RFdiffusion', 11.8), (3, 'NB-103', 'NaV1.7', 'ProteinMPNN', 14.1), (4, 'NB-201', 'NaV1.8', 'RFdiffusion', 13.5), (5, 'NB-202', 'NaV1.8', 'ProteinMPNN', 10.9), (6, 'NB-301', 'KCNQ2/3', 'RFdiffusion', 15.2), (7, 'NB-302', 'KCNQ2/3', 'ProteinMPNN', 12.7)]
    ex_cursor.executemany('INSERT INTO compounds VALUES (?, ?, ?, ?, ?)', compounds)
    np.random.seed(123)
    measurements = []
    m_id = 1
    for c_id in range(1, 8):
        for rep in range(1, 4):
            _kd = round(np.random.lognormal(mean=3, sigma=1) + rep * 0.1, 1)
            flag = 'OK' if _kd < 500 else 'high_kd'
            measurements.append((m_id, 1, c_id, _kd, 'nM', rep, flag))
            m_id += 1
    for c_id in [1, 2, 3]:
        for rep in range(1, 4):
            _kd = round(np.random.lognormal(mean=2, sigma=0.8) + rep * 0.1, 1)
            measurements.append((m_id, 2, c_id, _kd, 'nM', rep, 'OK'))
            m_id += 1
    for c_id in range(1, 8):
        _tm = round(np.random.normal(62, 7), 1)
        measurements.append((m_id, 3, c_id, _tm, 'C', 1, 'OK'))
        m_id += 1
    for c_id in [1, 2, 3]:
        ic50 = round(np.random.lognormal(mean=3.5, sigma=0.5), 1)
        measurements.append((m_id, 4, c_id, ic50, 'nM', 1, 'OK'))
        m_id += 1
    for c_id in [1, 4]:
        for rep in range(1, 4):
            vf = round(np.random.normal(0.8, 0.15), 2)
            measurements.append((m_id, 5, c_id, vf, 'g', rep, 'OK'))
    # Insert experiments
            m_id += 1
    ex_cursor.executemany('INSERT INTO measurements VALUES (?, ?, ?, ?, ?, ?, ?)', measurements)
    ex_conn.commit()
    print(f'Exercise database ready!')
    print(f'  {len(experiments)} experiments')
    print(f'  {len(compounds)} compounds')
    # Insert compounds
    # Insert measurements
    # SPR round 1 (experiment 1) -- all compounds, Kd in nM
    # SPR round 2 (experiment 2) -- only NaV1.7 compounds
    # DSF stability (experiment 3) -- all compounds, Tm in Celsius
    # Electrophysiology (experiment 4) -- NaV1.7 compounds only, IC50 in nM
    # Behavioral -- von Frey thresholds (experiment 5)
    print(f'  {len(measurements)} measurements')  # triplicates  # 3 mice per group
    return (ex_conn,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q1: List all experiments and their assay types

    Write a SQL query to show all experiments, ordered by date.
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint: SELECT ... FROM experiments ORDER BY date_performed
    # Use pd.read_sql() so you get a nice DataFrame
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q2: What is the average Kd from SPR round 1 for each target?

    This requires joining measurements -> compounds, filtering for experiment 1, and grouping by target.
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint:
    # pd.read_sql('''
    #     SELECT c.target, ROUND(AVG(m.value), 1) AS avg_kd_nM, COUNT(*) AS n_measurements
    #     FROM measurements m
    #     JOIN compounds c ON m.compound_id = c.compound_id
    #     WHERE m.experiment_id = 1
    #     GROUP BY c.target
    # ''', ex_conn)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q3: Find the best binder for each target

    For SPR round 1 data, find the compound with the lowest average Kd per target.
    """)
    return


@app.cell
def _():
    # Your code here
    # Strategy: first get average Kd per compound from round 1,
    # then find the minimum per target.
    #
    # Hint: You can use a subquery, or do it in two steps:
    # Step 1: pd.read_sql() to get avg Kd per compound
    # Step 2: use pandas .groupby().idxmin() to find the best
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q4: Which compounds have data from ALL assay types?

    Find compounds that have been tested in SPR, DSF, electrophysiology, AND behavioral assays.
    """)
    return


@app.cell
def _():
    # Your code here
    # Hint:
    # pd.read_sql('''
    #     SELECT c.name, c.target, COUNT(DISTINCT e.assay_type) AS n_assay_types
    #     FROM measurements m
    #     JOIN compounds c ON m.compound_id = c.compound_id
    #     JOIN experiments e ON m.experiment_id = e.experiment_id
    #     GROUP BY c.compound_id
    #     HAVING COUNT(DISTINCT e.assay_type) >= 4
    # ''', ex_conn)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Q5: Build a summary dashboard

    Create a DataFrame that shows, for each compound: name, target, average SPR Kd (round 1), thermal stability (Tm), and whether it has electrophysiology data. This is the kind of integrated view that justifies using a database.
    """)
    return


@app.cell
def _():
    # Your code here
    # One approach: run separate queries and merge in pandas
    # Another approach: write one big SQL query with LEFT JOINs and subqueries
    #
    # Start simple -- get the SPR round 1 averages, then the Tm values,
    # then merge them together.
    return


@app.cell
def _(ex_conn):
    # Clean up the exercise connection
    ex_conn.close()
    print("Exercise database closed.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    | Concept | What you learned |
    |---|---|
    | Database vs. CSV | Databases handle relationships, enforce integrity, and scale; CSVs are simple and portable |
    | SQLite | A full database in a single file, built into Python, no server needed |
    | CREATE TABLE | Define tables with columns, types, and foreign key relationships |
    | SELECT / WHERE / ORDER BY | Query data with filters and sorting |
    | JOIN | Combine related tables -- the core reason to use a database |
    | sqlite3 module | Python's built-in interface: `connect()`, `cursor.execute()`, `fetchall()` |
    | pd.read_sql() | Bridge from database to DataFrame for analysis and plotting |
    | df.to_sql() | Bridge from DataFrame to database for storage |
    | When to use what | Single flat file -> CSV; related tables or growing data -> SQLite; multi-user -> PostgreSQL |

    ### Key takeaway

    You don't need to memorize SQL syntax. You need to understand the *concepts* -- tables, relationships, joins, queries -- so that when Claude generates database code for your screening pipeline, you can read it, verify it's correct, and ask for modifications.

    ### References

    - SQLite documentation: [https://www.sqlite.org/docs.html](https://www.sqlite.org/docs.html)
    - Python sqlite3 module documentation: [https://docs.python.org/3/library/sqlite3.html](https://docs.python.org/3/library/sqlite3.html)
    - pandas `read_sql` documentation: [https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **Official documentation:**
    - [Python `sqlite3` module](https://docs.python.org/3/library/sqlite3.html) -- the official Python docs for the built-in SQLite interface, including connection management, cursor operations, and parameterized queries
    - [SQLite official documentation](https://sqlite.org/docs.html) -- comprehensive reference for SQL syntax, data types, and SQLite-specific features
    - [pandas `read_sql` documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_sql.html) -- reference for reading SQL query results directly into DataFrames

    **Books:**
    - *SQL for Data Scientists* by Renee M.P. Teate -- a practical introduction to SQL written specifically for people who analyze data (not database administrators). Covers SELECT, JOIN, GROUP BY, and subqueries with a data analysis focus.

    **Tutorials:**
    - [SQLite Tutorial](https://www.sqlitetutorial.net/) -- step-by-step SQLite tutorial with practical examples
    - [W3Schools SQL Tutorial](https://www.w3schools.com/sql/) -- interactive SQL reference; good for looking up syntax quickly
    - [Mode Analytics SQL Tutorial](https://mode.com/sql-tutorial/) -- free, progressive SQL tutorial oriented toward data analysis
    """)
    return


@app.cell
def _(conn):
    # Clean up the main connection
    conn.close()
    print("All database connections closed.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Real Data Analysis Workflow](03-real-data-analysis.py) | [Module Index](../README.md) | [Next: AI-Assisted Literature Review \u2192](../11-ai-research-workflows/01-literature-review.py)
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


if __name__ == "__main__":
    app.run()

