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
    # Module 4.3: Customizing Claude Code

    **What you'll learn:**
    - CLAUDE.md files -- project-level instructions that shape Claude Code's behavior
    - The memory system -- persistent context across sessions
    - Settings and permissions configuration
    - Hooks -- automating actions before/after Claude Code operations
    - Slash commands and custom skills
    - MCP servers -- extending Claude Code's capabilities
    - Best practices for getting the most out of Claude Code

    **Prerequisites:** [01-claude-code-basics.py](01-claude-code-basics.py), [02-advanced-workflows.py](02-advanced-workflows.py)

    **Key references:**
    - [CLAUDE.md and Memory](https://docs.anthropic.com/en/docs/claude-code/memory)
    - [Claude Code Settings](https://docs.anthropic.com/en/docs/claude-code/settings)
    - [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks)
    - [Model Context Protocol (MCP) Specification](https://spec.modelcontextprotocol.io/)
    - Local copy: [resources/references/anthropic-claude-code-overview.md](../resources/references/anthropic-claude-code-overview.md)

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Advanced Claude Code Workflows](02-advanced-workflows.py) | [Module Index](../README.md) | [Next: Setup & Best Practices for Claude Code \u2192](04-setup-and-best-practices.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - A well-written CLAUDE.md is the difference between re-explaining your project every session ("I work on de novo protein binders for NaV1.7...") and Claude Code already knowing your targets, your tools, your file organization, and your conventions. It turns a generic tool into a personalized research assistant.
    > - Memory and settings persistence mean Claude Code learns your preferences over time — your preferred plot style, your statistical thresholds, your naming conventions. This compounding improvement means Claude Code gets more useful the longer you use it.
    > - Custom slash commands let you create one-click workflows for repetitive tasks: `/analyze-data` for a new screening CSV, `/check-notebook` to validate a marimo notebook, `/digest` to generate a research summary. These encode your lab's best practices.
    > - MCP servers (PubMed, bioRxiv, ClinicalTrials) extend Claude Code into a research intelligence tool. Instead of switching between five browser tabs, you ask Claude Code to search literature, check clinical trials for NaV1.7 inhibitors, and find relevant preprints — all from one interface.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. CLAUDE.md: Your Project's AI Instructions

    The `CLAUDE.md` file is the single most important customization you can make. It's a markdown file at the root of your project that Claude Code reads at the start of every conversation.

    ### What to put in CLAUDE.md

    Think of it as a briefing document. Include:

    1. **Project purpose** -- What is this codebase for?
    2. **Structure** -- How are files organized?
    3. **Conventions** -- Naming conventions, coding style, etc.
    4. **Environment** -- Python version, key packages, virtual environment location
    5. **Domain knowledge** -- Anything specific to your field that Claude Code should know
    6. **Do's and don'ts** -- Rules Claude Code should follow

    ### A real example: this tutorial's CLAUDE.md

    Let's look at the CLAUDE.md that governs this very tutorial:
    """)
    return


@app.cell
def _():
    from pathlib import Path

    claude_md = Path('..') / 'CLAUDE.md'
    if claude_md.exists():
        content = claude_md.read_text()
        print(content)
    else:
        print("CLAUDE.md not found -- run /init in Claude Code to create one")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### CLAUDE.md hierarchy

    Claude Code supports multiple CLAUDE.md files at different levels:

    ```
    ~/.claude/CLAUDE.md                    # User-level (applies to ALL projects)
    ~/projects/my-research/CLAUDE.md       # Project root
    ~/projects/my-research/analysis/CLAUDE.md  # Subdirectory-specific
    ```

    They stack: Claude Code reads all of them, with more specific files taking precedence.

    **User-level CLAUDE.md** (`~/.claude/CLAUDE.md`) is great for preferences that apply everywhere:
    ```markdown
    # Global Preferences
    - I'm a pain biologist, not a software engineer. Keep code simple.
    - When writing Python, always include type hints and docstrings.
    - I prefer pandas over raw Python for data manipulation.
    - Use seaborn/matplotlib for plots, not plotly.
    - When dealing with concentrations, always clarify units (M, mM, uM, nM).
    ```

    ### Creating a CLAUDE.md

    You can create one in several ways:

    1. **Use `/init` in Claude Code** -- It will analyze your project and generate one
    2. **Write it yourself** -- Just create a `CLAUDE.md` file in your project root
    3. **Ask Claude Code to write it** -- "Create a CLAUDE.md for this project based on what you see"

    The `/init` command is the easiest starting point. You can then refine it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Configuration Hierarchy (Priority Order)

    ```mermaid
    graph TB
        subgraph "Highest Priority"
            A["Your Direct Message<br>'Use seaborn for this plot'"]
        end
        subgraph "Project-Specific"
            B["Subdirectory CLAUDE.md<br>analysis/CLAUDE.md"]
            C["Project CLAUDE.md<br>~/project/CLAUDE.md"]
        end
        subgraph "Global"
            D["User CLAUDE.md<br>~/.claude/CLAUDE.md"]
            E["Memory<br>Persistent learned preferences"]
        end
        subgraph "Lowest Priority"
            F["Claude Code Defaults<br>Built-in behavior"]
        end

        A --> B --> C --> D --> E --> F

        style A fill:#E24A33,color:#fff
        style B fill:#FDB863,color:#000
        style C fill:#FDB863,color:#000
        style D fill:#4878CF,color:#fff
        style E fill:#4878CF,color:#fff
        style F fill:#cccccc,color:#000
    ```

    More specific instructions always override more general ones. Your direct messages in a conversation have the highest priority -- they override everything else. This is why you can always say "ignore the CLAUDE.md convention and use plotly this time" and it will work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### CLAUDE.md tips and patterns

    **Be imperative, not descriptive.** Tell Claude Code what to DO:

    ```markdown
    # Bad (descriptive)
    This project uses pytest for testing.

    # Good (imperative)
    Always run `pytest tests/` after making changes to verify nothing is broken.
    ```

    **Include domain-specific rules:**

    ```markdown
    # Domain conventions
    - Ion channel nomenclature: NaV1.7 (not Nav1.7 or nav1.7)
    - Binding affinity: always express as Kd in nanomolar (nM)
    - Statistical tests: use non-parametric tests (Mann-Whitney) for n < 30
    - Figure style: use the lab's color palette defined in config/colors.py
    ```

    **Specify file organization:**

    ```markdown
    # File structure
    - data/raw/ -- original data files, NEVER modify these
    - data/processed/ -- cleaned/transformed data
    - analysis/ -- analysis scripts
    - figures/ -- generated figures
    - notebooks/ -- exploratory marimo notebooks
    ```

    **Set safety guardrails:**

    ```markdown
    # Safety rules
    - NEVER modify files in data/raw/
    - NEVER push to the main branch directly
    - ALWAYS create a backup before batch-processing data files
    - Do NOT install new packages without asking me first
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The Memory System

    While CLAUDE.md provides project-level context, Claude Code's **memory** system stores persistent notes across sessions.

    ### How memory works

    - Claude Code can save notes to its memory during a conversation
    - These notes persist across sessions
    - You can view and edit memory with the `/memory` command
    - Memory is stored locally on your machine

    ### When memory is useful

    Memory is great for things that change over time or are conversation-specific:

    - "Alex prefers violin plots over box plots"
    - "The NaV1.8 data uses a different column format than NaV1.7"
    - "When working on the RNA-seq pipeline, always activate the rnaseq-env conda environment"

    ### Memory vs CLAUDE.md

    | Feature | CLAUDE.md | Memory |
    |---|---|---|
    | Scope | Project-specific | Global |
    | Version controlled | Yes (in git) | No |
    | Shared with team | Yes | No |
    | Easy to edit | Yes (it's a file) | Via `/memory` command |
    | Best for | Project rules & structure | Personal preferences & learned context |

    **Rule of thumb:** If it's a project rule or convention, put it in CLAUDE.md. If it's a personal preference or something Claude Code learned about you, let it go in memory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Decision point: What belongs in CLAUDE.md vs settings.json vs memory**
    >
    > | Information | Where to put it | Why |
    > |-------------|----------------|-----|
    > | Project structure, file organization | **CLAUDE.md** | Version-controlled, shared with collaborators, project-specific |
    > | Coding conventions, domain rules (e.g., "NaV1.7 not Nav1.7") | **CLAUDE.md** | Everyone on the project should follow the same rules |
    > | Tool permissions, allowed/denied commands | **settings.json** | Machine-level config, not project knowledge |
    > | Personal preferences (plot style, verbosity) | **Memory** | Personal, not project-specific, applies across projects |
    > | Safety rules ("never modify data/raw/") | **CLAUDE.md** | Critical rules belong in version-controlled, visible files |
    > | API keys, environment paths | **Neither** -- use environment variables | Security: never commit secrets to files Claude reads |
    >
    > **Rule of thumb:** If a collaborator joining the project needs to know it, put it in CLAUDE.md. If it's about how YOUR Claude Code behaves, use settings.json or memory.

    > **Tip:** Keep your project CLAUDE.md under 200 lines. Claude Code reads it at the start of every conversation, so a bloated CLAUDE.md wastes context tokens and buries important rules in noise. If you need more detail, use the `@import` syntax to pull in separate files for specific subdirectories, or put detailed reference material in a `docs/` folder that Claude Code can read on demand.

    > **Warning:** Conflicting rules across multiple config files cause unpredictable behavior. If your user-level `~/.claude/CLAUDE.md` says "use plotly for all visualizations" and your project CLAUDE.md says "use matplotlib," Claude Code will follow the project-level rule (higher specificity wins) -- but the conflict can cause confusion in edge cases. Audit your config hierarchy periodically: check `~/.claude/CLAUDE.md`, project CLAUDE.md, and any subdirectory CLAUDE.md files for contradictions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Settings and Permissions

    Claude Code's behavior can be configured through its settings system.

    ### Settings locations

    Settings live in JSON files:

    ```
    ~/.claude/settings.json          # User-level settings (all projects)
    your-project/.claude/settings.json  # Project-level settings
    ```

    ### Key settings

    **Allowed tools** -- Control which tools Claude Code can use without asking:

    ```json
    {
      "permissions": {
        "allow": [
          "Read",
          "Glob",
          "Grep",
          "Bash(python *)",
          "Bash(git status)",
          "Bash(git diff*)",
          "Bash(git log*)"
        ],
        "deny": [
          "Bash(rm -rf *)",
          "Bash(git push --force*)"
        ]
      }
    }
    ```

    This lets Claude Code:
    - Read files, search, and run Python scripts without asking
    - Run safe git commands (status, diff, log) without asking
    - But still asks permission for file edits, other bash commands, etc.
    - Explicitly blocks dangerous operations

    ### Adjusting permissions for your workflow

    As you get comfortable, you might allow more:

    ```json
    {
      "permissions": {
        "allow": [
          "Read",
          "Glob",
          "Grep",
          "Edit",
          "Write",
          "Bash(python *)",
          "Bash(pip install *)",
          "Bash(git *)"
        ],
        "deny": [
          "Bash(rm -rf *)",
          "Bash(git push --force*)"
        ]
      }
    }
    ```

    > **Start restrictive, loosen over time.** Begin with the defaults, then allow specific tools as you learn to trust them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Hooks: Automating Actions

    Hooks let you run custom commands automatically before or after Claude Code performs certain actions.

    ### What hooks can do

    - Run linters/formatters after code edits
    - Run tests after file changes
    - Log actions for auditing
    - Validate changes before they're applied
    - Send notifications

    ### Hook types

    | Hook | When it runs |
    |---|---|
    | `PreToolUse` | Before Claude Code uses a tool (e.g., before editing a file) |
    | `PostToolUse` | After Claude Code uses a tool |
    | `Notification` | When Claude Code wants to notify you (e.g., task complete) |
    | `Stop` | When Claude Code finishes a response |

    ### Hook configuration

    Hooks are configured in your settings file:

    ```json
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "black $CLAUDE_FILE_PATH 2>/dev/null || true"
              }
            ]
          }
        ]
      }
    }
    ```

    This example automatically runs the `black` code formatter on any Python file after Claude Code edits it.

    ### Practical hook examples for research

    **Auto-format Python files:**
    ```json
    {
      "hooks": {
        "PostToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "if [[ \"$CLAUDE_FILE_PATH\" == *.py ]]; then black \"$CLAUDE_FILE_PATH\" 2>/dev/null; fi"
              }
            ]
          }
        ]
      }
    }
    ```

    **Prevent edits to raw data:**
    ```json
    {
      "hooks": {
        "PreToolUse": [
          {
            "matcher": "Edit|Write",
            "hooks": [
              {
                "type": "command",
                "command": "if [[ \"$CLAUDE_FILE_PATH\" == */data/raw/* ]]; then echo 'BLOCKED: Cannot modify raw data files' >&2; exit 2; fi"
              }
            ]
          }
        ]
      }
    }
    ```

    When a PreToolUse hook exits with code 2, Claude Code blocks the action. This is a great way to enforce safety rules.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. MCP Servers: Extending Claude Code

    **MCP ([Model Context Protocol](https://spec.modelcontextprotocol.io/))** is a way to give Claude Code access to external tools and data sources. Think of MCP servers as plugins that extend what Claude Code can do. The protocol is an [open specification](https://github.com/modelcontextprotocol/specification) with a growing ecosystem of community-built servers.

    ### What MCP servers enable

    Without MCP, Claude Code can read/write local files and run terminal commands. With MCP, it can also:

    - **Search PubMed** -- find papers relevant to your research
    - **Access bioRxiv** -- search preprints
    - **Query databases** -- connect to SQL databases, Airtable, etc.
    - **Use web APIs** -- interact with web services
    - **Manage Notion** -- read/write to your Notion workspace

    ### How MCP servers work

    ```
    You (natural language)
        |
        v
    Claude Code (understands intent)
        |
        v
    MCP Server (provides specialized tools)
        |
        v
    External Service (PubMed, database, API, etc.)
    ```

    You don't interact with MCP servers directly. You just talk to Claude Code normally, and it uses the MCP tools when needed:

    ```
    You: Search PubMed for recent papers on NaV1.7 protein binders for pain

    Claude Code: [uses PubMed MCP server to search]
                 Found 15 relevant papers. Here are the top 5:
                 1. "De novo design of selective NaV1.7 inhibitors..." (2025)
                 ...
    ```

    ### Configuring MCP servers

    MCP servers are configured in your Claude Code settings (see [Claude Code MCP documentation](https://docs.anthropic.com/en/docs/claude-code/mcp)):

    ```json
    {
      "mcpServers": {
        "pubmed": {
          "command": "npx",
          "args": ["-y", "@anthropic/mcp-pubmed"]
        },
        "filesystem": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
        }
      }
    }
    ```

    ### MCP servers relevant to pain biology research

    | Server | What it does | Use case |
    |---|---|---|
    | PubMed | Search biomedical literature | Find papers on ion channel pharmacology |
    | bioRxiv | Search preprints | Track new protein design papers |
    | Clinical Trials | Search clinicaltrials.gov | Find NaV1.7 inhibitor trials |
    | Filesystem | Extended file access | Access data on shared drives |
    | Notion | Notion workspace | Update your research notes |
    | Airtable | Airtable bases | Manage experiment tracking databases |

    > **Note:** MCP is a rapidly evolving ecosystem. New servers are being developed regularly. Check the [MCP server directory](https://github.com/modelcontextprotocol/servers) for the latest options.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Exercise: Write a CLAUDE.md for a Research Project

    Let's practice writing a CLAUDE.md for a hypothetical RNA-seq analysis pipeline. This exercise demonstrates the thinking process for creating effective project instructions.

    ### The scenario

    You're setting up a project to analyze RNA-seq data from dorsal root ganglion (DRG) neurons. You have three conditions:
    - Naive (control)
    - CFA-inflamed (inflammatory pain model)
    - SNI (spared nerve injury -- neuropathic pain model)

    The goal is to identify differentially expressed genes in pain states, with a focus on ion channels and GPCRs.

    ### Write it yourself first, then compare

    Before running the cell below, try writing your own CLAUDE.md. Think about:
    - What does someone (or an AI) need to know to work on this project?
    - What mistakes should be prevented?
    - What conventions should be followed?
    """)
    return


@app.cell
def _():
    # Example CLAUDE.md for an RNA-seq analysis project
    # Compare this to what you wrote

    example_claude_md = """\
    # DRG Pain Transcriptomics Pipeline

    ## Project purpose
    RNA-seq analysis of mouse DRG neurons across three pain conditions (naive, CFA, SNI).
    Goal: identify differentially expressed genes, focusing on ion channels (NaV, KCNQ, CaV)
    and GPCRs involved in nociceptor sensitization.

    ## Directory structure
    - data/raw/ -- FASTQ files and raw count matrices. NEVER modify.
    - data/processed/ -- normalized counts, filtered data
    - data/metadata/ -- sample info, experimental conditions
    - analysis/ -- analysis scripts (numbered: 01-qc.py, 02-normalize.py, etc.)
    - figures/ -- generated figures (PDF for publication, PNG for quick viewing)
    - results/ -- tables, gene lists, statistical results
    - notebooks/ -- exploratory marimo notebooks

    ## Python environment
    - Conda environment: `drg-rnaseq` (Python 3.11)
    - Key packages: scanpy, pydeseq2, pandas, numpy, matplotlib, seaborn
    - Activate: `conda activate drg-rnaseq`
    - Always use this environment for running scripts

    ## Data conventions
    - Gene names: official HUGO symbols (e.g., SCN9A not NaV1.7 in data columns)
    - Sample naming: {condition}_{replicate} (e.g., naive_01, cfa_03, sni_02)
    - Conditions: "naive", "cfa", "sni" (always lowercase in code)
    - Significance threshold: padj < 0.05, |log2FC| > 1
    - Use non-parametric tests when n < 6 per group

    ## Analysis conventions
    - All scripts should be runnable from the project root
    - Save intermediate results to data/processed/
    - Every figure must have: title, axis labels with units, legend, and be saved as PDF
    - Use the color scheme: naive=gray, cfa=orange, sni=purple
    - Log transform expression data before plotting (log2(CPM+1))

    ## Gene lists of interest
    - Voltage-gated sodium channels: SCN9A, SCN10A, SCN11A, SCN1A, SCN3A, SCN5A
    - Potassium channels: KCNQ2, KCNQ3, KCNA1, KCNA2
    - TRP channels: TRPV1, TRPA1, TRPM8
    - Nociceptor markers: CALCA, TAC1, P2RX3, MRGPRD
    These are stored in data/metadata/gene_lists.csv

    ## Safety rules
    - NEVER modify files in data/raw/
    - NEVER delete result files without asking
    - Always check that the conda environment is activated before running analysis
    - When in doubt about a statistical approach, explain options and ask before proceeding
    """

    print(example_claude_md)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Key elements in this CLAUDE.md

    Notice the structure:

    1. **Purpose** -- Claude Code immediately understands the domain and goals
    2. **Directory structure** -- Claude Code knows where to find and put things
    3. **Environment** -- Claude Code can activate the right tools
    4. **Conventions** -- Claude Code follows your naming and analysis standards
    5. **Domain knowledge** -- Gene names, significance thresholds, color schemes
    6. **Safety rules** -- Prevents accidental damage to raw data

    With this CLAUDE.md, you could say:
    ```
    You: Create a volcano plot for the CFA vs naive comparison
    ```

    And Claude Code would know:
    - Where to find the data
    - What significance thresholds to use
    - What colors to use (orange for CFA, gray for naive)
    - To save as PDF
    - To label key ion channel genes
    - To use the `drg-rnaseq` conda environment
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Best Practices for Getting the Most Out of Claude Code

    After covering all the customization options, here are the highest-impact practices:

    ### 1. Invest in your CLAUDE.md

    A good CLAUDE.md saves you from repeating the same context in every conversation. Spend 15 minutes writing one at the start of each project. Update it as the project evolves.

    ### 2. Use git religiously

    Git is your safety net. When Claude Code makes changes:
    - You can always see what changed (`git diff`)
    - You can always go back (`git checkout -- file.py`)
    - You can experiment on branches without risk

    Ask Claude Code to commit regularly:
    ```
    You: Commit the current changes -- we just finished the dose-response analysis
    ```

    ### 3. Break complex tasks into steps

    Instead of:
    ```
    You: Build me a complete RNA-seq analysis pipeline
    ```

    Do this:
    ```
    You: Let's build an RNA-seq analysis pipeline. First, let's handle
         data loading and QC. Read the count matrix and show me a summary.

    [iterate on QC]

    You: Good. Now let's add normalization.

    [iterate on normalization]

    You: Now let's do differential expression analysis.

    [iterate on DE]
    ```

    ### 4. Use /compact proactively

    Don't wait until Claude Code gets confused. After completing a major sub-task, compact the conversation:
    ```
    You: /compact
    You: Now let's move on to the visualization step.
    ```

    ### 5. Review changes before approving

    When Claude Code shows you a diff or asks permission:
    - Actually read what it's changing
    - Ask questions if something looks off
    - Don't blindly approve

    ### 6. Tell Claude Code when it's wrong

    Claude Code learns within a conversation. If it makes a mistake:
    ```
    You: That's not right. SCN9A encodes NaV1.7, not NaV1.8.
         NaV1.8 is SCN10A. Fix the analysis.
    ```

    It will correct itself and remember for the rest of the conversation.

    ### 7. Use Claude Code for code review

    Before running important analyses:
    ```
    You: Review analysis/differential_expression.py.
         Check for bugs, statistical errors, and anything that
         could produce incorrect results.
    ```

    ### 8. Teach Claude Code your preferences over time

    As you work with Claude Code, it builds up memory of your preferences. Help it learn:
    ```
    You: In the future, always use fig.savefig() with dpi=300 and bbox_inches='tight'
    ```

    Claude Code will remember this across sessions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Quick Reference: Claude Code Configuration Files

    Here's a summary of all the configuration files and where they go:

    ```
    ~/.claude/
      CLAUDE.md              # User-level instructions (all projects)
      settings.json          # User-level settings (permissions, etc.)

    your-project/
      CLAUDE.md              # Project-level instructions
      .claude/
        settings.json        # Project-level settings
        commands/            # Custom slash commands
          analyze-data.md
          generate-figure.md

      subdirectory/
        CLAUDE.md            # Subdirectory-specific instructions
    ```

    ### Priority order (highest to lowest)

    1. Direct instructions in your message
    2. Subdirectory CLAUDE.md
    3. Project CLAUDE.md
    4. User-level CLAUDE.md
    5. Claude Code's built-in behavior

    ### Getting started checklist

    For any new research project:

    - [ ] Run `/init` to generate a starting CLAUDE.md
    - [ ] Edit the CLAUDE.md with project-specific details
    - [ ] Initialize git (`git init`) if not already done
    - [ ] Consider creating custom slash commands for repeated tasks
    - [ ] Set up relevant MCP servers (PubMed, bioRxiv) if needed
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercises

    ### Exercise 1: Write a CLAUDE.md for your own project

    Think about your actual research project (NaV1.7/NaV1.8/KCNQ2/3 binder design). Write a CLAUDE.md that covers:
    - Project purpose and goals
    - Key file locations
    - Domain conventions (nomenclature, units, etc.)
    - Tools and environments you use
    - Safety rules

    You can write it here as a starting point, then save it to your actual project later.

    ### Exercise 2: Create a custom slash command

    In Claude Code, create a custom command for a task you do frequently. For example:

    1. Create `.claude/commands/` directory in this tutorial
    2. Create a file `check-notebook.md` with instructions for checking a notebook is complete and runnable
    3. Test it: `/check-notebook 04-mastering-claude-code/01-claude-code-basics.py`

    ### Exercise 3: Explore MCP servers

    If you have MCP servers configured, try:
    ```
    You: Search PubMed for recent papers on computational design of
         NaV1.7 selective inhibitors
    ```

    Or:
    ```
    You: Search bioRxiv for preprints about de novo protein binder
         design published in the last 3 months
    ```

    ### Exercise 4: Memory practice

    In Claude Code:
    1. Run `/memory` to see what's currently stored
    2. Add a preference: tell Claude Code something about how you like to work
    3. Start a new conversation (`/clear`) and verify the memory persists

    ---

    **Congratulations!** You've completed the Claude Code module. You now know how to:
    - Use Claude Code for reading, editing, searching, and running commands
    - Handle multi-step tasks and debug errors efficiently
    - Customize Claude Code with CLAUDE.md, memory, settings, hooks, and slash commands
    - Extend Claude Code with MCP servers

    **Next module:** [05-claude-api/](../05-claude-api/) -- Using Claude's API directly from Python for automated workflows.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Advanced Claude Code Workflows](02-advanced-workflows.py) | [Module Index](../README.md) | [Next: Setup & Best Practices for Claude Code \u2192](04-setup-and-best-practices.py)
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
    - 2026-03-25: QA pass — removed duplicate MCP Servers section
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
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
    - 2026-03-25: QA pass — removed duplicate MCP Servers section
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

