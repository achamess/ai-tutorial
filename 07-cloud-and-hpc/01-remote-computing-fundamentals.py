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
    # Module 7: Cloud & HPC Computing for Research
    # Notebook 1: Remote Computing Fundamentals

    > **Navigation:** [\u2190 Previous: Reproducibility and Project Structure](../06-systems-thinking/03-reproducibility-and-project-structure.py) | [Module Index](../README.md) | [Next: Job Schedulers and SLURM \u2192](02-job-schedulers-and-slurm.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    **Your laptop has 8 CPU cores and no GPU. RFdiffusion needs a GPU with 16GB VRAM. Your RNA-seq dataset is 200GB. Some problems simply don't fit on your machine — and that's normal, not a failure.**

    As a pain biologist designing de novo protein binders for NaV1.7 and NaV1.8, you'll regularly hit the limits of your MacBook. Running RFdiffusion for binder design, aligning RNA-seq reads with STAR, or doing batch structure prediction with ESMFold — these all need more compute than your laptop can provide.

    This notebook teaches you to reach beyond your laptop and use remote computers — whether that's WashU's RIS compute cluster, a collaborator's server, or a cloud GPU. By the end, you'll be able to connect to a remote machine, transfer files, manage software, and feel at home on someone else's computer.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 1: The Mental Model

    ### Your Laptop vs. a Remote Server vs. a Cluster vs. the Cloud

    Before we touch any commands, let's build a mental picture of what we're dealing with.

    > 🔑 **Key concept:** Remote computing just means using someone else's (bigger) computer, from your terminal. That's it. You type commands on your Mac, they execute on a machine with 64 CPU cores and 4 GPUs sitting in a data center. The results come back to your screen.

    Here's the hierarchy of compute resources you'll encounter:

    | Resource | What it is | Example | Who pays |
    |----------|-----------|---------|----------|
    | **Your laptop** | The Mac in front of you | MacBook Pro M-series | You (already own it) |
    | **A remote server** | A single powerful machine you SSH into | A lab workstation with a GPU | Your lab/department |
    | **An HPC cluster** | Hundreds of servers managed by a scheduler | WashU RIS compute cluster | Your institution |
    | **The cloud** | On-demand servers rented by the hour | AWS, Google Cloud, Lambda Labs | You/your grant (per hour) |

    The key insight: **they're all just Linux computers.** Once you can use one, you can use any of them. The only difference is how you get access and how you run jobs.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### Architecture Diagram

    Here's how an HPC cluster is structured. This is roughly what WashU's RIS looks like:

    """),
    mo.mermaid(
        """
        graph LR
            A["🖥️ Your MacBook<br/>(Terminal/VS Code)"] -->|SSH over internet| B["🚪 Login Node<br/>(Gateway — no heavy compute!)"]
            B -->|Job scheduler<br/>(SLURM)| C["⚙️ Compute Node 1<br/>64 cores, 256GB RAM"]
            B -->|Job scheduler| D["🎮 GPU Node 1<br/>64 cores, 4× A100 GPUs"]
            B -->|Job scheduler| E["⚙️ Compute Node 2<br/>64 cores, 256GB RAM"]
            B -->|Job scheduler| F["🎮 GPU Node 2<br/>64 cores, 4× V100 GPUs"]
        
            G["💾 Shared Storage<br/>(home, scratch, project)"] --- C
            G --- D
            G --- E
            G --- F
            G --- B
        
            style A fill:#e1f5fe
            style B fill:#fff3e0
            style D fill:#e8f5e9
            style F fill:#e8f5e9
        """
    ),
    mo.md(r"""

    **The key players:**
    - **Your laptop** — where you type commands and view results
    - **Login node** — the front door. You SSH here first. It's shared by everyone, so never run heavy jobs on it.
    - **Compute nodes** — the workhorses. Your jobs run here after being assigned by the scheduler.
    - **GPU nodes** — compute nodes with GPUs attached. This is where RFdiffusion, ESMFold, etc. run.
    - **Shared storage** — a filesystem that all nodes can see. Your files are the same whether you're on the login node or a compute node.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 2: SSH — Connecting to a Remote Machine

    ### What Is SSH?

    SSH (Secure Shell) is an encrypted tunnel between your computer and a remote machine. When you "SSH into a server," you're opening a terminal session on that remote machine. Everything you type goes through the encrypted tunnel; everything the remote machine sends back comes through the same tunnel.

    Think of it like a phone call to another computer: you talk (type commands), and you hear back (see output), but nobody can eavesdrop on the conversation.

    ### The Basic Command

    The most fundamental SSH command looks like this:

    ```bash
    ssh username@hostname
    ```

    For WashU's RIS cluster, that might look like:

    ```bash
    ssh alex.chamessian@compute1-client-1.ris.wustl.edu
    ```

    When you run this for the first time, you'll see something like:

    ```
    The authenticity of host 'compute1-client-1.ris.wustl.edu' can't be established.
    ED25519 key fingerprint is SHA256:xxxxxxxxxxxxxxxxxxxxxxxxxxx.
    Are you sure you want to continue connecting (yes/no/[fingerprint])?
    ```

    Type `yes`. This is your computer saying "I've never talked to this machine before — do you trust it?" You only see this once per server.

    Then it asks for your password. Type it (nothing will appear on screen — that's normal, it's a security feature) and press Enter.

    > 💡 **Tip:** Your WashU WUSTL Key credentials likely work for RIS. If you can log into other WashU systems, try those same credentials. If not, contact RIS at [ris.wustl.edu](https://ris.wustl.edu) to get an account.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SSH Config File — Stop Typing Long Hostnames

    Typing `ssh alex.chamessian@compute1-client-1.ris.wustl.edu` every time gets old fast. The SSH config file lets you create shortcuts.

    The file lives at `~/.ssh/config` on your Mac. If it doesn't exist, create it:

    ```bash
    # On your Mac terminal (NOT on the remote machine)
    mkdir -p ~/.ssh
    touch ~/.ssh/config
    chmod 600 ~/.ssh/config
    ```

    Then open it in any text editor and add:

    ```
    Host ris
        HostName compute1-client-1.ris.wustl.edu
        User alex.chamessian
        ForwardAgent yes
        ServerAliveInterval 60
        ServerAliveCountMax 3
    ```

    Now instead of the long command, you just type:

    ```bash
    ssh ris
    ```

    That's it. Let's break down what each line does:

    | Directive | What it does |
    |-----------|-------------|
    | `Host ris` | The shortcut name you'll type after `ssh` |
    | `HostName` | The actual server address |
    | `User` | Your username (so you don't have to type `user@` every time) |
    | `ForwardAgent yes` | Forwards your SSH keys to the remote machine (useful for Git) |
    | `ServerAliveInterval 60` | Sends a keepalive signal every 60 seconds |
    | `ServerAliveCountMax 3` | Disconnects if 3 keepalives fail (180 seconds of no response) |

    The `ServerAliveInterval` is important — without it, your connection will drop if you step away for coffee. With it, the connection stays alive as long as the network is up.

    > 💡 **Tip:** You can add multiple `Host` blocks — one for each server you use. A lab GPU workstation, a collaborator's machine, the RIS cluster — all accessible with short names.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### SSH Keys — Never Type Your Password Again

    Every time you SSH with a password, you're typing credentials over the network. SSH keys are a better approach: you create a key pair (a private key that stays on your Mac, and a public key that goes on the server), and the server recognizes you automatically.

    **Step 1: Generate a key pair (on your Mac)**

    ```bash
    ssh-keygen -t ed25519 -C "alex.chamessian@wustl.edu"
    ```

    It will ask:
    - **Where to save:** press Enter to accept the default (`~/.ssh/id_ed25519`)
    - **Passphrase:** enter a passphrase (like a password that protects the key file itself). You can leave it empty, but a passphrase adds security if someone steals your laptop.

    This creates two files:
    - `~/.ssh/id_ed25519` — your **private key** (never share this!)
    - `~/.ssh/id_ed25519.pub` — your **public key** (safe to share, goes on the server)

    **Step 2: Copy the public key to the server**

    ```bash
    ssh-copy-id ris
    ```

    (This uses the shortcut from your SSH config.) It will ask for your password one last time. After that, `ssh ris` will log you in without a password.

    > ⚠️ **Warning:** Never share your private key (`id_ed25519` — the one WITHOUT `.pub`). It's like your building access badge. If someone gets it, they can log into every server that trusts it. The public key (`id_ed25519.pub`) is safe to share — it's like the lock on the door.

    > 💡 **Tip:** On macOS, you can add your key to the SSH agent so you don't have to type the passphrase every time:
    > ```bash
    > ssh-add --apple-use-keychain ~/.ssh/id_ed25519
    > ```
    > This stores the passphrase in your Mac's Keychain, so it's unlocked when you log into your Mac.

    <details>
    <summary>📖 <strong>Deep dive:</strong> How SSH encryption actually works (click to expand)</summary>

    <br/>

    SSH uses **asymmetric cryptography** (also called public-key cryptography). Here's the simplified version:

    1. **Key generation:** You create a mathematically linked pair — a public key and a private key. Anything encrypted with the public key can only be decrypted with the private key, and vice versa.

    2. **The handshake:** When you connect to a server:
       - The server sends a random challenge encrypted with your public key
       - Only your private key can decrypt it
       - You send back the decrypted challenge, proving you hold the private key
       - The server never sees your private key

    3. **Session encryption:** After authentication, both sides agree on a temporary symmetric key (faster than asymmetric) for the actual session. All traffic is encrypted with this key.

    The `ed25519` algorithm you used is an elliptic curve algorithm — it's modern, fast, and produces short keys. Older alternatives like RSA work too but produce longer keys.

    This is the same fundamental math behind HTTPS (the padlock in your browser), cryptocurrency wallets, and secure messaging apps.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### VS Code Remote SSH — Your IDE on the Cluster

    You don't have to edit files in a bare terminal. VS Code has a **Remote - SSH** extension that lets you open folders on the remote machine as if they were local. You get syntax highlighting, file browsing, integrated terminal — everything you're used to, but the files live on the cluster.

    **Setup:**
    1. Install the [Remote - SSH extension](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-ssh) in VS Code
    2. Press `Cmd+Shift+P` → type "Remote-SSH: Connect to Host..."
    3. Select `ris` (it reads your `~/.ssh/config` automatically!)
    4. VS Code opens a new window connected to the cluster

    Now you can browse your project files, edit SLURM scripts, and run terminal commands — all through VS Code, all executing on the remote machine.

    ### Claude Code Over SSH

    If you have Claude Code installed, you can use it on the remote machine too. Just SSH in and run `claude` from the terminal. This is incredibly powerful for:
    - Debugging failed SLURM jobs by having Claude read the log files
    - Writing and editing SLURM submission scripts
    - Navigating unfamiliar cluster file structures

    > 💡 **Tip:** If Node.js is available on the cluster (check with `node --version`), Claude Code works over SSH just like it does locally. If it's not installed, you can use `module load nodejs` or install it in your home directory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 3: Transferring Files

    You'll constantly move files between your Mac and remote machines — uploading scripts, downloading results, syncing datasets. Here are the tools for each situation.

    ### `scp` — Copy Files Over the Network

    `scp` (secure copy) works just like `cp`, but between machines:

    ```bash
    # Copy a file FROM your Mac TO the cluster
    scp run_rfdiffusion.py ris:~/scripts/

    # Copy a file FROM the cluster TO your Mac
    scp ris:~/results/binder_designs.pdb ./local_results/

    # Copy an entire directory (add -r for recursive)
    scp -r ris:~/results/nav17_screen/ ./local_results/
    ```

    The syntax is `scp source destination`, where remote paths use the `host:path` format.

    ### `rsync` — Smarter File Synchronization

    `rsync` is like `scp` but much smarter:
    - It only transfers files that have changed (saves time on repeated syncs)
    - It can resume interrupted transfers (critical for large files)
    - It shows progress

    ```bash
    # Sync a local directory TO the cluster
    rsync -avP ./protein_designs/ ris:~/projects/nav17_binders/designs/

    # Sync results FROM the cluster to your Mac
    rsync -avP ris:~/projects/nav17_binders/results/ ./local_results/

    # Dry run — see what WOULD be transferred without actually doing it
    rsync -avPn ris:~/projects/nav17_binders/results/ ./local_results/
    ```

    The flags:
    - `-a` — archive mode (preserves permissions, timestamps, etc.)
    - `-v` — verbose (shows what's being transferred)
    - `-P` — shows progress AND enables resume on interruption
    - `-n` — dry run (simulate without transferring)

    > 💡 **Tip:** Always use `rsync -avPn` (dry run) first when syncing large directories. Make sure it's going to do what you expect before you let it run.

    ### 🤔 Decision Point: Which File Transfer Method?

    | Method | Best for | Speed | Resume? | Notes |
    |--------|----------|-------|---------|-------|
    | `scp` | Small files, one-time transfers | Fast | No | Simple, universally available |
    | `rsync` | Large datasets, repeated syncs | Fastest (incremental) | Yes | The go-to for most situations |
    | `sftp` | Interactive browsing & transfer | Medium | No | Like an FTP client; type `sftp ris` to start |
    | **Globus** | Multi-TB transfers between institutions | Fastest | Yes | Web interface, managed by research IT |

    > 💡 **Tip:** For really big genomics data (hundreds of GB), ask WashU RIS about [Globus](https://www.globus.org/). It's a managed file transfer service designed for research data. You upload through a web interface, and it handles reliability, retries, and optimization. Many institutions already have Globus endpoints set up.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 4: The Remote Filesystem

    When you SSH into a cluster, you land in your **home directory** (`~` or `/home/username`). But there are usually several different storage areas, each with different purposes and limits.

    ### Storage Tiers on a Typical HPC Cluster

    | Storage | Path (typical) | Size limit | Backed up? | Speed | Use for |
    |---------|---------------|------------|------------|-------|---------|
    | **Home** | `~/` or `/home/username` | 5-50 GB | Yes | Medium | Code, scripts, configs, small files |
    | **Scratch** | `/scratch/username` | Large (TB) | **No** | Fast | Temporary data, intermediate files, active jobs |
    | **Project/Group** | `/storage/group/lab_name` | Allocated per PI | Usually | Medium | Shared datasets, final results, archives |

    > ⚠️ **Warning:** HPC home directories are often tiny — 5 to 50 GB. If you try to put a 200GB RNA-seq dataset in your home directory, you'll fill it up and potentially break things (can't log in, jobs fail, etc.). Always put large data in scratch or project storage.

    > ⚠️ **Warning:** Scratch storage is usually **not backed up** and may be **automatically purged** (files older than 30-90 days get deleted). Never put your only copy of anything important in scratch.

    ### Checking Your Usage

    ```bash
    # How big is this directory?
    du -sh ~/projects/nav17_binders/

    # How big is each subdirectory? (sorted, human-readable)
    du -sh ~/projects/nav17_binders/*/ | sort -h

    # Check your quota (cluster-specific — try these)
    quota -s
    lfs quota -h /home/alex.chamessian   # for Lustre filesystems
    ```

    ### Where to Put What

    A practical layout for your protein design work:

    ```
    ~/                                    # Home (small, backed up)
    ├── scripts/                          # Your Python/bash scripts
    ├── envs/                             # Conda/venv environments
    ├── .ssh/config                       # SSH config
    └── projects/
        └── nav17_binders/
            ├── README.md                 # What this project is
            └── submit_scripts/           # SLURM submission scripts

    /scratch/alex.chamessian/             # Scratch (large, fast, NOT backed up)
    ├── rfdiffusion_runs/                 # Active RFdiffusion outputs
    ├── rnaseq_alignment/                 # STAR alignment intermediate files
    └── tmp/                              # Truly temporary stuff

    /storage/group/bhatt_lab/             # Project storage (shared, backed up)
    ├── datasets/
    │   ├── rnaseq_raw/                   # Raw FASTQ files
    │   └── proteomics/                   # Mass spec data
    └── results/
        ├── nav17_binder_candidates/      # Curated final designs
        └── deseq2_results/               # Final DE analysis
    ```

    <details>
    <summary>📖 <strong>Deep dive:</strong> Symbolic links for organizing across storage tiers (click to expand)</summary>

    <br/>

    You can create **symbolic links** (symlinks) to make files in one location appear to be in another. This is like a shortcut or alias.

    ```bash
    # Create a symlink so ~/data points to your scratch space
    ln -s /scratch/alex.chamessian/data ~/data

    # Now "cd ~/data" actually takes you to /scratch/alex.chamessian/data
    # Your scripts can reference ~/data without knowing the actual path

    # Another common pattern: link large datasets into your project directory
    ln -s /storage/group/bhatt_lab/datasets/rnaseq_raw ~/projects/nav17/data/raw_reads
    ```

    This keeps your project directory organized without duplicating large files. The symlink itself takes almost no space.

    **Caveat:** If the target of a symlink is deleted (e.g., scratch gets purged), the symlink becomes "dangling" — it points to nothing and will cause errors. Use `ls -la` to see where symlinks point.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 5: Software on Remote Machines

    Your Mac has Homebrew. HPC clusters have something different: the **module system**.

    ### The Module System

    Clusters serve hundreds of users who need different versions of software. One person needs Python 3.10, another needs 3.14. One project needs CUDA 11.8, another needs CUDA 12.0. The module system lets all these versions coexist.

    ```bash
    # What software is available?
    module avail

    # Search for specific software
    module avail python
    module avail cuda

    # Load software into your current session
    module load python/3.14
    module load cuda/12.0

    # See what you have loaded
    module list

    # Unload a module
    module unload python/3.14

    # Unload everything (clean slate)
    module purge
    ```

    When you `module load python/3.14`, it modifies your `PATH` and other environment variables so that typing `python` now runs Python 3.14 from the cluster's software collection. When you log out, the modules are unloaded automatically.

    > 🔑 **Key concept:** Modules don't install software — the software is already installed by the HPC admins. Modules just make it visible to your session. Think of it as turning on a light switch, not installing a light bulb.

    ### Conda Environments on HPC

    Sometimes the module system doesn't have what you need (e.g., a specific version of PyTorch, or RFdiffusion's exact dependency stack). That's when you use Conda:

    ```bash
    # Load conda (may be a module itself)
    module load conda

    # Create an environment for protein design
    conda create -n protein-design python=3.11 pytorch pytorch-cuda=12.1 -c pytorch -c nvidia

    # Activate it
    conda activate protein-design

    # Install additional packages
    pip install rfdiffusion proteinmpnn-wrapper
    ```

    > ⚠️ **Warning:** Do NOT run `pip install` without first activating a virtual environment or conda environment. Installing packages system-wide on a shared cluster can break things for other users, and you probably don't have permission anyway. Always use `conda activate myenv` or `source ~/envs/myenv/bin/activate` first.

    ### 🤔 Decision Point: Modules vs. Conda vs. Containers

    | Approach | Pros | Cons | Use when |
    |----------|------|------|----------|
    | **Modules** | Pre-installed, optimized for cluster hardware | Limited selection, can't customize | Standard tools (Python, R, CUDA, STAR, samtools) |
    | **Conda** | Full control, reproducible, any package | Uses your storage quota, slow to create | Custom environments, specific version combos (e.g., PyTorch + CUDA) |
    | **Containers (Singularity)** | Perfectly reproducible, portable | Learning curve, large files | Complex dependency stacks, sharing pipelines, publishing workflows |

    A practical approach:
    1. **First**, check if modules have what you need (`module avail toolname`)
    2. **If not**, create a conda environment
    3. **If you need to share** the exact environment with collaborators or publish it, build a container

    > 💡 **Tip:** Put your conda environments in scratch or project storage, NOT your home directory. Conda environments can easily be 5-10 GB each, and your home directory quota may be only 10 GB. Use:
    > ```bash
    > conda create --prefix /scratch/alex.chamessian/envs/protein-design python=3.11
    > ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercises

    ### Exercise 1: Write Your SSH Config

    Create (or update) your `~/.ssh/config` file with an entry for WashU's RIS cluster. If you don't have RIS access yet, create a placeholder entry that you'll fill in once you get your account.

    Your config entry should include:
    - A short `Host` name
    - The full `HostName`
    - Your `User`
    - `ForwardAgent yes`
    - `ServerAliveInterval 60`
    """)
    return


@app.cell
def _():
    # Exercise 1: Write your SSH config entry
    # Run this cell to create or view your SSH config

    import os
    from pathlib import Path

    ssh_dir = Path.home() / ".ssh"
    config_path = ssh_dir / "config"

    # Create .ssh directory if it doesn't exist
    ssh_dir.mkdir(exist_ok=True)

    # Example config entry — edit this with your actual details
    example_config = """
    # WashU RIS Compute Cluster
    Host ris
        HostName compute1-client-1.ris.wustl.edu
        User YOUR_WUSTL_USERNAME
        ForwardAgent yes
        ServerAliveInterval 60
        ServerAliveCountMax 3
    """.strip()

    # Check if config already exists
    if config_path.exists():
        current = config_path.read_text()
        print("Your current SSH config:")
        print("-" * 40)
        print(current)
        print("-" * 40)
        if "ris" not in current.lower():
            print("\nNo RIS entry found. Consider adding this:")
            print(example_config)
    else:
        print("No SSH config file found. Here's a starter config:")
        print(example_config)
        print(f"\nTo create it, save the above to: {config_path}")
        print("Then run: chmod 600 ~/.ssh/config")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Practice File Transfer Commands

    Even without a remote machine, you can practice the syntax. The cell below generates the commands you'd use for common file transfer scenarios.
    """)
    return


@app.cell
def _():
    # Exercise 2: File transfer command builder
    # Fill in the blanks for each scenario, then check your answers

    scenarios = [
        {
            "description": "Upload your RFdiffusion config to the cluster's scripts directory",
            "hint": "scp local_file remote:path",
            "answer": "scp rfdiffusion_config.yaml ris:~/scripts/"
        },
        {
            "description": "Download all PDB files from a results directory on the cluster",
            "hint": "scp -r for directories, or rsync for many files",
            "answer": "rsync -avP ris:~/results/binder_pdbs/ ./local_results/"
        },
        {
            "description": "Sync your local analysis scripts to the cluster (only changed files)",
            "hint": "rsync only transfers what changed",
            "answer": "rsync -avP ./analysis_scripts/ ris:~/projects/nav17/scripts/"
        },
        {
            "description": "Preview what rsync WOULD transfer before actually doing it",
            "hint": "There's a flag for dry run",
            "answer": "rsync -avPn ris:~/results/ ./local_results/"
        },
    ]

    for i, s in enumerate(scenarios, 1):
        print(f"Scenario {i}: {s['description']}")
        print(f"  Hint: {s['hint']}")
        your_answer = input(f"  Your command: ") if False else ""  # Change False to True to make interactive
        print(f"  Answer: {s['answer']}")
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Plan Your Cluster Storage Layout

    Think about your actual research projects. In the cell below, sketch out where you'd put different files on the cluster.
    """)
    return


@app.cell
def _():
    # Exercise 3: Plan your cluster storage layout
    # For each item, decide: home, scratch, or project storage?

    items = {
        "Python scripts for RFdiffusion runs": "your answer here",
        "200GB raw RNA-seq FASTQ files": "your answer here",
        "SLURM submission scripts": "your answer here",
        "Conda environments (5-10GB each)": "your answer here",
        "Intermediate STAR alignment BAM files": "your answer here",
        "Final DESeq2 results tables (CSV)": "your answer here",
        "1000 RFdiffusion output PDB files (active screen)": "your answer here",
        "Top 10 validated binder designs (to share with lab)": "your answer here",
        "Your .bashrc and config files": "your answer here",
    }

    # Suggested answers (uncomment to check)
    answers = {
        "Python scripts for RFdiffusion runs": "HOME — small, important, should be backed up",
        "200GB raw RNA-seq FASTQ files": "PROJECT — large, shared, needs backup",
        "SLURM submission scripts": "HOME — small, part of your workflow code",
        "Conda environments (5-10GB each)": "SCRATCH or PROJECT — too large for home",
        "Intermediate STAR alignment BAM files": "SCRATCH — large, temporary, reproducible",
        "Final DESeq2 results tables (CSV)": "PROJECT — small, important, share with lab",
        "1000 RFdiffusion output PDB files (active screen)": "SCRATCH — active work, can regenerate",
        "Top 10 validated binder designs (to share with lab)": "PROJECT — curated results, share with team",
        "Your .bashrc and config files": "HOME — tiny, critical, backed up automatically",
    }

    for item, answer in answers.items():
        print(f"  {item}")
        print(f"    → {answer}")
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Reproducibility and Project Structure](../06-systems-thinking/03-reproducibility-and-project-structure.py) | [Module Index](../README.md) | [Next: Job Schedulers and SLURM \u2192](02-job-schedulers-and-slurm.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - [MIT Missing Semester — Lecture 5: Command-line Environment](https://missing.csail.mit.edu/2020/command-line/) — covers SSH, tmux, and remote machines in depth
    - [SSH documentation (man page)](https://man.openbsd.org/ssh) — the official reference
    - [rsync manual](https://download.samba.org/pub/rsync/rsync.1) — all the flags and options
    - [WashU RIS Documentation](https://docs.ris.wustl.edu/) — specific to WashU's compute cluster
    - [VS Code Remote - SSH Extension](https://code.visualstudio.com/docs/remote/ssh) — official guide to remote development
    - [Globus File Transfer](https://www.globus.org/) — managed research data transfer service

    ---

    ## Navigation

    **← Previous:** [Module 6: Data Skills](../06-data-skills/) | **Next →** [Notebook 2: Job Schedulers and SLURM](02-job-schedulers-and-slurm.py)

    ---

    ## Edit Log

    | Date | Change |
    |------|--------|
    | 2026-03-25 | Initial creation |
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

