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
    # 02: Processes and Environment

    When you click "Run" on a code cell, something happens on your computer. When Claude Code executes a command, something happens. But what, exactly?

    This notebook explains **processes** (programs that are running) and the **environment** (the configuration they inherit). Understanding these is the key to debugging "it works on my machine" problems and understanding why things like virtual environments and API keys work the way they do.

    > **References:**
    > - [MIT Missing Semester — Lecture 1: The Shell](https://missing.csail.mit.edu/2020/course-shell/) — covers processes, environment variables, and how the shell works
    > - [MIT Missing Semester — Lecture 3: Editors (vim)](https://missing.csail.mit.edu/2020/editors/) — touches on process management and job control
    > - [MIT Missing Semester — Lecture 4: Data Wrangling](https://missing.csail.mit.edu/2020/data-wrangling/) — pipes, redirection, and combining commands
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: The Filesystem and the Shell](01-filesystem-and-shell.py) | [Module Index](../README.md) | [Next: Networking and APIs \u2192](03-networking-and-apis.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Your `ANTHROPIC_API_KEY` is stored as an environment variable. If you don't understand environment variables, you can't set up API access, debug "authentication failed" errors, or keep your key secure.
    > - Virtual environments are why `pip install` for one project doesn't break another. When you're running RFdiffusion in one environment and your data analysis in another, venvs keep them isolated. Understanding this prevents the nightmare of conflicting package versions.
    > - When a Python script "hangs" or Claude Code seems stuck, understanding processes tells you what's actually running and how to fix it. Every command Claude Code executes is a process — knowing that lets you understand timeouts, errors, and resource usage.
    > - Pipes and stdout/stderr are how Claude Code captures output from commands it runs. When you see Claude Code showing you the results of `python analysis.py`, it's reading that process's stdout.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What is a process?

    A **process** is a running instance of a program. When you:
    - Open VS Code → that's a process
    - Run a Python script → that's a process
    - Open Terminal → the shell (zsh) is a process
    - Run a marimo notebook → the Python process running it is a process
    - Use Claude Code → it spawns processes for every command it runs

    Right now, your computer is running hundreds of processes. Let's look.
    """)
    return


@app.cell
def _():
    import os

    # Every process gets a unique ID number (PID)
    my_pid = os.getpid()
    print(f"This Python process has PID: {my_pid}")

    # Every process also has a parent process
    parent_pid = os.getppid()
    print(f"Its parent process has PID: {parent_pid}")
    print()
    print("The parent is marimo — it started this Python process.")
    print("marimo was started by your shell. Your shell was started by Terminal/VS Code.")
    print("It's processes all the way down.")
    return (os,)


@app.cell
def _():
    # Let's see what's running on your Mac right now
    # ps aux lists all processes; we'll just grab a sample
    import subprocess

    result = subprocess.run(["ps", "aux"], capture_output=True, text=True)
    lines = result.stdout.strip().split("\n")

    print(f"Total processes running: {len(lines) - 1}")  # minus the header
    print()
    print("Header:")
    print(lines[0])
    print()
    print("First 5 processes:")
    for line in lines[1:6]:
        print(line)
    return lines, subprocess


@app.cell
def _(lines):
    # Find Python-related processes specifically
    python_processes = [line for line in lines if "python" in line.lower() or "marimo" in line.lower()]

    print(f"Python/marimo processes: {len(python_processes)}")
    for proc in python_processes:
        print(proc[:120])  # truncate long lines
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What happens when you "run" something

    Here's the sequence when you press `Shift+Enter` on a code cell:

    1. VS Code sends the cell's code to the **marimo** runtime (a running Python process)
    2. The kernel **executes** the code
    3. Any output (from `print()`, return values, etc.) gets sent back to VS Code
    4. VS Code **displays** the output below the cell

    When Claude Code runs a shell command:

    1. Claude Code tells your shell (zsh) to run the command
    2. The shell **creates a new process** for that command
    3. The command runs and produces output
    4. Claude Code **reads the output** and uses it to decide what to do next

    The key insight: **every command is a process**. It starts, does its work, and ends.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.mermaid(
        """
        graph TD
            subgraph "What happens when you press Shift+Enter on a code cell"
                A["You press <b>Shift+Enter</b><br/>in VS Code"] --> B["VS Code sends cell code to<br/>the <b>marimo</b> runtime<br/>(a running Python process)"]
                B --> C["The kernel <b>executes</b><br/>your Python code"]
                C --> D["Output from print() and<br/>return values go to <b>stdout</b>"]
                D --> E["VS Code <b>displays</b> the output<br/>below the cell"]
            end
        
            subgraph "What happens when Claude Code runs a command"
                F["Claude Code decides to run<br/>e.g. <code>pip install pandas</code>"] --> G["Your <b>shell</b> (zsh) creates<br/>a <b>new process</b>"]
                G --> H["The process <b>inherits</b><br/>environment variables<br/>(PATH, API keys, etc.)"]
                H --> I["Command runs, writes to<br/><b>stdout</b> and <b>stderr</b>"]
                I --> J["Claude Code <b>reads output</b><br/>and decides next step"]
            end
        
            style A fill:#4488cc,color:#fff
            style F fill:#44aa88,color:#fff
            style E fill:#4488cc,color:#fff
            style J fill:#44aa88,color:#fff
        """
    )
    return


@app.cell
def _(Path, subprocess):
    # We can create processes from Python too — this is what Claude Code does
    result_1 = subprocess.run(['ls', '-la', str(Path.home() / 'ai-tutorial')], capture_output=True, text=True)
    print('=== stdout (normal output) ===')
    # Run 'ls' as a separate process
    print(result_1.stdout[:500])
    print(f'\n=== Return code: {result_1.returncode} ===')
    print('(0 means success, anything else means error)')  # capture stdout and stderr  # return strings, not bytes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Environment variables

    Every process inherits a set of **environment variables** — key-value pairs that configure how things work. Think of them like lab-wide settings posted on the wall: any protocol can reference them.

    You already use one: `ANTHROPIC_API_KEY`. Instead of pasting your API key into every script, you set it as an environment variable once, and any program that needs it can read it.

    That's the whole point: **separate configuration from code**.
    """)
    return


@app.cell
def _(os):
    all_vars = dict(os.environ)
    print(f'Total environment variables: {len(all_vars)}')
    # See ALL environment variables
    # (There are a lot — let's just count them and show a few)
    print()
    interesting_vars = ['HOME', 'USER', 'SHELL', 'PATH', 'TERM', 'LANG']
    for var in interesting_vars:
        value = os.environ.get(var, '(not set)')
    # Some important ones
        if var == 'PATH':
            value = value[:80] + '...'
        print(f'{var:12s} = {value}')  # PATH is super long, so truncate it
    return


@app.cell
def _(os):
    # Check if your Anthropic API key is set
    # (We won't print the actual key — that's a secret!)
    api_key = os.environ.get("ANTHROPIC_API_KEY")

    if api_key:
        # Show just enough to confirm it's there
        print(f"ANTHROPIC_API_KEY is set: {api_key[:8]}...{api_key[-4:]}")
        print(f"Length: {len(api_key)} characters")
    else:
        print("ANTHROPIC_API_KEY is NOT set.")
        print("You'll need this for the API modules later.")
        print("It's typically set in your ~/.zshrc file.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** Never hardcode API keys in your code. Writing `client = anthropic.Anthropic(api_key="sk-ant-api03-REAL-KEY-HERE")` is a security disaster waiting to happen. If that code gets pushed to GitHub (even in a "private" repo), your key is exposed and anyone can use your API credits. Always use environment variables (`os.environ["ANTHROPIC_API_KEY"]`) or `.env` files that are listed in `.gitignore`. The `anthropic` library reads the environment variable automatically — you never need to pass the key explicitly.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.mermaid(
        """
        graph LR
            subgraph "How ANTHROPIC_API_KEY flows from config to API call"
                A["<b>~/.zshrc</b><br/><code>export ANTHROPIC_API_KEY=sk-ant-...</code>"] -->|"loaded on<br/>terminal open"| B["<b>Shell (zsh)</b><br/>Key is now in<br/>shell environment"]
                B -->|"inherited by<br/>child process"| C["<b>Python process</b><br/><code>os.environ['ANTHROPIC_API_KEY']</code>"]
                C -->|"read by<br/>anthropic library"| D["<b>API Request</b><br/>Key sent as HTTP header<br/><code>x-api-key: sk-ant-...</code>"]
                D -->|"over HTTPS"| E["<b>Anthropic Server</b><br/>Authenticates you,<br/>processes prompt"]
            end
        
            style A fill:#cc8844,color:#fff
            style B fill:#4488cc,color:#fff
            style C fill:#44aa88,color:#fff
            style D fill:#aa44aa,color:#fff
            style E fill:#cc4444,color:#fff
        """
    ),
    mo.md(r"""

    This is why you set the key in `~/.zshrc` once and it "just works" everywhere -- environment variable inheritance passes it from parent process to child process automatically.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use environment variables vs. config files?
    >
    > | Option | Pros | Cons | Use when... |
    > |--------|------|------|-------------|
    > | **Environment variables** (`~/.zshrc` or `.env`) | Standard for secrets (API keys), inherited by all child processes, easy to change per-session | Not version-controlled, easy to lose if you reinstall, limited to key=value strings | Storing secrets (API keys, passwords), machine-specific settings (PATH), values that differ between your laptop and a server |
    > | **Config files** (`.json`, `.yaml`, `.toml`) | Version-controllable, supports complex structures (nested data, lists), self-documenting | Must be explicitly loaded by your code, risk of accidentally committing secrets | Project settings (model name, default parameters), experiment configurations, tool settings that should be shared with collaborators |
    > | **`CLAUDE.md` / project files** | Checked into git, visible to collaborators, read by Claude Code | Public (never put secrets here), limited to text | Project conventions, coding standards, tool configurations that Claude Code should follow |
    >
    > **Golden rule:** Secrets go in environment variables. Everything else goes in config files. Never put secrets in files that get committed to git.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Where do environment variables come from?

    On your Mac, environment variables are typically set in:

    1. **`~/.zshrc`** — your shell's config file, loaded every time you open a terminal
    2. **`~/.zprofile`** — loaded on login (similar to `.zshrc` but runs less often)
    3. **`.env` files** — project-specific variables (used by some tools)
    4. **Inline** — `ANTHROPIC_API_KEY=sk-... python script.py` (temporary, just for that command)

    When you added your `ANTHROPIC_API_KEY` to `~/.zshrc`, here's what happens:
    1. You open a terminal → zsh starts → it reads `~/.zshrc` → your key is now in the environment
    2. You run `python` → the Python process **inherits** all env vars from the shell
    3. Your Python code calls `os.environ["ANTHROPIC_API_KEY"]` → it finds the key

    It's inheritance: parent passes environment to child.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** PATH is how your shell finds programs. When you type `python`, your shell doesn't magically know where Python lives — it searches through a list of directories (stored in the `PATH` variable) from first to last, and uses the first match. This is why activating a virtual environment works: it puts `.venv/bin/` at the *front* of PATH, so `.venv/bin/python` gets found before `/usr/bin/python`. When you see "command not found," it means the program isn't in any PATH directory. When you get the wrong Python version, it means the wrong directory is listed first in PATH.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## PATH: how your shell finds programs

    When you type `python` in the terminal, how does your Mac know where the Python program actually lives? The answer is the **PATH** environment variable.

    PATH is a list of directories, separated by colons. When you type a command, your shell searches through these directories in order until it finds a matching program.
    """)
    return


@app.cell
def _(os):
    path_dirs = os.environ['PATH'].split(':')
    print(f'Your PATH has {len(path_dirs)} directories:')
    # Let's look at your PATH, one directory per line
    print()
    for i, directory in enumerate(path_dirs, 1):
        print(f'  {i:2d}. {directory}')
    return


@app.cell
def _():
    # 'which' tells you which program the shell will use
    import shutil

    programs_to_find = ["python", "python3", "pip", "marimo", "git", "code", "claude"]

    print("Where key programs live:")
    for prog in programs_to_find:
        location = shutil.which(prog)
        if location:
            print(f"  {prog:12s} → {location}")
        else:
            print(f"  {prog:12s} → (not found in PATH)")
    return (shutil,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice how some programs live in `.venv/bin/` — that's the virtual environment at work.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Virtual environments demystified

    A Python **virtual environment** (venv) is one of those things that seems magical until you understand it. Here's the trick: **it's just a directory with its own copy of Python and packages, and an adjustment to PATH.**

    When you "activate" a virtual environment, all that happens is:
    1. The venv's `bin/` directory gets added to the **front** of your PATH
    2. So when you type `python`, your shell finds the venv's Python **first**
    3. When you `pip install` something, it goes into the venv's `lib/` directory

    That's it. No magic. Just PATH manipulation.
    """)
    return


@app.cell
def _():
    from pathlib import Path
    import sys

    # Where is the Python running THIS notebook?
    print(f"Python executable: {sys.executable}")
    print(f"Python version:    {sys.version}")
    print()

    # Is it inside a virtual environment?
    venv_path = Path.home() / "ai-tutorial" / ".venv"
    if venv_path.exists():
        print(f"Virtual environment exists at: {venv_path}")
        print()
    
        # What's inside the venv?
        print("Contents of .venv/:")
        for item in sorted(venv_path.iterdir()):
            print(f"  {item.name}/" if item.is_dir() else f"  {item.name}")
    return Path, sys


@app.cell
def _(subprocess, sys):
    # What packages are installed in our environment?
    result_2 = subprocess.run([sys.executable, '-m', 'pip', 'list', '--format=columns'], capture_output=True, text=True)
    lines_1 = result_2.stdout.strip().split('\n')
    print(f'Installed packages: {len(lines_1) - 2}')
    print()
    key_packages = ['marimo', 'pandas', 'numpy', 'matplotlib', 'anthropic', 'seaborn']
    for line_1 in lines_1:
        if any((pkg in line_1.lower() for pkg in key_packages)):
    # Show just a few key ones
            print(f'  {line_1.strip()}')  # minus header lines
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Why virtual environments matter

    Imagine you have two projects:
    - **Pain imaging analysis** needs pandas 2.0 and numpy 1.26
    - **Old RNA-seq pipeline** needs pandas 1.5 and numpy 1.24

    Without virtual environments, installing packages for one project would break the other. Each venv is an isolated bubble — its own Python, its own packages, no conflicts.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Stdin, stdout, stderr — what `print()` actually does

    Every process has three standard **streams** (channels for data):

    | Stream | Name | What it's for | Python example |
    |--------|------|---------------|----------------|
    | **stdin** | Standard input | Data coming IN to the program | `input("Enter value: ")` |
    | **stdout** | Standard output | Normal output | `print("Hello")` |
    | **stderr** | Standard error | Error messages, warnings | Error tracebacks |

    When you call `print("Hello")`, Python writes "Hello" to **stdout**. The terminal (or marimo) picks it up and shows it to you.

    When Python hits an error, the traceback goes to **stderr** — a separate channel. This separation matters because you can redirect them independently.
    """)
    return


@app.cell
def _(sys):
    print('This is stdout (normal output)')
    # Normal output goes to stdout
    # You can also write to stderr explicitly
    # Both appear in the notebook, but in a real terminal they're separate streams
    print('This is stderr (error channel)', file=sys.stderr)
    return


@app.cell
def _(subprocess):
    # When Claude Code runs a command, it captures both stdout and stderr separately
    result_3 = subprocess.run(['ls', '/tmp'], capture_output=True, text=True)
    print(f'stdout has {len(result_3.stdout)} characters')
    # This command succeeds — output goes to stdout
    print(f'stderr has {len(result_3.stderr)} characters')
    print(f'return code: {result_3.returncode}')
    print()
    result_3 = subprocess.run(['ls', '/nonexistent_directory'], capture_output=True, text=True)
    print(f'stdout has {len(result_3.stdout)} characters')
    print(f'stderr has {len(result_3.stderr)} characters')
    # This command fails — error goes to stderr
    print(f'stderr says: {result_3.stderr.strip()}')
    print(f'return code: {result_3.returncode}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Pipes and redirection

    In the shell, you can connect processes together like plumbing:

    - **Pipe** (`|`): send one command's stdout into another command's stdin
      ```bash
      cat data.csv | head -5      # read file, then show first 5 lines
      ps aux | grep python         # list processes, then filter for "python"
      ```

    - **Redirect** (`>`, `>>`): send stdout to a file instead of the screen
      ```bash
      ls -la > file_list.txt       # write output to file (overwrites)
      echo "new line" >> log.txt   # append to file
      ```

    - **Redirect stderr** (`2>`): send errors to a file
      ```bash
      python script.py 2> errors.log   # errors go to file, output to screen
      ```

    You'll see Claude Code use pipes all the time — for example, `grep -r "TRPV1" . | head -20` to search for a gene name and show just the first 20 matches.

    > **See also:** [MIT Missing Semester — Lecture 4: Data Wrangling](https://missing.csail.mit.edu/2020/data-wrangling/) goes deep on pipes and data manipulation.
    """)
    return


@app.cell
def _(subprocess):
    # Pipes in the shell
    # This is how you'd search for Python processes in the terminal:
    # ps aux | grep python

    # In marimo, we can use subprocess to run shell commands:
    #! ps aux | grep -i python | head -5
    subprocess.call(['ps', 'aux', '|', 'grep', '-i', 'python', '|', 'head', '-5'])
    return


@app.cell
def _(subprocess):
    # The Python equivalent of piping: subprocess with shell=True
    result_4 = subprocess.run("find ~/ai-tutorial -name '*.py' | wc -l", shell=True, capture_output=True, text=True)
    # Count how many .py files are in the project
    print(f'Number of notebooks in the project: {result_4.stdout.strip()}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Putting it all together: what Claude Code actually does

    When Claude Code runs a command on your behalf, here's the full picture:

    1. **Claude Code** (a process) asks your **shell** (zsh, another process) to run a command
    2. The shell **creates a new process** for that command
    3. The new process **inherits** the shell's environment variables (including `ANTHROPIC_API_KEY`, `PATH`, etc.)
    4. The command runs, writing to **stdout** (normal output) and **stderr** (errors)
    5. Claude Code **captures** both streams
    6. The process **exits** with a return code (0 = success)
    7. Claude Code reads the output and decides what to do next

    Now when you see Claude Code output like:
    ```
    Running: pip install pandas
    ```
    You know exactly what's happening under the hood.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercises

    ### Exercise 1: Inspect your environment

    Write code that:
    1. Prints the value of `HOME`, `USER`, and `SHELL` environment variables
    2. Checks whether `ANTHROPIC_API_KEY` is set (print "set" or "not set" — don't print the actual key)
    3. Counts how many directories are in your PATH
    """)
    return


@app.cell
def _(os):
    for var_1 in ['HOME', 'USER', 'SHELL']:
        print(f"{var_1} = {os.environ.get(var_1, '(not set)')}")
    # Your code here
    print()
    api_key_status = 'set' if os.environ.get('ANTHROPIC_API_KEY') else 'not set'
    print(f'ANTHROPIC_API_KEY: {api_key_status}')
    print()
    path_count = len(os.environ['PATH'].split(':'))
    print(f'PATH contains {path_count} directories')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Find where things live

    Use `shutil.which()` to find the location of these programs: `python3`, `git`, `pip`, `ls`, `zsh`. For each one, also check whether it's inside the `.venv` directory.
    """)
    return


@app.cell
def _(shutil):
    programs = ['python3', 'git', 'pip', 'ls', 'zsh']
    for prog_1 in programs:
    # Your code here
        location_1 = shutil.which(prog_1)
        if location_1:
            in_venv = '.venv' in location_1
            venv_note = ' (in virtual environment)' if in_venv else ''
            print(f'{prog_1:10s} → {location_1}{venv_note}')
        else:
            print(f'{prog_1:10s} → not found')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Run a command and inspect the result

    Use `subprocess.run()` to run `git log --oneline -5` in the `ai-tutorial` directory. Capture the output and print:
    - The return code
    - The number of lines of output
    - The output itself
    """)
    return


@app.cell
def _(Path, subprocess):
    result_5 = subprocess.run(['git', 'log', '--oneline', '-5'], capture_output=True, text=True, cwd=str(Path.home() / 'ai-tutorial'))
    print(f'Return code: {result_5.returncode}')
    lines_2 = result_5.stdout.strip().split('\n')
    # Your code here
    print(f'Lines of output: {len(lines_2)}')
    print()
    print('Recent commits:')
    print(result_5.stdout)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - A **process** is a running instance of a program — every command is a process
    - Processes have a **PID** (process ID) and a **parent** process
    - **Environment variables** are key-value pairs that configure processes (like `ANTHROPIC_API_KEY`)
    - **PATH** tells your shell where to find programs — that's how `python` resolves to an actual file
    - A **virtual environment** is just a directory with its own Python + packages, activated by modifying PATH
    - Processes have three streams: **stdin** (input), **stdout** (output), **stderr** (errors)
    - **Pipes** (`|`) connect one process's output to another's input
    - When Claude Code runs commands, it's creating processes and reading their stdout/stderr

    Next up: what happens when your code talks to the internet — networking and APIs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Missing Semester, Lecture 1**: [The Shell](https://missing.csail.mit.edu/2020/course-shell/) — foundational lecture covering processes, environment variables, PATH, and shell basics
    - **Missing Semester, Lecture 3**: [Editors (vim)](https://missing.csail.mit.edu/2020/editors/) — includes process management, job control (`Ctrl-Z`, `bg`, `fg`), and signals
    - [Python docs: `os` module](https://docs.python.org/3/library/os.html) — the official reference for `os.environ`, `os.getpid()`, `os.getppid()`, and other OS-level functions used in this notebook
    - [Python docs: `subprocess` module](https://docs.python.org/3/library/subprocess.html) — the official reference for `subprocess.run()` and process creation from Python
    - [Real Python: Environment Variables in Python](https://realpython.com/python-environment-variables/) — a practical guide to reading, setting, and using environment variables with `os.environ` and `.env` files
    - [Python docs: `venv`](https://docs.python.org/3/library/venv.html) — official documentation for virtual environments, explaining the PATH manipulation described in this notebook
    - [Python docs: `sys` module](https://docs.python.org/3/library/sys.html) — reference for `sys.executable`, `sys.version`, `sys.path`, and other interpreter-level attributes
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: The Filesystem and the Shell](01-filesystem-and-shell.py) | [Module Index](../README.md) | [Next: Networking and APIs \u2192](03-networking-and-apis.py)
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

