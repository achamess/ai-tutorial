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
    # Module 4.1: Claude Code Basics

    **What you'll learn:**
    - What Claude Code is and how it differs from chat-based Claude
    - The VS Code integration -- where it lives, how to invoke it
    - Basic commands and the conversation model
    - Reading files, searching code, and running commands through Claude Code
    - The permission model -- what Claude Code can and can't do automatically

    **Prerequisites:** Basic terminal familiarity (see [Missing Semester Lecture 1: The Shell](https://missing.csail.mit.edu/2020/course-shell/))

    **Reference:** [Anthropic Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Prompts for Research](../04-prompt-engineering/03-prompts-for-research.py) | [Module Index](../README.md) | [Next: Advanced Claude Code Workflows \u2192](02-advanced-workflows.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Claude Code is your primary interface for AI-assisted coding, file manipulation, and project management. Unlike chat-based Claude where you copy-paste code back and forth, Claude Code reads your files, edits them in place, and runs commands directly — it's the difference between describing surgery over the phone and having a surgeon in the room.
    > - Understanding Claude Code's permission model means you can delegate effectively and safely. You'll know when to let it run freely (reading files, searching code) and when to review before approving (editing analysis scripts, running commands on your data).
    > - The workflows in this notebook — "explain this code," "fix this error," "build this analysis" — are the ones you'll use daily as you build Python scripts for binder screening analysis, calcium imaging processing, and automated literature reviews.
    > - Knowing how Claude Code explores projects means you can hand it a new bioinformatics tool repository and say "help me understand this and set it up" — a real scenario when you're evaluating new protein design pipelines.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. What Is Claude Code?

    You already know Claude from the web interface at claude.ai -- you type a message, Claude responds, and you go back and forth. That's great for brainstorming, writing, and asking questions.

    **Claude Code is different.** It's an *agentic* coding assistant that lives inside your terminal and VS Code. Instead of just chatting, Claude Code can:

    | Capability | Chat Claude | Claude Code |
    |---|---|---|
    | Answer questions | Yes | Yes |
    | Read your files | No (you paste them) | Yes (reads directly) |
    | Edit your files | No (gives you code to copy) | Yes (edits in place) |
    | Run terminal commands | No | Yes (with your permission) |
    | Search your codebase | No | Yes (grep, glob, etc.) |
    | Use git | No | Yes |
    | Remember project context | Limited | Yes (via CLAUDE.md) |

    Think of it this way:
    - **Chat Claude** = a knowledgeable colleague you talk to on the phone
    - **Claude Code** = that same colleague sitting at your computer with you, able to look at and modify your files

    ### Why this matters for your research

    As a pain biologist designing de novo protein binders for NaV1.7/NaV1.8/KCNQ2/3, you'll increasingly work with:
    - Python scripts for data analysis (RNA-seq, calcium imaging, behavioral assays)
    - Configuration files for computational tools
    - Data processing pipelines
    - Manuscript figures and statistical analyses

    Claude Code can help with *all* of these, directly in your working environment.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### Claude Code Architecture

    """),
    mo.mermaid(
        """
        graph LR
            You["You<br>(natural language)"] -->|"describe task"| CC["Claude Code<br>(AI agent)"]
            CC -->|"Read / Grep / Glob"| Files["Your Files<br>& Codebase"]
            CC -->|"Edit / Write"| Files
            CC -->|"Bash commands"| Terminal["Terminal<br>(shell)"]
            CC -->|"git operations"| Git["Git<br>(version control)"]
            Terminal -->|"output"| CC
            Files -->|"contents"| CC
            Git -->|"status/diff"| CC
            CC -->|"response"| You
        
            style You fill:#4878CF,color:#fff
            style CC fill:#E24A33,color:#fff
            style Files fill:#55A868,color:#fff
            style Terminal fill:#8172B2,color:#fff
            style Git fill:#FDB863,color:#000
        """
    ),
    mo.md(r"""

    **Key insight:** You never interact with files, terminal, or git directly when using Claude Code. You describe what you want in plain English, and Claude Code uses its tools to make it happen. The permission model (Section 5) controls which of these tool-uses require your approval.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** Claude Code is a **tool-using agent**, not just a chatbot. It doesn't just generate text -- it reads files, runs commands, and makes edits by invoking tools in a loop. Each tool call is a discrete action (Read, Edit, Bash, Grep, etc.) that Claude Code chooses based on your request. Understanding this agent architecture helps you give better instructions, because you're directing an autonomous worker, not having a conversation.

    > **Decision point: When to use Claude Code vs Claude.ai vs the API**
    >
    > | Option | Best for | Strengths | Limitations |
    > |--------|----------|-----------|-------------|
    > | **Claude.ai (chat)** | Brainstorming, writing, one-off questions | Easy to use, no setup, great for exploration | Can't access your files or run commands |
    > | **Claude Code** | Working with files, editing code, project tasks | Reads/edits files directly, runs commands, knows your project | Requires terminal/VS Code, uses more tokens |
    > | **Claude API** | Automation, batch processing, custom tools | Programmable, scalable, structured output | Requires Python code, no interactive file access |
    >
    > **Use when:**
    > - **Claude.ai** -- you want to think through a problem, draft text, or ask a quick question
    > - **Claude Code** -- you want Claude to *do something* in your project (edit a script, run an analysis, explore a codebase)
    > - **Claude API** -- you want to process 50+ items automatically or build a reusable tool
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. The VS Code Integration

    ### Where Claude Code lives

    Claude Code integrates into VS Code in two ways:

    1. **The terminal** -- You can run `claude` from any VS Code terminal
    2. **The Claude Code panel** -- A dedicated sidebar panel (look for the Claude icon in the left sidebar, or press `Cmd+Shift+P` and type "Claude")

    ### How to invoke it

    **From the terminal:**
    ```bash
    # Start an interactive session
    claude

    # Ask a one-off question
    claude "what files are in this directory?"

    # Pipe input to Claude Code
    cat error_log.txt | claude "explain this error"
    ```

    **From VS Code:**
    - `Cmd+Shift+P` -> "Claude: Open Claude Code"
    - Click the Claude icon in the sidebar
    - Keyboard shortcut: `Cmd+Esc` (opens/focuses the Claude Code panel)

    ### The conversation model

    When you start Claude Code, you're in a **conversation**. Each message you send adds to the context. Claude Code can see:
    - Everything you've said in the current conversation
    - Files it has read during this conversation
    - Output from commands it has run
    - Your project's CLAUDE.md instructions (more on this later)

    **Key concept:** Unlike chat Claude where you often start fresh, Claude Code conversations maintain context about your project as you work. But each new conversation starts fresh (unless you use memory -- covered in notebook 03).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. Basic Commands and Interactions

    ### Talking to Claude Code

    You interact with Claude Code using natural language. There's no special syntax. Just describe what you want:

    ```
    You: Read the file calcium_imaging_analysis.py and explain what it does

    You: Find all Python files that import pandas

    You: Run the tests in test_analysis.py

    You: Create a new Python script that reads a CSV of behavioral assay data
         and plots withdrawal latencies over time
    ```

    ### Built-in slash commands

    Claude Code has several built-in commands you can use:

    | Command | What it does |
    |---|---|
    | `/help` | Show available commands |
    | `/clear` | Clear conversation history (start fresh) |
    | `/compact` | Summarize the conversation to save context space |
    | `/cost` | Show token usage and cost for this session |
    | `/doctor` | Check your Claude Code installation health |
    | `/init` | Create a CLAUDE.md file for your project |
    | `/memory` | View or edit Claude Code's memory |
    | `/review` | Ask Claude to review recent changes |
    | `/status` | Show current status and configuration |

    ### The conversation lifecycle

    ```
    1. You open Claude Code (new conversation starts)
    2. Claude Code reads your CLAUDE.md (if it exists)
    3. You ask questions / give instructions
    4. Claude Code reads files, runs commands, makes edits
    5. You continue the conversation or /clear to start fresh
    6. When you close the terminal/panel, the conversation ends
    ```

    > **Tip:** Use `/compact` when you've been working for a while and Claude Code starts to slow down or lose track of earlier context. It summarizes the conversation so far, freeing up space for new work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. How Claude Code Interacts with Your Files

    This is where Claude Code really shines compared to chat-based Claude. It has a set of **tools** it uses to interact with your project:

    ### Reading files

    Claude Code can read any file in your project. When you ask it to look at a file, it uses its `Read` tool:

    ```
    You: Look at the file data/nav17_binding_results.csv and tell me what columns it has

    Claude Code: [uses Read tool to open the file]
                 The file has the following columns:
                 - binder_id: unique identifier for each protein binder
                 - target: NaV1.7 subunit targeted
                 - kd_nm: binding affinity in nanomolar
                 - selectivity_ratio: selectivity over NaV1.5
                 ...
    ```

    ### Searching your codebase

    Claude Code can search across all your files:

    - **Glob** -- find files by name pattern (like `*.py` or `*_analysis*`)
    - **Grep** -- search file contents for a pattern (like finding every file that mentions "NaV1.7")

    ```
    You: Find all files that mention calcium imaging

    Claude Code: [uses Grep to search across all files]
                 Found references in:
                 - analysis/calcium_imaging.py (lines 12, 45, 89)
                 - notebooks/03-imaging-protocol.py (cell 5)
                 - README.md (line 23)
    ```

    ### Editing files

    Claude Code can modify files directly using its `Edit` tool. It makes targeted replacements:

    ```
    You: In analysis.py, change the significance threshold from 0.05 to 0.01

    Claude Code: [uses Edit tool to replace the specific line]
                 Done. Changed `alpha = 0.05` to `alpha = 0.01` on line 34.
    ```

    ### Creating files

    Claude Code can also create entirely new files:

    ```
    You: Create a Python script that reads behavioral assay data from a CSV,
         calculates mean withdrawal latencies per group, and runs a t-test

    Claude Code: [uses Write tool to create the new file]
                 Created behavioral_analysis.py with:
                 - CSV loading with pandas
                 - Group-wise mean calculation
                 - scipy.stats t-test
                 - Results summary output
    ```

    ### Running commands

    Claude Code can run terminal commands -- installing packages, running scripts, using git:

    ```
    You: Run the analysis script and show me the output

    Claude Code: [uses Bash tool to run: python behavioral_analysis.py]
                 Output:
                 Group A (vehicle): mean = 4.2s, n = 8
                 Group B (NaV1.7 binder): mean = 8.7s, n = 8
                 t-test p-value: 0.003 **
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Warning:** Always review file edits before accepting them. Claude Code shows you a diff of what it wants to change -- read it carefully, especially for analysis scripts that produce numerical results. A single wrong sign (`>` vs `<` in a filter) or column name mismatch can silently produce incorrect results. This is particularly critical for scripts that filter binder candidates by Kd or selectivity thresholds, where an inverted comparison means you'd advance the worst candidates instead of the best.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. The Permission Model

    Claude Code doesn't just do whatever it wants. It has a **permission system** that controls what it can do automatically vs. what requires your approval.

    ### Permission levels

    | Action | Default Permission |
    |---|---|
    | Read files | Allowed (no prompt) |
    | Search files (grep/glob) | Allowed (no prompt) |
    | Edit existing files | **Asks permission** |
    | Create new files | **Asks permission** |
    | Run bash commands | **Asks permission** |
    | Delete files | **Asks permission** |
    | Git operations | **Asks permission** |

    ### What the permission prompt looks like

    When Claude Code wants to do something that requires permission, you'll see something like:

    ```
    Claude wants to run: python analysis.py

      [Allow]  [Allow Always]  [Deny]
    ```

    - **Allow** -- let it run this one time
    - **Allow Always** -- let it run this command (or type of command) without asking again in this session
    - **Deny** -- don't run it

    ### Configuring permissions

    You can configure which tools are allowed without prompting. This is done in your settings (covered in notebook 03). For now, the defaults are safe and sensible:

    - Reading is always fine (can't break anything)
    - Writing and executing require your OK

    > **Important safety note:** Claude Code will never push to a remote git repository, delete files outside your project, or access the internet without your explicit permission. This is by design -- you always stay in control.

    ### The "dangerously skip permissions" mode

    There is a way to let Claude Code run without asking permission (using the `--dangerously-skip-permissions` flag), but **don't use this** until you're very comfortable with Claude Code and understand exactly what it might do. The permission prompts are your safety net.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Your First Claude Code Workflows

    Let's look at some practical patterns you'll use constantly.

    ### Pattern 1: "Explain this to me"

    ```
    You: Read calcium_imaging_analysis.py and explain it to me.
         I'm a biologist, not a programmer -- focus on what the code
         does scientifically, not the programming details.
    ```

    This is perfect for understanding code you've inherited or downloaded from a paper's supplementary materials.

    ### Pattern 2: "Fix this error"

    ```
    You: I'm getting this error when I run my analysis:

         KeyError: 'withdrawal_latency'

         The script is in analysis/behavior.py. Figure out what's wrong and fix it.
    ```

    Claude Code will read the file, identify the issue (maybe the column name is actually `withdrawal_latency_s`), and fix it.

    ### Pattern 3: "Help me build this"

    ```
    You: I have calcium imaging data in data/calcium_traces.csv.
         Each row is a timepoint, each column is a neuron.
         Help me write a script to:
         1. Identify responding neurons (>20% dF/F increase after stimulus)
         2. Calculate the percentage of responders
         3. Plot the average trace for responders vs non-responders
    ```

    ### Pattern 4: "Explore this project"

    ```
    You: I just cloned a repository for a computational protein design tool.
         Help me understand the project structure, what it does, and how to use it.
    ```

    Claude Code will systematically read key files (README, setup files, main scripts) and give you an overview.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Practical Demo: Exploring This Tutorial Repository

    Let's use Python to look at the structure of this very tutorial, the same way Claude Code would see it. This gives you a sense of how Claude Code explores projects.

    When you ask Claude Code to explore a project, it uses tools similar to the Python code below.
    """)
    return


@app.cell
def _():
    import os
    from pathlib import Path

    # This is analogous to what Claude Code does when you ask it to explore a project
    # It uses Glob to find files and Read to look at their contents

    tutorial_root = Path("..")

    print("=" * 60)
    print("Tutorial Repository Structure")
    print("=" * 60)

    for item in sorted(tutorial_root.iterdir()):
        if item.name.startswith("."):
            continue
        if item.is_dir():
            # Count contents
            contents = list(item.iterdir())
            n_files = len([f for f in contents if f.is_file()])
            n_dirs = len([f for f in contents if f.is_dir()])
            print(f"  {item.name}/  ({n_files} files, {n_dirs} subdirs)")
        else:
            size = item.stat().st_size
            print(f"  {item.name}  ({size} bytes)")
    return (tutorial_root,)


@app.cell
def _(tutorial_root):
    # Read the CLAUDE.md file -- this is what Claude Code reads first when it starts
    claude_md = tutorial_root / "CLAUDE.md"

    if claude_md.exists():
        print("Contents of CLAUDE.md (what Claude Code sees first):")
        print("=" * 60)
        print(claude_md.read_text())
    else:
        print("No CLAUDE.md found -- Claude Code would start without project context")
    return


@app.cell
def _(tutorial_root):
    # Simulating a "grep" search -- finding all notebooks that mention specific topics
    # This is what Claude Code's Grep tool does

    import re

    search_term = "pain"
    print(f"Searching for '{search_term}' across all notebooks...")
    print("=" * 60)

    notebook_files = list(tutorial_root.rglob("*.py"))
    matches_found = 0

    for nb_path in sorted(notebook_files):
        try:
            content = nb_path.read_text()
            # Count occurrences (simple search, not JSON-aware)
            count = content.lower().count(search_term.lower())
            if count > 0:
                print(f"  {nb_path.relative_to(tutorial_root)}: {count} occurrences")
                matches_found += count
        except Exception:
            pass

    print(f"\nTotal: {matches_found} occurrences across {len(notebook_files)} notebooks")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Terminal Concepts You'll Need

    Since Claude Code operates through the terminal, here are the essential terminal concepts from [Missing Semester Lecture 1: The Shell](https://missing.csail.mit.edu/2020/course-shell/) that are relevant:

    ### The working directory

    Claude Code always operates from your project's root directory. When it runs commands, they run relative to that directory.

    ```bash
    pwd                    # Print working directory
    ls                     # List files in current directory
    ls data/               # List files in the data subdirectory
    ```

    ### Paths

    ```bash
    # Absolute path (starts from root)
    /Users/alex/projects/nav17-binders/analysis.py

    # Relative path (from current directory)
    analysis.py
    data/results.csv
    ../other-project/
    ```

    ### Piping and redirection

    You can pipe output into Claude Code from the terminal:

    ```bash
    # Pipe an error log into Claude Code for analysis
    python my_script.py 2>&1 | claude "explain this error and suggest a fix"

    # Pipe file contents
    cat weird_data.csv | claude "what format is this data in?"
    ```

    For more on pipes and redirection, see [Missing Semester Lecture 1](https://missing.csail.mit.edu/2020/course-shell/).

    ### Environment variables

    Claude Code uses the `ANTHROPIC_API_KEY` environment variable for authentication. You typically set this once:

    ```bash
    export ANTHROPIC_API_KEY="sk-ant-..."
    ```

    Or better, add it to your shell profile (`~/.zshrc` on macOS) so it's always available. See [Missing Semester Lecture 5: Command-line Environment](https://missing.csail.mit.edu/2020/command-line/) for more on shell configuration.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 9. Tips for Effective Communication with Claude Code

    Claude Code responds best when you communicate clearly. Here are key principles:

    ### Be specific about what you want

    | Less effective | More effective |
    |---|---|
    | "Fix my code" | "The function `calculate_ec50` in `analysis.py` returns NaN for some inputs. Fix it so it handles edge cases." |
    | "Make a plot" | "Create a heatmap of gene expression data in `data/rnaseq.csv` with genes on rows and conditions on columns. Use a red-blue colormap." |
    | "Help with data" | "Read `data/behavior.csv` and tell me: how many subjects per group, any missing values, and the mean withdrawal latency per group." |

    ### Give context about your domain

    Claude Code knows about biology, but connecting the dots helps:

    ```
    You: I have calcium imaging data from DRG neurons exposed to capsaicin.
         The CSV has time in column A and dF/F for each neuron in subsequent columns.
         Capsaicin was applied at t=60s. I need to identify TRPV1+ responders
         (neurons with >20% dF/F increase within 30s of application).
    ```

    ### Iterate -- don't try to get everything in one message

    Claude Code maintains conversation context, so you can build up:

    ```
    You: Read the data file and show me a summary
    Claude: [reads and summarizes]

    You: Now plot the withdrawal latencies for each group
    Claude: [creates plot]

    You: Make the font bigger and add significance stars from the t-test
    Claude: [updates plot]

    You: Perfect. Save this as a publication-quality PDF
    Claude: [saves final version]
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Exercises

    These exercises are meant to be done *in Claude Code*, not in this notebook. Open a Claude Code session (in your VS Code terminal or sidebar) and try each one.

    ### Exercise 1: Explore this repository
    Open Claude Code and ask it:
    ```
    Explore this tutorial repository. Tell me:
    1. How many modules are there?
    2. How many notebooks exist so far?
    3. What does the CLAUDE.md say?
    ```

    ### Exercise 2: Search for content
    Ask Claude Code:
    ```
    Find all notebooks that mention "NaV1.7" or "ion channel"
    ```

    ### Exercise 3: Get information about a file
    Ask Claude Code:
    ```
    Read this notebook (04-mastering-claude-code/01-claude-code-basics.py)
    and give me a bullet-point summary of what it covers
    ```

    ### Exercise 4: Run a command
    Ask Claude Code:
    ```
    Show me what Python packages are installed in the ai-tutorial virtual environment
    ```

    (Notice how it asks your permission before running `pip list`)

    ### Exercise 5: Pipe something into Claude Code
    From your VS Code terminal (not inside a Claude Code session), try:
    ```bash
    ls -la | claude "explain what each of these files is"
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Quick Reference Card

    | What you want to do | What to tell Claude Code |
    |---|---|
    | Start a session | `claude` in terminal, or open VS Code panel |
    | Read a file | "Read [filename] and explain it" |
    | Search code | "Find all files that mention [topic]" |
    | Edit a file | "In [file], change [X] to [Y]" |
    | Create a file | "Create a script that does [X]" |
    | Run something | "Run [command] and show me the output" |
    | Debug an error | "I'm getting this error: [paste]. Fix it." |
    | Clear context | `/clear` |
    | Check cost | `/cost` |
    | Compact context | `/compact` |

    ---

    **Next:** [02-advanced-workflows.py](02-advanced-workflows.py) -- Multi-step tasks, git workflows, debugging, and context management.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [← Previous: Prompts for Research](../04-prompt-engineering/03-prompts-for-research.py) | [Module Index](../README.md) | [Next: Advanced Claude Code Workflows →](02-advanced-workflows.py)
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


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **[Anthropic Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)** -- Official documentation covering installation, capabilities, and usage patterns for Claude Code.
    - **[Missing Semester Lecture 1: The Shell](https://missing.csail.mit.edu/2020/course-shell/)** -- Essential terminal concepts (paths, pipes, environment variables) that underpin how Claude Code operates.
    - **[Missing Semester Lecture 5: Command-line Environment](https://missing.csail.mit.edu/2020/command-line/)** -- Shell configuration, aliases, and environment variables -- useful for setting up your `ANTHROPIC_API_KEY` and other preferences.
    - **[Anthropic Claude Code Permissions](https://docs.anthropic.com/en/docs/claude-code/security)** -- Details on the permission model, what Claude Code can and cannot do, and how to configure trust levels.
    - **Local reference:** [resources/references/anthropic-claude-code-overview.md](../resources/references/anthropic-claude-code-overview.md) -- Local copy of Claude Code documentation for offline use.
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

