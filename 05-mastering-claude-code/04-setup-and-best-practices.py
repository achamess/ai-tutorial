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
    # Setup & Best Practices for Claude Code

    **A practical guide to setting up Claude Code for maximum effectiveness**

    **Key references:** [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview) | [Claude Code Settings](https://docs.anthropic.com/en/docs/claude-code/settings) | [Missing Semester Lecture 5: Command-line Environment](https://missing.csail.mit.edu/2020/command-line/)

    ---

    ## Why This Matters

    Claude Code is powerful out of the box, but **how you set it up** determines whether it feels like a brilliant collaborator or a confused intern. The difference between a frustrating session and a productive one usually comes down to:

    1. **Project structure** -- Does Claude know where things are and what conventions you follow?
    2. **Permissions** -- Can Claude do what it needs to without asking you 50 times per session?
    3. **Context management** -- Is Claude working with the right information, or drowning in noise?

    Think of it like setting up a new postdoc in your lab. You wouldn't just hand them a pipette and say "do science." You'd show them where the reagents are, explain your lab's conventions, and tell them what they can and can't do independently. That's what this notebook teaches you to do for Claude Code.

    **By the end of this notebook, you'll have:**
    - A template project structure you can use for every research project
    - A working CLAUDE.md that makes Claude immediately effective
    - Permission settings that balance safety with speed
    - Hooks that automate tedious tasks
    - A multi-computer strategy for home and lab
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Customizing Claude Code](03-customizing-claude-code.py) | [Module Index](../README.md) | [Next: Decomposition and Design \u2192](../06-systems-thinking/01-decomposition-and-design.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - A well-configured Claude Code setup is the difference between a productive AI partner and a frustrating one. Spending 15 minutes on CLAUDE.md, permissions, and hooks saves hours of repeated explanations and permission clicks across every future session.
    > - Permission settings protect your raw data and prevent accidental destructive operations, while still letting Claude work fast on routine tasks like running scripts and editing analysis code.
    > - Hooks automate quality control -- auto-formatting Python files, blocking edits to raw data, and sending notifications -- so you can focus on the science instead of policing Claude's output.
    > - A multi-computer strategy (lab workstation + laptop) with synced CLAUDE.md and settings means consistent Claude Code behavior wherever you work, just like having the same SOPs posted in every bay of your lab.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Your Workspace Setup

    ### Why this matters

    Claude Code operates on **one project directory at a time**. It reads files, writes files, and runs commands *from your project root*. If your project is scattered across folders, Claude gets confused -- just like you would if someone's data files were in five different directories.

    ### The Golden Rule: One Project = One Directory

    Always launch Claude Code from the **root** of your project:

    ```bash
    cd ~/projects/drg-rnaseq-analysis
    claude
    ```

    NOT from your home directory, not from a parent folder with multiple projects. **The directory you launch from is the directory Claude works in.**

    ### The Ideal Project Structure

    Here's what a well-organized project looks like with Claude Code configuration:
    """)
    return


@app.cell
def _():
    # Let's visualize the ideal project folder structure

    project_tree = """
    drg-rnaseq-analysis/             <-- Your project root (launch claude here)
    |
    |-- CLAUDE.md                     <-- Project instructions (THE most important file)
    |
    |-- .claude/                      <-- Claude Code configuration directory
    |   |-- settings.json             <-- Team settings (committed to git)
    |   |-- settings.local.json       <-- Personal settings (gitignored)
    |   |-- rules/                    <-- Modular topic rules
    |   |   |-- python-style.md       <-- Rules for Python files
    |   |   |-- notebook-conventions.md  <-- Rules for notebooks
    |   |-- agents/                   <-- Custom subagents
    |   |   |-- code-reviewer.md      <-- Agent that reviews your scripts
    |   |-- skills/                   <-- Reusable workflows
    |   |   |-- run-deseq2.md         <-- Skill for DESeq2 analysis
    |   |-- hooks/                    <-- Automation scripts
    |   |   |-- format-on-save.sh     <-- Auto-format after edits
    |   |-- mcp.json                  <-- MCP tool integrations
    |
    |-- data/                         <-- Your actual project files
    |   |-- raw/
    |   |-- processed/
    |-- scripts/
    |-- notebooks/
    |-- results/
    |-- requirements.txt
    |-- .gitignore
    """

    print(project_tree)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Configuration Hierarchy

    Claude Code reads configuration from multiple levels. Higher levels override lower ones:

    ```mermaid
    graph TD
        A["Managed Policy<br/>(org admin, highest priority)"] --> B["CLI Flags<br/>(--permission-mode, --model)"]
        B --> C["Local Settings<br/>(.claude/settings.local.json)<br/>Personal, NOT committed"]
        C --> D["Project Settings<br/>(.claude/settings.json)<br/>Team-shared, committed to git"]
        D --> E["User Settings<br/>(~/.claude/settings.json)<br/>Your global defaults"]

        style A fill:#ff6b6b,color:#fff
        style B fill:#ffa07a,color:#fff
        style C fill:#98d8c8,color:#333
        style D fill:#87ceeb,color:#333
        style E fill:#dda0dd,color:#333
    ```

    **Practical implication:** Your team's `.claude/settings.json` sets baseline rules. Your personal `.claude/settings.local.json` can override them for your own workflow (e.g., you prefer a different editor mode). Org admins can lock things down with managed policies that nobody can override.
    """)
    return


