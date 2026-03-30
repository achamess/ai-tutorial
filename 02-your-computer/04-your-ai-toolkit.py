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
    # 04: Your AI Toolkit

    You've learned how your computer works — the filesystem, processes, and networking. Now let's map out the **tools and interfaces** you need to do AI-powered research work. This isn't a vague "tools to try" list. Every item here solves a specific problem you'll hit as a pain biologist using AI.

    We'll cover what you have, what you need next, and what's on the horizon.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Networking and APIs](03-networking-and-apis.py) | [Module Index](../README.md) | [Next: What Is an LLM? \u2192](../03-how-llms-work/01-what-is-an-llm.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **How this notebook works**
    >
    > This is a reference guide, not a hands-on coding exercise. The code cells verify that your tools are installed and configured correctly. By the end, you'll have a clear mental map of how all these pieces fit together — and a checklist to make sure everything is set up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Part 1: Essential Tools (You Need These Now)

    These are the foundation. You're already using most of them — this section makes sure you understand *why* each one matters and how they connect.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1.1 VS Code — Your Command Center

    **What it is:** A free code editor from Microsoft that has become the standard environment for scientific programming. It's not just a text editor — it's a workspace that ties together your files, terminal, notebooks, and AI tools in one window.

    **Why you need it:** When you're analyzing calcium imaging data, you might have a Python script open, a terminal running a long computation, a marimo notebook with plots, and Claude Code helping you debug — all at the same time. VS Code is the one place where all of that lives together. Without it, you'd be switching between five different apps.

    **How to set it up:**
    - Download from [https://code.visualstudio.com/](https://code.visualstudio.com/)
    - Install the **Python** extension (ms-python.python) — gives you syntax highlighting, linting, and notebook support
    - Install the **marimo** extension — lets you run marimo `.py` notebooks directly in VS Code
    - Install the **Claude Code** extension — brings AI assistance into the editor
    - Open your project folder with `File > Open Folder` (or `code ~/ai-tutorial` from the terminal)

    **Key features to know:**
    - **Integrated terminal** (`Ctrl+\`` or `Cmd+\``) — no need for a separate Terminal.app
    - **Command Palette** (`Cmd+Shift+P`) — search for any action instead of hunting through menus
    - **Split editor** — view your data file and analysis script side by side
    - **Source control panel** — visual git interface (though the terminal is often faster)
    - **Extensions marketplace** — add support for R, LaTeX, CSV preview, and hundreds of other tools

    Official docs: [https://code.visualstudio.com/docs](https://code.visualstudio.com/docs)
    """)
    return


@app.cell
def _(subprocess):
    # Verify VS Code is installed and accessible from the terminal
    #! which code && code --version
    subprocess.call(['which', 'code', '&&', 'code', '--version'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1.2 Terminal / Shell (zsh) — Direct Computer Control

    **What it is:** The text-based interface to your computer. On macOS, the default shell is **zsh** (Z shell). You type commands, the computer executes them. No GUI, no clicking — just direct instructions.

    **Why you need it:** Every AI tool you'll use — Claude Code, pip, git, Python scripts — runs through the terminal. When you need to install a bioinformatics package (`pip install scanpy`), start a marimo server, or push your analysis to GitHub, you're in the terminal. It's also how Claude Code communicates with your machine: every action it takes is a shell command.

    **How to set it up:**
    - It's already on your Mac: open Terminal.app, or use VS Code's integrated terminal
    - Your shell configuration lives in `~/.zshrc` — this is where environment variables and PATH additions go
    - We covered this in depth in Notebook 01 (Filesystem and Shell)

    **Key features to know:**
    - **Tab completion** — type the first few letters of a file/command, then press Tab
    - **Command history** — press Up arrow to cycle through previous commands, or `Ctrl+R` to search
    - **Piping** (`|`) — chain commands together: `cat data.csv | head -20 | wc -l`
    - **Redirection** (`>`, `>>`) — send output to a file instead of the screen
    - `Ctrl+C` — stop a running command (you'll use this often)

    Reference: [MIT Missing Semester — Lecture 1: The Shell](https://missing.csail.mit.edu/2020/course-shell/)
    """)
    return


@app.cell
def _(subprocess):
    # Confirm your shell and its version
    #! echo "Shell: $SHELL" && zsh --version
    subprocess.call(['echo', 'Shell: $SHELL', '&&', 'zsh', '--version'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1.3 Claude Code — AI Assistant in Your Editor

    **What it is:** An AI coding assistant from Anthropic that runs inside VS Code (and in the terminal). You describe what you want in plain English, and it writes code, edits files, runs commands, and explains results — all within your project.

    **Why you need it:** You're a pain biologist, not a software engineer. When you need to parse a DESeq2 output file, clean calcium imaging traces, or build a heatmap of gene expression across DRG subtypes, Claude Code can write the Python for you — and explain what it's doing. It sees your files, understands your project context (via `CLAUDE.md`), and can run the code to verify it works.

    **How to set it up:**
    - Install via npm: `npm install -g @anthropic-ai/claude-code`
    - Or install the VS Code extension from the marketplace
    - Run `claude` in your terminal from your project directory to start a session
    - It reads `CLAUDE.md` in your project root for project-specific context

    **Key features to know:**
    - **Project awareness** — it reads your files and understands your codebase
    - **Command execution** — it can run shell commands and Python scripts on your behalf
    - **File editing** — it can create and modify files directly
    - **Iterative problem-solving** — it tries something, checks the result, and adjusts
    - **`CLAUDE.md`** — a file in your project root that gives Claude Code persistent instructions (what the project is, conventions to follow, etc.)

    Official docs: [https://docs.anthropic.com/en/docs/claude-code](https://docs.anthropic.com/en/docs/claude-code)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** Claude Code and the terminal are the same thing under the hood. When Claude Code runs a command, it's typing into your shell (zsh) just like you would. Every `pip install`, `git commit`, `mkdir`, and `python script.py` that Claude Code executes is a shell command running as a process on your Mac. Understanding the terminal (Module 02, notebooks 01-03) means you understand exactly what Claude Code is doing — and you can verify, modify, or reproduce its actions manually.
    """)
    return


@app.cell
def _(subprocess):
    # Check that Claude Code is installed
    #! which claude && claude --version
    subprocess.call(['which', 'claude', '&&', 'claude', '--version'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1.4 Claude.ai (Browser) — Your Thinking Partner

    **What it is:** The web interface to Claude at [https://claude.ai](https://claude.ai). Same AI model as Claude Code, but designed for conversation rather than coding. You can upload documents, paste long texts, and have extended discussions.

    **Why you need it:** Not everything is a coding task. When you want to brainstorm experimental designs, draft a rebuttal to Reviewer 2, summarize 15 papers on Nav1.7 inhibitors, or think through the logic of a statistical analysis before writing code — Claude.ai is the right tool. Upload a PDF of a paper and ask "What are the key methodological limitations?" Upload your grant aims and ask "How could I strengthen Aim 2?"

    **How to set it up:**
    - Go to [https://claude.ai](https://claude.ai) and create an account (or use your existing one)
    - The free tier gives you access to Claude; a Pro subscription ($20/month) gives higher usage limits and access to the latest models

    **Key features to know:**
    - **Document upload** — drag in PDFs, CSVs, images, and other files for Claude to analyze
    - **Projects** — organize conversations by topic (one for your grant, one for data analysis, etc.)
    - **Artifacts** — Claude can create interactive documents, code snippets, and visualizations inline
    - **Long context** — you can paste entire papers or datasets into the conversation
    - **No code execution** — unlike Claude Code, the browser version can't run code on your machine. Use it for thinking, then move to Claude Code for implementation.

    **When to use Claude.ai vs. Claude Code:**

    | Task | Use |
    |------|-----|
    | Write a Python script to process data | Claude Code |
    | Brainstorm experimental controls | Claude.ai |
    | Debug an error in your notebook | Claude Code |
    | Summarize a stack of papers | Claude.ai |
    | Create a figure for your paper | Claude Code |
    | Draft a response to reviewers | Claude.ai |
    | Install a package or configure a tool | Claude Code |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1.5 Git and GitHub — Version Control, Collaboration, Backup

    **What it is:** **Git** is a version control system that tracks every change you make to your files — like an unlimited undo history for your entire project. **GitHub** ([https://github.com](https://github.com)) is a website that hosts your git repositories online, enabling backup, sharing, and collaboration.

    **Why you need it:** Imagine you have a working analysis pipeline. You make "one small change" and everything breaks. With git, you can see exactly what changed and instantly go back to the working version. It also solves the `analysis_final_v3_REAL_final.py` problem — every version is saved automatically. And when you collaborate with a computational colleague, git lets you both work on the same code without overwriting each other's changes.

    **How to set it up:**
    - Git is pre-installed on macOS (or install via `xcode-select --install`)
    - Create a GitHub account at [https://github.com](https://github.com)
    - Configure your identity:
      ```bash
      git config --global user.name "Your Name"
      git config --global user.email "your.email@example.com"
      ```
    - Set up SSH keys for GitHub: [https://docs.github.com/en/authentication/connecting-to-github-with-ssh](https://docs.github.com/en/authentication/connecting-to-github-with-ssh)

    **Key features to know:**
    - `git status` — see what's changed
    - `git add` + `git commit` — save a snapshot of your work
    - `git log` — see the history of changes
    - `git diff` — see exactly what changed between versions
    - `git push` / `git pull` — sync with GitHub
    - `.gitignore` — tell git to ignore large data files, API keys, and virtual environments

    Reference: [MIT Missing Semester — Lecture 6: Version Control (Git)](https://missing.csail.mit.edu/2020/version-control/)
    Official docs: [https://git-scm.com/doc](https://git-scm.com/doc)
    """)
    return


@app.cell
def _(subprocess):
    # Verify git is installed and configured
    #! git --version
    subprocess.call(['git', '--version'])
    #! echo "User: $(git config --global user.name)"
    subprocess.call(['echo', 'User: $(git config --global user.name)'])
    #! echo "Email: $(git config --global user.email)"
    subprocess.call(['echo', 'Email: $(git config --global user.email)'])
    return


@app.cell
def _():
    # Check that this project is a git repository
    import subprocess, os

    os.chdir(os.path.expanduser("~/ai-tutorial"))
    result = subprocess.run(["git", "log", "--oneline", "-5"], capture_output=True, text=True)
    print("Recent commits in this project:")
    print(result.stdout if result.stdout else "(no commits yet)")
    return os, subprocess


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1.6 Python + Virtual Environments — The Runtime for Everything

    **What it is:** Python is the programming language that ties all your AI and data tools together. A **virtual environment** is an isolated space where you install packages for a specific project, so they don't interfere with other projects.

    **Why you need it:** Every analysis you'll do — from processing RNA-seq count matrices to calling the Claude API to making publication-quality figures — runs on Python. The virtual environment matters because your calcium imaging analysis might need `numpy 1.26` while a colleague's scRNA-seq pipeline needs `numpy 2.0`. Virtual environments keep each project's dependencies separate.

    **How to set it up:**
    - Python is already installed (this tutorial uses Python 3.14)
    - Your virtual environment is at `.venv/` in the project root
    - Activate it: `source .venv/bin/activate`
    - Install packages: `pip install pandas numpy matplotlib`
    - marimo uses the Python from this virtual environment automatically

    **Key features to know:**
    - `python --version` — check which Python you're running
    - `pip list` — see what packages are installed
    - `pip install <package>` — add a new package
    - `pip freeze > requirements.txt` — save your package list (for reproducibility)
    - `which python` — verify you're using the virtual environment's Python, not the system one

    Official docs: [https://docs.python.org/3/](https://docs.python.org/3/)
    Virtual environments: [https://docs.python.org/3/library/venv.html](https://docs.python.org/3/library/venv.html)
    """)
    return


@app.cell
def _():
    import sys
    print(f"Python version: {sys.version}")
    print(f"Python location: {sys.executable}")

    # Check if we're in a virtual environment
    in_venv = sys.prefix != sys.base_prefix
    print(f"In virtual environment: {in_venv}")
    if in_venv:
        print(f"Venv path: {sys.prefix}")
    return (sys,)


@app.cell
def _():
    # Check that the key packages are installed
    packages_to_check = ["marimo", "pandas", "numpy", "matplotlib", "seaborn", "anthropic"]

    for pkg in packages_to_check:
        try:
            mod = __import__(pkg)
            version = getattr(mod, "__version__", "installed")
            print(f"  {pkg:15s} {version}")
        except ImportError:
            print(f"  {pkg:15s} NOT INSTALLED")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1.7 marimo Notebooks — Interactive Analysis Environment

    **What it is:** marimo notebooks are reactive Python notebooks stored as plain `.py` files. They mix executable code, rich text, equations, and visualizations in a single file. You're reading one right now.

    **Why you need it:** Notebooks match how research actually works. When you're exploring calcium imaging data, you don't write a complete script upfront — you load the data, look at it, try a filter, plot the result, adjust parameters, plot again. Notebooks let you work step-by-step, keeping your results and your reasoning together. They're also perfect for sharing — you can send a colleague a notebook that shows exactly what you did, with the figures inline. Because marimo notebooks are plain `.py` files, they work with git version control without merge conflicts.

    **How to set it up:**
    - Already installed in your virtual environment (`pip install marimo`)
    - Open `.py` marimo files directly in VS Code (with the marimo extension)
    - Or launch from the terminal: `marimo edit notebook.py`
    - marimo uses the Python from your active virtual environment — no kernel to configure

    **Key features to know:**
    - **Cell types** — Code cells (Python) and Markdown cells (via `mo.md()`)
    - **Run a cell** — `Shift+Enter` (runs and moves to next cell) or `Ctrl+Enter` (runs and stays)
    - **Reactivity** — when you change a cell, all dependent cells automatically re-run
    - **Cell output** — results, plots, and errors appear directly below each code cell
    - **No hidden state** — marimo enforces a clean execution model, preventing the "run cells out of order" bugs common in traditional notebooks
    - **Run All** — execute every cell top-to-bottom (guaranteed to work because of reactivity)

    Official docs: [https://docs.marimo.io/](https://docs.marimo.io/)
    """)
    return


@app.cell
def _():
    # Quick check: what kernel is this notebook using?
    import IPython
    print(f"IPython version: {IPython.__version__}")
    print(f"Kernel info: {IPython.sys_info()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Part 2: Important Tools (You'll Need These Soon)

    These aren't urgent, but you'll want them within the next few weeks as you work through this tutorial and start using AI in your research.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2.1 Anthropic API Account + API Key — Programmatic Claude Access

    **What it is:** The Anthropic API lets you call Claude from your own Python scripts — no browser, no chat window. You send a message, Claude sends back a response, and your code processes it however you want.

    **Why you need it:** This is where AI becomes truly powerful for research. Instead of manually asking Claude to summarize papers one at a time, you write a script that loops through 200 papers and extracts structured data from each. You could batch-process patient survey responses, auto-annotate gene lists, or build a pipeline that reads raw behavioral data and produces a formatted summary. We'll build exactly these workflows in Module 07.

    **How to set it up:**
    1. Create an account at [https://console.anthropic.com/](https://console.anthropic.com/)
    2. Add billing (API usage is pay-per-use, typically pennies per query)
    3. Generate an API key: Console > API Keys > Create Key
    4. Store the key securely — **never put it in your code or commit it to git**
    5. Set it as an environment variable:
       ```bash
       # Add this line to your ~/.zshrc
       export ANTHROPIC_API_KEY="sk-ant-..."
       ```
       Or use a `.env` file (which is listed in `.gitignore`)

    **Key features to know:**
    - The `anthropic` Python package is already installed in your environment
    - You pay per token (roughly per word) — monitoring costs is important
    - Different models have different capabilities and prices
    - Rate limits apply — you can't send 1000 requests per second

    Official docs: [https://docs.anthropic.com/en/api/getting-started](https://docs.anthropic.com/en/api/getting-started)
    """)
    return


@app.cell
def _(os):
    api_key = os.environ.get('ANTHROPIC_API_KEY', '')
    if api_key:
    # Check if the API key is configured (without revealing it)
        print(f'API key found: {api_key[:10]}...{api_key[-4:]}')
        print(f'Key length: {len(api_key)} characters')
    else:
        print('No ANTHROPIC_API_KEY found in environment.')  # Show just enough to confirm it's real, without exposing the key
        print("You'll set this up before Module 07. No rush.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2.2 GitHub Copilot — Real-Time Code Suggestions

    **What it is:** An AI code completion tool from GitHub that suggests code as you type, directly in your editor. Think of it as aggressive autocomplete that understands what you're trying to do.

    **Why you need it:** Copilot and Claude Code are complementary, not redundant. Claude Code is a conversation — you describe a task and it builds a solution. Copilot is a co-pilot (literally) — it watches you type and suggests the next line or block. When you're writing a loop to iterate through `.tif` calcium imaging files, Copilot will suggest the glob pattern before you finish typing. When you start typing `plt.xlabel(`, it'll suggest the label based on your data variable names.

    **How to set it up:**
    1. Sign up at [https://github.com/features/copilot](https://github.com/features/copilot) (free for verified students/educators, otherwise $10/month)
    2. Install the **GitHub Copilot** extension in VS Code
    3. Sign in with your GitHub account
    4. Suggestions appear automatically as you type — press `Tab` to accept

    **Key features to know:**
    - **Inline suggestions** — ghost text appears as you type; press Tab to accept
    - **Multiple suggestions** — press `Alt+]` to cycle through alternatives
    - **Comment-driven coding** — write a comment describing what you want, and Copilot suggests the code
    - **Context-aware** — it reads your open files and variable names to make relevant suggestions

    Official docs: [https://docs.github.com/en/copilot](https://docs.github.com/en/copilot)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2.3 Zotero + Better BibTeX — Reference Management with AI Potential

    **What it is:** Zotero is a free, open-source reference manager. Better BibTeX is a plugin that gives every reference a stable citation key and auto-exports your library to BibTeX format.

    **Why you need it (beyond what you already do):** You already use Zotero for managing references. The integration angle is what changes: with Better BibTeX exporting your library to a `.bib` file, you can write Python scripts that programmatically access your references. Imagine a script that takes your Zotero library, extracts all papers on TRPV1 from the last 3 years, sends their abstracts to the Claude API, and generates a structured literature summary table — with proper citations. That's Module 07 territory.

    **How to set it up (the new parts):**
    1. Install Better BibTeX: [https://retorque.re/zotero-better-bibtex/](https://retorque.re/zotero-better-bibtex/)
    2. Configure auto-export: Zotero > Preferences > Better BibTeX > Automatic Export
    3. Export your library (or a collection) to a `.bib` file in your project directory
    4. Now Python can read your references using the `bibtexparser` package

    **Key features to know:**
    - **Stable citation keys** — e.g., `basbaum2009CellularMolecularMechanisms` instead of random IDs
    - **Auto-export** — your `.bib` file updates automatically when you add papers to Zotero
    - **PDF storage** — Zotero stores PDFs that you can feed to Claude.ai for analysis
    - **Zotero API** — programmatic access to your library (for advanced workflows)

    Zotero: [https://www.zotero.org/](https://www.zotero.org/)
    Better BibTeX: [https://retorque.re/zotero-better-bibtex/](https://retorque.re/zotero-better-bibtex/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2.4 Obsidian — Knowledge Management with AI Integration

    **What it is:** A note-taking app that stores everything as plain Markdown files on your computer (not in the cloud). Notes link to each other, forming a personal knowledge graph.

    **Why you need it (the AI angle):** You already use Obsidian for notes. The power move is connecting it to your AI workflow. Because Obsidian notes are just Markdown files in a folder, Claude Code can read and search them directly. You can ask Claude Code to "find all my notes about CGRP signaling" or "create a new note summarizing today's experiment." Community plugins like **Smart Connections** add semantic search powered by AI embeddings — find related notes by meaning, not just keywords.

    **How to set it up (the AI parts):**
    1. Make sure your Obsidian vault is a folder on your local filesystem (which it is by default)
    2. Explore the **Smart Connections** community plugin for AI-powered note search
    3. Since notes are Markdown, you can include them in Claude Code conversations or feed them to the Claude API

    **Key features to know:**
    - **Local-first** — your notes are `.md` files on your disk, not locked in a proprietary format
    - **Backlinks** — see which notes reference the current note (great for connecting concepts)
    - **Graph view** — visualize how your notes connect to each other
    - **Community plugins** — hundreds of extensions including AI-powered ones
    - **Templates** — create standard formats for experiment notes, paper summaries, etc.

    Official site: [https://obsidian.md/](https://obsidian.md/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Part 3: Emerging Tools (Worth Watching)

    The AI tooling landscape is moving fast. These tools are either new, rapidly evolving, or not yet essential — but they may become part of your workflow within the next year.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3.1 Cursor — AI-Native Code Editor

    **What it is:** A code editor built from the ground up around AI assistance. It's a fork of VS Code, so it looks and feels the same, but AI features (chat, inline edits, codebase-wide understanding) are deeply integrated rather than bolted on as extensions.

    **Why it might matter:** If you find yourself wishing Claude Code were more tightly woven into the editing experience — selecting code and saying "refactor this," or having the AI see every file you have open — Cursor is exploring that direction. It can also use multiple AI models (Claude, GPT-4, etc.).

    **Current status:** Functional and popular, with a free tier. Worth trying once you're comfortable with VS Code + Claude Code. Your VS Code extensions and settings can be imported.

    Official site: [https://cursor.com/](https://cursor.com/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** Which AI-assisted code editor should you use?
    >
    > | Option | Pros | Cons | Use when... |
    > |--------|------|------|-------------|
    > | **VS Code + Claude Code** | Free, industry standard, massive extension ecosystem, Claude Code runs in terminal alongside your editor, full control over prompts | Claude Code is terminal-based (not inline), requires switching between editor and terminal | You want a stable, extensible editor AND powerful AI assistance via the terminal. Best for: complex multi-file projects, when you want full control over AI interactions |
    > | **Cursor** | AI deeply integrated into the editor (inline completions, chat, cmd-K editing), fast iteration on code changes | Paid after trial, smaller extension ecosystem than VS Code, AI suggestions can be distracting, less control over what the AI sees | You want AI woven into every keystroke. Best for: rapid prototyping, writing new code from scratch, when you want maximum AI integration |
    > | **Windsurf (Codeium)** | Free tier available, good inline completions, similar to Cursor's approach | Newer/less mature, smaller community, fewer integrations | You want a Cursor-like experience with a free tier |
    > | **GitHub Copilot** (in VS Code) | Great inline completions, integrates with VS Code, backed by GitHub/Microsoft | Paid, completions only (no chat-based editing in free tier), less control over context | You want fast autocomplete-style AI help while typing, especially for boilerplate code |
    >
    > **Our recommendation for this tutorial:** VS Code + Claude Code. VS Code gives you the most stable, well-supported editor, and Claude Code gives you the most powerful AI assistance for complex research tasks. You can always add Copilot for inline completions too — they complement each other.

    > 💡 **Tip:** Set up your tools in the right order. The dependencies flow downward, so install in this sequence: (1) VS Code, (2) Terminal/shell configuration, (3) Homebrew, (4) Python + venv, (5) Git, (6) Claude Code, (7) marimo, (8) API keys. Skipping ahead (e.g., trying to install Python packages before setting up the venv) creates problems that are harder to debug than just following the order.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3.2 Claude Desktop + MCP — Local AI with Tool Access

    **What it is:** The Claude Desktop app runs Claude on your computer with access to **Model Context Protocol (MCP)** servers — plugins that let Claude interact with external tools, databases, and APIs. For example, an MCP server could let Claude directly query a database, access your file system, or search PubMed.

    **Why it might matter:** Imagine asking Claude: "Look up the latest papers on TRPA1 cold sensitivity in PubMed, download the top 5, and summarize their methods sections." With MCP servers, Claude can actually do each of those steps — not just tell you how. This turns Claude from a text-in/text-out system into an agent that can take actions.

    **Current status:** Claude Desktop is available. MCP is an open protocol with a growing ecosystem of community-built servers. It's early days but developing quickly.

    Claude Desktop: [https://claude.ai/download](https://claude.ai/download)
    MCP specification: [https://modelcontextprotocol.io/](https://modelcontextprotocol.io/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3.3 Windsurf — Another AI-Native Editor

    **What it is:** An AI-native code editor (formerly Codeium), similar in concept to Cursor. It emphasizes "agentic" workflows where the AI can make multi-file changes and run commands autonomously.

    **Why it might matter:** Another strong contender in the AI editor space. The competition between Cursor, Windsurf, and VS Code + extensions is driving rapid innovation. You benefit no matter which wins.

    **Current status:** Available with a free tier. The AI editor market is competitive and evolving rapidly.

    Official site: [https://windsurf.com/](https://windsurf.com/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3.4 NotebookLM (Google) — Document Analysis and Podcast Generation

    **What it is:** A Google tool where you upload documents (papers, notes, reports) and get an AI that is grounded exclusively in those sources. It can answer questions, generate summaries, and even create an audio "podcast" discussion of your material.

    **Why it might matter:** Upload 10 papers on inflammatory mediator sensitization of nociceptors, and NotebookLM becomes an expert on exactly that topic — it won't hallucinate facts from outside your sources. The podcast feature is surprisingly useful: listening to a 10-minute audio summary of a dense paper while walking to the lab can prime your understanding before you sit down to read it in detail.

    **Current status:** Free to use. Good for literature review and document comprehension. Limited compared to Claude for general reasoning or coding.

    Official site: [https://notebooklm.google.com/](https://notebooklm.google.com/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3.5 Open-Source Models via Ollama — Local LLMs for Privacy-Sensitive Work

    **What it is:** Ollama lets you run open-source language models (Llama, Mistral, Gemma, etc.) entirely on your own computer. No data leaves your machine — everything runs locally.

    **Why it might matter:** If you work with protected health information (PHI), HIPAA-covered data, or unpublished results you're not comfortable sending to a cloud API, local models give you AI capabilities with complete data privacy. The trade-off: local models are smaller and less capable than Claude or GPT-4, and they require decent hardware (a Mac with 16GB+ RAM can run useful models).

    **How to try it:**
    1. Install Ollama: [https://ollama.com/](https://ollama.com/)
    2. Pull a model: `ollama pull llama3.2`
    3. Chat with it: `ollama run llama3.2`
    4. Or call it from Python — Ollama exposes a local API compatible with the OpenAI client library

    **Current status:** Easy to set up, useful for privacy-sensitive tasks, but not a replacement for Claude or GPT-4 for complex reasoning. Best for simple text processing, summarization, or classification of sensitive data.

    Official site: [https://ollama.com/](https://ollama.com/)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Part 4: How These Connect — The AI Researcher's Workflow

    These tools aren't isolated. They form a connected workflow where the output of one feeds into the next. Here's how they fit together for a typical AI-augmented research project:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```
                            YOUR AI RESEARCH WORKFLOW
                            ========================

        COLLECT                    THINK                     BUILD
        ──────                    ─────                     ─────
        ┌──────────┐         ┌────────────┐          ┌────────────────┐
        │  Zotero  │────────►│  Claude.ai │─────────►│   VS Code      │
        │  (papers)│         │  (reason,  │          │  + Claude Code │
        └──────────┘         │   plan)    │          │  (write code)  │
             │               └────────────┘          └───────┬────────┘
             │                     ▲                         │
             │                     │                         │
        ┌──────────┐          ┌────────────┐          ┌──────▼────────┐
        │ Obsidian │◄────────►│   Notes,   │          │    Python     │
        │ (notes)  │          │   ideas    │          │  + marimo     │
        └──────────┘          └────────────┘          │  (analysis)   │
                                                      └───────┬───────┘
                                                              │
        AUTOMATE                  SHARE                       │
        ────────                  ─────                       │
        ┌──────────────┐    ┌─────────────┐           ┌──────▼───────┐
        │  Claude API  │◄───┤  Git/GitHub │◄──────────┤   Results,   │
        │  (batch      │    │  (version   │           │   figures    │
        │   process)   │    │   control)  │           └──────────────┘
        └──────────────┘    └─────────────┘
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### A concrete example: from paper to analysis

    Here's how these tools chain together for a real research task:

    1. **Zotero** — You find 20 papers on Nav1.7 gain-of-function mutations in erythromelalgia. They're organized in a Zotero collection with PDFs attached.

    2. **Claude.ai** — You upload 3 key papers and ask: "What electrophysiology protocols were used to characterize the mutant channels? What were the common voltage protocols?" Claude helps you identify the standard approach.

    3. **Obsidian** — You create a note summarizing the consensus protocol and your planned modifications.

    4. **VS Code + Claude Code** — You ask Claude Code to write a Python script that reads your electrophysiology `.abf` files, extracts activation curves, and fits Boltzmann functions.

    5. **Python + marimo** — You run the analysis interactively, tweaking parameters and inspecting plots. The notebook documents every step.

    6. **Claude API** — You write a script that sends each mutation's electrophysiology summary to Claude and asks it to compare against published data for that mutation.

    7. **Git/GitHub** — Every version of your analysis is tracked. Your collaborator can pull the repo and reproduce your results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Where each tool excels

    | Task | Best tool | Why |
    |------|-----------|-----|
    | Manage and organize papers | Zotero | Built for reference management |
    | Think through a problem, brainstorm | Claude.ai | Long-form conversation with document upload |
    | Write and debug code | VS Code + Claude Code | Full project context, can run and test code |
    | Explore data interactively | marimo notebook | Step-by-step execution with inline plots |
    | Process data at scale (100+ items) | Claude API + Python | Programmatic, automated, scriptable |
    | Track changes, collaborate | Git + GitHub | Version control is irreplaceable |
    | Take and connect research notes | Obsidian | Local Markdown, backlinks, graph view |
    | Handle sensitive/PHI data with AI | Ollama (local models) | Data never leaves your machine |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    # Setup Checklist

    Here's what to install and configure, in order. Items marked with a checkmark are things you likely already have.

    ### Phase 1: Foundation (do this now)

    - [ ] **macOS Command Line Tools** — `xcode-select --install` (gives you git and basic dev tools)
    - [ ] **Homebrew** — [https://brew.sh](https://brew.sh) (Mac package manager, needed for many tools)
    - [ ] **VS Code** — [https://code.visualstudio.com/](https://code.visualstudio.com/)
      - [ ] Python extension installed
      - [ ] marimo extension installed
      - [ ] Shell command `code` available in PATH (VS Code > Command Palette > "Shell Command: Install")
    - [ ] **Python 3.12+** — via Homebrew (`brew install python`) or [https://www.python.org/](https://www.python.org/)
    - [ ] **Virtual environment** — created and activated for this project (`.venv/`)
    - [ ] **Core packages** — `pip install marimo pandas numpy matplotlib seaborn anthropic`
    - [ ] **marimo** — `marimo --version` prints a version number
    - [ ] **Git configured** — `git config --global user.name` and `user.email` set
    - [ ] **GitHub account** — [https://github.com](https://github.com) with SSH keys configured

    ### Phase 2: AI Tools (do this week)

    - [ ] **Claude Code** — `npm install -g @anthropic-ai/claude-code` (requires Node.js: `brew install node`)
    - [ ] **Claude.ai account** — [https://claude.ai](https://claude.ai) (consider Pro subscription for heavier use)
    - [ ] **CLAUDE.md** — in your project root, giving Claude Code project context

    ### Phase 3: Research Integration (this month)

    - [ ] **Anthropic API key** — [https://console.anthropic.com/](https://console.anthropic.com/), stored as `ANTHROPIC_API_KEY` environment variable
    - [ ] **GitHub Copilot** — [https://github.com/features/copilot](https://github.com/features/copilot), VS Code extension installed
    - [ ] **Better BibTeX** for Zotero — [https://retorque.re/zotero-better-bibtex/](https://retorque.re/zotero-better-bibtex/), auto-export configured
    - [ ] **Obsidian AI plugins** — explore Smart Connections or similar

    ### Phase 4: Explore (when you're curious)

    - [ ] **Cursor** — [https://cursor.com/](https://cursor.com/) (try importing your VS Code config)
    - [ ] **Ollama** — [https://ollama.com/](https://ollama.com/) (for local/private AI work)
    - [ ] **Claude Desktop** — [https://claude.ai/download](https://claude.ai/download) (for MCP integrations)
    - [ ] **NotebookLM** — [https://notebooklm.google.com/](https://notebooklm.google.com/) (for literature review)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Quick environment check

    Run this cell to verify the essential tools are set up on your system:
    """)
    return


@app.cell
def _(os, sys):
    import shutil
    print('=' * 50)
    print('  AI TOOLKIT ENVIRONMENT CHECK')
    print('=' * 50)
    print()
    tools = {'python3': 'Python interpreter', 'git': 'Version control', 'code': 'VS Code', 'claude': 'Claude Code', 'node': 'Node.js (needed for Claude Code)', 'marimo': 'marimo'}
    print('Command-line tools:')
    for cmd, description in tools.items():
    # Check command-line tools
        path = shutil.which(cmd)
        status = 'FOUND' if path else 'NOT FOUND'
        symbol = '+' if path else '-'
        print(f'  [{symbol}] {description:30s} ({cmd}) — {status}')
    print()
    packages = ['marimo', 'pandas', 'numpy', 'matplotlib', 'seaborn', 'anthropic']
    print('Python packages:')
    for pkg_1 in packages:
        try:
            __import__(pkg_1)
            print(f'  [+] {pkg_1:30s} — INSTALLED')
        except ImportError:
            print(f'  [-] {pkg_1:30s} — NOT INSTALLED')
    print()
    in_venv_1 = sys.prefix != sys.base_prefix
    print(f"Virtual environment active: {('Yes' if in_venv_1 else 'No')}")
    print(f'Python: {sys.executable}')
    print()
    # Check Python packages
    api_key_1 = os.environ.get('ANTHROPIC_API_KEY', '')
    print(f"Anthropic API key configured: {('Yes' if api_key_1 else 'No (not needed yet)')}")
    print()
    # Check virtual environment
    # Check API key (without exposing it)
    print('=' * 50)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - **VS Code** is your central workspace — editor, terminal, notebooks, and AI tools in one window
    - **Terminal/zsh** is how you (and Claude Code) control your computer directly
    - **Claude Code** writes, runs, and debugs code within your project context
    - **Claude.ai** is for thinking, brainstorming, and working with documents — no code execution
    - **Git/GitHub** tracks every change and enables collaboration and backup
    - **Python + virtual environments** keep your projects isolated and reproducible
    - **marimo notebooks** let you explore data interactively with inline results
    - **The API** (coming in Module 07) lets you automate AI tasks at scale
    - **Copilot** complements Claude Code with real-time code suggestions
    - **Zotero** and **Obsidian** become more powerful when connected to your AI workflow
    - **Emerging tools** (Cursor, MCP, Ollama) are expanding what's possible — worth watching but not urgent

    The key insight: these tools form a connected system, not a collection of isolated apps. The more you understand how data flows between them, the more effectively you'll use each one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    ### Essential Tools
    - [VS Code](https://code.visualstudio.com/) — download and documentation for Visual Studio Code
    - [Claude Code](https://docs.anthropic.com/en/docs/claude-code) — Anthropic's official CLI for Claude, documentation and setup guide
    - [Claude.ai](https://claude.ai/) — the web interface for Claude conversations
    - [Git](https://git-scm.com/) — official Git site with documentation and downloads
    - [GitHub](https://github.com/) — code hosting, collaboration, and version control platform
    - [Python](https://www.python.org/) — official Python site; see the [tutorial](https://docs.python.org/3/tutorial/) for getting started
    - [marimo](https://marimo.io/) — the marimo project; see [marimo docs](https://docs.marimo.io/) for the full guide

    ### Important Tools
    - [Anthropic API](https://docs.anthropic.com/en/api/getting-started) — getting started with the Claude API, including key management and pricing
    - [GitHub Copilot](https://github.com/features/copilot) — AI-powered code completion for VS Code
    - [Zotero](https://www.zotero.org/) — free, open-source reference manager; see [Better BibTeX plugin](https://retorque.re/zotero-better-bibtex/)
    - [Obsidian](https://obsidian.md/) — knowledge management app with markdown notes and graph visualization

    ### Emerging Tools
    - [Cursor](https://cursor.com/) — AI-native code editor built on VS Code
    - [Claude Desktop + MCP](https://docs.anthropic.com/en/docs/claude-code/mcp) — Claude Desktop with Model Context Protocol for tool integration
    - [Windsurf](https://codeium.com/windsurf) — AI-native code editor (formerly Codeium)
    - [NotebookLM](https://notebooklm.google/) — Google's document analysis and synthesis tool
    - [Ollama](https://ollama.ai/) — run open-source LLMs locally for privacy-sensitive work
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Networking and APIs](03-networking-and-apis.py) | [Module Index](../README.md) | [Next: What Is an LLM? \u2192](../03-how-llms-work/01-what-is-an-llm.py)
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
    - 2026-03-25: Added standardized callouts and decision frameworks
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

