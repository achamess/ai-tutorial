import marimo

__generated_with = "0.21.1"
app = marimo.App()


@app.cell
def _():
    import marimo as mo

    return (mo,)


@app.cell
def _():
    import subprocess

    return (subprocess,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    # 01: The Filesystem and the Shell

    When Claude Code runs a command like `mkdir data/calcium_imaging` or reads a file, it's navigating your computer's **filesystem** — the same tree of folders and files you see in Finder. This notebook gives you the mental model for what's actually happening.

    > **Reference:** This notebook parallels [MIT Missing Semester — Lecture 1: Course Overview + The Shell](https://missing.csail.mit.edu/2020/course-shell/). That lecture is worth watching in full — it covers the same ideas with more depth.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Data Structures in Practice](../01-python-foundations/04-data-structures-in-practice.py) | [Module Index](../README.md) | [Next: Processes and Environment \u2192](02-processes-and-environment.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Claude Code reads, writes, and manipulates files on your computer constantly. If you don't understand paths and directories, you can't verify where it's putting your data or catch mistakes like writing to the wrong folder.
    > - When Claude Code says "I'll create `data/calcium_imaging/peak_amplitudes.csv`," you need to know what that means, where that file will end up, and how to find it. That's filesystem literacy.
    > - Every "file not found" error you'll encounter — whether from a Python script, Claude Code, or a bioinformatics tool like RFdiffusion — comes down to a path problem. This notebook gives you the mental model to debug them instantly.
    > - The shell commands here (`ls`, `cd`, `cat`, `grep`) are exactly what Claude Code runs under the hood. Understanding them means understanding what Claude Code is actually doing on your machine.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What is a filesystem?

    Your computer stores everything — documents, code, images, data — in a **tree structure**. It's like the organizational hierarchy of folders you see in Finder, but the tree goes all the way down to a single root.

    ```
    /                          ← the root (top of the tree)
    ├── Users/
    │   └── alex/              ← your home directory (~)
    │       ├── Desktop/
    │       ├── Documents/
    │       ├── Downloads/
    │       └── ai-tutorial/   ← this project!
    │           ├── 01-python-foundations/
    │           ├── 02-your-computer/
    │           └── ...
    ├── Applications/
    ├── tmp/
    └── ...
    ```

    Every file on your Mac has a unique **path** — an address that describes how to get from the root to that file. When Claude Code says it's reading `/Users/alex/ai-tutorial/CLAUDE.md`, that's a path.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph TD
        ROOT["/  (root)"]
        ROOT --> USERS["/Users"]
        ROOT --> APPS["/Applications"]
        ROOT --> TMP["/tmp"]
        ROOT --> USR["/usr"]
        ROOT --> OPT["/opt"]

        USERS --> ALEX["/Users/alex  ~"]
        ALEX --> DESK["Desktop/"]
        ALEX --> DOCS["Documents/"]
        ALEX --> DOWN["Downloads/"]
        ALEX --> AI["<b>ai-tutorial/</b>"]
        ALEX --> ZSHRC[".zshrc"]

        AI --> M01["01-python-foundations/"]
        AI --> M02["02-your-computer/"]
        AI --> M03["03-how-llms-work/"]
        AI --> M04["04-prompt-engineering/"]
        AI --> VENV[".venv/"]
        AI --> GIT[".git/"]
        AI --> CMD["CLAUDE.md"]

        USR --> LOCAL["/usr/local/bin/<br/>Homebrew tools"]
        OPT --> BREW["/opt/homebrew/<br/>Homebrew (Apple Silicon)"]

        style ROOT fill:#cc4444,color:#fff
        style ALEX fill:#4488cc,color:#fff
        style AI fill:#44aa88,color:#fff
        style VENV fill:#888,color:#fff
        style GIT fill:#888,color:#fff
        style ZSHRC fill:#888,color:#fff
    ```

    Dotfiles (gray) are hidden -- they start with `.` and don't show up in Finder. The `ai-tutorial` directory (green) is where all your work for this course lives.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Paths: absolute vs. relative

    There are two ways to describe a location:

    | Type | Starts with | Example | Meaning |
    |------|------------|---------|--------|
    | **Absolute** | `/` | `/Users/alex/ai-tutorial/CLAUDE.md` | Full address from the root |
    | **Relative** | anything else | `../01-python-foundations/01-your-first-code.py` | Address relative to where you are now |

    **Special path symbols:**
    - `/` — the root of the filesystem (top of the tree)
    - `~` — shorthand for your home directory (`/Users/alex`)
    - `.` — the current directory ("right here")
    - `..` — the parent directory ("one level up")

    Think of it like giving directions in a building. Absolute: "Room 314, Building A, 3rd floor." Relative: "Two doors down on the left."

    > See the [Python `pathlib` docs](https://docs.python.org/3/library/pathlib.html) for the full API reference, and [Apple's File System Basics](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html) for macOS-specific filesystem details.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** Absolute vs. relative paths. An absolute path starts from `/` (the root) and works everywhere, regardless of where you are. A relative path starts from your current directory and only works from that location. When you see `/Users/alex/ai-tutorial/data/genes.txt`, that's absolute — it's an unambiguous address. When you see `../data/genes.txt`, that's relative — it means "go up one directory, then into data/." Most "file not found" errors come from using a relative path when you're in the wrong directory. When in doubt, use absolute paths.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Let's see this in action with Python. The `pathlib` module is Python's way of working with paths.
    """)
    return


@app.cell
def _():
    from pathlib import Path

    # Your home directory
    home = Path.home()
    print(f"Home directory: {home}")

    # The current working directory (where this notebook is running)
    cwd = Path.cwd()
    print(f"Current directory: {cwd}")

    # Build a path to this project
    project = home / "ai-tutorial"
    print(f"Project directory: {project}")
    print(f"Does it exist? {project.exists()}")
    return Path, project


@app.cell
def _(project):
    # Paths have parts you can inspect
    claude_md = project / "CLAUDE.md"

    print(f"Full path:  {claude_md}")
    print(f"File name:  {claude_md.name}")       # just the filename
    print(f"Stem:       {claude_md.stem}")        # filename without extension
    print(f"Extension:  {claude_md.suffix}")      # just the extension
    print(f"Parent dir: {claude_md.parent}")      # the folder it's in
    print(f"Is a file?  {claude_md.is_file()}")
    print(f"Is a dir?   {claude_md.is_dir()}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Your Mac's key directories

    Here are the directories you'll encounter most often:

    | Directory | What's there | When you'll care |
    |-----------|-------------|------------------|
    | `/Users/alex/` | Your home — everything personal | Always |
    | `/Applications/` | Installed apps (VS Code, etc.) | Rarely |
    | `/tmp/` | Temporary files, cleared on reboot | When debugging |
    | `/usr/local/bin/` | Command-line tools you install (Homebrew) | When `which` shows you where things live |
    | `/opt/homebrew/` | Homebrew's home on Apple Silicon Macs | When installing tools |

    Let's check some of these exist on your Mac:
    """)
    return


@app.cell
def _(Path):
    key_dirs = [
        Path.home(),
        Path("/Applications"),
        Path("/tmp"),
        Path("/usr/local/bin"),
        Path("/opt/homebrew"),
    ]

    for d in key_dirs:
        status = "exists" if d.exists() else "not found"
        print(f"{str(d):30s} — {status}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 💡 **Tip:** Tab completion is your best friend in the terminal. Start typing a file or directory name and press `Tab` — the shell will auto-complete it. If there are multiple matches, press `Tab` twice to see all options. This prevents typos in paths (a leading cause of errors), saves typing, and is how experienced users navigate the filesystem quickly. It works for commands too — try typing `git st` and pressing Tab.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The terminal and the shell

    The **terminal** is an app that gives you a text interface to your computer. The **shell** is the program running inside it that interprets your commands.

    On your Mac, the shell is **zsh** (Z shell). When you open Terminal.app or the VS Code terminal, you're talking to zsh.

    Every command has the same basic structure:

    ```
    command  [flags]  [arguments]
    ```

    For example:
    ```bash
    ls -la ~/ai-tutorial
    ```
    - `ls` — the command (list files)
    - `-la` — flags (`-l` for long format, `-a` for all including hidden)
    - `~/ai-tutorial` — the argument (which directory to list)

    **This is exactly what Claude Code does.** When Claude Code runs commands on your behalf, it's typing into a shell just like you would.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Essential shell commands

    These are the commands you'll see Claude Code running, and the ones you'll use yourself:

    | Command | What it does | Example |
    |---------|-------------|--------|
    | `pwd` | Print working directory (where am I?) | `pwd` |
    | `ls` | List files | `ls -la` |
    | `cd` | Change directory | `cd ~/ai-tutorial` |
    | `mkdir` | Make a new directory | `mkdir data` |
    | `cp` | Copy a file | `cp results.csv backup.csv` |
    | `mv` | Move or rename a file | `mv old_name.py new_name.py` |
    | `rm` | Remove a file (**no undo!**) | `rm temp.txt` |
    | `cat` | Print file contents | `cat CLAUDE.md` |
    | `head` | Print first N lines | `head -20 data.csv` |
    | `less` | Scroll through a file | `less big_file.txt` (press `q` to quit) |
    | `which` | Find where a program lives | `which python` |

    Let's run some of these from Python. In marimo, you can run shell commands using subprocess:
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** `rm` has no undo. When you run `rm file.txt`, that file is gone — it does not go to the Trash. And `rm -rf directory/` will delete a directory and everything inside it, instantly, without asking for confirmation. Claude Code will sometimes suggest `rm` commands; always read them carefully before approving. If you're not sure, use `mv` to move the file to a temporary location instead of deleting it. The most dangerous command on any Unix system is `rm -rf /` — which would try to delete your entire filesystem.
    """)
    return


@app.cell
def _(subprocess):
    # Where are we right now?
    #! pwd
    subprocess.call(['pwd'])
    return


@app.cell
def _(subprocess):
    # List files in the project root, including hidden ones
    #! ls -la ~/ai-tutorial/
    subprocess.call(['ls', '-la', '~/ai-tutorial/'])
    return


@app.cell
def _(subprocess):
    # Where does Python live on this system?
    #! which python
    subprocess.call(['which', 'python'])
    return


@app.cell
def _(subprocess):
    # Show the first 5 lines of CLAUDE.md
    #! head -5 ~/ai-tutorial/CLAUDE.md
    subprocess.call(['head', '-5', '~/ai-tutorial/CLAUDE.md'])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Doing the same things with Python's pathlib

    Every shell command has a Python equivalent. Here's the mapping — you don't need to memorize both, but it helps to see that they're doing the same thing.
    """)
    return


@app.cell
def _(Path):
    project_1 = Path.home() / 'ai-tutorial'
    print('Files in project root:')
    for item in sorted(project_1.iterdir()):
        kind = 'dir' if item.is_dir() else 'file'
    # ls — list files in a directory
        print(f'  {kind:4s}  {item.name}')
    return (project_1,)


@app.cell
def _(project_1):
    # cat — read a file's contents
    claude_md_1 = project_1 / 'CLAUDE.md'
    contents = claude_md_1.read_text()
    first_10_lines = contents.split('\n')[:10]
    # head — just the first few lines
    for line in first_10_lines:
        print(line)
    return


@app.cell
def _(project_1):
    # mkdir — create a directory
    # (exist_ok=True means "don't error if it already exists")
    temp_dir = project_1 / '02-your-computer' / '_scratch'
    temp_dir.mkdir(exist_ok=True)
    print(f'Created: {temp_dir}')
    print(f'Exists?  {temp_dir.exists()}')
    return (temp_dir,)


@app.cell
def _(temp_dir):
    # Write a file, then read it back (like echo > and cat)
    test_file = temp_dir / "test_data.txt"
    test_file.write_text("TRPV1\nTRPA1\nNaV1.7\nNaV1.8\n")

    print("Contents:")
    print(test_file.read_text())
    return


@app.cell
def _(project_1):
    # Find files matching a pattern (like ls *.py, but recursive)
    print('All notebooks in the project:')
    for nb in sorted(project_1.glob('**/*.py')):
        print(f'  {nb.relative_to(project_1)}')  # Show the path relative to the project root
    return


@app.cell
def _(temp_dir):
    # Clean up our scratch directory
    import shutil

    if temp_dir.exists():
        shutil.rmtree(temp_dir)
        print(f"Removed: {temp_dir}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why permissions matter for you:** Your `.env` file containing your `ANTHROPIC_API_KEY` should be readable only by you — not accidentally committed to GitHub where anyone can use your API credits. Understanding permissions is how you keep secrets secret.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## File permissions

    Every file on your Mac has **permissions** that control who can do what:

    - **r** (read) — can you look at the contents?
    - **w** (write) — can you change the contents?
    - **x** (execute) — can you run it as a program?

    When you see `ls -l` output like `-rw-r--r--`, that's three sets of rwx: **owner**, **group**, **everyone else**.

    You'll mostly encounter permissions when:
    - A command fails with "Permission denied" — you might need `sudo` (run as administrator)
    - A script won't run — it might need execute permission (`chmod +x script.sh`)
    - An API key file should be private — you want only your user to read it
    """)
    return


@app.cell
def _(Path):
    import os
    import stat
    claude_md_2 = Path.home() / 'ai-tutorial' / 'CLAUDE.md'
    # Check permissions on CLAUDE.md
    file_stat = claude_md_2.stat()
    mode = stat.filemode(file_stat.st_mode)
    print(f'File: {claude_md_2.name}')
    # Convert to the familiar rwx format
    print(f'Permissions: {mode}')
    print(f'Size: {file_stat.st_size} bytes')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Hidden files and dotfiles

    Files and directories that start with a `.` (dot) are **hidden** — they don't show up in Finder or regular `ls` by default. You need `ls -a` to see them.

    These are everywhere in development:

    | Dotfile | What it is |
    |---------|------------|
    | `.venv/` | Your Python virtual environment |
    | `.git/` | Git's internal data for version control |
    | `.gitignore` | Tells git which files to ignore |
    | `.env` | Environment variables (often contains API keys — **never commit this**) |
    | `.claude/` | Claude Code's project settings |
    | `.zshrc` | Your shell's configuration file (in your home directory) |

    When Claude Code creates a `.gitignore` or reads `.env`, now you know what those dots mean.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use the terminal vs. Finder for file operations?
    >
    > | Option | Pros | Cons | Use when... |
    > |--------|------|------|-------------|
    > | **Finder** (GUI) | Visual, familiar, drag-and-drop, preview files | Can't automate, can't do bulk operations, hidden files invisible by default | Browsing files casually, opening a specific file, drag-and-drop to an email |
    > | **Terminal** (shell commands) | Automatable, handles bulk operations, works with hidden files, scriptable | Learning curve, typos can be destructive (`rm`), no visual preview | Renaming 50 files at once, finding files by pattern (`*.csv`), anything you want to repeat or script, managing dotfiles and configs |
    > | **Python `pathlib`** | Cross-platform, integrates with your analysis code, safe (no `rm -rf` risk) | More verbose than shell one-liners | File operations inside a Python script or notebook, building file paths programmatically |
    >
    > **As a researcher:** You'll use Finder for browsing, the terminal for quick operations, and `pathlib` inside your analysis code. Claude Code uses the terminal, so understanding shell commands helps you verify what it's doing.
    """)
    return


@app.cell
def _(Path):
    # Find hidden files in the project root
    project_2 = Path.home() / 'ai-tutorial'
    print('Hidden items in the project root:')
    for item_1 in sorted(project_2.iterdir()):
        if item_1.name.startswith('.'):
            kind_1 = 'dir' if item_1.is_dir() else 'file'
            print(f'  {kind_1:4s}  {item_1.name}')
    return


@app.cell
def _(Path):
    # Hidden files in your home directory — there are a LOT
    home_1 = Path.home()
    hidden = [f.name for f in home_1.iterdir() if f.name.startswith('.')]
    print(f'You have {len(hidden)} hidden items in your home directory.')
    print(f'First 10: {sorted(hidden)[:10]}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why this matters for AI tools

    When you use Claude Code and it says something like:

    > *"I'll create the directory `data/calcium_imaging/` and write the processed results to `data/calcium_imaging/peak_amplitudes.csv`"*

    You now know:
    - It's creating a folder inside your project directory
    - The path is relative to wherever Claude Code is running
    - The file will be a regular text file (CSV) that you can open in Finder, Excel, or Python
    - You can verify it exists with `ls` or `Path(...).exists()`

    The filesystem isn't mysterious. It's a tree of folders and files, and every tool — Finder, the terminal, Python, Claude Code — is just navigating that same tree.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercises

    ### Exercise 1: Explore the project tree

    Using `pathlib`, list all the directories (modules) in the `ai-tutorial` project. For each directory, count how many `.py` files are inside.
    """)
    return


@app.cell
def _(Path):
    # Your code here
    project_3 = Path.home() / 'ai-tutorial'
    for module_dir in sorted(project_3.iterdir()):
        if module_dir.is_dir() and (not module_dir.name.startswith('.')):
            notebooks = list(module_dir.glob('*.py'))
            print(f'{module_dir.name}: {len(notebooks)} notebook(s)')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Build a path and read a file

    Using `pathlib`, construct the path to `CLAUDE.md` in the project root, read its contents, and print the number of lines and the number of times the word "pain" appears.
    """)
    return


@app.cell
def _(Path):
    # Your code here
    claude_md_3 = Path.home() / 'ai-tutorial' / 'CLAUDE.md'
    text = claude_md_3.read_text()
    lines = text.split('\n')
    pain_count = text.lower().count('pain')
    print(f'CLAUDE.md has {len(lines)} lines')
    print(f"The word 'pain' appears {pain_count} time(s)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Shell vs Python comparison

    Run the shell command `ls -la ~/ai-tutorial/` using the `!` prefix, then do the equivalent with `pathlib` (list all items with their sizes). Compare the output.
    """)
    return


@app.cell
def _(subprocess):
    # Shell version
    #! ls -la ~/ai-tutorial/
    subprocess.call(['ls', '-la', '~/ai-tutorial/'])
    return


@app.cell
def _(Path):
    # Python version — your code here
    project_4 = Path.home() / 'ai-tutorial'
    for item_2 in sorted(project_4.iterdir()):
        kind_2 = 'd' if item_2.is_dir() else '-'
        size = item_2.stat().st_size
        print(f'{kind_2}  {size:>8d}  {item_2.name}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - The **filesystem** is a tree of directories and files, rooted at `/`
    - **Absolute paths** start from root (`/`); **relative paths** start from where you are
    - `~` is your home directory, `.` is here, `..` is one level up
    - The **shell** (zsh) interprets commands in the form `command [flags] [arguments]`
    - Essential commands: `ls`, `cd`, `pwd`, `mkdir`, `cp`, `mv`, `rm`, `cat`, `head`, `which`
    - Python's `pathlib` can do everything the shell can, just with a different syntax
    - **Dotfiles** (hidden files starting with `.`) store configuration and project settings
    - **Permissions** (rwx) control who can read, write, or execute a file

    Next up: what happens when you actually *run* something — processes and environment variables.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Missing Semester, Lecture 1**: [Course Overview + The Shell](https://missing.csail.mit.edu/2020/course-shell/) — the full lecture covering shell navigation, file manipulation, and permissions in greater depth than this notebook; highly recommended
    - [Apple's File System Programming Guide](https://developer.apple.com/library/archive/documentation/FileManagement/Conceptual/FileSystemProgrammingGuide/FileSystemOverview/FileSystemOverview.html) — macOS-specific filesystem documentation, covering the directory structure, bundles, and macOS conventions
    - [Python docs: `pathlib`](https://docs.python.org/3/library/pathlib.html) — the full API reference for `Path`, including `glob()`, `iterdir()`, `stat()`, and all the methods used in this notebook
    - [Python docs: `shutil`](https://docs.python.org/3/library/shutil.html) — high-level file operations (copy, move, remove directory trees) used in the cleanup example
    - [Filesystem Hierarchy Standard](https://refspecs.linuxfoundation.org/FHS_3.0/fhs/index.html) — the Linux/Unix standard for directory layout; macOS follows a similar (but not identical) structure
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Data Structures in Practice](../01-python-foundations/04-data-structures-in-practice.py) | [Module Index](../README.md) | [Next: Processes and Environment \u2192](02-processes-and-environment.py)
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
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

