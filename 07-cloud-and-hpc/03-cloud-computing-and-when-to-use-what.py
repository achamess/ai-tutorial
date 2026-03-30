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
    # Notebook 3: Cloud Computing and When to Use What

    > **Navigation:** [\u2190 Previous: Job Schedulers and SLURM](02-job-schedulers-and-slurm.py) | [Module Index](../README.md) | [Next: Descriptive Stats and Distributions \u2192](../08-math-you-need/01-descriptive-stats-and-distributions.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    **Your institution's cluster is free but has queues. Cloud GPUs cost money but start immediately. A collaborator's server has the software you need but you don't control it. Knowing WHEN to use each option is as important as knowing HOW.**

    You now know how to SSH into a remote machine and submit SLURM jobs. But the HPC cluster isn't the only option — and sometimes it's not the best one. Maybe the GPU queue is backed up for days and you need ESMFold results by Friday. Maybe you want to share a runnable analysis with a collaborator who doesn't have cluster access. Maybe you need a specific GPU that your cluster doesn't have.

    This notebook helps you make the right decision for each computational task, understand cloud options, and avoid the pitfalls (especially the "I accidentally left a $30/hour GPU running for a week" pitfall).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 1: The Decision Framework

    ### 🤔 Decision Point: Local vs. HPC vs. Cloud

    This is the most important table in this entire module:

    | Factor | Your Laptop | HPC Cluster (RIS) | Cloud (AWS/GCP/Lambda) |
    |--------|-------------|-------------------|------------------------|
    | **Cost** | Free (already own it) | Free (institution pays) | Pay per hour ($1-30/hr for GPUs) |
    | **GPUs** | None (Mac) or limited | Shared, may have to queue | On-demand, any size |
    | **Setup time** | Already set up | Account needed, module system | Account + credit card, full config |
    | **Data access** | Local, fast | Shared filesystem, quotas | Must upload/download |
    | **Queue time** | None | Minutes to days | None (pay to skip the line) |
    | **Control** | Full | Limited (admin policies) | Full (you're root) |
    | **Best for** | Small analyses, writing code, prototyping | Production runs, large datasets, batch jobs | Burst GPU needs, specific software, deadlines |

    > 💡 **Tip:** The default strategy is: **develop on your laptop, run on the cluster, use cloud only when the other two can't do it.** This minimizes cost while maximizing convenience.

    ### Decision Tree

    ```mermaid
    graph TD
        A["🤔 I have a computation to run"] --> B{"Does it need a GPU?"}
        B -->|No| C{"Is the data > 10GB?"}
        B -->|Yes| D{"Is WashU RIS available<br/>with reasonable queue time?"}

        C -->|No| E["✅ Run on your laptop"]
        C -->|Yes| F{"Does it need > 32GB RAM?"}
        F -->|No| E
        F -->|Yes| G["✅ Run on HPC cluster"]

        D -->|Yes| H["✅ Submit to RIS<br/>(free GPU!)"]
        D -->|No, queue is days long| I{"How urgent is this?"}

        I -->|Can wait| H
        I -->|Need it this week| J{"Budget available?"}

        J -->|Yes| K["✅ Lambda Labs or<br/>cloud GPU (~$1-4/hr)"]
        J -->|No| L["✅ Try Google Colab<br/>(free tier, limited)"]

        style E fill:#e8f5e9
        style G fill:#e8f5e9
        style H fill:#e8f5e9
        style K fill:#fff3e0
        style L fill:#e3f2fd
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 2: Cloud Computing Basics

    ### What "The Cloud" Actually Is

    > 🔑 **Key concept:** "The cloud" is just someone else's data center, rented by the hour. You're paying to use a computer that sits in a warehouse somewhere. When you're done, you turn it off and stop paying.

    There's nothing magical about cloud computing. You get a Linux machine (called an "instance" or "VM") with an IP address. You SSH in, install your software, run your job, download results, and shut it down. The only difference from your HPC cluster is that you pay by the hour and you have root access.

    ### The Big Three (and When Each Matters)

    | Provider | Strengths | Weaknesses | Best for researchers when... |
    |----------|-----------|------------|------------------------------|
    | **AWS** (Amazon) | Largest selection of instance types, most tools | Complex, easy to rack up bills | You need specific/exotic hardware, or your institution has AWS credits |
    | **Google Cloud (GCP)** | Good ML/AI tools, Colab integration, life sciences APIs | Smaller GPU selection | You use Colab, or need Google's ML ecosystem (TPUs, Vertex AI) |
    | **Microsoft Azure** | Good enterprise integration, GitHub Codespaces | Less popular in academia | Your institution has a Microsoft agreement |

    For most researchers, the provider barely matters. What matters is: **can I get a GPU at a reasonable price?**

    > ⚠️ **Warning:** LEAVING A GPU INSTANCE RUNNING OVERNIGHT COSTS $20-50+. A forgotten p3.2xlarge on AWS costs ~$3/hour = $72/day = $500/week. Always shut down when done. Set calendar reminders. Set billing alerts.

    ### Instance Types That Matter for Your Research

    | Provider | Instance | GPU | RAM | Cost/hr (approx.) | Use for |
    |----------|----------|-----|-----|-------------------|---------|
    | AWS | p3.2xlarge | 1x V100 (16GB) | 61 GB | ~$3.00 | RFdiffusion, ESMFold |
    | AWS | p4d.24xlarge | 8x A100 (40GB) | 1.1 TB | ~$32.00 | Large-scale campaigns |
    | GCP | a2-highgpu-1g | 1x A100 (40GB) | 85 GB | ~$3.70 | Protein structure prediction |
    | GCP | g2-standard-4 | 1x L4 (24GB) | 16 GB | ~$0.70 | Budget-friendly GPU work |
    | Lambda Labs | gpu_1x_a100 | 1x A100 (40GB) | 200 GB | ~$1.10 | Best value single GPU |
    | Lambda Labs | gpu_1x_h100 | 1x H100 (80GB) | 200 GB | ~$2.00 | Latest GPU, great value |

    > 💡 **Tip:** Prices change frequently. Check current pricing before spinning up instances. The trend is downward — cloud GPUs are getting cheaper.

    <details>
    <summary>📖 <strong>Deep dive:</strong> Spot/preemptible instances — 60-90% cheaper (click to expand)</summary>

    <br/>

    Cloud providers have idle capacity that they sell at a steep discount as **spot instances** (AWS) or **preemptible instances** (GCP). The catch: they can be terminated with little warning (2 minutes on AWS, 30 seconds on GCP) when someone else wants that capacity at full price.

    | Type | Discount | Interruption risk | Good for |
    |------|----------|-------------------|----------|
    | On-demand | 0% (full price) | None | Critical jobs, deadlines |
    | Spot/preemptible | 60-90% off | Can be terminated anytime | Fault-tolerant jobs, job arrays, checkpointed training |

    **When spot instances work for you:**
    - Job arrays where losing one task doesn't lose everything
    - Training runs with checkpointing (saves progress every N minutes)
    - Quick experiments where you can just restart if interrupted

    **When to avoid spot:**
    - Single long-running job with no checkpointing
    - Anything where interruption means starting completely over

    A V100 on AWS drops from ~$3/hr to ~$0.90/hr as a spot instance. For a 50-design RFdiffusion campaign, that's $45 vs $150.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 3: Practical Cloud Options for Researchers

    Not all cloud services are created equal. Here are the ones most relevant to your work, ranked roughly from simplest to most complex.

    ### Lambda Labs — Simplest GPU Rental

    [Lambda Labs](https://lambdalabs.com/service/gpu-cloud) is the easiest way to rent a GPU. No complex configuration, no cloud-specific jargon. You pick an instance type, launch it, and SSH in. It's just a Linux machine with NVIDIA drivers and CUDA pre-installed.

    **The workflow:**
    1. Create an account at lambdalabs.com
    2. Add your SSH public key in the dashboard
    3. Launch an instance (e.g., 1x A100 for $1.10/hr)
    4. SSH in: `ssh ubuntu@<ip-address>`
    5. Run your job
    6. Download results
    7. **Terminate the instance** (stop paying)

    **Why researchers like it:** lowest prices for GPU-hours, minimal setup, no hidden fees. The downside: instances may not always be available during high demand.

    ### Google Colab Pro — Jupyter with GPUs in the Browser

    [Google Colab](https://colab.research.google.com/) gives you a Jupyter notebook with a GPU, right in your browser. No SSH, no setup.

    - **Free tier:** T4 GPU, ~12GB RAM, sessions time out after ~90 min of inactivity
    - **Colab Pro ($10/mo):** Longer runtimes, A100 access, more RAM
    - **Colab Pro+ ($50/mo):** Background execution, priority GPU access

    **Good for:** quick prototyping, sharing analyses with collaborators, running ESMFold on a few sequences.

    **Bad for:** production runs, large datasets (have to re-upload every session), anything needing more than ~12 hours of continuous runtime.

    > 💡 **Tip:** Colab is great for sharing. If you make a Colab notebook that runs a protein structure prediction, you can send the link to a collaborator and they can run it in their browser — no installation needed.

    ### Modal — Python-Native Cloud Compute

    [Modal](https://modal.com/) is a newer approach: instead of renting a whole machine, you write Python functions and Modal runs them on GPUs automatically. No SSH, no machine management.

    ```python
    import modal

    app = modal.App("protein-design")

    @app.function(gpu="A100", image=modal.Image.debian_slim().pip_install("torch"))
    def predict_structure(sequence: str):
        # This function runs on a cloud A100 GPU
        import torch
        # ... your ESMFold code here ...
        return structure

    # Run it
    with app.run():
        result = predict_structure.remote("MKTVRQERLKSIVRI...")
    ```

    **Good for:** burst compute, custom ML pipelines, when you don't want to manage servers. Free tier includes $30/month of credits.

    ### Other Options Worth Knowing

    | Platform | What it is | When to consider |
    |----------|-----------|-----------------|
    | **Binder** ([mybinder.org](https://mybinder.org/)) | Free, ephemeral Jupyter notebooks from a GitHub repo | Sharing this tutorial or an analysis with zero setup for the reader |
    | **GitHub Codespaces** | VS Code in the browser with configurable compute | Developing on a powerful machine without local setup |
    | **Vast.ai** | Marketplace for renting individual GPUs (often cheaper) | Budget-constrained GPU work, but less polished |

    ### 🤔 Decision Point: Which Cloud for Which Task

    | Task | Best option | Why |
    |------|-------------|-----|
    | Quick protein structure prediction (few sequences) | Google Colab (free) | Free GPU, Jupyter interface, fast setup |
    | RFdiffusion binder design campaign (50+ designs) | WashU RIS or Lambda Labs | Needs sustained GPU, batch jobs |
    | Sharing analysis notebook with collaborator | Google Colab or Binder | Zero setup for the reader |
    | Custom ML pipeline with complex dependencies | Modal or Lambda Labs | Full control, scalable |
    | One-off large computation (deadline pressure) | Lambda Labs | Cheapest GPU-hours, no queue |
    | Trying out a new tool before installing on HPC | Google Colab | Quick, disposable, no commitment |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 4: Containers — Reproducible Environments Anywhere

    ### What Are Containers?

    > 🔑 **Key concept:** A container is a snapshot of an entire computing environment — the OS, all libraries, all tools, all configuration — packaged into a single file. "It works on my machine" is solved by shipping the machine.

    Imagine you could take a picture of your perfectly configured computer (with RFdiffusion, ProteinMPNN, all the right CUDA versions, everything working) and hand that picture to a colleague. They "load" it on their machine and have an identical setup. That's what containers do.

    ### Docker vs. Singularity (Apptainer)

    You've probably heard of Docker. It's the most popular container system, but HPC clusters use **Singularity** (now called **Apptainer**) instead.

    **Why?** Docker requires root (administrator) access. On a shared cluster, giving every user root access is a security nightmare. Singularity runs as a normal user — no special privileges needed.

    The good news: Singularity can run Docker containers. So the vast ecosystem of Docker images (including NVIDIA's GPU-optimized images) works on your HPC cluster.

    ### Basic Singularity Workflow

    ```bash
    # Step 1: Pull a container image (do this once)
    # This downloads NVIDIA's PyTorch container from their registry
    singularity pull docker://nvcr.io/nvidia/pytorch:24.01-py3
    # Creates: pytorch_24.01-py3.sif (a single file, ~8GB)

    # Step 2: Run a command inside the container
    singularity exec --nv pytorch_24.01-py3.sif python my_script.py
    # --nv flag = enable NVIDIA GPU support inside the container

    # Step 3: Get an interactive shell inside the container
    singularity shell --nv pytorch_24.01-py3.sif
    # Now you're "inside" — all the container's software is available
    # Type 'exit' to leave
    ```

    That's it. The `.sif` file IS the container. You can copy it, share it, put it on any cluster with Singularity installed, and it will work identically.

    ### When You Need Containers

    - **Sharing pipelines:** "Here's exactly how to reproduce my RFdiffusion analysis" — hand them the `.sif` file
    - **Complex dependencies:** RFdiffusion needs specific versions of PyTorch, CUDA, and various libraries. A container bundles them all.
    - **Publishing:** For a paper, you can deposit the container alongside your code — perfect reproducibility
    - **Cross-cluster portability:** Move from WashU RIS to a collaborator's cluster without reinstalling anything

    ### 🤔 Decision Point: venv vs. Conda vs. Container

    | Approach | Reproducibility | Portability | Complexity | Setup time | Use when |
    |----------|----------------|-------------|------------|------------|----------|
    | **venv** | Medium | Low (Python-only) | Low | Minutes | Simple Python projects, quick scripts |
    | **Conda** | High | Medium | Medium | 10-30 min | Non-Python deps needed (CUDA drivers, C libraries) |
    | **Container** | Perfect | High (any machine) | Higher | 30-60 min first time | Sharing, publishing, complex dep stacks |

    > 💡 **Tip:** You don't have to use containers for everything. Most of the time, a conda environment is fine. Containers shine when you need to share or reproduce an environment exactly — which matters most for publications and collaborations.

    <details>
    <summary>📖 <strong>Deep dive:</strong> Building your own Docker container for a protein design pipeline (click to expand)</summary>

    <br/>

    If you need to build a custom container (because no existing image has exactly what you need), here's a Dockerfile example:

    ```dockerfile
    # Start from NVIDIA's PyTorch base image (has CUDA + PyTorch pre-installed)
    FROM nvcr.io/nvidia/pytorch:24.01-py3

    # Install system dependencies
    RUN apt-get update && apt-get install -y \
        git \
        wget \
        && rm -rf /var/lib/apt/lists/*

    # Install Python packages
    RUN pip install --no-cache-dir \
        biopython \
        pandas \
        matplotlib \
        seaborn \
        prody

    # Clone and install RFdiffusion
    RUN git clone https://github.com/RosettaCommons/RFdiffusion.git /opt/RFdiffusion
    WORKDIR /opt/RFdiffusion
    RUN pip install --no-cache-dir -e .

    # Download model weights
    RUN mkdir -p models && \
        wget -q https://files.example.com/rfdiffusion_weights.pt -O models/weights.pt

    # Set default working directory
    WORKDIR /workspace
    ```

    **Build it (on your laptop or a machine where you have Docker):**
    ```bash
    docker build -t protein-design:v1 .
    ```

    **Convert to Singularity for HPC:**
    ```bash
    # Option 1: Build Singularity image directly from Docker
    singularity build protein-design_v1.sif docker://protein-design:v1

    # Option 2: Push to Docker Hub first, then pull on HPC
    docker push yourusername/protein-design:v1
    # Then on the HPC cluster:
    singularity pull docker://yourusername/protein-design:v1
    ```

    **Use in a SLURM script:**
    ```bash
    #!/bin/bash
    #SBATCH --partition=gpu
    #SBATCH --gres=gpu:1
    #SBATCH --mem=32G

    singularity exec --nv \
        --bind /scratch/$USER:/workspace/data \
        protein-design_v1.sif \
        python run_rfdiffusion.py --target nav17 --n_designs 50
    ```

    The `--bind` flag maps a directory on the host into the container, so your container can read/write data on the cluster's filesystem.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 5: Claude Code on Remote Machines

    One of the most powerful combinations in your toolkit: running Claude Code on a remote machine where your data and compute actually live.

    ### Running Claude Code Over SSH

    If Node.js is available on the remote machine, Claude Code works over SSH exactly like it does locally:

    ```bash
    # SSH into the cluster
    ssh ris

    # Check if Node.js is available
    node --version
    # If not: module load nodejs  (or install via conda: conda install -c conda-forge nodejs)

    # Run Claude Code
    claude
    ```

    Now Claude Code can:
    - **Read your SLURM logs** and tell you why a job failed
    - **Write SLURM submission scripts** for your specific workflow
    - **Navigate unfamiliar file structures** on the cluster
    - **Debug Python scripts** using the cluster's actual environment
    - **Check resource usage** and suggest optimal SLURM parameters

    ### VS Code Remote SSH + Claude Code

    For the best experience:
    1. Connect to the cluster via VS Code Remote SSH (covered in Notebook 1)
    2. Claude Code runs in VS Code's integrated terminal, on the cluster
    3. You get full IDE features + Claude Code + cluster compute in one window

    This means you can say to Claude: "Look at the error log in logs/1234567_binder_screen.err and fix the submission script" — and it can read the actual files on the cluster and edit them directly.

    > 💡 **Tip:** This is incredibly powerful for debugging. Instead of manually reading error logs and googling error messages, Claude Code can read the log, understand the error in context, and suggest (or make) the fix — all on the remote machine.

    > ⚠️ **Warning:** Check your institution's policy on running AI tools on cluster login nodes. Some clusters restrict outbound internet access on login nodes (Claude Code needs to connect to Anthropic's API). If that's the case, you may need to use VS Code Remote SSH instead, which routes the connection through your laptop.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 6: Cost Management and Avoiding Surprises

    > ⚠️ **Warning:** Cloud billing horror stories are real. Researchers have accidentally left GPU instances running and received bills for thousands of dollars. This section exists to make sure that never happens to you.

    ### Rule #1: Set Budget Alerts FIRST

    Before you launch anything on any cloud platform, set up billing alerts:

    - **AWS:** Billing → Budgets → Create budget → set a monthly limit (e.g., $50) with email alerts at 50%, 80%, 100%
    - **Google Cloud:** Billing → Budgets & alerts → Create budget
    - **Lambda Labs:** Prepaid credits only (you can't overspend — but you also lose unused credits)

    ### Rule #2: Always Shut Down When Done

    ```bash
    # On AWS (from your laptop, using AWS CLI)
    aws ec2 stop-instances --instance-ids i-1234567890abcdef0
    # stop = preserves data but stops billing for compute (storage still costs pennies)
    # terminate = deletes everything, stops all billing

    # On Lambda Labs: use the web dashboard to terminate
    # On Google Cloud:
    gcloud compute instances stop my-gpu-instance --zone=us-central1-a
    ```

    > 💡 **Tip:** Set a calendar reminder for 1 hour after you launch a cloud instance: "Did you shut down the GPU?" Better yet, write a script that shuts it down after your job finishes.

    ### Estimating Costs Before Running

    Before you spin up cloud resources, do this quick calculation:

    ```
    Total cost = (estimated hours) × (price per hour) × (number of instances)
    ```

    For example:
    - RFdiffusion, 50 designs, ~1 hour each on 1 GPU = 50 GPU-hours
    - On Lambda Labs A100 at $1.10/hr = **$55**
    - On AWS p3.2xlarge at $3.00/hr = **$150**
    - On WashU RIS = **$0** (but might wait in queue)

    > 💡 **Tip:** Use `tmux` or `screen` on remote machines so your work survives if your SSH connection drops. This is essential for long-running jobs on cloud instances:
    > ```bash
    > # Start a tmux session
    > tmux new -s protein_design
    >
    > # Run your job inside tmux
    > python run_rfdiffusion.py --n_designs 50
    >
    > # Detach from tmux (job keeps running): press Ctrl+B, then D
    > # Reconnect later:
    > tmux attach -t protein_design
    > ```
    > If your WiFi drops or you close your laptop, the job keeps running inside tmux.

    ### Free and Cheap Options

    | Option | Cost | GPU access | Limitations |
    |--------|------|-----------|-------------|
    | **WashU RIS** | Free | Yes (shared) | Queue times, institutional policies |
    | **Google Colab free tier** | Free | T4 (limited) | 90-min idle timeout, ~12 hr max session |
    | **Google Colab Pro** | $10/month | T4, A100 | Longer sessions, not unlimited |
    | **Lambda Labs** | $1.10-2.00/hr | A100, H100 | Availability varies |
    | **Modal free tier** | $30/month credits | Various | Enough for testing and small runs |
    | **AWS/GCP free tier** | Free (limited) | No GPUs | CPU-only, small instances, 12 months |

    <details>
    <summary>📖 <strong>Deep dive:</strong> AWS cost calculator walkthrough (click to expand)</summary>

    <br/>

    AWS has an online [Pricing Calculator](https://calculator.aws/) that lets you estimate costs before committing. Here's how to use it for a protein design workflow:

    1. Go to [calculator.aws](https://calculator.aws/)
    2. Click "Add service" → search for "EC2"
    3. Configure:
       - **Region:** US East (cheapest for most instances)
       - **Instance type:** p3.2xlarge (1x V100)
       - **Usage:** 50 hours/month (for a binder screening campaign)
       - **Storage:** 100 GB General Purpose SSD
    4. See the estimate: ~$150 for compute + ~$10 for storage = **~$160/month**

    Compare this to Lambda Labs: 50 hours × $1.10 = **$55**. The savings are significant for simple GPU workloads.

    **Hidden costs to watch for:**
    - **Data transfer out:** AWS charges for downloading data from their servers (~$0.09/GB after the first 100GB/month). A 50GB results download costs ~$4.50.
    - **Storage:** Even when an instance is stopped, its disk still costs money (~$0.10/GB/month). A 500GB disk costs $50/month just sitting there.
    - **Elastic IPs:** If you reserve a public IP address and don't use it, AWS charges $0.005/hr (~$3.60/month).

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 7: Putting It All Together — Decision Matrix

    Here's the comprehensive decision matrix for your actual research tasks. Bookmark this section — you'll come back to it.

    ### Your Tasks, Mapped to the Right Platform

    | Task | Data size | GPU needed? | Recommended platform | Estimated cost |
    |------|-----------|-------------|---------------------|----------------|
    | Analyze calcium imaging (one session) | ~1 GB | No | **Your laptop** | Free |
    | RNA-seq DESeq2 analysis (counts → DE genes) | ~100 MB (count matrix) | No | **Your laptop** | Free |
    | RNA-seq alignment with STAR | ~200 GB (FASTQ files) | No, but 30-50 GB RAM | **HPC cluster** | Free |
    | RFdiffusion (10 designs, testing) | ~1 GB | Yes (1 GPU) | **HPC cluster** (interactive `srun`) | Free |
    | RFdiffusion (100-1000 designs, production) | ~1 GB | Yes (many GPUs) | **HPC cluster** (job array) | Free |
    | ESMFold batch prediction (50 sequences) | ~500 MB | Yes (1 GPU) | **HPC cluster** or Google Colab | Free |
    | ProteinMPNN sequence design | ~500 MB | Yes (1 GPU) | **HPC cluster** or Lambda Labs | Free / ~$5 |
    | BoltzGen conformational sampling | ~1 GB | Yes (1 GPU) | **HPC cluster** | Free |
    | Train custom ML model (e.g., pain classifier) | Varies | Yes (extended time) | **HPC cluster** or Lambda Labs | Free / $20-100 |
    | Quick protein structure check (1-2 sequences) | ~1 MB | Yes but brief | **Google Colab** (free tier) | Free |
    | Share analysis with collaborator | Varies | Maybe | **Google Colab** or **Binder** | Free |
    | Processing behavioral assay videos | ~10-50 GB | Maybe (DeepLabCut) | **HPC cluster** or laptop | Free |
    | Exploratory data analysis (plotting, stats) | ~1 GB | No | **Your laptop** | Free |

    ### The 80/20 Rule

    For 80% of your work, you'll use just two platforms:
    1. **Your laptop** — for writing code, small analyses, visualization, prototyping
    2. **WashU RIS cluster** — for everything that needs more compute (GPUs, lots of RAM, batch processing)

    The remaining 20% — cloud GPUs, Colab, containers — are for special situations: deadlines, sharing, unavailable resources, or specific software requirements.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercises

    ### Exercise 1: Map Your Computational Tasks to Platforms

    Think about the computational tasks you're currently doing or planning. For each one, decide the right platform and estimate cost.
    """)
    return


@app.cell
def _():
    # Exercise 1: Map your computational tasks to platforms
    # Fill in your own tasks and decisions

    import pandas as pd

    # Example template — replace with your actual tasks
    my_tasks = pd.DataFrame({
        "Task": [
            "RFdiffusion NaV1.7 binder screen (200 designs)",
            "RNA-seq analysis of DRG neurons (CFA model)",
            "ESMFold validation of top binder candidates",
            "Calcium imaging processing (10 sessions)",
            "ProteinMPNN sequence optimization",
            # Add your own tasks below:
            "YOUR TASK HERE",
        ],
        "Data Size": [
            "~1 GB",
            "~200 GB raw, ~100 MB counts",
            "~50 MB",
            "~10 GB",
            "~100 MB",
            "???",
        ],
        "GPU Needed?": [
            "Yes",
            "No (but lots of RAM for STAR)",
            "Yes",
            "No",
            "Yes",
            "???",
        ],
        "Platform": [
            "HPC (job array, gpu partition)",
            "HPC (STAR) + laptop (DESeq2)",
            "HPC or Colab",
            "Laptop",
            "HPC",
            "???",
        ],
        "Est. Cost": [
            "Free (RIS)",
            "Free (RIS + laptop)",
            "Free",
            "Free",
            "Free (RIS)",
            "???",
        ],
    })

    # Display nicely
    pd.set_option('display.max_colwidth', 50)
    print(my_tasks.to_string(index=False))
    print("\nEdit the DataFrame above to add your own tasks!")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Cloud Cost Estimator

    Practice estimating cloud costs for different scenarios.
    """)
    return


@app.cell
def _():
    # Exercise 2: Cloud cost estimator
    # Calculate costs for different scenarios

    def estimate_cost(hours_per_job, num_jobs, price_per_hour, parallel_jobs=1):
        """Estimate cloud computing cost.
    
        Args:
            hours_per_job: How long each job takes (in hours)
            num_jobs: How many jobs to run
            price_per_hour: Cost per GPU-hour
            parallel_jobs: How many jobs run simultaneously
    
        Returns:
            Total cost and wall-clock time
        """
        total_gpu_hours = hours_per_job * num_jobs
        wall_clock_hours = (hours_per_job * num_jobs) / parallel_jobs
        total_cost = total_gpu_hours * price_per_hour
    
        return {
            "Total GPU-hours": total_gpu_hours,
            "Wall-clock hours": wall_clock_hours,
            "Total cost": f"${total_cost:.2f}",
            "Cost per job": f"${(total_cost / num_jobs):.2f}",
        }

    # Scenario 1: RFdiffusion binder screen
    print("=" * 50)
    print("Scenario 1: RFdiffusion binder screen")
    print("=" * 50)
    scenarios = {
        "Lambda Labs A100 ($1.10/hr)": estimate_cost(
            hours_per_job=1, num_jobs=100, price_per_hour=1.10, parallel_jobs=5
        ),
        "AWS p3.2xlarge V100 ($3.00/hr)": estimate_cost(
            hours_per_job=1, num_jobs=100, price_per_hour=3.00, parallel_jobs=5
        ),
        "WashU RIS (free!)": estimate_cost(
            hours_per_job=1, num_jobs=100, price_per_hour=0.00, parallel_jobs=10
        ),
    }
    for provider, result in scenarios.items():
        print(f"\n  {provider}:")
        for k, v in result.items():
            print(f"    {k}: {v}")

    # Scenario 2: Forgotten GPU instance
    print("\n" + "=" * 50)
    print("Scenario 2: The 'I forgot to shut it down' scenario")
    print("=" * 50)
    forgotten_costs = {
        "Lambda Labs A100 - 1 day": 1.10 * 24,
        "Lambda Labs A100 - 1 week": 1.10 * 24 * 7,
        "AWS p3.2xlarge - 1 day": 3.00 * 24,
        "AWS p3.2xlarge - 1 week": 3.00 * 24 * 7,
        "AWS p4d.24xlarge - 1 day": 32.00 * 24,
        "AWS p4d.24xlarge - 1 week": 32.00 * 24 * 7,
    }
    for scenario, cost in forgotten_costs.items():
        warning = " ⚠️ OUCH" if cost > 100 else ""
        print(f"  {scenario}: ${cost:,.2f}{warning}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Design Your Compute Strategy

    Based on everything in this module, sketch out a compute strategy for a real research project. Think about a current or upcoming project and answer these questions:
    """)
    return


@app.cell
def _():
    # Exercise 3: Design your compute strategy
    # Fill in the template for one of your research projects

    project_plan = """
    PROJECT: De Novo NaV1.7 Binder Design Campaign
    ================================================

    1. DEVELOPMENT PHASE (laptop)
       - Write and test RFdiffusion wrapper scripts
       - Design target specifications (which NaV1.7 domains to target)
       - Small test runs (if GPU available via Colab)
       Platform: Laptop + Google Colab for GPU testing
       Cost: Free

    2. PRODUCTION SCREENING (HPC)
       - Run RFdiffusion: 500 designs across 5 target sites
       - Job array: --array=0-499%20 on gpu partition
       - Estimated time: ~1 hr per design, 20 parallel = ~25 hours wall time
       Platform: WashU RIS
       Cost: Free

    3. STRUCTURE VALIDATION (HPC)
       - ESMFold prediction on top 100 candidates (by RFdiffusion score)
       - Filter by pLDDT > 70
       - Job array: --array=0-99%10
       Platform: WashU RIS
       Cost: Free

    4. SEQUENCE OPTIMIZATION (HPC)
       - ProteinMPNN on top 50 structures
       - 10 sequence variants per structure = 500 sequences
       Platform: WashU RIS
       Cost: Free

    5. ANALYSIS & VISUALIZATION (laptop)
       - Score distributions, structure visualization
       - Select candidates for experimental testing
       Platform: Laptop
       Cost: Free

    6. SHARING WITH COLLABORATORS
       - Google Colab notebook showing top candidates
       - Interactive PyMOL/py3Dmol visualization
       Platform: Google Colab
       Cost: Free

    TOTAL ESTIMATED COST: $0 (all on institutional HPC + free tools)
    BACKUP PLAN: If RIS queue is >3 days, use Lambda Labs (~$55 for 50 GPU-hours)
    """

    print(project_plan)
    print("\nNow write your own project plan! Copy and modify the template above.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Job Schedulers and SLURM](02-job-schedulers-and-slurm.py) | [Module Index](../README.md) | [Next: Descriptive Stats and Distributions \u2192](../08-math-you-need/01-descriptive-stats-and-distributions.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - [AWS for Researchers](https://aws.amazon.com/government-education/research-and-technical-computing/) — AWS programs and credits for academic research
    - [Google Cloud for Life Sciences](https://cloud.google.com/life-sciences) — Google's life sciences-specific cloud tools
    - [Lambda Labs Cloud](https://lambdalabs.com/service/gpu-cloud) — GPU cloud pricing and documentation
    - [Modal Documentation](https://modal.com/docs) — Python-native cloud compute
    - [Singularity/Apptainer Documentation](https://apptainer.org/docs/user/latest/) — container system for HPC
    - [Docker Getting Started](https://docs.docker.com/get-started/) — container basics (transferable to Singularity)
    - [WashU RIS Documentation](https://docs.ris.wustl.edu/) — WashU-specific cluster resources
    - [MIT Missing Semester — Lecture 5: Command-line Environment](https://missing.csail.mit.edu/2020/command-line/) — tmux, SSH, and remote work
    - [AWS Pricing Calculator](https://calculator.aws/) — estimate costs before committing

    ---

    ## Navigation

    **← Previous:** [Notebook 2: Job Schedulers and SLURM](02-job-schedulers-and-slurm.py) | **Next Module →** [Module 8: AI Landscape](../08-ai-landscape/)

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

