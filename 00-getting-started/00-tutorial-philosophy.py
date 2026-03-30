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
    # The AI Power-User Tutorial: Philosophy & Design

    *Read this first. It takes 10 minutes and will change how you approach everything that follows.*
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [Module Index](../README.md) | [Next: Complete Setup Guide \u2192](01-complete-setup-guide.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Who this is for

    You are a **working scientist** — probably in pain biology, neuroscience, or a related field. You run experiments. You analyze data. You write grants and papers. You are not a programmer, and you are not trying to become one.

    But you've seen what AI tools can do, and you want to use them at a level beyond copy-pasting into a chat window. You want to understand what's happening well enough to **direct the tools, evaluate their output, and build workflows that save you real time**.

    This tutorial was built for that exact person.

    It was originally designed for a pain biologist who designs de novo protein binders for voltage-gated ion channels (NaV1.7, NaV1.8, KCNQ2/3). Every example in this tutorial — every dataset, every exercise, every analogy — comes from that world: DRG neurons, calcium imaging, RNA-seq, behavioral assays, binder screening, grant writing. If you work in a related field, these examples will feel familiar. If you don't, the principles transfer — just swap the domain.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What this is (and what it isn't)

    **This is:**
    - A tutorial on becoming a **power user** of AI tools — especially Claude, the Claude API, and Claude Code
    - A practical guide to the **minimum viable computing skills** a modern researcher needs
    - A curated path through Python, data analysis, prompt engineering, and AI workflows — with everything connected to real research tasks
    - A living document that tracks your progress, captures your insights, and adapts to how you learn

    **This is not:**
    - A computer science course
    - A machine learning course
    - A comprehensive Python textbook (we recommend [Think Python](https://allendowney.github.io/ThinkPython/) for that)
    - A certification or credential
    - Static content — it's designed to be a conversation between you and Claude Code
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The core philosophy

    ### 1. Learn what you need, when you need it

    Most tutorials teach programming bottom-up: syntax, then data structures, then algorithms, then maybe — after weeks — you do something useful. That's backwards for a working scientist.

    This tutorial is organized around **what you'll actually do**. You learn Python because you need it to call the Claude API. You learn about tokens because they affect how much context you can give Claude. You learn pandas because your screening data is in a CSV. Every concept earns its place by connecting to a real task.

    ### 2. Why before how

    Every notebook opens with **"Why this matters for your work"** — a concrete explanation of when and why you'd need this skill. Not "this is important because learning is good," but "you need this because when you run differential expression on your DRG RNA-seq data, you'll get 1,000 false positives without FDR correction."

    If you can't articulate why a topic matters for your research, you won't remember it. We made the choice to justify every single topic because scientists are (rightly) skeptical of claims without evidence.

    ### 3. Your data, your problems

    Generic tutorials use generic examples: to-do lists, weather apps, the Iris dataset. You'll never see those here. Every example uses:
    - Ion channel screening data (NaV1.7, NaV1.8, KCNQ2/3 binder candidates)
    - Calcium imaging traces from DRG neurons
    - Behavioral assay results (von Frey thresholds, tail-flick, conditioned place aversion)
    - RNA-seq differential expression tables
    - Grant writing and literature review scenarios

    When you see `candidate['kd_nm'] < 20`, that's not an abstract exercise — it's filtering your screening hits. The closer the examples are to your real work, the faster the skills transfer.

    ### 4. AI-native from the start

    This isn't a Python tutorial with AI bolted on at the end. AI tools (Claude, Claude Code, the API) are woven throughout from Module 01. You'll learn Python *by using Claude Code to help you*. You'll learn prompt engineering *by calling the API from notebooks*. The tutorial practices what it preaches: AI as a force multiplier for everything you do.

    ### 5. Understand enough to evaluate, not enough to build from scratch

    You don't need to implement a transformer from scratch to use Claude effectively. But you *do* need to understand:
    - Why Claude sometimes makes things up (so you can catch it)
    - What tokens are (so you can manage costs and context)
    - What p-values mean (so you can verify Claude's statistical claims)
    - How to read code you didn't write (so you can trust what Claude generates)

    The goal is **informed delegation** — the same skill you use when you review a collaborator's analysis or evaluate a paper's methods. You don't need to have done it yourself, but you need to know enough to judge whether it was done right.

    ### 6. Reproducibility is non-negotiable

    Every notebook runs top-to-bottom. Every dataset is generated inline (no mysterious external files). Every analysis can be re-run and will produce the same result. This mirrors good scientific practice: if your analysis isn't reproducible, it isn't an analysis.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Why we made the choices we made

    ### Why Python?
    Not because it's the best language — because it's the **language of AI tools, data science, and bioinformatics**. The Claude API has a Python SDK. Pandas is Python. NumPy is Python. Every bioinformatics pipeline you'll encounter speaks Python. Learning Python gives you access to this entire ecosystem.

    ### Why marimo notebooks?
    Because they let you **mix explanation with runnable code** — read a concept, then immediately execute it. This is how scientists think: hypothesis, then experiment. Marimo notebooks are reactive, reproducible, and stored as plain Python files — no JSON, no merge conflicts. The skills transfer directly to your real work.

    ### Why VS Code?
    Because it's where everything converges: editing code, running notebooks, using Claude Code, managing git, accessing the terminal — all in one window. Rather than juggling five different tools, you learn one environment deeply. Claude Code's VS Code integration makes it your AI-native IDE.

    ### Why Claude specifically?
    This tutorial uses Claude (by Anthropic) as its primary AI tool because:
    - Claude Code integrates directly into VS Code, the environment you'll work in
    - The Claude API is well-documented and has a clean Python SDK
    - Claude has strong performance on scientific and technical tasks
    - The prompt engineering principles you learn here transfer to any LLM

    Module 11 covers the broader AI landscape — you'll learn when other tools (GPT, Gemini, specialized biology AI like AlphaFold) are the better choice.

    ### Why 11 modules in this order?

    The sequence is deliberate:

    | Modules | Purpose |
    |---------|--------|
    | **01-02**: Python + Your Computer | Foundation — you need to speak the language and understand the machine |
    | **03-04**: LLMs + Prompt Engineering | Understanding — know what AI is and how to talk to it effectively |
    | **05-06**: Claude Code + Systems Thinking | Leverage — use AI as a daily tool, evaluate what it produces |
    | **07**: Math You Actually Need | Rigor — the stats and probability that keep you honest |
    | **08-09**: Claude API + Data Skills | Building — create custom tools and analyze real data |
    | **10-11**: Research Workflows + AI Landscape | Integration — put it all together for your actual research |

    Each layer builds on the last. You can't effectively use the Claude API (Module 08) without understanding prompt engineering (Module 04). You can't evaluate AI-generated code (Module 06) without basic Python (Module 01). The order isn't arbitrary — it's a dependency graph.

    ### Why pain biology examples?
    Because **transfer learning applies to humans too**. You already have deep mental models for calcium transients, dose-response curves, and experimental controls. When we map programming concepts onto those models ("a function is like a protocol", "a dictionary is like a structured lab record"), the new knowledge attaches to things you already understand. Abstract examples force you to learn the concept *and* the context simultaneously. Domain-specific examples cut that cognitive load in half.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## How to use this tutorial

    ### The basics
    1. **Work through notebooks in order.** They build on each other.
    2. **Run every cell** with `Shift+Enter`. Don't just read — execute.
    3. **Do the exercises.** Reading code and writing code are different skills. The exercises are where the learning happens.
    4. **Modify things.** After running a cell, change a value and rerun it. What happens? Break things on purpose.
    5. **Ask Claude Code for help.** Highlight code, ask questions. That's the whole point.

    ### The learning loop
    Each notebook follows this pattern:

    1. **Why** — why this topic matters for your work (concrete scenarios)
    2. **Show** — a working example you execute and observe
    3. **Explain** — what just happened and how it works
    4. **Practice** — exercises where you write code yourself
    5. **Connect** — how this applies to your actual research

    ### Predict before you execute
    Before pressing `Shift+Enter`, look at the code and predict what the output will be. If you're right, you understood it. If you're wrong, **that's where the learning is** — stop and figure out why your prediction was off.

    ### Track your progress
    - **`progress.md`** — update it as you complete notebooks. Seeing your progress is motivating.
    - **`learnings.md`** — write down insights that connect to your research. "I learned that FDR correction matters" is forgettable. "I need to apply BH correction to my next RNA-seq analysis because I'm testing 20,000 genes" is actionable.
    - **`sessions/`** — session logs capture the full conversation each time you sit down. These help you (and Claude) pick up where you left off.

    ### When you get stuck
    1. Read the error message. Python errors usually say exactly what went wrong.
    2. Ask Claude Code. Highlight the error, paste it, say "what went wrong?"
    3. Check the glossary (`resources/glossary.md`) if you hit an unfamiliar term.
    4. Check the cheat sheet (`resources/cheat-sheet.md`) for syntax reminders.
    5. Check the Further Reading section at the bottom of each notebook for deeper dives.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Design principles (the rules we followed building this)

    These principles guided every decision in the tutorial's construction:

    1. **Every topic must justify its inclusion.** If we can't explain why a researcher needs it with a concrete scenario, it doesn't belong.

    2. **Real examples only.** No toy data, no generic scenarios. Pain biology data, pain biology problems, pain biology workflows.

    3. **No fake citations.** When we reference a paper, it's real. When we need mock data, it's clearly labeled as fictional. Scientists should never have to wonder whether a reference is real — that erodes trust in everything else.

    4. **Cite everything.** Every factual claim links to its source — official docs, peer-reviewed papers, authoritative references. This tutorial practices the same epistemic standards it teaches.

    5. **Self-contained and reproducible.** Every notebook runs top-to-bottom without external dependencies. All data is generated inline. If it can't be reproduced, it doesn't ship.

    6. **Simple over clever.** Three clear lines of code are better than one clever one. Alex is learning tools, not becoming a developer. We optimize for readability, not elegance.

    7. **Visual over verbal.** Where a diagram explains a concept better than text, we use a diagram — Mermaid flowcharts for systems, matplotlib for data, ASCII art when nothing else fits.

    8. **Audit trail.** Every notebook has an edit log. Every session has a transcript. Changes are tracked, decisions are documented. This is how a research project should work.

    9. **Cross-referenced.** We don't exist in isolation. Think Python for deeper Python dives, MIT Missing Semester for computing skills, Anthropic docs for Claude specifics, primary literature for scientific claims. Further Reading sections point you to the next level.

    10. **Living document.** This tutorial is a git repository, not a PDF. It updates. It tracks your progress. It records your insights. It grows with you.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What success looks like

    When you finish this tutorial, you won't be a software engineer. You'll be something more useful: **a scientist who can leverage AI effectively**.

    Concretely, you'll be able to:

    - Write Python scripts that process your data (screening results, expression tables, behavioral scores)
    - Build custom Claude API pipelines for literature review, data interpretation, and writing assistance
    - Use Claude Code as a daily research accelerator — not just for coding, but for thinking
    - Create publication-quality figures programmatically (reproducible, not PowerPoint)
    - Evaluate AI-generated code and catch errors before they become problems
    - Structure your computational work for reproducibility (version control, environments, documentation)
    - Choose the right AI tool for each task (Claude vs GPT vs specialized biology AI)
    - Stay current as AI capabilities evolve — systematically, not reactively

    Most importantly, you'll have a **mental model** for how these tools work. Not memorized syntax, but understanding. That's what lets you adapt when the tools change — and they will change, faster than any tutorial can keep up with.

    ---

    Ready? Let's set up your environment.

    **[→ Next: Complete Setup Guide](01-complete-setup-guide.py)**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **[Think Python](https://allendowney.github.io/ThinkPython/)** (3rd ed., Allen Downey) — the Python textbook we reference throughout. Free online.
    - **[MIT Missing Semester](https://missing.csail.mit.edu/)** — the computing skills course that fills the gap between "I have a computer" and "I can use it effectively."
    - **[Anthropic Documentation](https://docs.anthropic.com/)** — official docs for Claude, the API, and Claude Code.
    - **[Good Enough Practices in Scientific Computing](https://doi.org/10.1371/journal.pcbi.1005510)** (Wilson et al., 2017, PLOS Comp Bio) — the paper that inspired Module 06's approach to reproducibility.
    - **[Writing Science](https://global.oup.com/academic/product/writing-science-9780199760244)** (Joshua Schimel) — the book on scientific writing that informs Module 10's approach.
    - **[The Bitter Lesson](http://www.incompleteideas.net/IncsIdent/BitterLesson.html)** (Rich Sutton, 2019) — a short, provocative essay on the trajectory of AI. Referenced in Module 11.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [Module Index](../README.md) | [Next: Complete Setup Guide \u2192](01-complete-setup-guide.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created tutorial philosophy and design principles document
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

