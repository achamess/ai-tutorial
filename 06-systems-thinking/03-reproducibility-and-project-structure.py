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
    # Module 6.3: Reproducibility and Project Structure

    ## Organizing Your Work So It Actually Works

    You've experienced this in the lab: you find an old notebook entry from 6 months ago. The protocol says "use the usual buffer." Which buffer? What concentration? Where's the recipe?

    Code projects have the exact same problem. If you don't organize them well, your future self (and your reviewers, and your PI) will be just as lost.

    This notebook covers the practices that make computational work **reproducible** — meaning anyone can re-run your analysis and get the same results.

    **Key reference:** Wilson, G. et al. (2017). "Good Enough Practices in Scientific Computing." *PLOS Computational Biology*, 13(6), e1005510. [doi:10.1371/journal.pcbi.1005510](https://doi.org/10.1371/journal.pcbi.1005510) -- This paper lays out practical recommendations for researchers who aren't software engineers but need reproducible code. Many of the practices in this notebook are drawn from it.

    **See also:** [Missing Semester Lecture 6: Version Control](https://missing.csail.mit.edu/2020/version-control/) | [Python docs: `venv` module](https://docs.python.org/3/library/venv.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Evaluating and Debugging Code](02-evaluating-and-debugging.py) | [Module Index](../README.md) | [Next: Remote Computing Fundamentals \u2192](../07-cloud-and-hpc/01-remote-computing-fundamentals.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - NIH and major journals (Nature, Science, Cell) now require computational reproducibility for published analyses. A well-structured project means your RNA-seq analysis or binder screening pipeline can be re-run by reviewers, collaborators, or future-you.
    > - Poor project structure leads to "it worked on my laptop" failures. When a collaborator asks to reproduce your volcano plot from 6 months ago and you can't find the right script or data version, that's a structure problem.
    > - Your binder design pipeline involves multiple tools (RFdiffusion, ProteinMPNN, AlphaFold) producing intermediate files at each stage. Without consistent organization, you lose track of which designs led to which experimental results.
    > - Reproducibility is also self-defense: when a reviewer questions your analysis, being able to re-run everything from raw data in one command is the difference between a minor revision and a major headache.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. Why Reproducibility Matters

    Reproducibility in computational work means: **anyone (including future-you) can re-run your analysis and get the same results**.

    ### Who benefits?

    | Person | Why they care |
    |---|---|
    | **Future you** (6 months from now) | "How did I generate Figure 3?" |
    | **Your PI** | "Can you re-run this with the new batch of data?" |
    | **Reviewers** | "We need to see the analysis code for the supplementary" |
    | **Collaborators** | "I want to apply your pipeline to our NaV1.8 data" |
    | **The field** | Reproducibility is becoming a publication requirement |

    ### The reproducibility checklist

    For a computational analysis to be reproducible, you need:

    1. **The code** (obviously)
    2. **The data** (or instructions to obtain it)
    3. **The environment** (Python version, package versions)
    4. **The parameters** (thresholds, settings, configurations)
    5. **The order of operations** (which script runs first?)

    If any one of these is missing, reproducibility breaks down.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Project Structure: Where Things Go

    A well-organized project is like a well-organized lab bench — you can find what you need without hunting.

    ### The Standard Layout

    ```
    nav17-binder-screen/
    |
    |-- data/
    |   |-- raw/              <- Original data. NEVER modify these.
    |   |   |-- candidates.csv
    |   |   |-- calcium_imaging_20260315/
    |   |   |-- rnaseq_counts.csv
    |   |
    |   |-- processed/        <- Cleaned/transformed data (can be regenerated)
    |       |-- filtered_candidates.csv
    |       |-- normalized_traces.csv
    |
    |-- scripts/              <- Reusable analysis scripts
    |   |-- filter_candidates.py
    |   |-- score_binders.py
    |   |-- generate_figures.py
    |
    |-- notebooks/            <- Exploratory analysis (marimo)
    |   |-- 01_explore_candidates.py
    |   |-- 02_calcium_analysis.py
    |   |-- 03_rnaseq_degs.py
    |
    |-- results/              <- Output (figures, tables, reports)
    |   |-- figures/
    |   |-- tables/
    |   |-- reports/
    |
    |-- config/               <- Settings and parameters
    |   |-- screening_params.yaml
    |   |-- analysis_config.yaml
    |
    |-- requirements.txt      <- Python package dependencies
    |-- README.md             <- What is this project? How to run it?
    ```

    ### Why this structure?

    - **`data/raw/`** is sacred — never modify raw data. If you mess up the analysis, you can always start over.
    - **`data/processed/`** is derived — can be regenerated from raw data + scripts.
    - **`scripts/`** vs **`notebooks/`** — scripts are for repeatable steps, notebooks are for exploration.
    - **`results/`** is ephemeral — figures and tables can be regenerated from processed data + scripts.
    - **`config/`** separates settings from code — change parameters without editing code.

    Think of it like this:
    - `data/raw/` = your tissue samples in the -80 freezer (precious, irreplaceable)
    - `data/processed/` = your RNA extractions (can redo from samples)
    - `scripts/` = your SOPs (standard operating procedures)
    - `results/` = your figures and stats (can regenerate from processed data)
    - `config/` = your experimental parameters (concentrations, timepoints, etc.)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Visual: Ideal Project Layout

    ```
    nav17-binder-screen/
    |
    |-- data/
    |   |-- raw/                 # SACRED -- never modify
    |   |   |-- binding_assay_batch1.csv
    |   |   |-- binding_assay_batch2.csv
    |   |   +-- README.md        # Describes data provenance
    |   |-- processed/            # Derived from raw -- can regenerate
    |   |   |-- filtered_candidates.csv
    |   |   +-- ranked_hits.csv
    |   +-- metadata/
    |       +-- sample_info.csv
    |
    |-- analysis/                 # Numbered scripts run in order
    |   |-- 01_load_and_validate.py
    |   |-- 02_compute_properties.py
    |   |-- 03_filter_and_rank.py
    |   +-- 04_generate_report.py
    |
    |-- notebooks/                # Exploration and prototyping
    |   +-- explore_batch1.py
    |
    |-- figures/                  # Generated output
    |   |-- screening_overview.pdf
    |   +-- top_hits_detail.pdf
    |
    |-- config/
    |   +-- screening_params.json # All tunable parameters
    |
    |-- requirements.txt          # Pinned package versions
    |-- CLAUDE.md                 # AI assistant instructions
    |-- .gitignore                # What NOT to track
    +-- README.md                 # Project documentation
    ```

    Notice three key principles: (1) raw data is isolated and untouchable, (2) scripts are numbered for execution order, and (3) configuration is separated from code.
    """)
    return


@app.cell
def _():
    # Let's build a well-structured mini-project programmatically
    # This shows you what to ask Claude to create when starting a new analysis

    from pathlib import Path
    import json

    def create_project_structure(project_name, base_path="."):
        """
        Create a standard project directory structure for a research analysis.
    
        Parameters:
            project_name: name of the project (will be the top-level directory)
            base_path: where to create the project
        """
        project_dir = Path(base_path) / project_name
    
        # Define the directory structure
        directories = [
            "data/raw",
            "data/processed",
            "scripts",
            "notebooks",
            "results/figures",
            "results/tables",
            "results/reports",
            "config",
        ]
    
        for directory in directories:
            dir_path = project_dir / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"  Created: {dir_path}")
    
        # Create a README
        readme_content = f"""# {project_name}

    ## Purpose
    [Describe what this project analyzes]

    ## Setup
    ```bash
    pip install -r requirements.txt
    ```

    ## Directory Structure
    - `data/raw/` — Original, unmodified data files
    - `data/processed/` — Cleaned and transformed data (regenerable from raw/)
    - `scripts/` — Reusable analysis scripts
    - `notebooks/` — Exploratory marimo notebooks
    - `results/` — Output figures, tables, and reports
    - `config/` — Configuration files and parameters

    ## How to Run
    [Document the order of operations]
    """
        (project_dir / "README.md").write_text(readme_content)
        print(f"  Created: {project_dir / 'README.md'}")
    
        # Create a requirements.txt template
        requirements = """# Core dependencies
    pandas>=2.0
    numpy>=1.24
    matplotlib>=3.7
    seaborn>=0.12
    scipy>=1.10
    """
        (project_dir / "requirements.txt").write_text(requirements)
        print(f"  Created: {project_dir / 'requirements.txt'}")
    
        print(f"\nProject '{project_name}' created at {project_dir.resolve()}")
        return project_dir


    # Create an example project (in a temp directory so we don't clutter things)
    import tempfile
    temp_dir = tempfile.mkdtemp()
    project_path = create_project_structure("nav17-binder-screen", temp_dir)
    return Path, json, project_path, temp_dir


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### When to Ask Claude to Create This

    Every time you start a new analysis project, tell Claude:

    > "I'm starting a new analysis for [describe project]. Create a project directory structure with separate folders for raw data, processed data, scripts, notebooks, results, and config. Include a README and requirements.txt."

    It takes 30 seconds and will save you hours of confusion later.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. Dependencies and Environments

    ### The "It Works on My Machine" Problem

    You write an analysis using pandas 2.2. Your collaborator has pandas 1.5. Your code crashes on their machine because a function you used didn't exist in that version. Sound familiar? It's like sharing a protocol that says "use the antibody" without specifying the catalog number.

    ### The Solution: `requirements.txt`

    A `requirements.txt` file lists every package your code needs, with version numbers. It's like a complete reagent list for a protocol.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** Always maintain a `requirements.txt` for every project. Run `pip freeze > requirements.txt` (or better, manually curate the list with only your direct dependencies) so that anyone -- including future-you -- can recreate your exact environment with `pip install -r requirements.txt`. This is the difference between "my analysis is reproducible" and "it worked on my machine six months ago."
    """)
    return


@app.cell
def _():
    # Let's see what packages we currently have
    import pandas as pd
    import numpy as np
    import matplotlib

    print("Current package versions:")
    print(f"  pandas:     {pd.__version__}")
    print(f"  numpy:      {np.__version__}")
    print(f"  matplotlib: {matplotlib.__version__}")
    print()
    print("These versions should go in requirements.txt so anyone can recreate your environment.")
    return np, pd


@app.cell
def _():
    # What a good requirements.txt looks like:

    requirements_example = """
    # === requirements.txt ===
    # Pin exact versions for reproducibility

    # Data manipulation
    pandas==2.2.0
    numpy==1.26.3

    # Visualization
    matplotlib==3.8.2
    seaborn==0.13.1

    # Statistics
    scipy==1.12.0

    # AI/API
    anthropic==0.43.0

    # marimo
    marimo==0.21.1
    ipykernel==6.29.0
    """

    print(requirements_example)
    print("---")
    print("To install all these: pip install -r requirements.txt")
    print("To generate from your current environment: pip freeze > requirements.txt")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Virtual Environments (What We're Using Right Now)

    This tutorial runs in a virtual environment (`.venv/` with the `ai-tutorial` kernel). A virtual environment is an isolated set of packages -- like having a separate reagent shelf for each project. See the [Python `venv` documentation](https://docs.python.org/3/library/venv.html) for the full reference.

    Why this matters:
    - Project A needs pandas 2.2
    - Project B needs pandas 1.5 (because of a legacy tool)
    - With virtual environments, each project gets its own pandas version
    - Without them, you can only have one version and something breaks

    When you start a new project, ask Claude:

    > "Create a virtual environment for this project and a requirements.txt with the packages I'll need for [describe analysis]."
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. Version Control Concepts

    **Reference**: See *The Missing Semester*, Lecture 6 (Version Control / Git) for a comprehensive introduction.

    Git is a version control system. Here's what it gives you in practical terms:

    ### What Git Does (Conceptually)

    Imagine your lab notebook, but with superpowers:

    | Lab Notebook | Git |
    |---|---|
    | Date each entry | Each save ("commit") has a timestamp |
    | Can't erase old entries | Complete history, can always go back |
    | One notebook per person | Multiple people can work on the same project |
    | "See page 47 for previous version" | Instantly view any previous version |
    | Photocopy to share | Push/pull to share with collaborators |

    ### Key Concepts (Just Enough to Be Useful)

    1. **Repository (repo)**: A project folder tracked by Git
    2. **Commit**: A snapshot of your project at a point in time, with a description of what changed
    3. **Branch**: A parallel version of your project (like running the same experiment with a modified protocol)
    4. **Push/Pull**: Send your changes to / get changes from a shared copy (like syncing a shared drive)

    ### What to Track in Git

    | Track | Don't Track |
    |---|---|
    | Scripts (.py) | Raw data (too large, use separate storage) |
    | Notebooks (.py) | Processed data (can regenerate) |
    | Config files | API keys / passwords |
    | requirements.txt | Virtual environment folders (.venv/) |
    | README.md | Generated results (figures, reports) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Decision point: Git vs manual backups vs cloud storage for version control**
    >
    > | Approach | Pros | Cons | Use when |
    > |----------|------|------|----------|
    > | **Git** | Full history, branching, can revert any change, industry standard | Learning curve, doesn't handle large binary files well | Code, scripts, notebooks, config files, CLAUDE.md -- anything text-based |
    > | **Manual backups** (`script_v2_final.py`) | No learning curve | Cluttered, no real history, can't diff versions, error-prone | Never -- this is the anti-pattern Git was invented to replace |
    > | **Cloud storage** (Dropbox, Google Drive, OneDrive) | Automatic sync, no commands | No branching, poor conflict handling, can't see diffs, silent overwrites | Sharing raw data files with collaborators, backing up large binary data |
    > | **Git + cloud storage** | Best of both: code in Git, data in cloud | Two systems to maintain | Most research projects: Git for code, cloud for large data files |
    >
    > **Recommendation:** Use Git for all code and text files. Use cloud storage or a shared drive for large data files (imaging stacks, raw sequencing data). Add a `.gitignore` to exclude data files from Git.
    """)
    return


@app.cell
def _():
    # A .gitignore file tells Git which files to NOT track
    # This is important for keeping secrets and large files out of version control

    gitignore_example = """# === .gitignore ===

    # Python virtual environment
    .venv/
    env/

    # Data files (track these separately — too large for Git)
    data/raw/
    data/processed/

    # Generated results (can be regenerated from code + data)
    results/

    # Secrets — NEVER commit these
    .env
    *.key
    credentials.json

    # Python cache files
    __pycache__/
    *.pyc

    # Notebook checkpoints
    .py_checkpoints/

    # OS files
    .DS_Store
    Thumbs.db
    """

    print(gitignore_example)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Git in Practice (What You'll Actually Do)

    You don't need to memorize Git commands. Claude can run them for you via Claude Code. But you should understand the workflow:

    1. **Make changes** to your scripts/notebooks
    2. **Commit** the changes with a description: "Added filtering step for binder solubility"
    3. **Push** to GitHub so it's backed up and shareable

    When things go wrong (and they will), Git lets you:
    - See what changed: "What did I modify since last week?"
    - Go back: "Undo the changes I made today, they broke everything"
    - Compare: "What's different between the working version and the broken version?"

    Tell Claude: *"Initialize a Git repo for this project, create a .gitignore that excludes data files and secrets, and make the first commit."*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Configuration: Separating Settings from Code

    One of the most common mistakes is hardcoding settings directly in your analysis code. It's like writing concentrations in pen directly into your protocol instead of having a separate sheet of experimental parameters.

    ### The Problem
    """)
    return


@app.cell
def _():
    # BAD: Settings mixed into the code
    # If you want to change a threshold, you have to hunt through the code

    def analyze_bad(data):
        # Where did these numbers come from? Can I change them easily?
        filtered = data[data["kd"] < 50]                    # Why 50?
        filtered = filtered[filtered["solubility"] > 0.3]   # Why 0.3?
        filtered["score"] = (
            0.4 * filtered["affinity_norm"] +               # Why 0.4?
            0.35 * filtered["selectivity_norm"] +           # Why 0.35?
            0.25 * filtered["solubility_norm"]              # Why 0.25?
        )
        return filtered

    print("Bad: settings are buried in code. See the clean version below.")
    return


@app.cell
def _():
    # GOOD: Settings in a configuration dictionary (or file)
    # All parameters in one place, easy to find, easy to change

    # This could come from a config file (YAML, JSON, etc.)
    SCREENING_CONFIG = {
        "filters": {
            "max_kd_nm": 50,              # Maximum Kd (nM) — tighter is better
            "min_solubility": 0.3,         # Minimum predicted solubility (0-1 scale)
        },
        "scoring_weights": {
            "affinity": 0.40,              # Weight for binding affinity
            "selectivity": 0.35,           # Weight for NaV1.7 selectivity
            "solubility": 0.25,            # Weight for solubility
        },
        "target": "NaV1.7",
        "description": "Standard screening parameters for NaV1.7 binder candidates",
    }


    def analyze_good(data, config):
        """Score binder candidates using configurable parameters."""
        # Filter using config values
        filters = config["filters"]
        filtered = data[data["kd"] < filters["max_kd_nm"]]
        filtered = filtered[filtered["solubility"] > filters["min_solubility"]]
    
        # Score using config weights
        w = config["scoring_weights"]
        filtered = filtered.copy()
        filtered["score"] = (
            w["affinity"] * filtered["affinity_norm"] +
            w["selectivity"] * filtered["selectivity_norm"] +
            w["solubility"] * filtered["solubility_norm"]
        )
        return filtered


    print("Config:")
    for key, value in SCREENING_CONFIG.items():
        print(f"  {key}: {value}")
    print()
    print("Now anyone can see exactly what parameters were used.")
    print("Change the config, re-run the analysis — no code changes needed.")
    return (SCREENING_CONFIG,)


@app.cell
def _(Path, SCREENING_CONFIG, json, temp_dir):
    # Even better: save config to a file that you can version control and share
    config_path = Path(temp_dir) / 'nav17-binder-screen' / 'config' / 'screening_params.json'
    config_path.parent.mkdir(parents=True, exist_ok=True)
    # Save config
    config_path.write_text(json.dumps(SCREENING_CONFIG, indent=2))
    print(f'Config saved to: {config_path}')
    print()
    loaded_config = json.loads(config_path.read_text())
    print('Loaded config:')
    # Load config (this is what your script would do)
    print(json.dumps(loaded_config, indent=2))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Environment Variables for Secrets

    API keys (like your Anthropic API key) should **never** be in your code or config files. They go in environment variables.

    ```python
    # BAD — key is visible in your code and Git history
    client = anthropic.Anthropic(api_key="sk-ant-abc123...")

    # GOOD — key is stored in the environment, not in code
    import os
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    ```

    You can store environment variables in a `.env` file (which is in `.gitignore` so it never gets committed):

    ```
    # .env file (NEVER commit this)
    ANTHROPIC_API_KEY=sk-ant-abc123...
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Data Management Tiers

    ```mermaid
    graph TD
        subgraph "SACRED -- Never Modify"
            RAW["data/raw/<br>Original experimental data<br>Binding assays, imaging, RNA-seq<br><br>Backup to external drive<br>Version control the README only"]
        end

        subgraph "REPRODUCIBLE -- Can Regenerate"
            PROC["data/processed/<br>Cleaned, filtered, normalized<br>Generated by scripts from raw/<br><br>OK to delete and re-create<br>Version control is optional"]
        end

        subgraph "EPHEMERAL -- Disposable"
            RESULTS["results/ and figures/<br>Plots, tables, reports<br>Generated from processed data<br><br>Re-run scripts to regenerate<br>Do NOT version control large files"]
        end

        RAW -->|"analysis scripts<br>(01_load.py)"| PROC
        PROC -->|"analysis scripts<br>(03_analyze.py)"| RESULTS

        style RAW fill:#E24A33,color:#fff
        style PROC fill:#FDB863,color:#000
        style RESULTS fill:#55A868,color:#fff
    ```

    **The rule:** Data flows in one direction -- from raw to processed to results. You should be able to delete everything in `processed/` and `results/`, then re-run your scripts to regenerate it all. If you can't, your pipeline isn't reproducible yet.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. Data Management: Raw Data Is Sacred

    The most important rule of data management:

    ### **Never modify raw data files.**

    This is the computational equivalent of "never contaminate your stock solutions."

    ### The Three Tiers of Data

    ```
    SACRED (never modify, always back up)
      |-- data/raw/calcium_imaging_20260315/
      |-- data/raw/rnaseq_counts_batch1.csv
      |-- data/raw/behavioral_von_frey.xlsx

    DERIVED (regenerable from raw + code)
      |-- data/processed/normalized_traces.csv
      |-- data/processed/filtered_candidates.csv
      |-- data/processed/deg_results.csv

    EPHEMERAL (regenerable from processed + code)
      |-- results/figures/figure_1_dose_response.png
      |-- results/tables/top_10_binders.csv
      |-- results/reports/screening_report.html
    ```

    ### Rules

    1. **Raw data is read-only.** Your scripts read from `data/raw/`, never write to it.
    2. **Processed data can be deleted.** If you can regenerate it by running your pipeline on raw data, it's safe to delete.
    3. **Results are disposable.** Figures and tables should always be regenerable from code + data.
    4. **Document how raw data was obtained.** Include a `data/raw/README.md` that says where data came from and when.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Warning:** Raw data is sacred -- never modify original files. This is the computational equivalent of "never contaminate your stock solutions." If you need to clean, filter, or transform data, write a script that reads from `data/raw/` and writes to `data/processed/`. This way you can always regenerate processed data from the originals, and you have a complete audit trail of every transformation. If Claude Code ever tries to edit a file in `data/raw/`, deny the permission.
    """)
    return


@app.cell
def _(Path, project_path):
    # Demo: A data management pattern for your analysis scripts
    import shutil

    class ProjectPaths:
        """Centralized path management for a research project.
    
        Ensures consistent paths and prevents accidental writes to raw data.
        """

        def __init__(self, project_root):
            self.root = Path(project_root)
            self.raw_data = self.root / 'data' / 'raw'
            self.processed_data = self.root / 'data' / 'processed'
            self.results = self.root / 'results'
            self.figures = self.results / 'figures'
            self.tables = self.results / 'tables'
            self.config = self.root / 'config'

        def get_raw(self, filename):
            """Get path to a raw data file (read-only)."""
            path = self.raw_data / filename
            if not path.exists():
                raise FileNotFoundError(f'Raw data file not found: {path}')
            return path

        def get_processed(self, filename):
            """Get path for a processed data file (will create directory if needed)."""
            self.processed_data.mkdir(parents=True, exist_ok=True)
            return self.processed_data / filename

        def get_figure(self, filename):
            """Get path for a figure file (will create directory if needed)."""
            self.figures.mkdir(parents=True, exist_ok=True)
            return self.figures / filename

        def get_table(self, filename):
            """Get path for a results table (will create directory if needed)."""
            self.tables.mkdir(parents=True, exist_ok=True)
            return self.tables / filename
    paths = ProjectPaths(project_path)
    print('Project paths:')
    print(f'  Raw data:      {paths.raw_data}')
    # Usage example
    print(f'  Processed:     {paths.processed_data}')
    print(f'  Figures:       {paths.figures}')
    print(f'  Tables:        {paths.tables}')
    print()
    print('Example usage in a script:')
    print("  raw_file = paths.get_raw('candidates.csv')")
    print("  output_file = paths.get_processed('filtered_candidates.csv')")
    return paths, shutil


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. Demo: A Well-Structured Mini-Project

    Let's put it all together and build a small but properly structured analysis project for binder screening. This demonstrates what you'd ask Claude to create as a starting point.
    """)
    return


@app.cell
def _(np, paths, pd):
    # Create a complete mini-project with sample data and analysis script
    import textwrap
    np.random.seed(42)
    n = 50
    sample_candidates = pd.DataFrame({'binder_id': [f'NaV17-B{i:03d}' for i in range(1, n + 1)], 'sequence_length': np.random.randint(80, 200, n), 'predicted_kd_nm': np.random.lognormal(3, 1.5, n).round(1), 'predicted_solubility': np.random.uniform(0.1, 1.0, n).round(3), 'nav17_selectivity': np.random.uniform(0.5, 50, n).round(1), 'thermal_stability_c': np.random.normal(65, 10, n).round(1)})
    # Step 1: Create sample raw data
    raw_data_path = paths.raw_data / 'binder_candidates_batch1.csv'
    sample_candidates.to_csv(raw_data_path, index=False)
    print(f'Created raw data: {raw_data_path}')
    print(f'  {n} candidates with 6 properties each')
    # Save as "raw" data
    print()
    return (raw_data_path,)


@app.cell
def _(json, paths):
    # Step 2: Create configuration file

    screening_config = {
        "project": "NaV1.7 Binder Screening — Batch 1",
        "date": "2026-03-25",
        "target": "NaV1.7 (SCN9A)",
        "filters": {
            "max_kd_nm": 100,
            "min_solubility": 0.3,
            "min_selectivity": 5.0,
            "min_thermal_stability_c": 50,
        },
        "scoring": {
            "weights": {
                "affinity": 0.35,
                "selectivity": 0.30,
                "solubility": 0.20,
                "stability": 0.15,
            },
            "description": "Weighted composite score. Higher is better."
        },
        "output": {
            "top_n": 10,
        }
    }

    config_file = paths.config / "screening_params.json"
    config_file.write_text(json.dumps(screening_config, indent=2))
    print(f"Created config: {config_file}")
    print(json.dumps(screening_config, indent=2))
    return (config_file,)


@app.cell
def _(config_file, json, pd, raw_data_path):
    # Step 3: Run the analysis (this is what a script would do)

    # Load config
    config = json.loads(config_file.read_text())

    # Load raw data
    candidates = pd.read_csv(raw_data_path)
    print(f"Loaded {len(candidates)} candidates from {raw_data_path.name}")

    # Apply filters
    f = config["filters"]
    filtered = candidates[
        (candidates["predicted_kd_nm"] <= f["max_kd_nm"]) &
        (candidates["predicted_solubility"] >= f["min_solubility"]) &
        (candidates["nav17_selectivity"] >= f["min_selectivity"]) &
        (candidates["thermal_stability_c"] >= f["min_thermal_stability_c"])
    ].copy()

    print(f"After filtering: {len(filtered)} candidates remain ({len(candidates) - len(filtered)} removed)")
    print(f"  Filters applied: Kd <= {f['max_kd_nm']}nM, solubility >= {f['min_solubility']}, "
          f"selectivity >= {f['min_selectivity']}, stability >= {f['min_thermal_stability_c']}C")
    return config, filtered


@app.cell
def _(config, filtered, pd):
    # Step 4: Score and rank

    def normalize_column(series, lower_is_better=False):
        """Normalize values to 0-1 range."""
        min_val, max_val = series.min(), series.max()
        if max_val == min_val:
            return pd.Series(0.5, index=series.index)
        normed = (series - min_val) / (max_val - min_val)
        return 1 - normed if lower_is_better else normed

    # Normalize properties
    filtered["affinity_score"] = normalize_column(filtered["predicted_kd_nm"], lower_is_better=True)
    filtered["selectivity_score"] = normalize_column(filtered["nav17_selectivity"])
    filtered["solubility_score"] = normalize_column(filtered["predicted_solubility"])
    filtered["stability_score"] = normalize_column(filtered["thermal_stability_c"])

    # Compute composite score
    w = config["scoring"]["weights"]
    filtered["composite_score"] = (
        w["affinity"] * filtered["affinity_score"] +
        w["selectivity"] * filtered["selectivity_score"] +
        w["solubility"] * filtered["solubility_score"] +
        w["stability"] * filtered["stability_score"]
    ).round(3)

    # Rank
    ranked = filtered.sort_values("composite_score", ascending=False).reset_index(drop=True)
    ranked.index += 1
    ranked.index.name = "rank"

    print(f"\nTop {config['output']['top_n']} candidates:")
    display_cols = ["binder_id", "predicted_kd_nm", "nav17_selectivity", 
                    "predicted_solubility", "thermal_stability_c", "composite_score"]
    print(ranked[display_cols].head(config["output"]["top_n"]).to_string())
    return display_cols, ranked


@app.cell
def _(config, display_cols, paths, ranked):
    # Step 5: Save results

    # Save processed data
    processed_path = paths.get_processed("ranked_candidates_batch1.csv")
    ranked.to_csv(processed_path)
    print(f"Saved ranked candidates: {processed_path}")

    # Save top-N table
    top_n_path = paths.get_table("top_10_binders.csv")
    ranked[display_cols].head(config["output"]["top_n"]).to_csv(top_n_path)
    print(f"Saved top 10 table: {top_n_path}")

    # Generate a figure
    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    # Plot 1: Score distribution
    axes[0].hist(ranked["composite_score"], bins=15, edgecolor="black", alpha=0.7, color="steelblue")
    axes[0].set_xlabel("Composite Score")
    axes[0].set_ylabel("Number of Candidates")
    axes[0].set_title("Score Distribution (Filtered Candidates)")
    axes[0].axvline(ranked["composite_score"].head(10).min(), color="red", 
                    linestyle="--", label=f"Top 10 cutoff")
    axes[0].legend()

    # Plot 2: Affinity vs Selectivity colored by score
    scatter = axes[1].scatter(
        ranked["predicted_kd_nm"], 
        ranked["nav17_selectivity"],
        c=ranked["composite_score"],
        cmap="RdYlGn",
        s=60,
        edgecolors="black",
        linewidth=0.5,
    )
    axes[1].set_xlabel("Predicted Kd (nM) — lower is better")
    axes[1].set_ylabel("NaV1.7 Selectivity Ratio — higher is better")
    axes[1].set_title("Affinity vs Selectivity")
    plt.colorbar(scatter, ax=axes[1], label="Composite Score")

    plt.suptitle(f"{config['project']}", fontsize=14, fontweight="bold")
    plt.tight_layout()

    figure_path = paths.get_figure("binder_screening_overview.png")
    plt.savefig(figure_path, dpi=150, bbox_inches="tight")
    print(f"Saved figure: {figure_path}")
    plt.show()
    return


@app.cell
def _(Path, project_path):
    # Let's see what our project looks like now
    import os

    def show_tree(path, prefix="", max_depth=3, current_depth=0):
        """Show directory tree structure."""
        if current_depth >= max_depth:
            return
        path = Path(path)
        entries = sorted(path.iterdir(), key=lambda p: (not p.is_dir(), p.name))
        for i, entry in enumerate(entries):
            is_last = i == len(entries) - 1
            connector = "+-- " if is_last else "|-- "
            print(f"{prefix}{connector}{entry.name}{'/' if entry.is_dir() else ''}")
            if entry.is_dir():
                extension = "    " if is_last else "|   "
                show_tree(entry, prefix + extension, max_depth, current_depth + 1)

    print(f"Project structure:")
    print(f"{project_path.name}/")
    show_tree(project_path)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 8. Exercise: Restructure a Messy Project

    Below is a description of a messy project directory. Your job: sketch out what the clean version should look like.

    ### The Mess

    ```
    my_analysis/
    |-- analysis.py
    |-- analysis_v2.py
    |-- analysis_v2_FINAL.py
    |-- analysis_v2_FINAL_fixed.py
    |-- raw_counts.csv
    |-- raw_counts_cleaned.csv
    |-- figure1.png
    |-- figure1_v2.png
    |-- figure1_FINAL.png
    |-- notes.txt
    |-- Untitled.py
    |-- Untitled2.py
    |-- .env                    (contains API key!)
    |-- results_20260101.csv
    |-- results_20260215.csv
    |-- todo.md
    ```

    ### Problems:
    - Multiple versions of scripts (no version control)
    - Raw and processed data mixed together
    - Figures with version suffixes (no version control)
    - Unnamed notebooks
    - Everything in one directory
    - API key in the project folder
    """)
    return


@app.cell
def _():
    # EXERCISE: Define what the clean version should look like
    # Fill in the directory structure

    clean_structure = """
    my_analysis/
    |
    |-- data/
    |   |-- raw/
    |   |   |-- ___                  # What goes here?
    |   |
    |   |-- processed/
    |       |-- ___                  # What goes here?
    |
    |-- scripts/
    |   |-- ___                      # How many scripts? What should they be called?
    |
    |-- notebooks/
    |   |-- ___                      # What should the notebooks be called?
    |
    |-- results/
    |   |-- figures/
    |   |   |-- ___                  # What goes here?
    |   |-- tables/
    |       |-- ___                  # What goes here?
    |
    |-- config/
    |   |-- ___                      # What config files?
    |
    |-- .gitignore                   # What should be in here?
    |-- .env                         # API key — excluded by .gitignore!
    |-- requirements.txt
    |-- README.md
    """

    print(clean_structure)
    print("Fill in the blanks above!")
    print("\nKey decisions to make:")
    print("  1. Which file is the raw data? (hint: the original, unmodified one)")
    print("  2. Do you need all 4 script versions? (hint: use git instead)")
    print("  3. What should the notebooks be named? (hint: describe what they analyze)")
    print("  4. Do you need 3 copies of figure1? (hint: regenerate from code)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Suggested Clean Structure

    <details>
    <summary>Click to reveal answer</summary>

    ```
    my_analysis/
    |
    |-- data/
    |   |-- raw/
    |   |   |-- raw_counts.csv           # Original data, never modified
    |   |   |-- README.md                # Where data came from, when collected
    |   |
    |   |-- processed/
    |       |-- cleaned_counts.csv        # Output of cleaning step
    |
    |-- scripts/
    |   |-- analyze_counts.py             # ONE script (use git for versions)
    |
    |-- notebooks/
    |   |-- 01_explore_counts.py       # Renamed with descriptive name
    |   |-- 02_differential_expression.py
    |
    |-- results/
    |   |-- figures/
    |   |   |-- figure1.png              # ONE copy (regenerable from code)
    |   |-- tables/
    |       |-- results.csv              # Latest results only
    |
    |-- config/
    |   |-- analysis_params.json         # Thresholds, settings
    |
    |-- .gitignore                        # Excludes: .env, data/raw/, .venv/, __pycache__/
    |-- .env                              # API key — NEVER committed to git
    |-- requirements.txt
    |-- README.md                         # Project description, how to run
    ```

    Key changes:
    - Raw data isolated in `data/raw/` (read-only)
    - One script instead of 4 versions (use git for history)
    - Notebooks have descriptive names
    - One figure (regenerable), not 3 versions
    - Config separated from code
    - `.env` excluded from git

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Key Takeaways

    1. **Reproducibility = code + data + environment + config + order of operations**
    2. **Use a standard project structure** — `data/raw/`, `data/processed/`, `scripts/`, `notebooks/`, `results/`, `config/`
    3. **Pin your dependencies** in `requirements.txt` — versions matter
    4. **Use Git for version control** — no more `script_FINAL_v2_fixed.py`
    5. **Separate settings from code** — put parameters in config files
    6. **Raw data is sacred** — never modify it, only read from it
    7. **Never commit secrets** — API keys go in `.env`, which goes in `.gitignore`

    ### What to Tell Claude When Starting a New Project

    > "I'm starting a new analysis for [describe project]. Set up a project directory with the standard structure: raw data, processed data, scripts, notebooks, results, and config directories. Create a .gitignore that excludes data files, secrets, and Python cache. Initialize a Git repo and make the first commit. Create a config file with these parameters: [list your parameters]."

    That one instruction will save you hours of confusion down the road.
    """)
    return


@app.cell
def _(shutil, temp_dir):
    # Clean up the temporary directory we created
    shutil.rmtree(temp_dir, ignore_errors=True)
    print('Cleaned up temporary project directory.')
    print('\nYou now have the knowledge to structure any research computing project.')
    print('Next time you start an analysis, begin with the structure — not the code.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Evaluating and Debugging Code](02-evaluating-and-debugging.py) | [Module Index](../README.md) | [Next: Remote Computing Fundamentals \u2192](../07-cloud-and-hpc/01-remote-computing-fundamentals.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Wilson, G. et al. (2017). "Good Enough Practices in Scientific Computing." *PLOS Computational Biology*, 13(6), e1005510.** [doi:10.1371/journal.pcbi.1005510](https://doi.org/10.1371/journal.pcbi.1005510) -- The foundational paper on organizing computational research projects.
    - **[Missing Semester Lecture 6: Version Control (Git)](https://missing.csail.mit.edu/2020/version-control/)** -- How Git tracks changes, branches, merging, and collaboration.
    - **[Git Official Documentation](https://git-scm.com/doc)** -- Comprehensive reference including the free *Pro Git* book.
    - **[Python docs: `venv` -- Creation of Virtual Environments](https://docs.python.org/3/library/venv.html)** -- Official reference for creating and managing isolated Python environments.
    - **[Python docs: `pip` -- Installing Packages](https://pip.pypa.io/en/stable/user_guide/)** -- How to use `requirements.txt`, install packages, and manage dependencies.
    - **[GitHub: `.gitignore` Templates](https://github.com/github/gitignore)** -- Pre-built `.gitignore` files for Python and other languages.
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
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

