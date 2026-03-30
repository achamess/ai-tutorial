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
    # 03: Staying Current

    ## How to keep up without drowning

    AI is moving faster than any technology in the history of science. In the time since GPT-3 launched (2020), we've gone from "interesting toy" to "changes how I do research daily." And the pace is accelerating.

    This notebook isn't about any specific tool — it's about building habits so you're never caught off guard by the next breakthrough.

    The goal: **informed, not overwhelmed.**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: The AI Tools Ecosystem](02-tools-ecosystem.py) | [Module Index](../README.md)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - AI capabilities are changing faster than any other technology you use. The tools available in 6 months will be meaningfully different from today -- RFdiffusion didn't exist before 2023, and it's already core to your binder design pipeline.
    > - A systematic approach to staying current prevents both FOMO-driven distraction (chasing every new tool announcement) and falling behind on genuinely useful advances (missing a new protein design method that could improve your hit rates).
    > - Your competitive advantage as a pain biologist who uses computational protein design AND AI tools depends on staying at the frontier. If a new structure prediction model improves binder-target complex accuracy, you need to know about it before your competitors do.
    > - The protein design AI field specifically is evolving rapidly -- generative flow matching, multimodal protein models, and closed-loop design systems are all emerging. Having a structured "radar" means you catch these developments early enough to incorporate them.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The pace of change — a timeline

    Let's visualize what's happened to make the pace concrete.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Key sources for staying current

    You don't need to follow everything. Here's a curated list organized by how much time they take:

    > 🔑 **Key concept:** Systematic beats reactive for staying current. If you only learn about new AI tools when someone on Twitter gets excited, you'll chase hype. If you have a structured weekly routine — even just 15 minutes — you'll catch the genuinely important developments and skip the noise.

    ### 5 minutes/week (minimum viable awareness)

    | Source | What you get | Link |
    |--------|-------------|------|
    | **Anthropic blog** | Major Claude updates, safety research | [anthropic.com/news](https://www.anthropic.com/news) |
    | **OpenAI blog** | GPT updates, new capabilities | [openai.com/blog](https://openai.com/blog) |
    | **Google DeepMind blog** | Gemini updates, AlphaFold news | [deepmind.google/blog](https://deepmind.google/blog) |

    ### 15 minutes/week (recommended)

    | Source | What you get | Link |
    |--------|-------------|------|
    | **The Batch** (Andrew Ng) | Weekly AI newsletter, well-curated | [deeplearning.ai/the-batch](https://www.deeplearning.ai/the-batch/) |
    | **Import AI** (Jack Clark) | Weekly newsletter, policy + technical | [importai.substack.com](https://importai.substack.com/) |
    | **Ahead of AI** (Sebastian Raschka) | Monthly deep-dives, practical | [magazine.sebastianraschka.com](https://magazine.sebastianraschka.com/) |

    > 🤔 **Decision point: How much time to spend on AI updates**
    >
    > | Time budget | What you cover | Who this is for |
    > |-------------|---------------|-----------------|
    > | **5 min/week** | Skim 3 provider blogs | Researchers who use AI as a tool but don't need cutting-edge |
    > | **15 min/week** | Provider blogs + 1 newsletter | **Most researchers (recommended)** |
    > | **30 min/week** | Newsletters + arXiv skimming + try one new thing | Researchers where AI is central to their methods |
    > | **1 hour/week** | All of the above + read 1 paper in depth | Computational researchers building AI pipelines |
    > | **2+ hours/week** | Deep engagement with AI research community | Only if AI methods ARE your research |
    >
    > **Your sweet spot:** 15-30 min/week. You use AI daily for coding, writing, and literature review, and your protein design pipeline depends on AI tools. That puts you in the "AI is central to methods" tier — but you're a biologist first, so don't let AI news crowd out reading pain biology papers.

    ### 30 minutes/week (if AI is becoming central to your work)

    | Source | What you get |
    |--------|-------------|
    | **[arXiv cs.CL](https://arxiv.org/list/cs.CL/recent)** | Latest NLP/LLM papers (skim titles) |
    | **[arXiv cs.AI](https://arxiv.org/list/cs.AI/recent)** | Broader AI research papers |
    | **[arXiv q-bio](https://arxiv.org/list/q-bio/recent)** | Computational biology preprints |
    | **[bioRxiv computational biology](https://www.biorxiv.org/collection/bioinformatics)** | Preprints on AI + biology |
    | **Twitter/X** | Follow 10-15 key researchers (see list below) |

    ### Key people to follow (Twitter/X)

    **AI researchers:**
    - Dario Amodei (@DarioAmodei) — Anthropic CEO, big-picture AI
    - Andrej Karpathy (@karpathy) — clear AI explanations
    - Sebastian Raschka (@rasaborsky) — practical ML

    **Biology + AI:**
    - David Baker (@baaboraker) — protein design (Baker Lab)
    - Mohammed AlQuraishi (@MoAlQuraishi) — protein structure prediction
    - Sergey Ovchinnikov (@sokrypton) — protein design methods
    - Possu Huang (@PossuHuang) — computational protein design

    **Pain biology + computational:**
    - Follow the key labs publishing on NaV channel structures and computational neuroscience
    - Set Google Scholar alerts for "NaV1.7 structure" and "de novo protein binder"
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Evaluating new tools and claims

    Every week someone announces "the AI tool that will revolutionize biology." Most won't. Here's how to evaluate:

    ### The skeptic's checklist

    1. **Does it solve a problem I actually have?** (Not a problem they invented)
    2. **Can I try it in 10 minutes?** (Good tools have low friction to try)
    3. **What's the data story?** (Where does my data go? Is it private?)
    4. **Is there a paper?** (Peer-reviewed methods > marketing claims)
    5. **Who built it?** (Academic lab? Startup? Big tech? Each has different incentives)
    6. **What do power users say?** (Not the press release — actual users on Twitter/forums)

    ### Red flags

    - "Replaces your entire workflow" — nothing does
    - No clear explanation of how it works
    - Benchmarks only on cherry-picked examples
    - Requires you to upload all your data with no privacy policy
    - "10x improvement" with no peer review

    ### Green flags

    - Open-source or published methodology
    - Clear, honest limitations section
    - Active user community
    - Works with your existing tools (not a walled garden)
    - Used by researchers you respect

    > ⚠️ **Warning: Hype cycles are predictable — most announced tools won't matter in 6 months.** Of the AI tools announced in any given month, roughly 80% will be abandoned, acqui-hired, or irrelevant within a year. The ones that survive are usually: (1) backed by large organizations with sustained funding, (2) solving a genuine workflow problem, and (3) building a real user community. Before investing time learning a new tool, check if it's been around for at least 3 months and still has active development.

    > This evaluation framework echoes the thinking in Rich Sutton's "[The Bitter Lesson](http://www.incompleteideas.net/IncsIdeas/BitterLesson.html)" (2019) — a short, influential essay arguing that general methods leveraging computation always win over approaches that try to encode human knowledge. Worth reading for perspective on where AI is heading.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Building habits: weekly AI exploration

    The best way to stay current isn't reading about AI — it's *trying things*.

    ### The 30-minute weekly AI experiment

    Set aside 30 minutes each week (maybe Friday afternoon) to try one new thing:

    **Week 1:** Try a new prompt technique on a real research question
    **Week 2:** Test a tool you've heard about (Elicit, Consensus, etc.)
    **Week 3:** Automate something small with the Claude API
    **Week 4:** Read one AI paper or blog post relevant to your field

    Then repeat. In a year, you'll have tried 50+ things, and the useful ones will stick.

    ### Keep a log

    A simple text file or notebook:

    ```
    2026-03-28: Tried Elicit for systematic review of NaV1.7 blockers
      - Pros: extracted dosing info from 15 papers automatically
      - Cons: missed 3 relevant papers that Semantic Scholar found
      - Verdict: useful for extraction, but don't rely on it for search
    ```

    This log becomes your personalized guide to what works.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The evolving role of AI in science

    ### Where we are now (2026)

    AI is your research assistant. It helps you:
    - Read and synthesize literature faster
    - Write and edit more efficiently
    - Analyze data with less friction
    - Design proteins computationally (AlphaFold, RFdiffusion)
    - Code without being a professional programmer

    ### What's coming (next 2-3 years)

    **Agentic AI workflows**
    - AI that can plan and execute multi-step research tasks
    - "Find all papers on KCNQ2 openers, extract IC50 values, create a comparison table, and draft a paragraph summarizing the state of the field"
    - We're already seeing early versions of this (Claude's tool use, computer use capabilities)

    **AI-driven experimental design**
    - AI suggests which experiments to run next based on your results so far
    - Active learning loops: experiment → AI analysis → next experiment suggestion
    - Already happening in drug discovery and materials science

    **Better biology-specific models**
    - Models trained specifically on biological data (not just text)
    - Better integration of sequence, structure, and function information
    - Models that understand experimental context ("this is a Western blot, the loading control looks uneven")

    **Lab automation + AI**
    - Robotic labs controlled by AI planning
    - Cloud labs (Emerald Cloud Lab, Strateos) that you program remotely
    - AI decides what experiment to run, robot executes it, AI interprets results

    ### What probably won't change

    - You still need domain expertise to ask good questions
    - Experimental validation remains essential
    - Scientific judgment can't be outsourced (is this result biologically meaningful?)
    - Peer review and reproducibility standards
    - The need to understand your own results deeply
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Protein design AI: the trajectory

    This section is especially relevant for your de novo binder work. Let's trace the evolution:
    """)
    return


@app.cell
def _():
    import pandas as pd

    # The protein design AI trajectory
    trajectory = pd.DataFrame({
        "Year": [2020, 2021, 2022, 2023, 2024, 2025, "2026+"],
        "Milestone": [
            "AlphaFold 2 — structure prediction solved",
            "RoseTTAFold — alternative structure prediction",
            "ESMFold — fast language model-based prediction; AlphaFold DB release",
            "RFdiffusion — generative protein design; ProteinMPNN mature",
            "AlphaFold 3 — complexes; Chai-1, Boltz emerge",
            "Flow matching models; improved binder design pipelines",
            "Integrated design-test-learn loops; multimodal protein models",
        ],
        "Impact_on_your_work": [
            "Can predict target structures without crystallography",
            "More options for structure prediction",
            "Screen hundreds of designs quickly",
            "Generate de novo binders computationally — core of your pipeline",
            "Better complex prediction — see how binder meets target",
            "Higher success rates, more diverse designs",
            "AI suggests what to test next, learns from your experimental data",
        ]
    })

    # Display nicely
    for _, row in trajectory.iterrows():
        print(f"\n{row['Year']}: {row['Milestone']}")
        print(f"  → For your work: {row['Impact_on_your_work']}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What to watch next in protein design AI

    1. **Generative flow matching** — next-gen diffusion models for proteins, potentially higher quality designs
    2. **Multimodal protein models** — models that jointly understand sequence, structure, function, and dynamics
    3. **Closed-loop design** — AI systems that learn from your experimental results to improve the next round of designs
    4. **Function prediction** — going beyond structure to predict what a protein *does* (binding affinity, stability, expressibility)
    5. **Membrane protein binders** — harder than soluble proteins, but directly relevant to ion channels

    ### Your competitive advantage

    You're a pain biologist who understands ion channel function AND can use computational design tools AND can leverage AI effectively. That combination is rare. Most computational people don't understand the biology deeply, and most biologists don't use these tools.

    Keep investing in all three areas.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Create your personal "AI Radar"

    An AI radar is a structured plan for staying current. Let's build one.

    First, let's use Claude to help brainstorm, then you'll customize it.
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np

    fig, ax = plt.subplots(figsize=(9, 9), subplot_kw={'projection': 'polar'})

    # Radar rings: daily, weekly, monthly, quarterly
    rings = [1, 2, 3, 4]
    ring_labels = ['DAILY\nuse', 'WEEKLY\ncheck', 'MONTHLY\ndive', 'QUARTERLY\nevaluate']
    ring_colors = ['#e74c3c', '#f39c12', '#3498db', '#8e44ad']

    # Draw rings
    for r, label, color in zip(rings, ring_labels, ring_colors):
        circle = plt.Circle((0, 0), r, transform=ax.transData + ax.transAxes,
                            fill=False, edgecolor=color, linewidth=2, linestyle='--', alpha=0.4)
        theta_label = np.pi / 4  # 45 degrees
        ax.text(theta_label, r - 0.35, label, fontsize=8, fontweight='bold',
                color=color, ha='center', va='center',
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white', edgecolor=color, alpha=0.9))

    # Items at each ring level, positioned at different angles
    items = [
        # (angle_degrees, ring, label, color)
        # Daily ring
        (30, 0.8, "Claude Code", '#e74c3c'),
        (150, 0.8, "Claude chat", '#e74c3c'),
        (270, 0.8, "Jupyter", '#e74c3c'),
    
        # Weekly ring
        (0, 1.8, "Anthropic blog", '#f39c12'),
        (60, 1.8, "The Batch\nnewsletter", '#f39c12'),
        (120, 1.8, "Twitter/X\nkey researchers", '#f39c12'),
        (180, 1.8, "Google Scholar\nalerts", '#f39c12'),
        (240, 1.8, "Try one\nnew thing", '#f39c12'),
        (310, 1.8, "Baker Lab\nupdates", '#f39c12'),
    
        # Monthly ring
        (20, 2.8, "arXiv cs.CL\nskim titles", '#3498db'),
        (90, 2.8, "Deep-dive:\none topic", '#3498db'),
        (160, 2.8, "bioRxiv\ncomp bio", '#3498db'),
        (230, 2.8, "Review AI\nexperiment log", '#3498db'),
        (310, 2.8, "Ahead of AI\nnewsletter", '#3498db'),
    
        # Quarterly ring
        (45, 3.8, "Try new tool\nseriously", '#8e44ad'),
        (135, 3.8, "Reassess model\nchoices", '#8e44ad'),
        (225, 3.8, "Share learnings\nwith lab", '#8e44ad'),
        (315, 3.8, "Update tools\ninventory", '#8e44ad'),
    ]

    for angle_deg, r, label, color in items:
        theta = np.radians(angle_deg)
        ax.plot(theta, r, 'o', color=color, markersize=8, alpha=0.8)
        ax.text(theta, r + 0.25, label, fontsize=7, ha='center', va='bottom',
                color=color, fontweight='bold')

    # Draw the rings
    for r, color in zip(rings, ring_colors):
        theta_range = np.linspace(0, 2 * np.pi, 100)
        ax.plot(theta_range, [r] * 100, color=color, linewidth=1.5, alpha=0.3, linestyle='--')

    ax.set_ylim(0, 4.5)
    ax.set_rticks([])
    ax.set_thetagrids([])
    ax.spines['polar'].set_visible(False)
    ax.set_title("Your AI Radar\nCloser to center = higher frequency", fontsize=14, fontweight='bold', pad=20)

    # Legend
    legend_handles = [
        mpatches.Patch(color=c, label=l) for c, l in 
        zip(ring_colors, ['Daily use', 'Weekly check', 'Monthly deep-dive', 'Quarterly evaluation'])
    ]
    ax.legend(handles=legend_handles, loc='lower right', fontsize=9, 
              bbox_to_anchor=(1.15, -0.05))

    plt.tight_layout()
    plt.show()

    print("Customize this radar for your own workflow in the exercise below.")
    return


@app.cell
def _():
    import anthropic

    client = anthropic.Anthropic()

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{
            "role": "user",
            "content": """I'm a pain biologist who designs de novo protein binders targeting NaV1.7, 
    NaV1.8, and KCNQ2/3 ion channels. I use tools like RFdiffusion, ProteinMPNN, 
    and AlphaFold in my computational pipeline, and I use Claude for coding, writing, 
    and literature review.

    Create a concise "AI Radar" — a structured weekly/monthly plan for staying current 
    on AI developments relevant to my work. Include:
    1. Specific sources to check weekly (with URLs)
    2. Monthly deep-dive topics
    3. Quarterly goals for trying new tools
    4. Key search terms for Google Scholar alerts

    Keep it realistic — I have maybe 30 minutes per week for this."""
        }]
    )

    print("Claude's suggested AI Radar:")
    print("=" * 60)
    print(response.content[0].text)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Final thoughts: your AI journey

    You've now completed this tutorial series. Here's what you've built:

    | Module | What you learned |
    |--------|------------------|
    | 01: Python Foundations | Variables, data structures, functions, files |
    | 02: How LLMs Work | Tokens, attention, context windows, limitations |
    | 03: Prompt Engineering | System prompts, few-shot, chain-of-thought, structured output |
    | 04: Mastering Claude Code | Your AI-powered development environment |
    | 05: Claude API | Programmatic access, batch processing, automation |
    | 06: Data Skills | pandas, visualization, real research data analysis |
    | 07: AI Research Workflows | Literature review, writing, complete research pipelines |
    | 08: AI Landscape | Models, tools, staying current, what's coming |

    ### The three things that matter most

    1. **Keep using the tools.** Skills decay without practice. Use Claude Code for real work, not just tutorials.

    2. **Stay curious, stay skeptical.** Try new things, but always evaluate them honestly. Not everything that's hyped is useful.

    3. **Your domain expertise is your superpower.** AI tools are powerful but generic. You bring the pain biology knowledge, the experimental intuition, the understanding of what questions matter. That's irreplaceable.

    ### Resources for continued learning

    - **[Think Python](https://allendowney.github.io/ThinkPython/)** (Allen Downey) — free online, deeper Python when you're ready
    - **[MIT Missing Semester](https://missing.csail.mit.edu/)** — command line, git, and developer tools (all 11 lectures are freely available)
    - **[Anthropic documentation](https://docs.anthropic.com/)** — reference for the Claude API
    - **The cheat sheet** in `resources/cheat-sheet.md` — quick reference for everything in this tutorial

    > **Missing Semester connection:** The entire [Missing Semester course](https://missing.csail.mit.edu/) is about becoming a power user of your computing environment. Combined with AI tools, these skills compound — every terminal trick you learn makes Claude Code more powerful, every git concept makes collaboration easier.

    Good luck with the binder designs. Go make something that helps people with pain.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **Essential essays and perspectives:**
    - Rich Sutton, "[The Bitter Lesson](http://www.incompleteideas.net/IncsIdeas/BitterLesson.html)" (2019) -- a short, influential essay on why general methods leveraging computation beat hand-engineered approaches. Important context for understanding AI's trajectory.

    **AI news and newsletters:**
    - [Anthropic Blog](https://www.anthropic.com/news) -- major Claude updates and research
    - [The Batch](https://www.deeplearning.ai/the-batch/) (Andrew Ng) -- weekly AI newsletter, well-curated
    - [Import AI](https://importai.substack.com/) (Jack Clark, Anthropic co-founder) -- weekly newsletter on AI policy and technical developments
    - [Ahead of AI](https://magazine.sebastianraschka.com/) (Sebastian Raschka) -- monthly deep-dives on practical ML topics

    **Preprint servers and paper discovery:**
    - [arXiv cs.CL](https://arxiv.org/list/cs.CL/recent) -- computational linguistics / NLP papers (where most LLM research appears)
    - [arXiv cs.AI](https://arxiv.org/list/cs.AI/recent) -- broader artificial intelligence research
    - [bioRxiv](https://www.biorxiv.org/) -- biology preprints, including computational biology and structural biology

    **Continued learning:**
    - [Think Python](https://allendowney.github.io/ThinkPython/) by Allen Downey -- free online textbook for deepening Python skills
    - [MIT Missing Semester](https://missing.csail.mit.edu/) -- 11 free lectures on command-line tools, version control, debugging, and more
    - [Anthropic documentation](https://docs.anthropic.com/) -- complete API reference and guides
    - [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) -- practical examples and patterns for building with Claude

    **Protein design AI (staying current):**
    - [Baker Lab](https://www.bakerlab.org/) -- follow for RFdiffusion, ProteinMPNN, and related tool updates
    - [AlphaFold](https://alphafold.ebi.ac.uk/) -- structure database and server updates
    - [CASP](https://predictioncenter.org/) -- Critical Assessment of protein Structure Prediction; biennial competition that drives the field
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
    - 2026-03-25: QA pass — converted sources cell from code to markdown, removed duplicate sections (evaluating tools, Edit Log)
    - 2026-03-25: Added callout boxes — key concept (systematic beats reactive), decision point (time investment table), warning (hype cycles)
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: The AI Tools Ecosystem](02-tools-ecosystem.py) | [Module Index](../README.md)
    """)
    return


if __name__ == "__main__":
    app.run()

