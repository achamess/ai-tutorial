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
    # 02: Working with Files

    Most of your research data lives in files — gene lists, experiment logs, CSV spreadsheets from plate readers. This notebook covers how Python reads and writes them.

    > **References:**
    > - [Think Python — Chapter 14: Files](https://allendowney.github.io/ThinkPython/chap14.html)
    > - [MIT Missing Semester — Lecture 1: The Shell](https://missing.csail.mit.edu/2020/course-shell/) (file paths, navigating directories)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Your First Code](01-your-first-code.py) | [Module Index](../README.md) | [Next: Libraries and Packages \u2192](03-libraries-and-packages.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Your research generates files constantly — CSV exports from plate readers, FASTA sequences from binder designs, experiment logs, RNA-seq count matrices. Knowing how to read and write files programmatically is the first step to automating hours of manual data wrangling.
    > - When you ask Claude Code to "process all the calcium imaging CSVs in this folder," it writes file-handling code exactly like what's in this notebook. Understanding it means you can verify the output.
    > - Parsing structured text (like experiment logs or screening results) is a skill you'll use every time you build an automated pipeline — from batch-processing binder candidates to generating weekly research digests.
    > - The jump from manual copy-paste in Excel to programmatic file processing is the single biggest productivity gain for a working scientist.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## File paths: where things live

    Before you can read a file, Python needs to know where it is. A **file path** is like a mailing address for a file on your computer.

    There are two kinds:

    | Type | Example | Meaning |
    |------|---------|--------|
    | **Absolute** | `/Users/alex/data/genes.txt` | Full address from the root of your drive |
    | **Relative** | `data/genes.txt` | Address relative to where your code is running |

    Python has a built-in module called [`pathlib`](https://docs.python.org/3/library/pathlib.html) that makes working with paths easy and cross-platform.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    # Where is this notebook running?
    here = Path.cwd()
    print(f"Current directory: {here}")

    # Build a path to a file (doesn't have to exist yet)
    data_dir = here / "sample_data"
    print(f"Data directory: {data_dir}")
    print(f"Does it exist? {data_dir.exists()}")
    return (Path,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The `/` operator joins path pieces together. This is cleaner and more reliable than gluing strings with `+`.

    > **Tip from Missing Semester:** On the command line you navigate with `cd`, `ls`, `pwd`. In Python, `pathlib` gives you the same power — `Path.cwd()` is like `pwd`, `.iterdir()` is like `ls`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** File paths with spaces will break your code if you're not careful. A path like `/Users/alex/My Data/genes.txt` works fine with `pathlib.Path` (which handles quoting automatically), but will fail if you pass it as a raw string to a shell command. Always use `pathlib` in Python, and if you must use shell commands, wrap paths in quotes. This is especially common with macOS folders like "Google Drive" or "iCloud Drive".
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Setup: create some sample files to work with

    Let's create a small directory with realistic research files. Run this cell — it writes the files we'll read in the rest of the notebook.
    """)
    return


@app.cell
def _(Path):
    data_dir_1 = Path.cwd() / 'sample_data'
    data_dir_1.mkdir(exist_ok=True)
    gene_list = 'SCN9A\nSCN10A\nSCN11A\nKCNQ2\nKCNQ3\nTRPV1\nTRPA1\nCALCA\nTAC1\nP2RX3\n'
    (data_dir_1 / 'target_genes.txt').write_text(gene_list)
    experiment_log = '2026-03-10 | Calcium imaging | DRG culture #14 | DNB-Nav17-003 at 100nM | 23/45 neurons responded\n2026-03-12 | Calcium imaging | DRG culture #14 | DNB-Nav17-003 at 500nM | 38/45 neurons responded\n2026-03-14 | Patch clamp | DRG culture #15 | DNB-Nav18-001 at 100nM | NaV1.8 current reduced 34%\n2026-03-17 | Behavioral | CFA mice cohort 3 | DNB-Nav17-003 IP 10mg/kg | von Frey threshold +42%\n2026-03-19 | Calcium imaging | DRG culture #16 | Vehicle control | 3/40 neurons responded\n2026-03-21 | RNA-seq | DRG L4-L5 | SNI day 7 vs sham | 1,247 DEGs (padj < 0.05)\n'
    # --- File 1: A gene list (one gene per line) ---
    (data_dir_1 / 'experiment_log.txt').write_text(experiment_log)
    screening_csv = 'candidate_id,target,binding_region,predicted_kd_nm,solubility_score,thermal_stability_c\nDNB-Nav17-001,NaV1.7,C-terminus,8.3,0.82,67.2\nDNB-Nav17-002,NaV1.7,extracellular loop,45.1,0.91,72.1\nDNB-Nav17-003,NaV1.7,C-terminus,3.7,0.78,64.8\nDNB-Nav18-001,NaV1.8,interdomain I-II,12.7,0.85,69.3\nDNB-Nav18-002,NaV1.8,C-terminus,92.0,0.43,51.2\nDNB-KQ2-001,KCNQ2,N-terminus,5.4,0.88,71.0\nDNB-KQ2-002,KCNQ2,pore domain,67.3,0.62,58.4\nDNB-KQ3-001,KCNQ3,N-terminus,18.9,0.79,65.7\n'
    (data_dir_1 / 'binder_screening.csv').write_text(screening_csv)
    digest = '=== WEEKLY RESEARCH DIGEST: Pain Biology & Ion Channels ===\n# NOTE: All papers, authors, DOIs, and journals below are fictional mock data for tutorial purposes.\nWeek of 2026-03-16\nCompiled by: Lab AI Assistant\n\n--- KEY PAPERS ---\n\nPAPER: Author A et al. (2026) "Selective NaV1.7 degraders reverse inflammatory\nhyperalgesia in a CFA mouse model." Mock Journal of Neuroscience, 29(3):412-425.\nDOI: 10.xxxx/mock-doi-001\nTAGS: NaV1.7, PROTAC, inflammatory pain, CFA, behavioral\nRELEVANCE: HIGH\nSUMMARY: First demonstration that targeted protein degradation of NaV1.7 via\na binder-E3 ligase chimera reverses established hyperalgesia. Used a de novo\ndesigned binder with CRBN recruitment. EC50 = 15 nM in DRG neurons.\n\nPAPER: Author B & Author C (2026) "KCNQ2/3 channel openers as non-opioid\nanalgesics: structure-guided optimization." Mock Science Journal, 381:892-901.\nDOI: 10.xxxx/mock-doi-002\nTAGS: KCNQ2, KCNQ3, retigabine, neuropathic pain, DRG\nRELEVANCE: HIGH\nSUMMARY: Cryo-EM structure of KCNQ2/3 heteromer bound to retigabine analog.\nIdentified a novel binding pocket suitable for de novo binder design.\nShowed analgesic efficacy in SNI and CCI models without sedation.\n\nPAPER: Author D et al. (2026) "Single-cell atlas of human DRG reveals nociceptor\nsubtypes with distinct ion channel signatures." Mock Cell Journal, 189(5):1023-1041.\nDOI: 10.xxxx/mock-doi-003\nTAGS: scRNA-seq, DRG, nociceptor, NaV1.7, NaV1.8, TRPV1, human\nRELEVANCE: MEDIUM\nSUMMARY: Comprehensive single-cell transcriptomic atlas of human DRG. Identified\n12 neuronal subtypes. Key finding: NaV1.7 and NaV1.8 co-express in a specific\npeptidergic nociceptor subtype (hPEP2) that is enriched in patients with\nchronic inflammatory pain.\n\n--- PREPRINTS ---\n\nPAPER: Author E et al. (2026) "CaV2.2 targeted degradation reduces mechanical\nallodynia without affecting motor coordination." Mock Preprint Server 2026.03.10.123456.\nDOI: 10.xxxx/mock-doi-004\nTAGS: CaV2.2, PROTAC, neuropathic pain, SNI\nRELEVANCE: MEDIUM\nSUMMARY: Extends the targeted degradation approach to CaV2.2 calcium channels\nin DRG. 60% reduction in allodynia at 3 mg/kg. No motor side effects.\n\n--- LAB UPDATES ---\n\nUPDATE: DNB-Nav17-003 passed thermal stability re-screen (Tm = 64.8C).\nMoving to in vivo PK study next week.\n\nUPDATE: New batch of DRG cultures (#16-#20) plated on 2026-03-18.\nReady for calcium imaging by 2026-03-25.\n\nUPDATE: RNA-seq data from SNI day 7 experiment uploaded to shared drive.\n1,247 DEGs identified. Analysis notebook in progress.\n'
    (data_dir_1 / 'weekly_digest.txt').write_text(digest)
    print('Sample files created:')
    for f in sorted(data_dir_1.iterdir()):
    # --- File 2: A simple experiment log ---
    # --- File 3: A CSV of binder screening results ---
    # --- File 4: A mock research digest ---
        print(f'  {f.name}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Reading text files

    The simplest way to read a file in Python:
    """)
    return


@app.cell
def _(Path):
    gene_file = Path.cwd() / 'sample_data' / 'target_genes.txt'
    contents = gene_file.read_text()
    # Read the entire file as one string
    print(contents)
    return (contents,)


@app.cell
def _(contents):
    # Split into a list of lines
    genes = contents.strip().split("\n")
    print(genes)
    print(f"\nNumber of target genes: {len(genes)}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Two useful string methods:
    - `.strip()` — removes whitespace (including blank lines) from the beginning and end
    - `.split("\n")` — chops the string at each newline, giving you a list of lines

    This pattern — `read_text().strip().split("\n")` — is one you'll use constantly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Doing something useful: parsing the experiment log

    Let's read the experiment log and extract structured information from it.
    """)
    return


@app.cell
def _(Path):
    log_file = Path.cwd() / 'sample_data' / 'experiment_log.txt'
    lines = log_file.read_text().strip().split('\n')
    print(f'Total experiments logged: {len(lines)}')
    print()
    for line in lines:
        parts = line.split(' | ')
        date = parts[0]
        assay = parts[1]
    # Parse each line into its parts
        sample = parts[2]
        treatment = parts[3]
        result = parts[4]
        print(f'  {date}  [{assay}]  {result}')
    return (lines,)


@app.cell
def _(lines):
    # Filter: show only calcium imaging experiments
    print('Calcium imaging experiments only:\n')
    for line_1 in lines:
        parts_1 = line_1.split(' | ')
        assay_1 = parts_1[1]
        if assay_1 == 'Calcium imaging':
            treatment_1 = parts_1[3]
            result_1 = parts_1[4]
            print(f'  {treatment_1}: {result_1}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This is the core pattern of data work in Python:
    1. **Read** the file
    2. **Split** it into pieces
    3. **Filter** or **transform** what you need

    It scales from a 6-line experiment log to a million-row RNA-seq dataset (with the right libraries — we'll get there).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.mermaid(
        """
        graph LR
            subgraph "The File Processing Pattern"
                READ["1. READ<br/><code>read_text()</code><br/>File → String"]
                SPLIT["2. SPLIT<br/><code>.strip().split('\\n')</code><br/>String → Lines"]
                FILTER["3. FILTER / TRANSFORM<br/><code>if</code> / <code>for</code><br/>Lines → Results"]
                WRITE["4. WRITE<br/><code>write_text()</code><br/>Results → File"]
        
                READ --> SPLIT --> FILTER --> WRITE
            end
        
            style READ fill:#4488cc,color:#fff
            style SPLIT fill:#44aa88,color:#fff
            style FILTER fill:#cc8844,color:#fff
            style WRITE fill:#aa44aa,color:#fff
        """
    ),
    mo.md(r"""

    This is the core workflow for all file-based data processing in Python -- from 6-line experiment logs to million-row RNA-seq tables. The tools change (you'll eventually use pandas instead of manual splitting), but the pattern stays the same.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Writing text files

    Writing is just as simple. Let's save our filtered results.
    """)
    return


@app.cell
def _(Path):
    log_file_1 = Path.cwd() / 'sample_data' / 'experiment_log.txt'
    lines_1 = log_file_1.read_text().strip().split('\n')
    ca_results = []
    for line_2 in lines_1:
        parts_2 = line_2.split(' | ')
    # Collect calcium imaging results
        if parts_2[1] == 'Calcium imaging':
            ca_results.append(line_2)
    output_file = Path.cwd() / 'sample_data' / 'calcium_imaging_only.txt'
    output_file.write_text('\n'.join(ca_results) + '\n')
    print(f'Wrote {len(ca_results)} lines to {output_file.name}')
    print()
    # Write them to a new file
    # Verify by reading it back
    print(output_file.read_text())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Key point: `"\n".join(ca_results)` takes a list of strings and glues them together with newlines between each one. It's the reverse of `.split("\n")`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why CSV specifically?** CSV is the universal exchange format for tabular scientific data. Your plate reader, flow cytometer, RNA-seq pipeline, and binder screening database all export CSV. Knowing how to read and write CSV files is the bridge between your instruments and your analysis code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## CSV files: structured data in rows and columns

    CSV (Comma-Separated Values) is the universal format for tabular data. Your plate reader, flow cytometer, and RNA-seq pipeline all export CSV or TSV files.

    Python has a built-in [`csv` module](https://docs.python.org/3/library/csv.html). Let's use it to read the binder screening data.
    """)
    return


@app.cell
def _(Path):
    import csv
    csv_file = Path.cwd() / 'sample_data' / 'binder_screening.csv'
    with open(csv_file) as f_1:
        reader = csv.DictReader(f_1)
        candidates = list(reader)
    print(f'Loaded {len(candidates)} candidates\n')
    print('First candidate:')
    for key, value in candidates[0].items():
    # Each row is now a dictionary
        print(f'  {key}: {value}')
    return candidates, csv


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 💡 **Tip:** Always use `with` statements when opening files. The `with open(csv_file) as f:` pattern guarantees the file gets closed when you're done, even if an error occurs mid-read. Without `with`, a crash could leave files locked or data partially written. `pathlib`'s `.read_text()` and `.write_text()` handle this automatically, but whenever you see `open()`, wrap it in `with`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    `csv.DictReader` reads each row as a dictionary, using the header row as keys. This is much nicer than working with raw lists of values.

    The `with open(...)` pattern is Python's way of safely opening a file — it automatically closes the file when you're done, even if something goes wrong.
    """)
    return


@app.cell
def _(candidates):
    # Find candidates with Kd < 20 nM
    print("High-affinity candidates (Kd < 20 nM):\n")

    for c in candidates:
        kd = float(c["predicted_kd_nm"])  # CSV values are always strings — convert to number
        if kd < 20:
            print(f"  {c['candidate_id']:16s}  {c['target']:8s}  {c['binding_region']:20s}  Kd = {kd:.1f} nM")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Important gotcha:** Everything from a CSV file comes in as a string. If you want to do math or comparisons with numbers, you need to convert them with `float()` or `int()`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Writing CSV files
    """)
    return


@app.cell
def _(Path, csv):
    csv_file_1 = Path.cwd() / 'sample_data' / 'binder_screening.csv'
    with open(csv_file_1) as f_2:
        reader_1 = csv.DictReader(f_2)
    # Filter to high-affinity candidates and save
        all_candidates = list(reader_1)
        fieldnames = reader_1.fieldnames
    hits = [c for c in all_candidates if float(c['predicted_kd_nm']) < 20]
    output_csv = Path.cwd() / 'sample_data' / 'high_affinity_hits.csv'
    with open(output_csv, 'w', newline='') as f_2:  # remember the column names
        writer = csv.DictWriter(f_2, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(hits)
    print(f'Saved {len(hits)} hits to {output_csv.name}')
    print()
    print(output_csv.read_text())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use the `csv` module vs. pandas for reading CSVs?
    >
    > | Option | Pros | Cons | Use when... |
    > |--------|------|------|-------------|
    > | **`csv` module** | Built-in (no install needed), lightweight, works row-by-row | No built-in filtering, sorting, or statistics; everything is strings | You need to process a few rows, the file is simple, or you want to keep dependencies minimal |
    > | **`pandas.read_csv()`** | One-line filtering, groupby, statistics, plotting integration; auto-detects types | Heavier dependency, slower to import, overkill for 5-row files | You need to analyze, filter, group, or plot data — basically any real data analysis task |
    >
    > **Rule of thumb:** If you're going to do anything *with* the data beyond reading it, use pandas. The `csv` module is for simple read/write tasks and for understanding what pandas does under the hood.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That one-liner `[c for c in all_candidates if float(c["predicted_kd_nm"]) < 20]` is called a **list comprehension**. It's a compact way to filter a list. Read it as: *"give me each candidate c where the Kd is less than 20."*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Preview: pandas makes this much easier

    The `csv` module is fine for simple tasks, but for real data analysis you'll use **pandas**. Here's a preview — we'll cover it properly in Module 06.
    """)
    return


@app.cell
def _(Path):
    import pandas as pd
    csv_file_2 = Path.cwd() / 'sample_data' / 'binder_screening.csv'
    df = pd.read_csv(csv_file_2)
    # One line to read the CSV into a table (called a DataFrame)
    df
    return (df,)


@app.cell
def _(df):
    # One line to filter
    hits_1 = df[df['predicted_kd_nm'] < 20]
    hits_1
    return


@app.cell
def _(df):
    # One line to get summary statistics
    df.describe()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three lines to do what took us 15 lines with the `csv` module. That's why pandas exists.

    Don't worry about the details now — just know it's there and it's what you'll graduate to.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Parse the weekly research digest

    The file `sample_data/weekly_digest.txt` is a mock weekly digest of papers and lab updates. Your task:

    1. Read the file
    2. Extract all lines that start with `PAPER:` and print just the author/title info
    3. Extract all lines that start with `TAGS:` and collect every unique tag into a set
    4. Extract all lines that start with `RELEVANCE:` and count how many are HIGH vs MEDIUM

    **Hints:**
    - `line.startswith("PAPER:")` checks if a line begins with that prefix
    - `line.replace("TAGS: ", "\")` strips the prefix to get just the tags
    - A Python `set()` holds unique values — `my_set.add(item)` won't add duplicates

    Try it yourself first, then check the solution below.
    """)
    return


@app.cell
def _(Path):
    # YOUR CODE HERE
    digest_file = Path.cwd() / 'sample_data' / 'weekly_digest.txt'
    # Step 1: Find and print PAPER lines
    # Step 2: Collect all unique tags
    # Step 3: Count HIGH vs MEDIUM relevance
    lines_2 = digest_file.read_text().strip().split('\n')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### Solution
    """)
    return


@app.cell
def _(Path):
    digest_file_1 = Path.cwd() / 'sample_data' / 'weekly_digest.txt'
    lines_3 = digest_file_1.read_text().strip().split('\n')
    print('=== PAPERS FOUND ===')
    for line_3 in lines_3:
        if line_3.startswith('PAPER:'):
    # --- Step 1: Papers ---
            paper_info = line_3.replace('PAPER: ', '')
            print(f'  {paper_info}')
    print()
    all_tags = set()  # Remove the "PAPER: " prefix
    for line_3 in lines_3:
        if line_3.startswith('TAGS:'):
            tag_string = line_3.replace('TAGS: ', '')
            tags = tag_string.split(', ')
            for tag in tags:
    # --- Step 2: Unique tags ---
                all_tags.add(tag)
    print(f'=== UNIQUE TAGS ({len(all_tags)}) ===')
    for tag in sorted(all_tags):
        print(f'  {tag}')
    print()
    high_count = 0
    medium_count = 0
    for line_3 in lines_3:
        if line_3.startswith('RELEVANCE:'):
            level = line_3.replace('RELEVANCE: ', '')
            if level == 'HIGH':
                high_count = high_count + 1
            elif level == 'MEDIUM':
                medium_count = medium_count + 1
    # --- Step 3: Relevance counts ---
    print(f'=== RELEVANCE ===')
    print(f'  HIGH:   {high_count}')
    print(f'  MEDIUM: {medium_count}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Build a summary report and save it

    Using what you've learned, create a summary report file:

    1. Read `binder_screening.csv`
    2. Group candidates by target (NaV1.7, NaV1.8, KCNQ2, KCNQ3)
    3. For each target, find the best (lowest Kd) candidate
    4. Write a text file `sample_data/screening_summary.txt` with your results

    **Hint:** Use a dictionary to track the best candidate per target.
    """)
    return


@app.cell
def _():
    # YOUR CODE HERE

    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 📖 **Deep dive:** <details><summary>Click to expand — Text encodings: UTF-8 vs ASCII</summary>
    >
    > When Python reads a text file, it decodes the raw bytes into characters. The encoding tells it how. **ASCII** covers the basic Latin alphabet (A-Z, 0-9, common punctuation) — 128 characters total. **UTF-8** is a superset that covers every character in every language, plus symbols like `°`, `µ`, `±`, `α`, and `→`.
    >
    > Why this matters for you: scientific text is full of non-ASCII characters (µM, °C, ΔF/F₀, ±). If you open a UTF-8 file assuming ASCII, those characters turn into garbage or cause errors. Python 3 defaults to UTF-8, so this usually just works. But if you see `UnicodeDecodeError`, it means the file uses a different encoding. Fix it with: `Path("file.txt").read_text(encoding="utf-8")` or try `encoding="latin-1"` for older files.
    >
    > </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ### Solution
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
    - 2026-03-25: Added standardized callouts and decision frameworks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - **File paths** with `pathlib.Path` — build paths safely with `/`
    - **Reading text files** — `.read_text()`, then `.strip().split("\n")` for lines
    - **Writing text files** — `.write_text()`, join lines with `"\n".join()`
    - **CSV files** — `csv.DictReader` for reading, `csv.DictWriter` for writing
    - **String methods** — `.startswith()`, `.replace()`, `.split()`
    - **pandas preview** — `pd.read_csv()` for when you're ready for bigger data

    Next up: understanding libraries and packages — how to tap into the massive ecosystem of tools other people have built.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Your First Code](01-your-first-code.py) | [Module Index](../README.md) | [Next: Libraries and Packages \u2192](03-libraries-and-packages.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Think Python, Chapter 14**: [Files](https://allendowney.github.io/ThinkPython/chap14.html) — reading and writing files in Python, covering the same patterns used in this notebook with additional depth
    - [Python docs: `pathlib` — Object-oriented filesystem paths](https://docs.python.org/3/library/pathlib.html) — the official reference for the `Path` class used throughout this notebook
    - [Python docs: `csv` — CSV file reading and writing](https://docs.python.org/3/library/csv.html) — the official reference for `csv.DictReader` and `csv.DictWriter`
    - [Python docs: String methods](https://docs.python.org/3/library/stdtypes.html#string-methods) — reference for `.strip()`, `.split()`, `.startswith()`, `.replace()`, and other methods used for text parsing
    - **Missing Semester, Lecture 1**: [The Shell](https://missing.csail.mit.edu/2020/course-shell/) — covers navigating directories and working with files from the command line, complementing the Python approach in this notebook
    - [Pandas `read_csv()` documentation](https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html) — for when you're ready to graduate from the `csv` module to pandas (previewed at the end of this notebook)
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

