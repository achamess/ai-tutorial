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
    # Module 4.2: Advanced Claude Code Workflows

    **What you'll learn:**
    - Multi-step tasks: asking Claude Code to plan then execute
    - Working with git through Claude Code
    - Editing files -- how Claude Code reads, edits, and creates files
    - Using Claude Code for debugging
    - Context management -- CLAUDE.md, memory, giving Claude Code project context

    **Prerequisites:** [01-claude-code-basics.py](01-claude-code-basics.py), basic git concepts (see [Missing Semester Lecture 6: Version Control](https://missing.csail.mit.edu/2020/version-control/))

    **References:** [Anthropic Claude Code Best Practices](https://docs.anthropic.com/en/docs/claude-code/overview) | [Git Official Documentation](https://git-scm.com/doc)

    ---
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Claude Code Basics](01-claude-code-basics.py) | [Module Index](../README.md) | [Next: Customizing Claude Code \u2192](03-customizing-claude-code.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Multi-step tasks are where Claude Code saves the most time. "Read my screening data, filter for hits, generate figures, and write a summary" is a single conversation that replaces an hour of manual work. Understanding how to structure these workflows multiplies your productivity.
    > - Git through Claude Code means version control without memorizing commands. When you're iterating on an analysis script and need to track changes, revert mistakes, or create branches for different analysis approaches, you just describe what you want in English.
    > - Debugging with Claude Code is transformative — instead of spending 45 minutes googling a scipy curve_fit error, you paste the traceback and get a fix in 10 seconds. This notebook teaches you the patterns that make debugging instant.
    > - Context management (knowing when to `/compact`, when to start fresh, and how to provide strategic context) is the difference between Claude Code being a sharp assistant and a confused one. Long sessions without context management lead to degraded performance.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 1. Multi-Step Tasks: Plan Then Execute

    One of Claude Code's most powerful capabilities is handling complex, multi-step tasks. The key is knowing how to break things down and when to let Claude Code plan before executing.

    ### The "Plan first" pattern

    For anything non-trivial, ask Claude Code to make a plan before it starts:

    ```
    You: I need to process a batch of calcium imaging .tif files.
         For each file, I need to:
         1. Load the image stack
         2. Define ROIs around cell bodies
         3. Extract fluorescence traces
         4. Calculate dF/F
         5. Save results to CSV

         Before writing any code, outline the approach you'd take.
         What libraries would you use? What's the file structure?
    ```

    Claude Code will propose a plan. You review it, ask questions, and *then* tell it to proceed:

    ```
    You: Good plan, but use scikit-image instead of OpenCV for the ROI detection.
         Also, my .tif files are in data/raw/imaging/. Go ahead and build it.
    ```

    ### Why planning matters

    Without a plan, Claude Code might:
    - Choose libraries you don't have installed
    - Organize files differently than you'd like
    - Make assumptions about your data format that are wrong

    **Rule of thumb:** If the task involves creating more than one file or more than ~50 lines of code, ask for a plan first.

    ### The "Think step by step" technique

    For analytical tasks, you can ask Claude Code to think through the problem:

    ```
    You: I have RNA-seq count data for DRG neurons from three conditions:
         naive, CFA-inflamed, and SNI (nerve injury). I want to find genes
         that are differentially expressed in pain states but not shared
         between inflammatory and neuropathic pain.

         Think through the analysis strategy step by step before writing code.
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Tip:** The "plan first" pattern is the single most effective habit for working with Claude Code. Before any task involving more than one file or more than ~50 lines of code, say "outline your plan before writing code." This gives you a chance to catch wrong assumptions (wrong library, wrong file format, wrong directory) before Claude Code generates hundreds of lines of code you'll have to review. Think of it like discussing an experiment design before starting benchwork.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### The Multi-Step Workflow

    """),
    mo.mermaid(
        """
        graph TD
            A["1. PLAN<br>Describe what you want<br>Ask Claude Code to outline approach"] --> B["2. REVIEW<br>Read the plan<br>Ask questions, suggest changes"]
            B --> C["3. EXECUTE<br>Tell Claude Code to build it<br>It reads, writes, runs"]
            C --> D["4. VERIFY<br>Check the output<br>Run tests, inspect results"]
            D --> E{"Correct?"}
            E -->|"Yes"| F["5. COMMIT<br>Save with git<br>Meaningful commit message"]
            E -->|"No"| G["6. ITERATE<br>Describe what's wrong<br>Claude Code fixes it"]
            G --> D
        
            style A fill:#4878CF,color:#fff
            style B fill:#55A868,color:#fff
            style C fill:#E24A33,color:#fff
            style D fill:#8172B2,color:#fff
            style F fill:#FDB863,color:#000
            style G fill:#E24A33,color:#fff
        """
    ),
    mo.md(r"""

    This plan-execute-verify-commit loop is the core workflow for productive Claude Code use. Notice how it mirrors the scientific method: hypothesis (plan), experiment (execute), analyze (verify), publish (commit).
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why git for a biologist?** Git is your "undo button" for code. When Claude Code edits your analysis script and something breaks, git lets you instantly revert to the working version. It also tracks every change you and Claude Code make, so you always know what was modified and when — essential for reproducible research.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Decision point: When to use git through Claude Code vs manually**
    >
    > | Approach | Pros | Cons | Use when |
    > |----------|------|------|----------|
    > | **Git through Claude Code** | No commands to remember, natural language, Claude writes good commit messages | Less control over exact commands, harder to learn git itself | Day-to-day commits, simple branching, checking status |
    > | **Git manually (terminal)** | Full control, builds muscle memory, faster for quick operations | Must remember commands, easy to make mistakes | Interactive rebases, complex merges, when you need exact control |
    > | **VS Code git panel** | Visual diffs, click-to-stage, good overview | Less powerful than CLI, can't do complex operations | Reviewing changes visually, staging individual hunks |
    >
    > **Recommendation:** Start by using git through Claude Code to build comfort with version control concepts. As you learn what the commands do, you'll naturally start typing `git status` yourself for quick checks while still asking Claude Code for complex operations like merge conflict resolution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 2. Working with Git Through Claude Code

    Git is the version control system that tracks changes to your code. If you're not familiar with git, the [Missing Semester Lecture 6: Version Control](https://missing.csail.mit.edu/2020/version-control/) is an excellent introduction. The [official Git documentation](https://git-scm.com/doc) is also a comprehensive reference, though it can be dense for beginners.

    Claude Code is exceptionally good at git operations. You don't need to memorize git commands -- just describe what you want.

    ### Common git tasks through Claude Code

    **Check what's changed:**
    ```
    You: What files have I changed since my last commit?
    ```
    Claude Code runs `git status` and `git diff` and summarizes the changes in plain English.

    **Make a commit:**
    ```
    You: Commit my changes with an appropriate message
    ```
    Claude Code will:
    1. Run `git status` to see what's changed
    2. Run `git diff` to understand the changes
    3. Stage the appropriate files
    4. Write a meaningful commit message
    5. Create the commit (after you approve)

    **Review recent history:**
    ```
    You: Show me what changed in the last 5 commits
    ```

    **Create a branch for a new experiment:**
    ```
    You: Create a new branch called 'nav18-selectivity-analysis'
         for the new analysis I'm about to build
    ```

    **Handle a merge conflict:**
    ```
    You: I tried to merge the feature branch and got conflicts.
         Help me resolve them.
    ```

    ### Git workflow for research projects

    Here's a practical workflow for your research code:

    ```
    main branch          = stable, working code
      |
      +-- analysis/nav17  = new NaV1.7 analysis
      +-- fix/calcium-bug = fixing a bug in calcium imaging code
      +-- data/new-cohort = adding new behavioral data
    ```

    You can manage all of this through Claude Code without memorizing a single git command:

    ```
    You: Create a new branch for my NaV1.7 binding analysis,
         make the changes there, then when I'm ready, help me
         merge it back to main.
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 3. How Claude Code Edits Files

    Understanding how Claude Code modifies files helps you work with it more effectively.

    ### The Edit tool: surgical replacements

    Claude Code's primary editing mechanism is **find and replace**. It finds a unique string in the file and replaces it. This is important because:

    1. **It preserves everything else** -- only the targeted section changes
    2. **It's precise** -- no accidental changes to other parts of the file
    3. **It requires reading first** -- Claude Code must read a file before editing it

    Example of what happens under the hood:

    ```python
    # Claude Code reads your file and sees:
    def analyze_binding(data):
        threshold = 100  # nM
        hits = data[data['kd'] < threshold]
        return hits

    # You say: "Change the binding threshold to 50 nM"
    # Claude Code replaces:
    #   old: "threshold = 100  # nM"
    #   new: "threshold = 50  # nM"
    ```

    ### The Write tool: creating or rewriting files

    For new files or complete rewrites, Claude Code uses its Write tool. It writes the entire file contents at once.

    ### Best practices for file editing with Claude Code

    1. **Let Claude Code read before editing** -- If you want changes to a file, mention the file name. Claude Code will read it first.

    2. **Be specific about what to change** -- "Change the threshold" is better than "update the code."

    3. **Review the changes** -- Claude Code shows you what it changed. Read the diff before approving.

    4. **Use git for safety** -- If Claude Code makes a change you don't like:
       ```
       You: Undo the last change to analysis.py
       ```
       Or if you committed:
       ```
       You: Revert the last commit
       ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Warning:** The context window fills up during long sessions. When you've been working with Claude Code for 20+ minutes or across many files, Claude Code starts losing track of earlier context -- it may forget file contents it read, repeat itself, or miss details you mentioned earlier. Use `/compact` proactively after completing each major sub-task (e.g., after finishing a data loading step, before moving to visualization). Don't wait for degraded responses -- compact early and often.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 4. Debugging with Claude Code

    Debugging is one of the highest-value uses of Claude Code. Instead of spending hours googling cryptic error messages, you can paste them directly.

    ### Pattern 1: Paste the error

    ```
    You: I'm running my analysis and getting this error:

    Traceback (most recent call last):
      File "analysis/binding_assay.py", line 47, in <module>
        results = calculate_ic50(concentrations, responses)
      File "analysis/binding_assay.py", line 23, in calculate_ic50
        popt, pcov = curve_fit(hill_equation, conc, resp)
      File "/opt/homebrew/lib/python3.14/site-packages/scipy/optimize/_minpack_py.py", line 822
        raise RuntimeError("Optimal parameters not found: " + errmsg)
    RuntimeError: Optimal parameters not found: Number of calls to function has reached maxfev = 800.

    Fix this.
    ```

    Claude Code will:
    1. Read `analysis/binding_assay.py`
    2. Understand the Hill equation fitting context
    3. Diagnose the issue (likely: bad initial parameter guesses or poorly scaled data)
    4. Fix it (add `p0` initial guesses, increase `maxfev`, or normalize the data)

    ### Pattern 2: "It runs but gives wrong results"

    ```
    You: My script runs without errors but the EC50 values seem way off.
         For capsaicin on TRPV1, I'm getting EC50 = 5 mM but it should be
         around 100 nM. The script is analysis/dose_response.py and the
         data is in data/capsaicin_dr.csv. Figure out what's wrong.
    ```

    Claude Code will read both files and might discover you have a units mismatch (concentrations in M vs nM).

    ### Pattern 3: "I don't understand this warning"

    ```
    You: When I run my RNA-seq analysis, I get:
         FutureWarning: The default value of numeric_only in DataFrameGroupBy.mean
         is deprecated. What does this mean and how do I fix it?
    ```

    ### Pattern 4: Pipe the error directly

    From your terminal:
    ```bash
    python analysis/binding_assay.py 2>&1 | claude "fix this error in analysis/binding_assay.py"
    ```

    The `2>&1` captures both standard output and error output, piping everything to Claude Code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 5. Context Management

    One of the most important skills for getting good results from Claude Code is **managing context** -- making sure Claude Code has the information it needs to help you effectively.

    ### Layer 1: CLAUDE.md files

    The `CLAUDE.md` file at the root of your project is the single most important context tool. Claude Code reads it at the start of every conversation.

    Think of it as a briefing document for your AI assistant. It should contain:
    - What the project is about
    - How the code is organized
    - Important conventions
    - Which tools/libraries you use
    - Any domain-specific knowledge Claude Code needs

    We'll cover CLAUDE.md in detail in [notebook 03](03-customizing-claude-code.py).

    ### Layer 2: Conversation context

    Everything you say in a conversation becomes context. Use this to your advantage:

    ```
    You: Before we start, here's some context about my project:
         - I'm studying NaV1.7 protein binders for pain therapeutics
         - Data comes from SPR binding assays and patch clamp electrophysiology
         - Concentrations are always in nanomolar unless stated otherwise
         - We use GraphPad Prism conventions for dose-response curves

         Now, help me build a dose-response analysis script.
    ```

    ### Layer 3: Files as context

    When Claude Code reads a file, its contents become part of the conversation context. You can strategically point Claude Code at files:

    ```
    You: Read these files to understand my project:
         - README.md
         - analysis/config.py
         - data/README.md

         Then help me add a new analysis module.
    ```

    ### Layer 4: Memory (persistent context)

    Claude Code can remember things across conversations using its memory system. This is covered in [notebook 03](03-customizing-claude-code.py).

    ### Context limits and /compact

    Claude Code has a context window (how much it can "hold in mind" at once). When you're working on a complex task, you might hit this limit. Signs:
    - Claude Code forgets something you told it earlier
    - Responses get slower
    - Claude Code starts repeating itself or losing coherence

    **Solution:** Use `/compact` to summarize the conversation. This condenses everything into a brief summary, freeing up space:

    ```
    You: /compact
    Claude: [Summarized conversation: working on NaV1.7 binding analysis,
             created dose_response.py, fixed units bug, currently adding
             selectivity ratio calculation...]

    You: Great, now let's continue with the selectivity analysis.
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 6. Practical Demo: Building a Data Processing Script

    Let's walk through what it looks like to work with Claude Code on a real task. Below, we'll create a mock dataset and a processing script -- the same kind of task you'd ask Claude Code to do.

    ### Step 1: Create mock data

    In a real workflow, you'd say:
    ```
    You: Create a mock dataset of NaV1.7 binding assay results for testing.
         Include binder IDs, binding affinity (Kd), selectivity ratios, and
         thermal stability measurements.
    ```

    Here's what that looks like in code:
    """)
    return


@app.cell
def _():
    import pandas as pd
    import numpy as np

    # Create mock NaV1.7 binder screening data
    np.random.seed(42)
    n_binders = 50

    data = pd.DataFrame({
        'binder_id': [f'NB-{i:03d}' for i in range(1, n_binders + 1)],
        'target': 'NaV1.7-VSD4',
        'kd_nM': np.round(np.random.lognormal(mean=4, sigma=1.5, size=n_binders), 1),
        'selectivity_vs_nav15': np.round(np.random.lognormal(mean=1.5, sigma=1, size=n_binders), 1),
        'selectivity_vs_nav16': np.round(np.random.lognormal(mean=1, sigma=0.8, size=n_binders), 1),
        'tm_celsius': np.round(np.random.normal(loc=55, scale=8, size=n_binders), 1),
        'expression_yield_mg_per_L': np.round(np.random.lognormal(mean=2, sigma=0.8, size=n_binders), 1),
        'aggregation_percent': np.round(np.random.uniform(0, 60, size=n_binders), 1)
    })

    # Add some realistic constraints
    # Higher affinity binders tend to have slightly lower stability (trade-off)
    data.loc[data['kd_nM'] < 50, 'tm_celsius'] -= np.random.uniform(2, 5, size=(data['kd_nM'] < 50).sum())

    print(f"Mock dataset: {len(data)} binders")
    print(f"\nColumn descriptions:")
    print(f"  binder_id: unique identifier")
    print(f"  target: NaV1.7 domain targeted")
    print(f"  kd_nM: binding affinity (lower = tighter binding)")
    print(f"  selectivity_vs_nav15: fold selectivity over cardiac NaV1.5 (higher = better)")
    print(f"  selectivity_vs_nav16: fold selectivity over NaV1.6 (higher = better)")
    print(f"  tm_celsius: melting temperature (higher = more stable)")
    print(f"  expression_yield_mg_per_L: protein yield (higher = easier to produce)")
    print(f"  aggregation_percent: % aggregation by SEC (lower = better)")

    data.head(10)
    return data, np, pd


@app.cell
def _(data):
    # Save the mock data
    import os
    os.makedirs('data', exist_ok=True)
    data.to_csv('data/nav17_binder_screen.csv', index=False)
    print("Saved to data/nav17_binder_screen.csv")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 2: Process the data

    In Claude Code, you'd say:
    ```
    You: Read data/nav17_binder_screen.csv and identify the top binder candidates.
         A good candidate has:
         - Kd < 100 nM
         - Selectivity > 10x over NaV1.5
         - Tm > 50C
         - Aggregation < 20%
         Show me the results ranked by affinity.
    ```

    Here's the analysis Claude Code would generate:
    """)
    return


@app.cell
def _(pd):
    # Load and filter -- this is what Claude Code would produce
    df = pd.read_csv('data/nav17_binder_screen.csv')

    # Define hit criteria
    criteria = (
        (df['kd_nM'] < 100) &
        (df['selectivity_vs_nav15'] > 10) &
        (df['tm_celsius'] > 50) &
        (df['aggregation_percent'] < 20)
    )

    hits = df[criteria].sort_values('kd_nM')

    print(f"Screening results:")
    print(f"  Total binders screened: {len(df)}")
    print(f"  Hits meeting all criteria: {len(hits)}")
    print(f"  Hit rate: {len(hits)/len(df)*100:.1f}%")
    print(f"\nIndividual filter counts:")
    print(f"  Kd < 100 nM: {(df['kd_nM'] < 100).sum()}")
    print(f"  Selectivity > 10x: {(df['selectivity_vs_nav15'] > 10).sum()}")
    print(f"  Tm > 50C: {(df['tm_celsius'] > 50).sum()}")
    print(f"  Aggregation < 20%: {(df['aggregation_percent'] < 20).sum()}")
    print(f"\nTop candidates:")
    if len(hits) > 0:
        print(hits.to_string(index=False))
    else:
        print("  No binders met all criteria. Consider relaxing thresholds.")
    return df, hits


@app.cell
def _(df, hits):
    import matplotlib.pyplot as plt
    import seaborn as sns
    _fig, axes = plt.subplots(1, 3, figsize=(14, 4))
    _ax = axes[0]
    _ax.scatter(df['kd_nM'], df['selectivity_vs_nav15'], c='gray', alpha=0.4, label='All binders')
    # Plot 1: Affinity vs Selectivity
    if len(hits) > 0:
        _ax.scatter(hits['kd_nM'], hits['selectivity_vs_nav15'], c='red', s=80, zorder=5, label='Hits')
    _ax.axvline(100, color='blue', linestyle='--', alpha=0.3, label='Kd cutoff')
    _ax.axhline(10, color='green', linestyle='--', alpha=0.3, label='Selectivity cutoff')
    _ax.set_xlabel('Kd (nM)')
    _ax.set_ylabel('Selectivity vs NaV1.5 (fold)')
    _ax.set_xscale('log')
    _ax.set_yscale('log')
    _ax.legend(fontsize=8)
    _ax.set_title('Affinity vs Selectivity')
    _ax = axes[1]
    _ax.scatter(df['tm_celsius'], df['aggregation_percent'], c='gray', alpha=0.4, label='All binders')
    if len(hits) > 0:
        _ax.scatter(hits['tm_celsius'], hits['aggregation_percent'], c='red', s=80, zorder=5, label='Hits')
    _ax.axvline(50, color='blue', linestyle='--', alpha=0.3)
    # Plot 2: Tm vs Aggregation
    _ax.axhline(20, color='green', linestyle='--', alpha=0.3)
    _ax.set_xlabel('Tm (C)')
    _ax.set_ylabel('Aggregation (%)')
    _ax.set_title('Stability vs Aggregation')
    _ax.legend(fontsize=8)
    _ax = axes[2]
    _ax.hist(df['kd_nM'], bins=20, color='steelblue', alpha=0.7, edgecolor='white')
    _ax.axvline(100, color='red', linestyle='--', linewidth=2, label='100 nM cutoff')
    _ax.set_xlabel('Kd (nM)')
    _ax.set_ylabel('Count')
    _ax.set_title('Binding Affinity Distribution')
    _ax.legend(fontsize=8)
    plt.suptitle('NaV1.7 Binder Screening Results', fontsize=14, fontweight='bold', y=1.02)
    # Plot 3: Distribution of Kd values
    plt.tight_layout()
    plt.show()
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 3: What iterating with Claude Code looks like

    After seeing the initial results, you might continue:

    ```
    You: Good, but I also want to see:
         1. A correlation matrix between all numeric properties
         2. Which binders are in the "sweet spot" -- top 25% affinity AND top 25% stability
         3. Export the hits to an Excel file with conditional formatting
    ```

    Claude Code would handle all three in one go, reading the data it already knows about and generating the additional analysis.

    **This is the power of the conversational model** -- you don't start from scratch each time. You build on what's already been done in the session.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 7. Git Workflow Demo

    Let's see what a git-based workflow looks like using Python to simulate the operations. In practice, you'd just tell Claude Code what to do in natural language.
    """)
    return


@app.cell
def _():
    # Simulating what Claude Code does when you ask about git status
    # In practice, you'd just say "what's my git status?" and Claude Code
    # would run these commands and summarize the results

    import subprocess

    def run_git(cmd):
        """Run a git command and return output (for demonstration)"""
        try:
            result = subprocess.run(
                f'git {cmd}', shell=True, capture_output=True, text=True,
                cwd='..'
            )
            return result.stdout.strip()
        except Exception as e:
            return f"Error: {e}"

    # These are the exact commands Claude Code would run
    print("Current branch:")
    print(f"  {run_git('branch --show-current')}")

    print("\nRecent commits:")
    log = run_git('log --oneline -5')
    for line in log.split('\n'):
        print(f"  {line}")

    print("\nWorking tree status:")
    status = run_git('status --short')
    if status:
        for line in status.split('\n')[:10]:
            print(f"  {line}")
    else:
        print("  Clean working tree")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Git commands you'll use through Claude Code

    You never need to remember these -- just describe what you want. But it's helpful to know what's happening:

    | What you say | What Claude Code does |
    |---|---|
    | "What's changed?" | `git status`, `git diff` |
    | "Save my work" | `git add`, `git commit` |
    | "Start a new branch for X" | `git checkout -b branch-name` |
    | "Go back to main" | `git checkout main` |
    | "Undo my last change to file.py" | `git checkout -- file.py` |
    | "Show me what I did yesterday" | `git log --since='yesterday'` |
    | "Push my changes" | `git push` |

    > **Important:** Claude Code will always ask permission before destructive git operations (force push, hard reset, etc.). Pay attention to these prompts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 8. Debugging Walkthrough

    Let's create a script with a deliberate bug, then see how you'd use Claude Code to fix it.
    """)
    return


@app.cell
def _(np, plt):
    def calculate_delta_f_over_f(trace, baseline_frames=20):
        """
        Calculate dF/F for a calcium imaging trace.
    
        Parameters:
            trace: array of fluorescence values over time
            baseline_frames: number of frames to use for baseline (F0)
    
        Returns:
            dF/F values
        """
        f0 = np.mean(trace[baseline_frames:])
        df_over_f = (trace - f0) / f0
        return df_over_f
    np.random.seed(42)
    n_frames = 200
    time = np.arange(n_frames) / 10
    baseline = 1000 + np.random.normal(0, 20, n_frames)
    response = np.zeros(n_frames)
    response[50:80] = 400 * np.exp(-np.arange(30) / 10)
    trace = baseline + response
    df_f = calculate_delta_f_over_f(trace)
    _fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(time, trace, 'k-', linewidth=0.8)
    ax1.set_ylabel('Fluorescence (AU)')
    ax1.set_title('Raw Trace')
    ax1.axvline(2, color='gray', linestyle='--', alpha=0.5, label='Baseline period end')
    ax1.axvline(5, color='red', linestyle='--', alpha=0.5, label='Stimulus')
    ax1.legend()
    ax2.plot(time, df_f, 'b-', linewidth=0.8)
    ax2.set_ylabel('dF/F')
    ax2.set_xlabel('Time (s)')
    ax2.set_title('dF/F (BUGGY -- baseline calculated incorrectly)')
    ax2.axhline(0, color='gray', linestyle='-', alpha=0.3)
    ax2.axvline(5, color='red', linestyle='--', alpha=0.5, label='Stimulus')
    ax2.legend()
    plt.tight_layout()
    plt.show()
    print(f'Peak dF/F (buggy): {df_f[50:80].max():.3f}')
    print(f'\nThe bug: baseline is calculated from frames AFTER the baseline period')
    print(f'Fix: change trace[baseline_frames:] to trace[:baseline_frames]')
    return time, trace


@app.cell
def _(np, plt, time, trace):
    # The fixed version
    def calculate_delta_f_over_f_fixed(trace, baseline_frames=20):
        """Calculate dF/F with correct baseline."""
        f0 = np.mean(trace[:baseline_frames])  # FIXED: use first N frames
        df_over_f = (trace - f0) / f0
        return df_over_f
    df_f_fixed = calculate_delta_f_over_f_fixed(trace)
    _fig, _ax = plt.subplots(figsize=(10, 3))
    _ax.plot(time, df_f_fixed, 'b-', linewidth=0.8)
    _ax.set_ylabel('dF/F')
    _ax.set_xlabel('Time (s)')
    _ax.set_title('dF/F (Fixed)')
    _ax.axhline(0, color='gray', linestyle='-', alpha=0.3)
    _ax.axhline(0.2, color='green', linestyle='--', alpha=0.5, label='20% threshold')
    _ax.axvline(5, color='red', linestyle='--', alpha=0.5, label='Stimulus')
    _ax.legend()
    plt.tight_layout()
    plt.show()
    print(f'Peak dF/F (fixed): {df_f_fixed[50:80].max():.3f}')
    print(f"This neuron {('IS' if df_f_fixed[50:80].max() > 0.2 else 'is NOT')} a responder (>20% dF/F)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### How you'd handle this in Claude Code

    Instead of hunting for the bug yourself, you'd just say:

    ```
    You: My dF/F calculation seems wrong -- the baseline period shows
         a dip instead of being near zero. The script is calcium_analysis.py.
         Find and fix the bug.
    ```

    Claude Code would:
    1. Read the file
    2. Identify the slicing bug (`trace[baseline_frames:]` instead of `trace[:baseline_frames]`)
    3. Fix it with a single targeted edit
    4. Explain what was wrong

    Total time: ~10 seconds.
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
    > **Navigation:** [\u2190 Previous: Claude Code Basics](01-claude-code-basics.py) | [Module Index](../README.md) | [Next: Customizing Claude Code \u2192](03-customizing-claude-code.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **[Missing Semester Lecture 6: Version Control (Git)](https://missing.csail.mit.edu/2020/version-control/)** -- Comprehensive introduction to Git concepts: commits, branches, merging, and collaboration workflows.
    - **[Git Official Documentation](https://git-scm.com/doc)** -- The definitive reference for all Git commands, including the free *Pro Git* book.
    - **[Anthropic Claude Code Overview](https://docs.anthropic.com/en/docs/claude-code/overview)** -- Best practices for working with Claude Code, including multi-step workflows and context management.
    - **[Anthropic Claude Code Memory](https://docs.anthropic.com/en/docs/claude-code/memory)** -- How Claude Code's CLAUDE.md and memory systems provide persistent context across sessions.
    - **[Git Branching Tutorial](https://learngitbranching.js.org/)** -- Interactive visual tutorial for understanding Git branching, merging, and rebasing.
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

