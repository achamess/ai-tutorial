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
    # Notebook 2: Job Schedulers and SLURM

    > **Navigation:** [\u2190 Previous: Remote Computing Fundamentals](01-remote-computing-fundamentals.py) | [Module Index](../README.md) | [Next: Cloud Computing and When to Use What \u2192](03-cloud-computing-and-when-to-use-what.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Why This Matters

    **You can't just run RFdiffusion on a login node — it would hog resources and get killed. HPC clusters use a scheduler (usually SLURM) to fairly distribute compute. Understanding SLURM is the difference between "submitted 100 binder designs overnight" and "my job has been pending for 3 days."**

    WashU's RIS cluster uses SLURM (Simple Linux Utility for Resource Management). So do most academic clusters in the US. Once you learn SLURM, you can use practically any university HPC system.

    This notebook teaches you to write SLURM scripts, submit jobs, monitor them, and — most importantly — request the right resources so your jobs start quickly and finish successfully.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ---

    ## Section 1: How a Cluster Works

    ### Login Nodes vs. Compute Nodes

    When you `ssh ris`, you land on a **login node**. This is the gateway — a shared machine where you:
    - Edit scripts
    - Transfer files
    - Submit jobs
    - Check job status

    You do NOT run heavy computation here. The login node is shared by every user on the cluster.

    """),
    mo.mermaid(
        """
        graph TD
            A["👤 You (ssh ris)"] --> B["🚪 Login Node<br/><i>Edit scripts, submit jobs</i><br/>⚠️ NO heavy compute!"]
            B -->|sbatch submit.sh| C["📋 SLURM Scheduler<br/><i>Manages the queue</i>"]
            C -->|assigns resources| D["⚙️ Compute Node<br/>64 cores, 256GB RAM"]
            C -->|assigns resources| E["🎮 GPU Node<br/>4× A100, 256GB RAM"]
            C -->|assigns resources| F["⚙️ Compute Node<br/>64 cores, 256GB RAM"]
        
            D --> G["📊 Your RNA-seq<br/>alignment runs here"]
            E --> H["🧬 Your RFdiffusion<br/>job runs here"]
        
            style B fill:#fff3e0
            style C fill:#e3f2fd
            style E fill:#e8f5e9
        """
    ),
    mo.md(r"""

    > ⚠️ **Warning:** NEVER run heavy computation on a login node. This includes RFdiffusion, STAR alignment, large Python scripts, anything GPU-intensive, or even `conda create` (which can use lots of CPU). If you do, your process will likely be killed automatically, and you may receive a warning email from the HPC admins. Use `sbatch` or `srun` instead.

    ### The Job Queue

    The scheduler works like a restaurant host:

    1. You **submit** a job (like putting your name on the waitlist)
    2. You tell the scheduler what you need: "I need a table for 4 (4 CPUs), with a view (GPU), for about 2 hours"
    3. The scheduler **finds resources** that match your request
    4. When resources are available, your job **starts running**
    5. When it finishes (or runs out of time), the resources are freed

    > 🔑 **Key concept:** You're not running things interactively (usually). You write a script that contains your commands, submit it to the scheduler, and check back later. This is called **batch processing** — and it's why you can submit 100 binder designs at 5pm and find results waiting at 9am.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 2: Your First SLURM Job

    ### Anatomy of a SLURM Script

    A SLURM script is just a bash script with special `#SBATCH` comments at the top. These comments tell the scheduler what resources you need. Here's a complete example for running RFdiffusion:

    ```bash
    #!/bin/bash
    #SBATCH --job-name=binder_screen
    #SBATCH --output=logs/%j_%x.out
    #SBATCH --error=logs/%j_%x.err
    #SBATCH --partition=gpu
    #SBATCH --gres=gpu:1
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=32G
    #SBATCH --time=04:00:00
    #SBATCH --mail-user=alex.chamessian@wustl.edu
    #SBATCH --mail-type=END,FAIL

    # --- Everything above is for SLURM. Everything below is your actual work. ---

    # Load required software
    module load python/3.11 cuda/12.0
    source ~/envs/protein-design/bin/activate

    # Create output directory
    mkdir -p results/nav17_binders

    # Run the actual computation
    python run_rfdiffusion.py --target nav17_cterminus --n_designs 50

    echo "Job finished at $(date)"
    ```

    Let's break down every `#SBATCH` directive:

    | Directive | Value | What it means | What happens if wrong |
    |-----------|-------|---------------|----------------------|
    | `--job-name` | `binder_screen` | A human-readable name for your job | Nothing breaks, but `squeue` output is confusing |
    | `--output` | `logs/%j_%x.out` | Where stdout goes. `%j`=job ID, `%x`=job name | Output is lost or goes to default file |
    | `--error` | `logs/%j_%x.err` | Where stderr goes | Error messages are lost |
    | `--partition` | `gpu` | Which group of nodes to use | Job rejected if partition doesn't exist |
    | `--gres=gpu:1` | 1 GPU | Request 1 GPU | No GPU allocated — CUDA errors |
    | `--cpus-per-task` | `4` | Number of CPU cores | Too few = slow; too many = longer queue wait |
    | `--mem` | `32G` | RAM (memory) | Too little = job killed (OOM); too much = longer wait |
    | `--time` | `04:00:00` | Max walltime (4 hours) | Too little = job killed at time limit; too much = longer wait |
    | `--mail-user` | your email | Where to send notifications | No notifications |
    | `--mail-type` | `END,FAIL` | When to email (job ends or fails) | Wrong events or no emails |

    > 💡 **Tip:** Always request email notifications with `--mail-type=END,FAIL`. You don't want to manually check `squeue` every hour. When your binder design run finishes (or crashes), you'll get an email.

    > ⚠️ **Warning:** The `logs/` directory in `--output=logs/%j_%x.out` must exist BEFORE you submit the job. SLURM won't create it for you. Add `mkdir -p logs` to your workflow, or create it once in your project directory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Essential SLURM Commands

    Once you have a script, here are the commands you'll use daily:

    ```bash
    # Submit a job
    sbatch submit_rfdiffusion.sh
    # Output: "Submitted batch job 1234567"

    # Check YOUR jobs
    squeue -u $USER
    # Output:
    #   JOBID  PARTITION  NAME           STATE    TIME   NODES  NODELIST
    #   1234567  gpu      binder_screen  RUNNING  01:23  1      gpu-node-05

    # Check a specific job in detail
    scontrol show job 1234567

    # Cancel a job
    scancel 1234567

    # Cancel ALL your jobs (careful!)
    scancel -u $USER

    # Check a COMPLETED job's details (runtime, memory used)
    sacct -j 1234567

    # More useful sacct format — shows what resources you actually used
    sacct -j 1234567 --format=JobID,JobName,Elapsed,MaxRSS,MaxVMSize,TotalCPU,State
    ```

    The job states you'll see in `squeue`:

    | State | Meaning | What to do |
    |-------|---------|-----------|
    | `PENDING (PD)` | Waiting for resources | Wait, or check why with `squeue -j JOBID -o "%R"` (shows reason) |
    | `RUNNING (R)` | Actively executing | Check progress in output file: `tail -f logs/1234567_binder_screen.out` |
    | `COMPLETING (CG)` | Finishing up | Almost done, just wait |
    | `FAILED (F)` | Crashed | Check error file: `cat logs/1234567_binder_screen.err` |
    | `TIMEOUT (TO)` | Ran out of time | Increase `--time` and resubmit |
    | `OUT_OF_MEMORY (OOM)` | Ran out of RAM | Increase `--mem` and resubmit |

    > 💡 **Tip:** If your job is stuck in `PENDING`, check why:
    > ```bash
    > squeue -j 1234567 -o "%.18i %.9P %.8j %.8u %.8T %.10M %.6D %R"
    > ```
    > The last column (`%R`) shows the reason: `Resources` (waiting for nodes to free up), `Priority` (other jobs have higher priority), or `QOSMaxJobsPerUserLimit` (you've hit your concurrent job limit).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 3: Resource Requests — Getting It Right

    This is where most beginners struggle. Request too much and your job waits forever in the queue. Request too little and your job gets killed mid-run. Here's how to get it right.

    > ⚠️ **Warning:** The scheduler prioritizes smaller, shorter jobs. A job requesting 1 GPU for 2 hours will start much sooner than one requesting 4 GPUs for 24 hours. Always request only what you need.

    ### The Strategy: Test Small, Then Scale

    1. **Start with a test run** — run your job on a tiny subset (1 binder design instead of 100, 1 million reads instead of 200 million)
    2. **Check actual usage** — after the test finishes, see what resources it actually consumed
    3. **Scale up** — request resources based on real data, with ~20% buffer

    ```bash
    # After your test job (ID 1234567) completes, check what it actually used:
    sacct -j 1234567 --format=JobID,JobName,Elapsed,MaxRSS,MaxVMSize,TotalCPU,State

    # Example output:
    # JobID       JobName      Elapsed    MaxRSS     MaxVMSize  TotalCPU   State
    # 1234567     binder_test  00:45:23   12582912K  -          02:30:15   COMPLETED
    ```

    Reading this output:
    - **Elapsed:** 45 minutes wall time. So for 50 designs, estimate ~50 × 45 min = 37.5 hours. But with a GPU, designs run in parallel, so maybe 4-8 hours.
    - **MaxRSS:** ~12 GB peak memory. Request 16 GB (20% buffer) with `--mem=16G`.
    - **TotalCPU:** 2.5 hours of CPU time across all cores.

    ### 🤔 Decision Point: How to Estimate Resources

    | Resource | How to estimate | Rule of thumb |
    |----------|----------------|---------------|
    | **CPUs** | Most Python/bioinformatics tools use 1-8 cores | Start with 4, increase if tool supports multithreading |
    | **Memory** | Run test job, check MaxRSS | Actual usage + 20% buffer. STAR alignment needs 30-50 GB. |
    | **GPU** | Check tool documentation | RFdiffusion: 1 GPU (16GB VRAM). Most tools need just 1. |
    | **Time** | Run test on small input, extrapolate | Actual time × scale factor + 50% buffer |

    ### GPU Types Matter

    Not all GPUs are equal. Here's a rough comparison of what you might find on a cluster:

    | GPU | VRAM | Speed (relative) | Best for |
    |-----|------|-------------------|----------|
    | V100 | 16-32 GB | 1× | RFdiffusion, ESMFold, ProteinMPNN |
    | A100 | 40-80 GB | 2-3× | Large models, longer sequences, faster training |
    | H100 | 80 GB | 4-5× | Cutting-edge, rarely available on academic clusters |

    Check what your cluster has:
    ```bash
    # See available partitions and GPU types
    sinfo -o "%P %G %D %C"

    # More detailed: nodes, GPUs, and their states
    sinfo -N -l --partition=gpu
    ```

    ### Partitions

    Partitions are groups of nodes organized by type or policy:

    | Partition | Typical use | Time limit | Notes |
    |-----------|------------|------------|-------|
    | `general` | CPU-only jobs | 24-72 hours | Default, most nodes |
    | `gpu` | GPU jobs | 24-48 hours | Must request `--gres=gpu:N` |
    | `interactive` | Quick debugging | 2-4 hours | Shorter queue wait, but short time limit |
    | `priority` / `preempt` | Urgent jobs | Varies | May preempt lower-priority jobs |
    | `long` | Extended runs | 7-30 days | Fewer nodes, longer queue wait |

    > 💡 **Tip:** Check your cluster's specific partitions with `sinfo`. The names and limits vary by institution. WashU RIS may have different partition names — check their documentation.

    <details>
    <summary>📖 <strong>Deep dive:</strong> SLURM priority system — why some jobs start faster (click to expand)</summary>

    <br/>

    SLURM doesn't just use first-come-first-served. It uses a **fairshare** system:

    1. **Fairshare:** If you haven't used the cluster recently, your jobs get higher priority. If you've been running hundreds of jobs, your priority drops. This ensures everyone gets a fair share over time.

    2. **Job size:** Smaller jobs (fewer resources, shorter time) get priority because they're easier to schedule into gaps.

    3. **QOS (Quality of Service):** Some users or groups may have higher QOS levels, giving them priority access.

    4. **Age:** Jobs that have been waiting longer get a priority boost.

    You can check your fairshare standing with:
    ```bash
    sshare -u $USER
    ```

    The `RawShares` vs `RawUsage` columns tell you how much of your "fair share" you've consumed. If your usage is high relative to your shares, your next jobs will have lower priority.

    **Practical implication:** Don't submit 1000 jobs requesting 48 hours each if you only need 4 hours. Requesting less time improves your fairshare score AND lets the scheduler backfill your jobs into small gaps.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 4: Job Arrays — Running Many Jobs at Once

    This is the killer feature of SLURM for computational biology. Instead of submitting 100 separate jobs, you submit **one** job array that spawns 100 tasks.

    ### The Scenario

    You want to screen 100 de novo binder candidates against NaV1.7. Each design uses a different random seed. Without job arrays, you'd write 100 scripts. With job arrays, you write one:

    ```bash
    #!/bin/bash
    #SBATCH --job-name=nav17_screen
    #SBATCH --output=logs/%A_%a.out
    #SBATCH --error=logs/%A_%a.err
    #SBATCH --partition=gpu
    #SBATCH --gres=gpu:1
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=16G
    #SBATCH --time=02:00:00
    #SBATCH --array=0-99
    #SBATCH --mail-user=alex.chamessian@wustl.edu
    #SBATCH --mail-type=END,FAIL

    module load python/3.11 cuda/12.0
    source ~/envs/protein-design/bin/activate

    # Each array task gets a unique ID: $SLURM_ARRAY_TASK_ID (0, 1, 2, ..., 99)
    echo "Running design ${SLURM_ARRAY_TASK_ID} of 100"

    python design_binder.py \
        --seed $SLURM_ARRAY_TASK_ID \
        --target nav17_pore_loop \
        --output results/design_${SLURM_ARRAY_TASK_ID}.pdb
    ```

    Key differences from a regular job:
    - `--array=0-99` creates 100 tasks, numbered 0 through 99
    - `%A` in the output filename = the array job ID (same for all tasks)
    - `%a` in the output filename = the array task ID (unique per task: 0, 1, 2, ..., 99)
    - `$SLURM_ARRAY_TASK_ID` is available as an environment variable inside the script

    > 💡 **Tip:** This is how you screen 100 binder candidates overnight with one `sbatch` command. Submit at 5pm, check results at 9am. The scheduler runs as many in parallel as resources allow.

    ### Controlling Concurrency

    If you submit `--array=0-999`, you might overwhelm the cluster (or get your fairshare tanked). Limit how many run at once:

    ```bash
    #SBATCH --array=0-999%20
    ```

    This submits 1000 tasks but runs at most 20 at a time. The rest wait in the queue and start as others finish.

    > ⚠️ **Warning:** Think about total resource usage. 100 jobs × 16 GB RAM each = 1.6 TB of RAM. 100 jobs × 1 GPU each = 100 GPUs. Most clusters don't have that many GPUs available. Use `%N` to be a good citizen: `--array=0-99%10` runs 10 at a time.

    ### Using Array IDs Creatively

    The `$SLURM_ARRAY_TASK_ID` is just a number. You can use it to index into a file:

    ```bash
    # Read the Nth line from a file of protein targets
    TARGET=$(sed -n "${SLURM_ARRAY_TASK_ID}p" targets.txt)
    python design_binder.py --target "$TARGET" --output "results/${TARGET}.pdb"
    ```

    Where `targets.txt` might be:
    ```
    nav17_pore_loop
    nav17_vsd_domain
    nav18_pore_loop
    kcnq2_selectivity_filter
    kcnq3_pore_domain
    ```

    This lets you run different analyses for each array task, not just different seeds.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 5: Interactive Sessions

    Sometimes you need to be hands-on: debugging a script, testing GPU access, or exploring data interactively. That's what `srun` is for.

    ```bash
    # Request an interactive session with a GPU (2-hour limit)
    srun --pty --partition=gpu --gres=gpu:1 --cpus-per-task=4 --mem=16G --time=02:00:00 bash
    ```

    This puts you in a shell on a compute node (with a GPU), where you can:
    - Test your Python scripts interactively
    - Check that CUDA works: `nvidia-smi`
    - Debug failed jobs
    - Run quick one-off analyses

    When you're done, type `exit` to release the resources.

    ### 🤔 Decision Point: Interactive vs. Batch

    | Mode | Best for | Tradeoff |
    |------|----------|----------|
    | **Interactive (`srun`)** | Debugging, testing, verifying GPU access, small exploratory tasks | Ties up resources while you think. If you step away, the resources are wasted. |
    | **Batch (`sbatch`)** | Production runs, overnight jobs, job arrays, anything > 30 min | No immediate feedback — you submit and check later. |
    | **Jupyter on cluster** | Data exploration, visualization, interactive analysis | Setup overhead (port forwarding), but familiar Jupyter interface. |

    **A practical workflow:**
    1. **Write** your script on the login node (or via VS Code Remote SSH)
    2. **Test** interactively with `srun` on a small input
    3. **Submit** the full run with `sbatch` once you're confident it works
    4. **Go home** and wait for the email notification

    ### Running Jupyter on the Cluster

    If you want to run Jupyter notebooks on a compute node (useful for exploring large datasets that live on the cluster):

    ```bash
    # Step 1: Start an interactive session
    srun --pty --partition=gpu --gres=gpu:1 --mem=16G --time=04:00:00 bash

    # Step 2: On the compute node, start Jupyter (note the port and node name)
    module load python/3.11
    source ~/envs/protein-design/bin/activate
    jupyter notebook --no-browser --port=8888 --ip=0.0.0.0
    # Note: it will print a URL like http://gpu-node-05:8888/?token=abc123...

    # Step 3: On your Mac (in a NEW terminal), create an SSH tunnel
    ssh -L 8888:gpu-node-05:8888 ris

    # Step 4: Open http://localhost:8888/?token=abc123... in your Mac's browser
    ```

    > 💡 **Tip:** This is more setup than Google Colab, but it gives you access to the cluster's full filesystem and GPUs. Good for interactive exploration of RNA-seq results or visualizing protein structures when the data is already on the cluster.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Section 6: Practical Workflows

    Here are three complete, real-world SLURM workflows for your research.

    ### Workflow 1: RFdiffusion Binder Design Campaign

    Design 50 de novo binders against the NaV1.7 pore loop:

    ```bash
    #!/bin/bash
    #SBATCH --job-name=rfdiff_nav17
    #SBATCH --output=logs/%A_%a.out
    #SBATCH --error=logs/%A_%a.err
    #SBATCH --partition=gpu
    #SBATCH --gres=gpu:1
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=16G
    #SBATCH --time=01:00:00
    #SBATCH --array=0-49%10
    #SBATCH --mail-user=alex.chamessian@wustl.edu
    #SBATCH --mail-type=END,FAIL

    module load python/3.11 cuda/12.0
    source ~/envs/protein-design/bin/activate

    OUTDIR=results/nav17_rfdiff_$(date +%Y%m%d)
    mkdir -p $OUTDIR

    python run_rfdiffusion.py \
        --config configs/nav17_binder.yaml \
        --seed $SLURM_ARRAY_TASK_ID \
        --output_dir $OUTDIR/design_${SLURM_ARRAY_TASK_ID}

    echo "Design ${SLURM_ARRAY_TASK_ID} complete at $(date)"
    ```

    ### Workflow 2: RNA-seq Pipeline (Multi-Step with Dependencies)

    A real RNA-seq pipeline has multiple steps that must run in order. SLURM's `--dependency` flag chains them:

    ```bash
    # Step 1: Align reads with STAR (high memory, no GPU)
    # File: submit_star.sh
    #!/bin/bash
    #SBATCH --job-name=star_align
    #SBATCH --output=logs/%j_star.out
    #SBATCH --partition=general
    #SBATCH --cpus-per-task=8
    #SBATCH --mem=48G
    #SBATCH --time=06:00:00
    #SBATCH --array=0-11

    module load star/2.7.11 samtools/1.18

    SAMPLES=(sample_DRG_naive_1 sample_DRG_naive_2 sample_DRG_naive_3 \
             sample_DRG_CFA_1 sample_DRG_CFA_2 sample_DRG_CFA_3 \
             sample_DRG_SNI_1 sample_DRG_SNI_2 sample_DRG_SNI_3 \
             sample_SC_naive_1 sample_SC_naive_2 sample_SC_naive_3)

    SAMPLE=${SAMPLES[$SLURM_ARRAY_TASK_ID]}

    STAR --runThreadN 8 \
         --genomeDir /storage/group/lab/references/mouse_star_index \
         --readFilesIn /scratch/$USER/fastq/${SAMPLE}_R1.fastq.gz \
                       /scratch/$USER/fastq/${SAMPLE}_R2.fastq.gz \
         --readFilesCommand zcat \
         --outSAMtype BAM SortedByCoordinate \
         --outFileNamePrefix /scratch/$USER/aligned/${SAMPLE}_

    samtools index /scratch/$USER/aligned/${SAMPLE}_Aligned.sortedByCoord.out.bam
    ```

    ```bash
    # Step 2: Count features with featureCounts (depends on Step 1)
    # File: submit_counts.sh
    #!/bin/bash
    #SBATCH --job-name=featurecounts
    #SBATCH --output=logs/%j_counts.out
    #SBATCH --partition=general
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=16G
    #SBATCH --time=02:00:00

    module load subread/2.0

    featureCounts -T 4 -p --countReadPairs \
        -a /storage/group/lab/references/gencode.vM33.annotation.gtf \
        -o results/counts_matrix.txt \
        /scratch/$USER/aligned/*_Aligned.sortedByCoord.out.bam
    ```

    Submit them with dependencies:
    ```bash
    # Submit STAR alignment first
    STAR_JOB=$(sbatch --parsable submit_star.sh)
    echo "STAR job: $STAR_JOB"

    # Submit featureCounts to run ONLY after ALL STAR array tasks finish
    sbatch --dependency=afterok:$STAR_JOB submit_counts.sh
    echo "featureCounts will start after STAR completes"
    ```

    > 💡 **Tip:** The `--dependency=afterok:JOBID` flag means "only start this job if job JOBID completed successfully." If STAR fails, featureCounts won't waste time running on incomplete data. Other options: `afterany` (run regardless of success/failure), `afternotok` (run only if the dependency failed — useful for error handling).

    ### Workflow 3: Batch Protein Structure Prediction with ESMFold

    Predict structures for a list of designed sequences:

    ```bash
    #!/bin/bash
    #SBATCH --job-name=esmfold_predict
    #SBATCH --output=logs/%A_%a.out
    #SBATCH --error=logs/%A_%a.err
    #SBATCH --partition=gpu
    #SBATCH --gres=gpu:1
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=32G
    #SBATCH --time=00:30:00
    #SBATCH --array=0-49%5
    #SBATCH --mail-user=alex.chamessian@wustl.edu
    #SBATCH --mail-type=END,FAIL

    module load python/3.11 cuda/12.0
    source ~/envs/protein-design/bin/activate

    OUTDIR=results/esmfold_predictions
    mkdir -p $OUTDIR

    # Read the sequence for this array task from a FASTA-like list
    SEQUENCE=$(sed -n "$((SLURM_ARRAY_TASK_ID + 1))p" sequences.txt)

    python predict_structure.py \
        --sequence "$SEQUENCE" \
        --output $OUTDIR/prediction_${SLURM_ARRAY_TASK_ID}.pdb

    echo "Prediction ${SLURM_ARRAY_TASK_ID} complete: pLDDT score logged above"
    ```
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercises

    ### Exercise 1: SLURM Command Cheat Sheet

    Let's build a quick-reference of the commands you'll use most. Run this cell to see the cheat sheet, and add any notes of your own.
    """)
    return


@app.cell
def _():
    # Exercise 1: SLURM command cheat sheet
    # Run this cell to print a quick-reference card

    cheat_sheet = """
    ╔══════════════════════════════════════════════════════════════════════╗
    ║                     SLURM QUICK REFERENCE                          ║
    ╠══════════════════════════════════════════════════════════════════════╣
    ║                                                                    ║
    ║  SUBMITTING & MANAGING JOBS                                        ║
    ║  ─────────────────────────────                                     ║
    ║  sbatch script.sh              Submit a batch job                  ║
    ║  squeue -u $USER               Check your jobs                     ║
    ║  scancel JOBID                 Cancel a job                        ║
    ║  scancel -u $USER              Cancel ALL your jobs                ║
    ║  scontrol show job JOBID       Detailed job info                   ║
    ║                                                                    ║
    ║  INTERACTIVE SESSIONS                                              ║
    ║  ────────────────────                                              ║
    ║  srun --pty --partition=gpu \\                                      ║
    ║    --gres=gpu:1 --mem=16G \\                                        ║
    ║    --time=02:00:00 bash        GPU interactive session              ║
    ║                                                                    ║
    ║  CHECKING RESOURCES                                                ║
    ║  ──────────────────                                                ║
    ║  sinfo                         Cluster overview                    ║
    ║  sinfo -o "%P %G %D %C"       Partitions, GPUs, nodes             ║
    ║  sacct -j JOBID                Completed job details               ║
    ║  sacct -j JOBID --format=\\                                         ║
    ║    JobID,Elapsed,MaxRSS,\\                                          ║
    ║    TotalCPU,State              What you actually used               ║
    ║  sshare -u $USER               Your fairshare standing             ║
    ║                                                                    ║
    ║  JOB ARRAYS                                                        ║
    ║  ───────────                                                       ║
    ║  #SBATCH --array=0-99          100 tasks (0 through 99)            ║
    ║  #SBATCH --array=0-99%10       Max 10 running at once              ║
    ║  $SLURM_ARRAY_TASK_ID          Current task's index                ║
    ║                                                                    ║
    ║  DEPENDENCIES                                                      ║
    ║  ────────────                                                      ║
    ║  --dependency=afterok:JOBID    Run after JOBID succeeds            ║
    ║  --dependency=afterany:JOBID   Run after JOBID finishes            ║
    ║                                                                    ║
    ╚══════════════════════════════════════════════════════════════════════╝
    """
    print(cheat_sheet)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 2: Write a SLURM Script for a Binder Screening Campaign

    Write a SLURM script that:
    - Runs 50 binder design candidates against NaV1.8
    - Uses the GPU partition
    - Limits to 10 concurrent tasks
    - Sends you an email when it finishes or fails
    - Requests appropriate resources (1 GPU, 4 CPUs, 16GB RAM, 2 hours per design)

    Fill in the template below:
    """)
    return


@app.cell
def _():
    # Exercise 2: Write a SLURM script for binder screening
    # Fill in the #SBATCH directives marked with ???

    slurm_template = """#!/bin/bash
    #SBATCH --job-name=???
    #SBATCH --output=logs/%A_%a.out
    #SBATCH --error=logs/%A_%a.err
    #SBATCH --partition=???
    #SBATCH --gres=???
    #SBATCH --cpus-per-task=???
    #SBATCH --mem=???
    #SBATCH --time=???
    #SBATCH --array=???
    #SBATCH --mail-user=???
    #SBATCH --mail-type=???

    module load python/3.11 cuda/12.0
    source ~/envs/protein-design/bin/activate

    mkdir -p results/nav18_binders

    python design_binder.py \\
        --seed $SLURM_ARRAY_TASK_ID \\
        --target nav18_pore_domain \\
        --output results/nav18_binders/design_${SLURM_ARRAY_TASK_ID}.pdb

    echo "Design ${SLURM_ARRAY_TASK_ID} complete at $(date)"
    """

    print("Fill in the ??? values in this template:")
    print(slurm_template)

    # --- Solution (scroll down) ---











    solution = """#!/bin/bash
    #SBATCH --job-name=nav18_screen
    #SBATCH --output=logs/%A_%a.out
    #SBATCH --error=logs/%A_%a.err
    #SBATCH --partition=gpu
    #SBATCH --gres=gpu:1
    #SBATCH --cpus-per-task=4
    #SBATCH --mem=16G
    #SBATCH --time=02:00:00
    #SBATCH --array=0-49%10
    #SBATCH --mail-user=alex.chamessian@wustl.edu
    #SBATCH --mail-type=END,FAIL

    module load python/3.11 cuda/12.0
    source ~/envs/protein-design/bin/activate

    mkdir -p results/nav18_binders

    python design_binder.py \\
        --seed $SLURM_ARRAY_TASK_ID \\
        --target nav18_pore_domain \\
        --output results/nav18_binders/design_${SLURM_ARRAY_TASK_ID}.pdb

    echo "Design ${SLURM_ARRAY_TASK_ID} complete at $(date)"
    """

    print("\n" + "=" * 60)
    print("SOLUTION:")
    print("=" * 60)
    print(solution)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Exercise 3: Diagnose a Failed Job

    You submitted a job and it failed. Here's the scenario — figure out what went wrong and how to fix it.
    """)
    return


@app.cell
def _():
    # Exercise 3: Diagnose failed SLURM jobs
    # For each scenario, identify the problem and the fix

    scenarios = [
        {
            "symptom": "Job immediately fails. Error log says: 'error: Unable to open output file logs/1234567_binder.out'",
            "diagnosis": "The 'logs/' directory doesn't exist. SLURM can't create it automatically.",
            "fix": "Add 'mkdir -p logs' before submitting, or create it once in your project directory."
        },
        {
            "symptom": "Job was RUNNING for 2 hours then state changed to TIMEOUT",
            "diagnosis": "Your --time was too short. The job hit the walltime limit.",
            "fix": "Increase --time (e.g., from 02:00:00 to 06:00:00). Check actual runtime of test jobs first."
        },
        {
            "symptom": "Job was RUNNING then state changed to OUT_OF_MEMORY",
            "diagnosis": "Your --mem was too low. The job tried to use more RAM than allocated.",
            "fix": "Increase --mem. Check actual peak memory with: sacct -j JOBID --format=MaxRSS"
        },
        {
            "symptom": "Error log says: 'RuntimeError: CUDA out of memory. Tried to allocate 2.00 GiB'",
            "diagnosis": "The GPU doesn't have enough VRAM for your model/batch size. Different from system RAM (--mem).",
            "fix": "Request a GPU with more VRAM (e.g., A100 80GB instead of V100 16GB), or reduce batch size in your script."
        },
        {
            "symptom": "Job has been PENDING for 24 hours. Reason: 'Resources'",
            "diagnosis": "The cluster doesn't have free nodes matching your request right now.",
            "fix": "Reduce resource requests (less time, less memory, fewer GPUs). Or wait — jobs do eventually start."
        },
    ]

    for i, s in enumerate(scenarios, 1):
        print(f"{'='*60}")
        print(f"Scenario {i}")
        print(f"{'='*60}")
        print(f"Symptom:    {s['symptom']}")
        print(f"Diagnosis:  {s['diagnosis']}")
        print(f"Fix:        {s['fix']}")
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Remote Computing Fundamentals](01-remote-computing-fundamentals.py) | [Module Index](../README.md) | [Next: Cloud Computing and When to Use What \u2192](03-cloud-computing-and-when-to-use-what.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - [SLURM Official Documentation](https://slurm.schedmd.com/documentation.html) — comprehensive reference for all commands and directives
    - [SLURM Quick Start User Guide](https://slurm.schedmd.com/quickstart.html) — shorter, beginner-friendly
    - [WashU RIS Documentation](https://docs.ris.wustl.edu/) — WashU-specific cluster info, partitions, and policies
    - [MIT Missing Semester — Lecture 5: Command-line Environment](https://missing.csail.mit.edu/2020/command-line/) — tmux, job control, SSH
    - [HPC Carpentry](https://www.hpc-carpentry.org/) — free workshop materials for learning HPC

    ---

    ## Navigation

    **← Previous:** [Notebook 1: Remote Computing Fundamentals](01-remote-computing-fundamentals.py) | **Next →** [Notebook 3: Cloud Computing and When to Use What](03-cloud-computing-and-when-to-use-what.py)

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