@app.cell
def _():
    # Let's see what config files exist on YOUR system
    import os
    from pathlib import Path

    config_locations = {
        "User settings (global)": Path.home() / ".claude" / "settings.json",
        "User CLAUDE.md": Path.home() / ".claude" / "CLAUDE.md",
        "Project CLAUDE.md": Path.cwd() / "CLAUDE.md",
        "Project settings": Path.cwd() / ".claude" / "settings.json",
        "Local settings": Path.cwd() / ".claude" / "settings.local.json",
        "MCP config": Path.cwd() / ".claude" / "mcp.json",
    }

    print("Configuration file status:")
    print("=" * 60)
    for name, path in config_locations.items():
        exists = "EXISTS" if path.exists() else "not found"
        print(f"  {name:30s} {exists}")
        print(f"    {path}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. CLAUDE.md -- Your Project's Brain

    ### Why this matters

    CLAUDE.md is **the single most impactful thing you can do** to improve Claude Code's performance. Without it, Claude has to guess your conventions, your project structure, your preferences. With it, Claude knows exactly how you work.

    Think of CLAUDE.md as a lab protocol: concise, specific, and written for someone who's smart but doesn't know your particular setup.

    ### What to Include

    | Category | Examples | Why |
    |----------|----------|-----|
    | **Build/run commands** | `pip install -r requirements.txt`, `python -m pytest` | Claude needs to know how to run your code |
    | **Code style** | "Use type hints", "Prefer pathlib over os.path" | Prevents constant style corrections |
    | **Project conventions** | "Data files go in data/processed/" | Keeps things organized |
    | **Known gotchas** | "The calcium imaging data uses 1-indexed frames" | Prevents bugs Claude can't discover by reading code |
    | **Key dependencies** | "We use scanpy 1.10+ for single-cell analysis" | Prevents version conflicts |

    ### What NOT to Include

    | Don't Include | Why Not |
    |---------------|--------|
    | Full API documentation | Claude can read the actual source code |
    | Obvious language features | Claude already knows Python |
    | Entire file listings | Claude can explore the directory |
    | Long tutorials or explanations | Keep it directive, not educational |

    ### The 200-Line Rule

    **Keep CLAUDE.md under 200 lines.** This is loaded into context on every conversation. If it's too long:
    - Claude spends context window on instructions instead of your actual task
    - Important rules get buried among less important ones
    - Performance degrades

    If you need more than 200 lines, **split into `.claude/rules/` files** (covered below).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The @import Syntax

    CLAUDE.md supports importing other files to keep things modular:

    ```markdown
    # My Project

    ## Build commands
    pip install -r requirements.txt
    python -m pytest tests/

    @import docs/coding-standards.md
    @import docs/data-dictionary.md
    ```

    Imported files are pulled into context when needed. This keeps your main CLAUDE.md lean while making additional documentation available.

    ### Path-Specific Rules with `.claude/rules/`

    For rules that only apply to certain files, create markdown files in `.claude/rules/` with YAML frontmatter:

    ```markdown
    ---
    globs: "scripts/*.py"
    ---

    # Python Script Conventions

    - Always include a docstring at the top of each script
    - Use argparse for command-line arguments
    - Log to stderr, output data to stdout
    - Include if __name__ == "__main__": guard
    ```

    ```markdown
    ---
    globs: "notebooks/*.py"
    ---

    # Notebook Conventions

    - First cell should be markdown with title and description
    - Second cell should be imports
    - Use seaborn for all plots
    - Include figure titles and axis labels on every plot
    ```

    These rules are **only loaded when Claude is working on matching files**, keeping context clean.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Worked Example: CLAUDE.md for a Binder Screening Project
    """)
    return


@app.cell
def _():
    # A realistic CLAUDE.md for a pain biology research project

    example_claude_md = '''
    # Nav1.7 Binder Screening Analysis

    ## Project overview
    Analysis pipeline for high-throughput screening of Nav1.7 channel binders.
    Calcium imaging data from DRG neurons treated with candidate compounds.

    ## Setup
    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

    ## Run tests
    ```bash
    python -m pytest tests/ -v
    ```

    ## Code style
    - Python 3.11+, use type hints on all function signatures
    - Use pathlib for file paths, never os.path
    - Prefer pandas for tabular data, numpy for arrays
    - All plots: seaborn style, include title + axis labels, save as SVG

    ## Data conventions
    - Raw imaging data: data/raw/ (TIF stacks, DO NOT modify)
    - Processed traces: data/processed/ (CSV, one file per plate)
    - Plate maps: data/plate_maps/ (CSV with compound_id, concentration, well)
    - Results: results/ (figures in results/figures/, tables in results/tables/)

    ## Key gotchas
    - Calcium traces are deltaF/F0, baseline is frames 1-20 (1-indexed)
    - Well IDs use the format "A01" not "A1" -- always zero-pad
    - Plate 7 had a temperature excursion -- exclude from analysis
    - Concentration is in MOLAR (not nM) in the raw plate maps

    ## Analysis pipeline order
    1. scripts/01_extract_traces.py -- TIF to CSV
    2. scripts/02_normalize.py -- baseline correction
    3. scripts/03_fit_dose_response.py -- Hill equation fits
    4. scripts/04_hit_calling.py -- identify active compounds
    5. notebooks/05_summary_figures.py -- publication figures

    @import docs/compound-library.md
    '''

    print(f"Example CLAUDE.md ({len(example_claude_md.strip().splitlines())} lines):")
    print("=" * 60)
    print(example_claude_md)
    return (example_claude_md,)


@app.cell
def _(example_claude_md):
    # Count lines to verify we're under the 200-line guideline
    line_count = len(example_claude_md.strip().splitlines())
    print(f"Line count: {line_count}")
    print(f"Under 200-line limit: {'Yes' if line_count < 200 else 'NO -- needs trimming!'}")
    print(f"\nThis leaves {200 - line_count} lines of headroom for future additions.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Settings & Configuration

    ### Why this matters

    Settings control Claude's behavior *before* it starts working. Getting these right means fewer interruptions, consistent behavior across your team, and safer defaults.

    ### The 4 Configuration Scopes

    | Scope | File | Committed to Git? | Who Sets It |
    |-------|------|-------------------|-------------|
    | **Managed** | Set by org admin via Anthropic console | N/A | Organization admin |
    | **Project** | `.claude/settings.json` | **Yes** | Team |
    | **Local** | `.claude/settings.local.json` | **No** (gitignored) | You personally |
    | **User** | `~/.claude/settings.json` | N/A | You (all projects) |

    **Priority order:** Managed > CLI flags > Local > Project > User

    ### What to Commit vs. What to Gitignore

    ```
    # In your .gitignore:
    .claude/settings.local.json    # Personal preferences
    .claude/mcp.json               # May contain local paths

    # DO commit:
    .claude/settings.json          # Team settings
    .claude/rules/                 # Shared conventions
    .claude/agents/                # Shared agents
    .claude/hooks/                 # Shared automation
    CLAUDE.md                      # Project brain
    ```
    """)
    return


