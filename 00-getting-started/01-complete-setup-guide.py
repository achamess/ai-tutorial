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
    # Complete Setup Guide: From Zero to Running Code

    **Time required:** ~30 minutes (one-time setup)

    **What this notebook is:** A step-by-step guide to setting up every tool you need for this tutorial. It covers **macOS, Windows, and Linux (Ubuntu/Debian)** — no programming experience, no developer tools, nothing assumed. Every single step is spelled out explicitly, with platform-specific instructions clearly labeled.

    **Why this matters:** In the lab, you would never start an experiment without preparing your bench, calibrating your instruments, and checking your reagents. This is the same thing for computational work. You are going to install five tools that work together, and then you will never have to do this again. Everything after this is the fun part.

    > **Navigation:** [\u2190 Previous: Tutorial Philosophy](00-tutorial-philosophy.py) | [Module Index](../README.md) | [Next: Pre-Flight Check \u2192](02-preflight-check.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Part 1: Understanding What We're Setting Up (and Why)

    You need five things to work through this tutorial. Here is what they are and why you need each one:

    | Tool | What it is | Lab analogy |
    |------|-----------|-------------|
    | **VS Code** | A text editor designed for code | Your lab notebook — where you write and organize everything |
    | **Python** | A programming language | Your experimental protocol language — how you tell the computer what to do |
    | **marimo** | An interactive coding environment | Your bench — where you actually run experiments (code) and see results immediately |
    | **Git** | Version control software | Your lab notebook's revision history — tracks every change so you can always go back |
    | **Claude Code** | An AI assistant in your terminal | A very knowledgeable colleague sitting next to you, available 24/7 |

    Here is how they connect:

    ```
    ┌─────────────────────────────────────────────────┐
    │                   VS Code                        │
    │          (your workspace — everything            │
    │           lives inside this app)                 │
    │                                                  │
    │   ┌──────────────┐    ┌──────────────────────┐   │
    │   │   marimo      │    │   Terminal            │   │
    │   │   Notebooks   │    │                      │   │
    │   │  (interactive │    │  ┌────────────────┐  │   │
    │   │   coding)     │    │  │  Claude Code   │  │   │
    │   │              │    │  │  (AI assistant) │  │   │
    │   └──────┬───────┘    │  └────────────────┘  │   │
    │          │            │                      │   │
    │          ▼            │  ┌────────────────┐  │   │
    │   ┌──────────────┐    │  │     Git        │  │   │
    │   │   Python      │    │  │  (version      │  │   │
    │   │  (runs your   │    │  │   control)     │  │   │
    │   │   code)       │    │  └────────────────┘  │   │
    │   └──────────────┘    └──────────────────────┘   │
    └─────────────────────────────────────────────────┘
    ```

    **Reassurance:** This entire setup takes about 30 minutes. You do it once, and then you are set for the entire tutorial (and for any future Python projects). If anything goes wrong, there is a troubleshooting section at the end of this guide.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 2: Install VS Code

    VS Code (Visual Studio Code) is a free code editor made by Microsoft. It is where you will write code, open notebooks, and manage your project files. Think of it as a specialized word processor designed for code instead of essays.

    ### Step 2.1: Download VS Code

    1. Open your web browser (Safari, Chrome, whatever you use).
    2. Go to: **https://code.visualstudio.com/**

    **macOS:**
    3. You will see a big blue button that says **"Download for Mac"**. Click it.
    4. A file called something like `VSCode-darwin-arm64.zip` or `VSCode-darwin-universal.zip` will download to your Downloads folder.

    **Windows:**
    3. You will see a big blue button that says **"Download for Windows"**. Click it. This downloads a `.exe` installer.
    4. Run the installer and follow the prompts. Check the boxes for **"Add to PATH"** and **"Add 'Open with Code' action"** when offered — both are useful.

    **Linux (Ubuntu/Debian):**
    3. The easiest method is to install via Snap:
    ```bash
    sudo snap install code --classic
    ```
    Alternatively, download the `.deb` package from the VS Code website and install it:
    ```bash
    sudo apt install ./code_*.deb
    ```

    ### Step 2.2: Install VS Code

    **macOS:**
    1. Open your **Downloads** folder (click the Finder icon in your Dock, then click "Downloads" in the left sidebar).
    2. You should see the downloaded file. If it is a `.zip` file, double-click it to unzip it. You will get an app called **"Visual Studio Code"**.
    3. **Drag "Visual Studio Code" into your Applications folder.** You can do this by:
       - Opening a new Finder window
       - Clicking "Applications" in the left sidebar
       - Dragging the Visual Studio Code icon from Downloads into Applications
    4. Open VS Code by going to **Applications** and double-clicking **"Visual Studio Code"**.
    5. If macOS asks "Are you sure you want to open it?" — click **Open**. This is normal for apps downloaded from the internet.

    **Windows:**
    If you ran the `.exe` installer in Step 2.1, VS Code is already installed. You can find it in your Start Menu. Launch it from there.

    **Linux (Ubuntu/Debian):**
    If you used `snap install` or installed the `.deb` package in Step 2.1, VS Code is already installed. Launch it from your application menu or by typing `code` in your terminal.

    ### Step 2.3: Install the "code" command in PATH (Important!)

    This lets you open VS Code from the Terminal by typing `code`. You will use this later.

    **macOS:**
    1. With VS Code open, press **Cmd+Shift+P** (hold Command and Shift, then press P). This opens the "Command Palette" — a search bar at the top of VS Code.
    2. Type: **Shell Command: Install 'code' command in PATH**
    3. Click on the matching result.
    4. You should see a brief confirmation message. Done.

    **Windows:**
    If you checked **"Add to PATH"** during installation, this is already done. If not, you can add it manually: open VS Code, press **Ctrl+Shift+P**, type **Shell Command: Install 'code' command in PATH**, and click the result. You may need to restart your terminal afterward.

    **Linux (Ubuntu/Debian):**
    The `code` command is usually added to PATH automatically during installation. If not, open VS Code, press **Ctrl+Shift+P**, type **Shell Command: Install 'code' command in PATH**, and click the result.

    ### Step 2.4: Install essential extensions

    Extensions add features to VS Code. You need three:

    1. Press **Cmd+Shift+X** (macOS) or **Ctrl+Shift+X** (Windows/Linux). This opens the Extensions panel on the left side.
    2. In the search box at the top, type: **marimo**
       - Find the one by **marimo** (the official marimo VS Code extension).
       - Click the blue **Install** button.
    3. Clear the search box. Type: **Python**
       - Find the one by **Microsoft** (again, millions of installs, blue checkmark).
       - Click **Install**.
    4. Clear the search box. Type: **Markdown Preview Mermaid Support**
       - Find the one by **Matt Bierner**.
       - Click **Install**.

    ### Step 2.5: Verify

    **macOS:** Close VS Code completely (Cmd+Q) and reopen it from Applications.

    **Windows:** Close VS Code completely (Alt+F4) and reopen it from the Start Menu.

    **Linux:** Close VS Code completely and reopen it from your application menu.

    Press **Cmd+Shift+X** (macOS) or **Ctrl+Shift+X** (Windows/Linux) — you should see marimo, Python, and Markdown Preview Mermaid Support listed under "Installed" in the extensions panel.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 3: Install a Package Manager and Terminal

    A package manager lets you install developer tools from the command line instead of hunting down download pages. You type a short command and it handles everything.

    ### Step 3.1: Open your terminal

    **macOS:**
    1. Press **Cmd+Space** to open Spotlight (the search bar in the top-right of your screen).
    2. Type: **Terminal**
    3. Press **Enter**.
    4. A window will appear with a blinking cursor. This is the Terminal — a text-based way to talk to your computer. Everything you type here is a command.

    **What it looks like:** You will see something like this:

    ```
    alex@MacBook-Pro ~ %
    ```

    The `%` (or sometimes `$`) is the "prompt" — it means the Terminal is ready for you to type a command. The text before it shows your username and computer name. Do not worry about what it says — just know that the blinking cursor after the `%` is where you type.

    **Windows:**
    1. First, install **Windows Terminal** from the Microsoft Store (search for "Windows Terminal"). This is a modern terminal app that is much better than the old `cmd.exe`. **Do not use cmd.exe** — it is outdated and will cause problems.
    2. Open **Windows Terminal** from the Start Menu.
    3. By default it opens **PowerShell**, which is what you want.

    **What it looks like:** You will see something like this:

    ```
    PS C:\Users\alex>
    ```

    The `PS` stands for PowerShell. The path shows your current location. The `>` is the prompt — that is where you type commands.

    **Linux (Ubuntu/Debian):**
    1. Open your default terminal application. On Ubuntu, you can press **Ctrl+Alt+T** or find "Terminal" in your application menu.
    2. A window will appear with a blinking cursor.

    **What it looks like:** You will see something like this:

    ```
    alex@ubuntu:~$
    ```

    The `$` is the prompt — that is where you type commands.

    ### Step 3.2: Install your package manager

    **macOS — Install Homebrew:**

    Homebrew is like an app store for developer tools, but you use it from the Terminal instead of clicking through a website. Almost every developer on a Mac uses Homebrew.

    Copy and paste this entire line into the Terminal, then press **Enter**:

    ```bash
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    ```

    **How to paste in Terminal:** Press **Cmd+V** (same as pasting anywhere else on your Mac).

    **What will happen:**
    - It will show a list of things it is about to install and ask you to press **Enter** to continue. Press **Enter**.
    - It will ask for your **password**. This is your Mac login password (the one you use to unlock your computer). **When you type your password, nothing will appear on screen** — no dots, no asterisks, nothing. This is normal! Just type your password and press Enter.
    - It will download and install files. This takes 1-5 minutes. Let it run.

    **Windows — winget (already installed) or Chocolatey:**

    Good news: if you are running Windows 11 (or a recent Windows 10), you already have **winget** — the Windows Package Manager. You can verify by typing:

    ```powershell
    winget --version
    ```

    If you see a version number, you are all set. If not, install **Chocolatey** as an alternative:
    1. Go to **https://chocolatey.org/install**
    2. Follow the installation instructions (it involves running a PowerShell command as Administrator).

    We will use `winget` commands throughout this guide. If you use Chocolatey instead, the commands are similar but use `choco install` instead of `winget install`.

    **Linux (Ubuntu/Debian) — apt (already installed):**

    Great news: your package manager `apt` is already installed. No action needed. You can verify by typing:

    ```bash
    apt --version
    ```

    You should see a version number.

    ### Step 3.3: Post-install setup (macOS only)

    **macOS only — Add Homebrew to your PATH (Critical!):**

    After the Homebrew install finishes, **read the output carefully**. Near the bottom, you will see a section that says something like:

    ```
    ==> Next steps:
    - Run these commands in your terminal to add Homebrew to your PATH:
        echo >> /Users/alex/.zprofile
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> /Users/alex/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    ```

    **You MUST copy and run each of those commands.** They will look slightly different on your machine (your username instead of "alex"), but the structure will be the same. Copy each line one at a time, paste it into Terminal, and press Enter.

    **Why this matters:** Homebrew is installed, but your Terminal does not know where to find it yet. These commands tell your Terminal where Homebrew lives. If you skip this, every `brew` command will fail with "command not found."

    ### Step 3.4: Verify

    **macOS:** Close the Terminal completely (Cmd+Q), then reopen it (Cmd+Space, type "Terminal", Enter). Then type:

    ```bash
    brew --version
    ```

    You should see something like `Homebrew 4.x.x`. If you see "command not found: brew", go back to Step 3.3 — you missed the PATH setup.

    **Windows:** Close and reopen Windows Terminal. Then type:

    ```powershell
    winget --version
    ```

    You should see a version number.

    **Linux:** No verification needed — `apt` is always available.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 4: Install Python 3.14

    Your computer may come with an older version of Python (or sometimes none at all). We need Python 3.14 specifically because this tutorial uses features from that version.

    ### Step 4.1: Install Python

    **macOS:**

    In Terminal, type:

    ```bash
    brew install python@3.14
    ```

    Press **Enter**. Homebrew will download and install Python 3.14. This takes 1-3 minutes.

    **Windows:**

    Option A (recommended) — use winget:

    ```powershell
    winget install Python.Python.3.14
    ```

    Option B — download the installer:
    1. Go to **https://www.python.org/downloads/**
    2. Download the Python 3.14 installer for Windows.
    3. Run the installer.
    4. **CRITICAL: On the first screen of the installer, check the box that says "Add Python to PATH."** If you miss this, Python will not work from the command line and you will get "python is not recognized" errors. If you already installed without checking this, uninstall Python and reinstall it with the box checked.
    5. Click **Install Now** and let it complete.

    **Linux (Ubuntu/Debian):**

    Python 3.14 may not be in the default Ubuntu repositories yet. Use the **deadsnakes PPA** to get it:

    ```bash
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.14 python3.14-venv
    ```

    If `add-apt-repository` is not found, install it first:

    ```bash
    sudo apt install software-properties-common
    ```

    Then run the three commands above.

    ### Step 4.2: Verify

    After the install finishes:

    **macOS:**
    ```bash
    python3.14 --version
    ```

    You should see: `Python 3.14.x` (where x is some number — the exact patch version does not matter).

    **If you see "command not found":** Try closing and reopening Terminal, then run the command again. If it still fails, try:

    ```bash
    brew link python@3.14
    ```

    Then try `python3.14 --version` again.

    **Windows:**
    ```powershell
    python --version
    ```

    You should see: `Python 3.14.x`. If you see **"python is not recognized"**, Python was not added to PATH during installation. Uninstall Python (Settings → Apps → Installed Apps → Python 3.14 → Uninstall), then reinstall and **check the "Add Python to PATH" box**.

    **Linux (Ubuntu/Debian):**
    ```bash
    python3.14 --version
    ```

    You should see: `Python 3.14.x`.

    **Note:** You might wonder why we type `python3.14` (macOS/Linux) instead of just `python`. Your system may have other Python versions installed, and typing the full version number makes sure you get the right one. On Windows, the installer sets `python` to point to the version you just installed. Later, when we set up the virtual environment, we will not have to worry about this anymore.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 5: Install Git

    Git is version control software. It keeps track of every change you make to your files, so you can always go back to a previous version. Think of it as an infinite "undo" system for your entire project, with the ability to annotate what you changed and why — like a detailed lab notebook for your code.

    ### Step 5.1: Install Git

    **macOS:**

    In Terminal, type:

    ```bash
    brew install git
    ```

    Press **Enter**. This is quick — usually under a minute.

    **Windows:**

    ```powershell
    winget install Git.Git
    ```

    Alternatively, download the installer from **https://git-scm.com/** and run it. The installer comes with **Git Bash**, a Unix-like terminal that can be useful on Windows.

    After installation, **close and reopen Windows Terminal** so it can find the new `git` command.

    **Linux (Ubuntu/Debian):**

    ```bash
    sudo apt install git
    ```

    ### Step 5.2: Verify

    ```bash
    git --version
    ```

    You should see something like `git version 2.x.x`.

    ### Step 5.3: Configure Git with your identity

    Git attaches your name and email to every change you save. This is not creating an account anywhere — it is just labeling your work locally.

    Run these two commands (these work the same on all platforms), replacing the placeholder text with your actual name and email:

    ```bash
    git config --global user.name "Your Name"
    ```

    ```bash
    git config --global user.email "your@email.com"
    ```

    For example:

    ```bash
    git config --global user.name "Alex Johnson"
    git config --global user.email "alex.johnson@university.edu"
    ```

    You will not see any output — that means it worked. You can verify by running:

    ```bash
    git config --global --list
    ```

    You should see your name and email listed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 6: Get the Tutorial Files

    You need the `ai-tutorial` folder on your computer. There are two scenarios:

    ### Scenario A: You received a link to clone the tutorial

    If someone shared a Git URL with you (it looks something like `https://github.com/username/ai-tutorial.git`), run:

    ```bash
    git clone https://github.com/username/ai-tutorial.git
    ```

    (Replace the URL with the actual one you were given.)

    Then move into the folder:

    ```bash
    cd ai-tutorial
    ```

    ### Scenario B: You already have the folder

    If you already have the `ai-tutorial` folder on your computer (because someone shared it with you directly, or you are reading this notebook right now), you are all set. Just navigate to it in your terminal:

    **macOS/Linux:**
    ```bash
    cd ~/ai-tutorial
    ```

    (If your folder is somewhere else, replace `~/ai-tutorial` with the actual path. For example, if it is on your Desktop: `cd ~/Desktop/ai-tutorial`)

    **Windows:**
    ```powershell
    cd $HOME\ai-tutorial
    ```

    (If your folder is somewhere else, replace `$HOME\ai-tutorial` with the actual path. For example, if it is on your Desktop: `cd $HOME\Desktop\ai-tutorial`)

    ### Open the project in VS Code

    Once you are in the ai-tutorial folder in your terminal, type:

    ```bash
    code .
    ```

    This opens the entire project folder in VS Code. The `.` means "this folder" — so `code .` means "open VS Code here."

    **What you should see:** VS Code opens with a file explorer on the left showing all the tutorial folders (00-getting-started, 01-python-foundations, etc.).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 7: Set Up the Python Virtual Environment

    ### What is a virtual environment?

    A virtual environment is an isolated copy of Python with its own set of installed packages. It is like having a separate reagent shelf for each project in the lab — the chemicals (packages) for your calcium imaging analysis do not mix with the chemicals for your RNA-seq pipeline.

    Without a virtual environment, installing a package for one project could accidentally break another project. The virtual environment prevents that.

    ### Step 7.1: Navigate to the project folder

    If you are not already there, open your terminal and navigate to the project:

    **macOS/Linux:**
    ```bash
    cd ~/ai-tutorial
    ```

    **Windows:**
    ```powershell
    cd $HOME\ai-tutorial
    ```

    ### Step 7.2: Create the virtual environment

    **macOS:**
    ```bash
    python3.14 -m venv .venv
    ```

    **Windows:**
    ```powershell
    python -m venv .venv
    ```

    **Linux (Ubuntu/Debian):**
    ```bash
    python3.14 -m venv .venv
    ```

    **What this does:** Creates a folder called `.venv` inside your project. This folder contains a private copy of Python 3.14 and a place to install packages. The dot at the start of `.venv` makes it a hidden folder — it will not clutter your file explorer.

    This command produces no output. If you see no error, it worked.

    ### Step 7.3: Activate the virtual environment

    **macOS/Linux:**
    ```bash
    source .venv/bin/activate
    ```

    **Windows (PowerShell):**
    ```powershell
    .venv\Scripts\activate
    ```

    > **Windows note:** Notice the backslashes (`\`) and `Scripts` instead of `bin`. Windows uses backslashes for file paths. If this command fails with an error about "execution of scripts is disabled", run this command first and then try again:
    > ```powershell
    > Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    > ```
    > Alternatively, you can use **Git Bash** (installed with Git) instead of PowerShell, and use the macOS/Linux command: `source .venv/bin/activate`

    **What you should see:** Your terminal prompt changes. A `(.venv)` prefix appears:

    **macOS:**
    ```
    (.venv) alex@MacBook-Pro ai-tutorial %
    ```

    **Windows:**
    ```
    (.venv) PS C:\Users\alex\ai-tutorial>
    ```

    **Linux:**
    ```
    (.venv) alex@ubuntu:~/ai-tutorial$
    ```

    The `(.venv)` prefix tells you the virtual environment is active. From now on, any `python` or `pip` commands you run will use the Python inside `.venv`, not your system Python.

    **Important:** You need to activate the virtual environment every time you open a new terminal window and want to work on this project. If you forget, you will get errors about missing packages. Look for `(.venv)` in your prompt to confirm it is active.

    ### Step 7.4: Upgrade pip

    Pip is Python's package installer. Let's make sure it is up to date:

    ```bash
    pip install --upgrade pip
    ```

    You will see some output about downloading and installing. This is normal.

    ### Step 7.5: Install the tutorial packages

    ```bash
    pip install marimo pandas numpy matplotlib seaborn anthropic scipy
    ```

    **What this installs:**
    - **marimo** — the notebook system (interactive code documents, like this one)
    - **pandas** — data manipulation (think: Excel but programmable)
    - **numpy** — numerical computing (math on large arrays of numbers)
    - **matplotlib** — plotting and visualization
    - **seaborn** — statistical visualization (prettier plots built on matplotlib)
    - **anthropic** — the official Python client for the Claude API
    - **scipy** — scientific computing (statistics, signal processing, etc.)

    This will take 1-3 minutes. You will see lots of text scrolling by as packages download and install. Wait until you see the prompt (with `(.venv)` prefix) again.

    ### Step 7.6: Verify

    ```bash
    python --version
    ```

    This should show `Python 3.14.x`. Notice you can now type just `python` instead of `python3.14` — that is because the virtual environment's Python is the active one.

    You can also verify a package installed correctly:

    ```bash
    python -c "import pandas; print(pandas.__version__)"
    ```

    This should print a version number (like `2.2.0` or similar).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 8: Verify marimo

    ### What is marimo?

    Marimo is a reactive notebook system. Unlike traditional Jupyter notebooks, marimo notebooks are stored as plain `.py` files and automatically track dependencies between cells. There is no separate kernel to register — marimo runs your code directly using the Python in your active virtual environment.

    ### Step 8.1: Verify marimo is installed

    Make sure your virtual environment is still active (you should see `(.venv)` in your prompt). Then run:

    ```bash
    marimo --version
    ```

    You should see a version number (like `0.21.1` or similar).

    ### Step 8.2: Test marimo

    ```bash
    marimo edit --headless --port 0 --no-token
    ```

    This should start a marimo server. Press **Ctrl+C** to stop it. If it starts without errors, marimo is working correctly.

    ### Step 8.3: VS Code integration

    With the marimo VS Code extension installed (from Part 2), you can open `.py` marimo notebooks directly in VS Code. The extension will detect marimo notebooks and offer to run them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 9: Install Claude Code (Optional for Early Modules)

    Claude Code is an AI assistant that runs in your terminal and inside VS Code. It can read your files, write code, run commands, and answer questions about your project. It is like having a knowledgeable colleague who can see your screen and help in real time.

    **You do not need Claude Code for Modules 01-04.** It becomes essential starting in Module 05. You can skip this step and come back later if you prefer.

    ### Step 9.1: Install Node.js (required for Claude Code)

    Claude Code requires Node.js (a runtime for JavaScript). Install it with your package manager:

    **macOS:**
    ```bash
    brew install node
    ```

    **Windows:**
    ```powershell
    winget install OpenJS.NodeJS
    ```

    After installation, **close and reopen Windows Terminal** so it can find the new commands.

    **Linux (Ubuntu/Debian):**
    ```bash
    sudo apt install nodejs npm
    ```

    Verify (all platforms):

    ```bash
    node --version
    ```

    You should see a version number like `v22.x.x` or higher.

    ### Step 9.2: Install Claude Code

    ```bash
    npm install -g @anthropic-ai/claude-code
    ```

    **What this does:** `npm` is the Node.js package manager (similar to `pip` for Python). The `-g` flag installs it globally so you can use it from anywhere.

    **Note:** If you see a permission error:

    **macOS/Linux:**
    ```bash
    sudo npm install -g @anthropic-ai/claude-code
    ```
    (This will ask for your password.)

    **Windows:**
    Close Windows Terminal and reopen it **as Administrator** (right-click → Run as administrator), then run the `npm install` command again.

    ### Step 9.3: Verify

    ```bash
    claude --version
    ```

    You should see a version number. If you see "command not found", close and reopen your terminal, then try again.

    ### Step 9.4: First-time setup

    The first time you run Claude Code, you will need to authenticate. Simply run:

    ```bash
    claude
    ```

    It will walk you through connecting to your Anthropic account. Follow the prompts on screen. You can type `/exit` to leave Claude Code when done.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 10: Set Up Your API Key (Optional for Now)

    The Anthropic API key lets you send requests to Claude from your Python code. Several later modules (especially Module 05: Claude API) require this. You do not need it for Modules 01-04.

    ### Step 10.1: Create an Anthropic account

    1. Go to: **https://console.anthropic.com/**
    2. Click **Sign Up** (or **Log In** if you already have an account).
    3. Follow the account creation steps.

    ### Step 10.2: Create an API key

    1. Once logged in, look at the left sidebar and click **API Keys**.
    2. Click **Create Key**.
    3. Give it a name like "ai-tutorial" (this is just a label for your reference).
    4. Click **Create Key**.
    5. **IMPORTANT:** You will see the key displayed once. It starts with `sk-ant-`. **Copy it immediately** — you will not be able to see it again after you close this dialog. If you lose it, you can always create a new one, but you cannot retrieve the old one.

    ### Step 10.3: Add the key to your environment

    This stores the key so your terminal can find it every time you open a new window.

    **macOS:**

    In Terminal, run this command — but replace `sk-ant-your-key-here` with the actual key you just copied:

    ```bash
    echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.zshrc
    ```

    Then reload your profile:

    ```bash
    source ~/.zshrc
    ```

    **What this does:** The `echo ... >> ~/.zshrc` command adds a line to your shell configuration file (`.zshrc`). Every time you open Terminal, this file runs automatically, which sets the `ANTHROPIC_API_KEY` variable so your Python code can find it.

    **Windows:**

    There are two options:

    **Option A (permanent — recommended):** Set it as a system environment variable.
    1. Press the **Windows key**, type **"Environment Variables"**, and click **"Edit the system environment variables"**.
    2. Click the **"Environment Variables..."** button at the bottom.
    3. Under **"User variables"** (the top section), click **"New..."**.
    4. Variable name: `ANTHROPIC_API_KEY`
    5. Variable value: paste your key (starting with `sk-ant-`)
    6. Click **OK** on all dialogs.
    7. **Close and reopen Windows Terminal** for the change to take effect.

    **Option B (PowerShell profile):** Add it to your PowerShell profile so it loads every time you open PowerShell:
    ```powershell
    notepad $PROFILE
    ```
    If Notepad says the file does not exist, click **Yes** to create it. Add this line to the file:
    ```
    $env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
    ```
    Save and close Notepad, then close and reopen Windows Terminal.

    **Option C (session only — temporary):** Set it for the current PowerShell session only:
    ```powershell
    $env:ANTHROPIC_API_KEY = "sk-ant-your-key-here"
    ```
    This will be lost when you close the terminal.

    **Linux (Ubuntu/Debian):**

    ```bash
    echo 'export ANTHROPIC_API_KEY="sk-ant-your-key-here"' >> ~/.bashrc
    ```

    Then reload your profile:

    ```bash
    source ~/.bashrc
    ```

    **Note:** Linux typically uses `.bashrc` instead of macOS's `.zshrc` because most Linux distributions default to the Bash shell (macOS defaults to Zsh). If you use Zsh on Linux, use `~/.zshrc` instead.

    ### Step 10.4: Verify

    **macOS/Linux:**
    ```bash
    echo $ANTHROPIC_API_KEY
    ```

    **Windows (PowerShell):**
    ```powershell
    echo $env:ANTHROPIC_API_KEY
    ```

    You should see your key printed out (starting with `sk-ant-`).

    ### Security warning

    Your API key is like a password. It grants access to your Anthropic account and any credits you have.

    - **Never share your key** with anyone.
    - **Never paste your key** directly into a notebook or Python file.
    - **Never commit your key** to Git. The shell profile approach above keeps it out of your project files.
    - If you ever accidentally expose your key, go to https://console.anthropic.com/, delete the compromised key, and create a new one.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 11: Open Your First Notebook

    Everything is installed. Now let's make sure it all works together.

    ### Step 11.1: Open the project in VS Code

    If VS Code is not already open with the ai-tutorial project, open your terminal and run:

    **macOS/Linux:**
    ```bash
    cd ~/ai-tutorial
    code .
    ```

    **Windows:**
    ```powershell
    cd $HOME\ai-tutorial
    code .
    ```

    ### Step 11.2: Navigate to the pre-flight check notebook

    1. In VS Code, look at the **Explorer** panel on the left side (the top icon in the left sidebar, looks like two overlapping documents). If the panel is not visible, press **Cmd+Shift+E** (macOS) or **Ctrl+Shift+E** (Windows/Linux) to open it.
    2. Click the arrow next to **00-getting-started** to expand it.
    3. Click on **02-preflight-check.py**.

    ### Step 11.3: Understanding what you see

    The notebook should open as an interactive document with alternating blocks of text and code. This is what a marimo notebook looks like in VS Code.

    **If the notebook opens as plain Python text** instead of an interactive notebook, the marimo extension is not installed or not active. Go back to Part 2, Step 2.4 and install the marimo extension.

    ### Step 11.4: Select the kernel

    1. Look at the **top-right corner** of the notebook. You should see a button that says **"Select Kernel"** (or it might show a kernel name).
    2. Click it.
    3. A dropdown will appear. Select **"ai-tutorial"**.
    4. If you do not see "ai-tutorial" in the list:
       - Click "Select Another Kernel..."
       - Click "Python Environments..."
       - Look for "ai-tutorial" in the expanded list
       - If it is still not there, go back to Part 8 and make sure you registered the kernel

    ### Step 11.5: Run the first cell

    1. Click on the first code cell (a gray block that contains Python code, as opposed to the white text blocks).
    2. Press **Shift+Enter** to run it. This executes the code and moves to the next cell.
    3. You should see output appear below the cell.
    4. Continue pressing **Shift+Enter** to work through the entire notebook.

    ### What success looks like

    The pre-flight check notebook will test your Python version, installed packages, kernel, virtual environment, and optionally your API key. If you followed this guide, most or all checks should pass. The notebook will tell you exactly what to fix if anything failed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 12: Troubleshooting

    If something went wrong, find your error message below. The issues are organized by platform.

    ### All Platforms

    #### Notebook opens as raw JSON in VS Code

    The marimo extension is not installed. In VS Code, press **Cmd+Shift+X** (macOS) or **Ctrl+Shift+X** (Windows/Linux), search for **marimo**, and install it. Then close and reopen the notebook file. See **Part 2, Step 2.4**.

    #### "No kernel named ai-tutorial"

    marimo is not installed or the virtual environment is not active. Make sure your virtual environment is active (you should see `(.venv)` in your prompt), then run:

    ```bash
    pip install ipykernel
    python -m ipykernel install --user --name ai-tutorial --display-name "ai-tutorial"
    ```

    See **Part 8**.

    #### "ModuleNotFoundError: No module named 'pandas'" (or numpy, matplotlib, etc.)

    Your virtual environment is not active, or the packages were not installed in it. Fix:

    1. Open your terminal
    2. Navigate to the project folder (`cd ~/ai-tutorial` on macOS/Linux, `cd $HOME\ai-tutorial` on Windows)
    3. Activate the virtual environment:
       - **macOS/Linux:** `source .venv/bin/activate`
       - **Windows:** `.venv\Scripts\activate`
    4. `pip install marimo pandas numpy matplotlib seaborn anthropic scipy`

    If you are running a notebook in VS Code, also make sure the kernel is set to "ai-tutorial" (top-right corner of the notebook).

    #### VS Code cannot find Python interpreter

    Press **Cmd+Shift+P** (macOS) or **Ctrl+Shift+P** (Windows/Linux), type **"Python: Select Interpreter"**, and choose the one inside `.venv` (it will show the path to your virtual environment).

    #### pip install fails with a permissions error

    You are probably trying to install outside the virtual environment. Make sure you see `(.venv)` in your terminal prompt before running `pip install`. If you do not, activate the virtual environment first. See **Part 7, Step 7.3**.

    #### Something else went wrong

    If you have Claude Code installed, open your terminal, navigate to the project folder, and type:

    ```bash
    claude
    ```

    Then describe your problem. Claude Code can see your system and help you debug. Alternatively, copy the exact error message and search for it on the web — chances are someone else has had the same issue.

    ---

    ### macOS-Specific Issues

    #### "command not found: brew"

    You installed Homebrew but did not add it to your PATH. Go back to **Part 3, Step 3.3**. After Homebrew installs, it prints "Next steps" with commands you need to run. If you already closed that Terminal window and lost the output, run these two commands:

    ```bash
    echo >> ~/.zprofile
    echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
    eval "$(/opt/homebrew/bin/brew shellenv)"
    ```

    Then close and reopen Terminal.

    #### "command not found: python3.14"

    Either `brew install python@3.14` did not complete, or you have a PATH issue. Try:

    ```bash
    brew install python@3.14
    brew link python@3.14
    ```

    Close and reopen Terminal, then try `python3.14 --version` again.

    #### "command not found: code"

    You did not install the VS Code shell command. Open VS Code, press **Cmd+Shift+P**, type **Shell Command: Install 'code' command in PATH**, and click it. See **Part 2, Step 2.3**.

    #### "xcrun: error: invalid active developer path"

    macOS needs its command-line developer tools. Run:

    ```bash
    xcode-select --install
    ```

    A dialog will pop up asking you to install the tools. Click **Install** and wait for it to finish (this can take 5-10 minutes). Then retry the command that failed.

    ---

    ### Windows-Specific Issues

    #### "python is not recognized as an internal or external command"

    Python was not added to PATH during installation. Fix:
    1. Open **Settings → Apps → Installed Apps**.
    2. Find **Python 3.14** and uninstall it.
    3. Re-download the installer from https://www.python.org/downloads/.
    4. Run the installer and **check the "Add Python to PATH" box** on the first screen.
    5. Click **Install Now**.
    6. Close and reopen Windows Terminal, then try `python --version` again.

    #### "Execution of scripts is disabled on this system" (PowerShell)

    PowerShell's default security policy blocks scripts, including the virtual environment activation script. Fix by running:

    ```powershell
    Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
    ```

    Then try `.venv\Scripts\activate` again. This only needs to be done once.

    Alternatively, use **Git Bash** (installed alongside Git) instead of PowerShell. In Git Bash, you can use the macOS/Linux activation command: `source .venv/bin/activate`.

    #### ".venv\Scripts\activate" fails or does nothing

    - First, check the execution policy fix above.
    - Make sure you are in the correct directory (the one containing the `.venv` folder).
    - Try using **Git Bash** instead of PowerShell, and use `source .venv/bin/activate`.

    #### "winget is not recognized"

    You are likely on an older version of Windows 10 that does not include winget. Either:
    - Update Windows to the latest version (Settings → Windows Update), or
    - Install **Chocolatey** instead (https://chocolatey.org/install) and use `choco install` instead of `winget install`, or
    - Download installers manually from the websites listed in each step.

    #### "'npm' is not recognized"

    Node.js was not added to PATH. Close and reopen Windows Terminal after installing Node.js. If it still does not work, uninstall Node.js and reinstall it using `winget install OpenJS.NodeJS`, then close and reopen the terminal.

    ---

    ### Linux-Specific Issues

    #### "command not found: python3.14"

    Python 3.14 is probably not in your default repositories. You need the deadsnakes PPA:

    ```bash
    sudo apt install software-properties-common
    sudo add-apt-repository ppa:deadsnakes/ppa
    sudo apt update
    sudo apt install python3.14 python3.14-venv
    ```

    #### "Error: Command 'python3.14' not found" after installing from deadsnakes

    Make sure you also installed the venv module:

    ```bash
    sudo apt install python3.14-venv
    ```

    Without this, `python3.14 -m venv .venv` will fail.

    #### Permission denied when running pip install

    On Linux, never use `sudo pip install`. Instead, make sure your virtual environment is active (`source .venv/bin/activate`) and then run `pip install` normally. The virtual environment gives you a user-owned Python where no `sudo` is needed.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Setup Complete!

    If you made it through all the parts above, your environment is fully configured. Here is a summary of what you installed:

    | Tool | How to check it works |
    |------|----------------------|
    | VS Code | Opens from Applications/Start Menu; `code .` works in terminal |
    | Package manager | macOS: `brew --version` / Windows: `winget --version` / Linux: `apt --version` |
    | Python 3.14 | macOS/Linux: `python3.14 --version` / Windows: `python --version` — prints 3.14.x |
    | Git | `git --version` prints a version number |
    | Virtual environment | Activate it and see `(.venv)` in your prompt |
    | marimo | `marimo --version` prints a version number |
    | Claude Code | `claude --version` prints a version number (optional) |
    | API key | macOS/Linux: `echo $ANTHROPIC_API_KEY` / Windows: `echo $env:ANTHROPIC_API_KEY` (optional) |

    **Your next step:** Open **[02-preflight-check.py](02-preflight-check.py)** and run it to automatically verify everything is working.

    ---

    ## Further Reading

    These are the official documentation pages for every tool you installed. You do not need to read them now, but they are here if you ever want to learn more or troubleshoot.

    - **VS Code:** https://code.visualstudio.com/docs — official documentation
    - **Homebrew (macOS):** https://brew.sh/ — the Homebrew homepage with install instructions
    - **Chocolatey (Windows):** https://chocolatey.org/ — alternative Windows package manager
    - **Python:** https://docs.python.org/3.14/ — Python 3.14 documentation
    - **Git:** https://git-scm.com/doc — official Git documentation
    - **Virtual environments:** https://docs.python.org/3/library/venv.html — Python venv module docs
    - **marimo:** https://docs.marimo.io/ — marimo notebook documentation
    - **Anthropic API:** https://docs.anthropic.com/en/docs/initial-setup — getting started with the Claude API
    - **Claude Code:** https://docs.anthropic.com/en/docs/claude-code/overview — Claude Code documentation

    ---

    ## Edit Log

    | Date | Change |
    |------|--------|
    | 2026-03-25 | Created comprehensive setup guide |
    | 2026-03-25 | Added Windows and Linux setup instructions alongside Mac |
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Tutorial Philosophy](00-tutorial-philosophy.py) | [Module Index](../README.md) | [Next: Pre-Flight Check \u2192](02-preflight-check.py)
    """)
    return


if __name__ == "__main__":
    app.run()