@app.cell
def _():
    import json

    # Example: A practical .claude/settings.json for a research project
    project_settings = {
        "permissions": {
            "allow": [
                "Read(*)",           # Can read any file
                "Edit(*)",           # Can edit any file
                "Bash(python *)",    # Can run Python scripts
                "Bash(pytest *)",    # Can run tests
                "Bash(pip install *)",  # Can install packages
            ],
            "deny": [
                "Bash(rm -rf *)",    # Never delete recursively
                "Bash(git push *)",  # Don't push without asking
            ]
        },
        "env": {
            "PYTHONDONTWRITEBYTECODE": "1"  # Keep things clean
        }
    }

    print("Example .claude/settings.json (team settings):")
    print(json.dumps(project_settings, indent=2))
    return (json,)


@app.cell
def _(json):
    # Example: Personal overrides in .claude/settings.local.json
    local_settings = {
        "defaultMode": "auto",  # You trust Claude enough for auto mode
        "env": {
            "ANTHROPIC_API_KEY": "$ANTHROPIC_API_KEY"  # Reference env var, don't hardcode!
        }
    }

    print("Example .claude/settings.local.json (personal, gitignored):")
    print(json.dumps(local_settings, indent=2))
    print("\nNOTE: Never put actual API keys in settings files!")
    print("Use environment variables or your shell profile instead.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Key Settings Reference

    | Setting | What It Does | Example |
    |---------|-------------|--------|
    | `permissions.allow` | Tools/commands Claude can use without asking | `["Bash(python *)"]` |
    | `permissions.deny` | Tools/commands Claude must never use | `["Bash(rm -rf *)"]` |
    | `defaultMode` | Starting permission mode | `"default"`, `"auto"`, `"plan"` |
    | `env` | Environment variables to set | `{"VAR": "value"}` |
    | `model` | Override the default model | `"claude-sonnet-4-20250514"` |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. The Permission Model

    ### Why this matters

    Permissions balance **safety** with **speed**. Too restrictive and you're clicking "approve" every 10 seconds. Too loose and Claude might overwrite your data. Getting this right is crucial for productive sessions.

    ### Permission Modes

    | Mode | What Claude Can Do | You Approve | Best For |
    |------|-------------------|-------------|----------|
    | **`default`** | Read files freely | Edits, bash commands, MCP tools | Starting out, unfamiliar projects |
    | **`acceptEdits`** | Read + edit files freely | Bash commands, MCP tools | Trusted editing, careful execution |
    | **`plan`** | Read files, make plans | Everything else (great for learning) | Understanding what Claude *would* do |
    | **`auto`** | Most operations freely | Only things flagged by safety classifier | Trusted projects, experienced users |
    | **`dontAsk`** | Everything, never asks | Nothing | CI/CD pipelines, automated workflows |
    | **`bypassPermissions`** | Everything including dangerous ops | Nothing | **Only in sandboxed environments!** |

    ### Recommended Progression

    ```mermaid
    graph LR
        A["Week 1-2<br/>default mode<br/>Learn the tool"] --> B["Week 3-4<br/>acceptEdits mode<br/>Trust file edits"]
        B --> C["Month 2+<br/>auto mode<br/>Full speed"]
        C --> D["CI/CD only<br/>dontAsk mode<br/>Automated pipelines"]

        style A fill:#98d8c8,color:#333
        style B fill:#87ceeb,color:#333
        style C fill:#ffa07a,color:#333
        style D fill:#ff6b6b,color:#fff
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Permission Rule Syntax

    Permission rules use a `Tool(pattern)` syntax:

    ```json
    {
      "permissions": {
        "allow": [
          "Read(*)",               // Read any file
          "Edit(scripts/*.py)",     // Edit Python scripts
          "Bash(python *)",         // Run python commands
          "Bash(git status)",       // Check git status
          "Bash(git diff *)",       // View diffs
          "Bash(git add *)",        // Stage files
          "Bash(git commit *)"      // Commit changes
        ],
        "deny": [
          "Edit(data/raw/*)",       // Protect raw data!
          "Bash(git push *)",       // No pushing without review
          "Bash(rm *)",             // No deleting files
          "Bash(curl *)",           // No network requests
        ]
      }
    }
    ```

    ### Auto Mode Natural Language Rules

    In Auto Mode, you can also define rules in plain English. Claude's safety classifier evaluates these dynamically:

    ```json
    {
      "permissions": {
        "allow": [
          "Running Python scripts in the scripts/ directory",
          "Installing packages listed in requirements.txt",
          "Creating and editing files in results/"
        ],
        "deny": [
          "Modifying any file in data/raw/",
          "Pushing to remote git repositories",
          "Accessing the network except for pip install"
        ]
      }
    }
    ```

    This is a newer feature and is particularly useful when glob patterns can't capture the nuance you need.
    """)
    return


@app.cell
def _():
    # Decision helper: which permission mode should you use?

    scenarios = [
        ("First time using Claude Code",             "default",      "Learn what Claude does before trusting it"),
        ("Editing a familiar analysis script",        "acceptEdits",  "Trust edits, review bash commands"),
        ("Exploring a new dataset",                   "plan",         "See what Claude would do before doing it"),
        ("Refactoring your own well-tested code",     "auto",         "You know the codebase, trust the process"),
        ("Running in a CI/CD pipeline",               "dontAsk",      "No human in the loop"),
        ("Writing analysis for a grant deadline",     "auto",         "Speed matters, trusted project"),
        ("Working with sensitive patient data",       "default",      "Extra caution with protected data"),
        ("Quick one-off data formatting task",        "auto",         "Low stakes, want it done fast"),
    ]

    print(f"{'Scenario':<45} {'Mode':<15} {'Reasoning'}")
    print("=" * 110)
    for scenario, mode, reason in scenarios:
        print(f"{scenario:<45} {mode:<15} {reason}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Decision point: Which permission mode for which situation**
    >
    > | Mode | What Claude can do without asking | Best for | Risk level |
    > |------|----------------------------------|----------|------------|
    > | **`default`** | Read files, search | First-time use, unfamiliar projects | Lowest -- you approve everything |
    > | **`plan`** | Read files, search | Complex tasks where you want to review the plan | Low -- see the plan before execution |
    > | **`acceptEdits`** | Read, search, edit files | Familiar projects, trusted code changes | Medium -- edits happen without approval |
    > | **`auto`** | Everything except dangerous operations | Well-understood codebases, repetitive tasks | Higher -- less oversight |
    > | **`--dangerously-skip-permissions`** | Everything, no restrictions | CI/CD pipelines, sandboxed environments only | Highest -- no safety net |

    > **Warning:** Never use `--dangerously-skip-permissions` outside of sandboxed environments (Docker containers, CI/CD, disposable VMs). In your normal development environment, a permission bypass means Claude Code could delete files, overwrite data, or run arbitrary commands without your review. Even experienced users should keep at least `default` mode for projects containing irreplaceable data.

    > **Tip:** Practice progressive trust -- start with `default` mode on every new project. After a few sessions where you've seen what Claude Code does and approved its patterns, move to `acceptEdits`. Only move to `auto` for projects where you have git as a safety net and understand the codebase well. This mirrors how you'd onboard a new lab member: supervised at first, then increasingly independent.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Hooks -- Automation That Just Works

    ### Why this matters

    Hooks let you run scripts automatically at specific points in Claude's workflow. Instead of telling Claude "please format that file" after every edit, a hook does it automatically. Instead of hoping Claude doesn't touch your raw data, a hook blocks it.

    Think of hooks like lab equipment interlocks -- they enforce rules mechanically, not through trust.

    ### When Hooks Fire

    ```mermaid
    sequenceDiagram
        participant You
        participant Claude
        participant Hook
        participant Tool

        You->>Claude: "Fix the normalize script"
        Note over Hook: PreToolUse fires
        Hook-->>Claude: (can block or modify)
        Claude->>Tool: Edit(scripts/normalize.py)
        Tool-->>Claude: File edited
        Note over Hook: PostToolUse fires
        Hook-->>Claude: (can auto-format, validate)
        Note over Hook: Notification hook fires
        Hook-->>You: Desktop notification
    ```

    ### Hook Types

    | Hook | When It Fires | Use For |
    |------|--------------|--------|
    | **PreToolUse** | Before Claude uses a tool | Block dangerous operations, validate inputs |
    | **PostToolUse** | After Claude uses a tool | Auto-format, run linters, log actions |
    | **Notification** | When Claude needs your attention | Desktop alerts, sound notifications |
    | **Stop** | When Claude finishes a task | Cleanup, final validation |
    | **SubagentStop** | When a subagent finishes | Process subagent results |
    | **PreCompact** | Before context compaction | Re-inject critical information |
    """)
    return


@app.cell
def _(json):
    # Example: Hook configuration in .claude/settings.json
    hooks_config = {'hooks': {'PostToolUse': [{'matcher': 'Edit', 'command': 'black --quiet $CLAUDE_FILE_PATH', 'description': 'Auto-format Python files after editing'}], 'PreToolUse': [{'matcher': 'Edit', 'command': "echo $CLAUDE_FILE_PATH | grep -q 'data/raw/' && echo 'BLOCKED: Cannot edit raw data files' && exit 1 || exit 0", 'description': 'Protect raw data files from modification'}], 'Notification': [{'command': 'osascript -e \'display notification "Claude needs your input" with title "Claude Code"\'', 'description': 'macOS notification when Claude needs attention'}], 'PreCompact': [{'command': 'cat .claude/context-reminder.md', 'description': 'Re-inject critical context before compaction'}]}}
    print('Example hooks configuration:')
    print(json.dumps(hooks_config, indent=2))
    return


@app.cell
def _():
    # Example: A simple hook script (.claude/hooks/format-on-save.sh)

    hook_script = '''#!/bin/bash
    # .claude/hooks/format-on-save.sh
    # Auto-format Python files after Claude edits them
    #
    # Environment variables available to hooks:
    #   $CLAUDE_FILE_PATH  - The file that was edited
    #   $CLAUDE_TOOL_NAME  - The tool that was used (Edit, Write, etc.)

    # Only format Python files
    if [[ "$CLAUDE_FILE_PATH" == *.py ]]; then
        # Run black formatter (quiet mode)
        black --quiet "$CLAUDE_FILE_PATH" 2>/dev/null
    
        # Run isort for import sorting
        isort --quiet "$CLAUDE_FILE_PATH" 2>/dev/null
    fi
    '''

    print(hook_script)
    print("---")
    print("Remember to make hook scripts executable: chmod +x .claude/hooks/format-on-save.sh")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Subagents -- Delegating Work

    ### Why this matters

    Your main Claude Code conversation has a finite context window. Once it fills up, Claude starts forgetting things and performance degrades. Subagents let you **delegate** exploration and analysis to a separate context, keeping your main conversation clean.

    It's like sending a grad student to do a literature search -- they come back with a summary, and you don't have to read every paper yourself.

    ### Built-in Agents

    | Agent | What It Does | When to Use |
    |-------|-------------|-------------|
    | **Explore** | Reads files and searches code, no edits | "What does this codebase do?" |
    | **Plan** | Analyzes and creates an action plan | "How should I refactor this?" |
    | **General** | Full capabilities in isolated context | Complex subtasks |

    Use them with the `/agents` command or by asking Claude to delegate:

    ```
    Use the explore agent to understand how the calcium imaging pipeline works,
    then summarize what you found.
    ```

    ### Creating Custom Agents

    Place `.md` files in `.claude/agents/` to create reusable agents:
    """)
    return


@app.cell
def _():
    # Example: A custom code reviewer agent

    reviewer_agent = '''---
    tools:
      - Read
      - Grep
      - Glob
      - Bash(python *)
    model: claude-sonnet-4-20250514
    memory: true
    isolation: worktree
    ---

    # Code Reviewer Agent

    You are a code reviewer for pain biology research scripts.

    ## Review checklist
    1. **Correctness**: Are calculations right? Are units consistent?
    2. **Data safety**: Is raw data ever modified? Are there proper backups?
    3. **Reproducibility**: Are random seeds set? Are file paths relative?
    4. **Statistics**: Are statistical tests appropriate? Multiple comparison corrections?
    5. **Plotting**: Do all figures have titles, axis labels, and legends?

    ## Output format
    Provide a structured review with:
    - PASS / NEEDS CHANGES / CRITICAL for each category
    - Specific line numbers for any issues
    - Suggested fixes
    '''

    print("Example agent file (.claude/agents/code-reviewer.md):")
    print("=" * 55)
    print(reviewer_agent)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Agent Frontmatter Options

    | Option | Values | What It Does |
    |--------|--------|-------------|
    | `tools` | List of tool names | Restrict which tools the agent can use |
    | `model` | Model ID string | Use a different model (e.g., Sonnet for speed) |
    | `memory` | `true`/`false` | Agent remembers across invocations |
    | `isolation` | `worktree`, `none` | `worktree` = agent works in a git worktree (can't affect your files) |

    ### When to Use Subagents vs. Doing It Yourself

    | Situation | Approach | Why |
    |-----------|----------|-----|
    | Quick file edit | Main context | Not worth the overhead of spawning an agent |
    | Exploring an unfamiliar codebase | **Explore agent** | Keeps exploration out of your main context |
    | Writing a complex analysis | Main context | You want to interact and iterate |
    | Reviewing code changes | **Custom agent** | Consistent checklist, isolated context |
    | Generating boilerplate for 5 scripts | **General agent** | Repetitive work, delegate it |
    | Planning a major refactor | **Plan agent** | Get the plan first, then execute in main context |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 7. MCP Servers -- Extending Claude's Reach

    ### Why this matters

    Out of the box, Claude Code can read files, edit code, and run commands. But what if you want it to query a database, search your lab notebook in Notion, or interact with GitHub issues? **MCP (Model Context Protocol) servers** add these capabilities.

    Think of MCP servers as lab instruments that Claude can operate -- each one gives Claude a new capability.

    ### How MCP Works

    ```mermaid
    graph LR
        A[Claude Code] -->|uses tools from| B[MCP Server: GitHub]
        A -->|uses tools from| C[MCP Server: PostgreSQL]
        A -->|uses tools from| D[MCP Server: Notion]
        A -->|uses tools from| E[MCP Server: Slack]

        B -->|reads/writes| F[(GitHub API)]
        C -->|queries| G[(Lab Database)]
        D -->|reads| H[(Lab Notebook)]
        E -->|posts| I[(Lab Channel)]

        style A fill:#87ceeb,color:#333
    ```

    ### Configuration

    MCP servers are configured in `.claude/mcp.json`:
    """)
    return


@app.cell
def _(json):
    mcp_config = {'mcpServers': {'github': {'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-github'], 'env': {'GITHUB_TOKEN': '$GITHUB_TOKEN'}}, 'postgres': {'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-postgres'], 'env': {'DATABASE_URL': '$LAB_DB_URL'}}, 'filesystem': {'command': 'npx', 'args': ['-y', '@modelcontextprotocol/server-filesystem', '/Users/alex/shared-lab-data']}}}
    print('Example .claude/mcp.json:')
    print(json.dumps(mcp_config, indent=2))
    print('\nNote: Use environment variable references ($VAR) for secrets, not actual values!')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Useful MCP Servers for Research

    | Server | What It Does | Use Case |
    |--------|-------------|----------|
    | `server-github` | GitHub issues, PRs, repos | Track analysis code, collaborate |
    | `server-postgres` / `server-sqlite` | Query databases | Lab databases, experiment logs |
    | `server-filesystem` | Access files outside project | Shared lab data folders |
    | `server-notion` | Read/write Notion pages | Lab notebook integration |
    | `server-slack` | Send/read Slack messages | Get notifications, share results |
    | `server-fetch` | Make HTTP requests | Download data, query APIs |

    ### Adding a Server

    The easiest way is to use the Claude Code command:

    ```bash
    claude mcp add github npx -y @modelcontextprotocol/server-github
    ```

    This automatically adds the entry to `.claude/mcp.json`. You can also edit the file manually.

    Learn more at the [MCP documentation](https://modelcontextprotocol.io/).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 8. Working Across Multiple Computers

    ### Why this matters

    If you work on a Mac at home and a Mac in the lab (like most researchers), you need a strategy for keeping Claude Code's configuration in sync. The good news: most of it syncs via git. The bad news: some things don't.

    ### What Syncs vs. What Doesn't

    | Thing | Syncs via Git? | Strategy |
    |-------|---------------|----------|
    | `CLAUDE.md` | **Yes** | Just commit it |
    | `.claude/settings.json` | **Yes** | Commit team settings |
    | `.claude/rules/` | **Yes** | Commit all rules |
    | `.claude/agents/` | **Yes** | Commit all agents |
    | `.claude/hooks/` | **Yes** | Commit all hooks |
    | `.claude/settings.local.json` | **No** | Recreate per machine, or use dotfiles repo |
    | `.claude/mcp.json` | **Maybe** | Commit if paths are portable, gitignore if not |
    | `~/.claude/settings.json` | **No** | Use a dotfiles repo or setup script |
    | Claude's memory (`/memory`) | **No** | Stored locally per machine |
    | Conversation history | **No** | Ephemeral by design |
    """)
    return


@app.cell
def _():
    # A setup script you could run on a new machine

    setup_script = '''#!/bin/bash
    # setup-claude.sh -- Run this on each new computer
    # Usage: ./setup-claude.sh

    echo "Setting up Claude Code environment..."

    # 1. Create user-level config directory
    mkdir -p ~/.claude

    # 2. Set up global settings (your personal defaults)
    cat > ~/.claude/settings.json << 'EOF'
    {
      "defaultMode": "auto",
      "env": {
        "PYTHONDONTWRITEBYTECODE": "1"
      }
    }
    EOF

    # 3. Ensure API key is set (should be in your .zshrc)
    if [ -z "$ANTHROPIC_API_KEY" ]; then
        echo "WARNING: ANTHROPIC_API_KEY not set!"
        echo "Add this to your ~/.zshrc:"
        echo '  export ANTHROPIC_API_KEY="your-key-here"'
    else
        echo "API key found."
    fi

    # 4. Install common MCP servers
    echo "Installing MCP servers..."
    npm install -g @modelcontextprotocol/server-github 2>/dev/null

    echo "Done! Claude Code is ready to use."
    '''

    print("Multi-computer setup script:")
    print(setup_script)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Remote and Cloud Sessions

    Claude Code also supports **remote sessions** where the Claude Code agent runs in the cloud or on a remote machine:

    - **Claude Desktop app** can connect to a remote Claude Code session -- useful when you want the desktop UI but the code lives on a lab server
    - **Cloud sessions** run Claude Code on Anthropic's infrastructure -- useful for CI/CD or when you don't want to leave your laptop running
    - **SSH connections** let you run Claude Code on a remote machine and interact from your local terminal

    For most research workflows, running Claude Code locally is simplest. Remote sessions become valuable when:
    - You need to access data that lives on a lab server
    - You want to run long analyses without keeping your laptop open
    - You're working from a low-powered machine but need heavy computation
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 9. Best Practices (Do This)

    ### Why this matters

    These are hard-won lessons from extensive Claude Code usage. Following them will save you hours of frustration.

    ### The Essential Practices

    **1. Start every project with CLAUDE.md**

    Before you even start coding, run `/init` or create a CLAUDE.md manually. It takes 5 minutes and saves hours.

    ```bash
    cd ~/projects/new-analysis
    claude
    > /init
    ```

    **2. Use `/clear` between unrelated tasks**

    Context from a previous task can confuse Claude on the next one. If you switch from "fix the plotting script" to "write a new data loader," clear first.

    ```
    > /clear
    > Now let's work on the data loader...
    ```

    **3. Monitor context usage with `/cost`**

    When performance degrades, check context usage. If you're above 80%, use `/compact` to compress the conversation or `/clear` to start fresh.

    ```
    > /cost
    Context: 87% full | Tokens: 174,000 / 200,000 | Cost: $2.34
    ```

    **4. Use subagents for exploration**

    Don't waste your main context on "go read all the files in this directory and tell me what they do." Delegate that to the Explore agent.

    **5. Commit `.claude/` to git** (except `settings.local.json`)

    Your team benefits from shared settings, agents, hooks, and rules.

    **6. Use hooks for deterministic behavior**

    If something should *always* happen (formatting, validation), don't rely on Claude remembering. Use a hook.

    **7. Start restrictive, loosen as you trust**

    Begin with `default` mode and explicit permission rules. As you get comfortable, move to `acceptEdits` then `auto`.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 10. Anti-Patterns (Don't Do This)

    ### Why this matters

    These are the most common mistakes that lead to wasted time, lost work, or poor results.
    """)
    return


@app.cell
def _():
    # Anti-patterns and their fixes

    anti_patterns = [
        {
            "anti_pattern": "Overstuffing CLAUDE.md (>200 lines)",
            "why_bad": "Wastes context, important rules get buried",
            "fix": "Split into .claude/rules/ with path-specific targeting",
        },
        {
            "anti_pattern": "Correcting Claude 3+ times on the same thing",
            "why_bad": "Context pollution, Claude gets confused by contradictions",
            "fix": "Use /clear and write a better prompt. Add rule to CLAUDE.md",
        },
        {
            "anti_pattern": "Using bypassPermissions outside a sandbox",
            "why_bad": "Claude could delete files, run dangerous commands",
            "fix": "Use 'auto' mode with deny rules instead",
        },
        {
            "anti_pattern": "Ignoring context limits (>95% full)",
            "why_bad": "Degraded performance, missed instructions, hallucinations",
            "fix": "Use /cost to monitor, /compact to compress, /clear to reset",
        },
        {
            "anti_pattern": "Running open-ended exploration in main context",
            "why_bad": "Fills context with file contents you may not need",
            "fix": "Use the Explore subagent for discovery tasks",
        },
        {
            "anti_pattern": "Putting secrets in settings files",
            "why_bad": "Secrets end up in git history, exposed to collaborators",
            "fix": "Use environment variables ($VAR syntax in settings)",
        },
        {
            "anti_pattern": "Conflicting rules across multiple CLAUDE.md files",
            "why_bad": "Claude picks one arbitrarily, unpredictable behavior",
            "fix": "One canonical CLAUDE.md at project root, use rules/ for specifics",
        },
    ]

    for i, ap in enumerate(anti_patterns, 1):
        print(f"Anti-pattern #{i}: {ap['anti_pattern']}")
        print(f"  Why it's bad: {ap['why_bad']}")
        print(f"  Fix: {ap['fix']}")
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### The Correction Trap (Most Common Mistake)

    This deserves special emphasis. When Claude does something wrong:

    ```
    Attempt 1: "No, use seaborn not matplotlib"
    Attempt 2: "I said seaborn, and make the title bigger"
    Attempt 3: "The colors are still wrong and you're using plt.show()"
    ```

    After 3 corrections, you now have a conversation full of contradictory context. Claude is trying to satisfy all your feedback simultaneously and getting confused.

    **Instead:**

    ```
    > /clear
    > Create a figure using seaborn (not matplotlib directly).
    > Use the 'colorblind' palette, 14pt title, and save as SVG.
    > Here's exactly what I want: [clear, complete specification]
    ```

    One clear prompt beats three corrections every time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 11. Latest Features (as of March 2026)

    ### Why this matters

    Claude Code evolves quickly. These features are recent and powerful but not always well-known yet.

    ### Feature Overview

    | Feature | What It Does | Status |
    |---------|-------------|--------|
    | **Auto Mode classifier** | Natural language permission rules evaluated by AI | Stable |
    | **Path-specific rules** | `.claude/rules/` with YAML frontmatter glob targeting | Stable |
    | **Subagent isolation** | Agents work in separate git worktrees | Stable |
    | **Persistent subagent memory** | Agents remember context across invocations | Stable |
    | **Cloud sessions** | Run Claude Code on Anthropic infrastructure | Stable |
    | **Background tasks** | Claude works while you do other things | Stable |
    | **Scheduled tasks** | Trigger Claude on a schedule (cron-like) | Stable |
    | **Channels** | Webhook/CI integration for triggering Claude | Stable |
    | **Desktop app + remote sessions** | GUI with remote backend | Stable |
    | **Extended thinking** | Claude shows reasoning, with configurable effort | Stable |

    ### Auto Mode Classifier

    Instead of just glob-based permission rules, you can now write rules in natural language:

    ```json
    {
      "permissions": {
        "allow": [
          "Running any Python analysis script in the scripts/ directory",
          "Installing packages from PyPI that are related to data analysis"
        ],
        "deny": [
          "Any operation that would modify files in the data/raw/ directory",
          "Network requests other than pip install"
        ]
      }
    }
    ```

    Claude's safety classifier evaluates these in context, which is more flexible than pattern matching.

    ### Background Tasks

    You can now start a task and let Claude work on it in the background:

    ```bash
    claude --background "Refactor all scripts in scripts/ to use pathlib instead of os.path"
    ```

    Claude works asynchronously and notifies you when done. Great for large refactoring tasks while you focus on other work.

    ### Scheduled Tasks

    Set up recurring tasks:

    ```bash
    claude schedule "Every Monday at 9am, review any new scripts added last week and check for common issues"
    ```

    ### Channels

    Channels let external systems trigger Claude Code. Use cases:
    - CI/CD pipeline fails -> Claude investigates and proposes a fix
    - New GitHub issue -> Claude creates a draft PR
    - Webhook from lab instrument -> Claude processes new data

    ### Extended Thinking with Effort Levels

    Claude can now show its reasoning process. You can control how deeply it thinks:

    - **Low effort**: Quick responses, minimal reasoning (good for simple edits)
    - **Medium effort**: Balanced reasoning (default)
    - **High effort**: Deep analysis before responding (complex debugging, architecture decisions)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 12. Quick Reference

    ### Configuration Files

    | File | Location | Commit to Git? | Purpose |
    |------|----------|---------------|--------|
    | `CLAUDE.md` | Project root | **Yes** | Project instructions, conventions, gotchas |
    | `.claude/settings.json` | Project `.claude/` | **Yes** | Team permission rules, shared env vars |
    | `.claude/settings.local.json` | Project `.claude/` | **No** | Personal mode, local env vars |
    | `.claude/rules/*.md` | Project `.claude/rules/` | **Yes** | Path-specific rules with YAML frontmatter |
    | `.claude/agents/*.md` | Project `.claude/agents/` | **Yes** | Custom subagent definitions |
    | `.claude/skills/*.md` | Project `.claude/skills/` | **Yes** | Reusable workflow templates |
    | `.claude/hooks/*.sh` | Project `.claude/hooks/` | **Yes** | Automation scripts |
    | `.claude/mcp.json` | Project `.claude/` | **Maybe** | MCP server configuration |
    | `~/.claude/settings.json` | Home directory | N/A | Global user defaults |
    | `~/.claude/CLAUDE.md` | Home directory | N/A | Global instructions for all projects |

    ### Key Slash Commands

    | Command | What It Does | When to Use |
    |---------|-------------|-------------|
    | `/clear` | Reset conversation context | Between unrelated tasks, after confusion |
    | `/compact` | Compress conversation to save context | When context is getting full (>80%) |
    | `/cost` | Show context usage, token count, spend | Monitor session health |
    | `/memory` | View/edit persistent memory | Store long-term preferences |
    | `/init` | Initialize CLAUDE.md for current project | Starting a new project |
    | `/agents` | List and invoke subagents | Delegating tasks |
    | `/model` | Switch the active model | Need speed (Sonnet) vs. capability (Opus) |
    | `/permissions` | View/modify permission settings | Adjusting safety boundaries |
    | `/config` | View current configuration | Debugging settings issues |
    """)
    return


@app.cell
def _():
    # Quick reference: generate a checklist for setting up a new project

    checklist = """
    NEW PROJECT SETUP CHECKLIST
    ===========================

    [ ] 1. Create project directory and initialize git
          $ mkdir ~/projects/my-analysis && cd ~/projects/my-analysis
          $ git init

    [ ] 2. Create CLAUDE.md with project overview, commands, and conventions
          $ claude
          > /init

    [ ] 3. Create .claude/ directory structure
          $ mkdir -p .claude/rules .claude/agents .claude/hooks

    [ ] 4. Add team settings (.claude/settings.json)
          - Permission allow/deny rules
          - Shared environment variables

    [ ] 5. Add personal settings (.claude/settings.local.json)
          - Your preferred mode (default/auto)
          - Local environment overrides

    [ ] 6. Update .gitignore
          .claude/settings.local.json
          .claude/mcp.json  (if it contains local paths)

    [ ] 7. Add path-specific rules if needed (.claude/rules/)

    [ ] 8. Set up hooks for auto-formatting (.claude/hooks/)

    [ ] 9. Commit .claude/ directory to git
          $ git add CLAUDE.md .claude/settings.json .claude/rules/ .claude/agents/ .claude/hooks/
          $ git commit -m "Add Claude Code configuration"

    [ ] 10. Test: launch claude and verify it reads your CLAUDE.md
           $ claude
           > What do you know about this project?
    """

    print(checklist)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Further Reading

    **Anthropic Claude Code Documentation:**
    - [Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview) -- Installation, capabilities, and getting started.
    - [Claude Code Configuration / Settings](https://docs.anthropic.com/en/docs/claude-code/settings) -- Permissions, allowed/denied tools, and project vs. user settings.
    - [CLAUDE.md and Memory](https://docs.anthropic.com/en/docs/claude-code/memory) -- How project instructions and persistent memory work.
    - [Claude Code Hooks](https://docs.anthropic.com/en/docs/claude-code/hooks) -- Pre/post tool-use automation (formatting, validation, notifications).
    - [Claude Code Sub-agents](https://docs.anthropic.com/en/docs/claude-code/sub-agents) -- Delegating work to sub-agents for exploration and analysis.
    - [Claude Code Security & Permissions](https://docs.anthropic.com/en/docs/claude-code/security) -- Permission model details and security considerations.
    - [Claude Code GitHub Repository](https://github.com/anthropics/claude-code) -- Source, issues, and release notes.

    **MCP (Model Context Protocol):**
    - [MCP Specification](https://spec.modelcontextprotocol.io/) -- The open protocol powering Claude Code's extensibility.
    - [MCP Server Directory](https://github.com/modelcontextprotocol/servers) -- Community-maintained list of available MCP servers.

    **Shell and Environment:**
    - [Missing Semester Lecture 5: Command-line Environment](https://missing.csail.mit.edu/2020/command-line/) -- Shell configuration, environment variables, tmux, and SSH -- relevant for setting up Claude Code on remote machines.

    **Local reference:** [resources/references/anthropic-claude-code-overview.md](../resources/references/anthropic-claude-code-overview.md) -- Local copy of Claude Code documentation for offline use.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Customizing Claude Code](03-customizing-claude-code.py) | [Module Index](../README.md) | [Next: Decomposition and Design \u2192](../06-systems-thinking/01-decomposition-and-design.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Summary

    Setting up Claude Code well is like setting up a new lab: a few hours of organization saves months of frustration. Here's the hierarchy of impact:

    1. **CLAUDE.md** -- The single highest-impact thing you can do. 5 minutes of setup, permanent benefit.
    2. **Permissions** -- Get these right early. Start with `default`, graduate to `auto`.
    3. **Hooks** -- Automate the things you'd otherwise nag Claude about.
    4. **Subagents** -- Keep your main context clean by delegating exploration.
    5. **MCP servers** -- Extend Claude's reach when you need external integrations.

    The most important habit: **when something goes wrong, improve your setup** (CLAUDE.md, rules, hooks) rather than just fixing it in the moment. That's how you build a system that gets better over time.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log
    - 2026-03-25: Created notebook with comprehensive Claude Code setup guide and best practices
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: QA pass — added "Why this matters" rationale blockquote
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

