# AI Power-User Tutorial for Pain Biology

A hands-on tutorial that teaches a pain biologist to become a master user of AI tools. This is not about building AI systems — it is about leveraging tools like Claude, the Claude API, and Claude Code to accelerate real research: literature review, data analysis, figure generation, writing, and experimental design. Every example uses pain biology scenarios (DRG neurons, nociceptors, inflammatory mediators, calcium imaging, RNA-seq, behavioral assays) so the skills transfer directly to the bench.

## Who this is for

Alex — a pain biologist who is comfortable with benchwork and wants to add computational and AI skills to the toolkit. No programming experience required. If you can run a Western blot, you can run a Python script.

## Prerequisites

- A Mac (this tutorial was built on macOS)
- VS Code installed (with the Jupyter extension)
- Basic computer literacy (you know what a file is, you can use a terminal)
- A Claude Pro or API account (for modules that call the API)

## Getting started

1. Open the project folder in VS Code
2. Activate the virtual environment:
   ```
   source .venv/bin/activate
   ```
3. Open `00-getting-started/01-preflight-check.ipynb` and run every cell to verify your setup
4. Then proceed to Module 01 and work through the notebooks in order

## Module map

| # | Module | Notebooks | What you will learn |
|---|--------|-----------|---------------------|
| 00 | **Getting Started** | 1 | Pre-flight check — verify your environment is ready |
| 01 | **Python Foundations** | 3 | Variables, files, libraries — just enough Python to be dangerous |
| 02 | **Your Computer** | 4 | Filesystem, shell, networking, and your AI toolkit |
| 03 | **How LLMs Work** | 3 | What an LLM is, tokens, context windows, how Claude thinks |
| 04 | **Prompt Engineering** | 3 | Anatomy of a prompt, techniques that work, prompts for research |
| 05 | **Mastering Claude Code** | 4 | Basics, advanced workflows, customization, best practices |
| 06 | **Systems Thinking** | 3 | Decomposition, debugging, reproducibility, project structure |
| 07 | **Math You Actually Need** | 3 | Descriptive stats, hypothesis testing, probability and AI math |
| 08 | **Claude API** | 3 | First API call, structured outputs, building research tools |
| 09 | **Data Skills** | 4 | Pandas, visualization, real data analysis, databases |
| 10 | **AI Research Workflows** | 3 | Literature review, data analysis pipelines, writing with AI |
| 11 | **AI Landscape** | 3 | Models and providers, tools ecosystem, staying current |

**Total: 12 modules, 37 notebooks**

## How sessions work

Each working session is logged in `sessions/` with a dated markdown file. These capture what was covered, what clicked, and what to revisit. Two other files track the big picture:

- **`progress.md`** — table showing module status, notebooks completed, and last-worked dates
- **`learnings.md`** — accumulating journal of insights that connect back to your research

## How to navigate

- Notebooks are numbered within each module (`01-...`, `02-...`, `03-...`)
- Work through them in order — later notebooks build on earlier ones
- Each notebook is self-contained and runnable top-to-bottom
- Every notebook opens with a "Why this matters" section connecting the topic to pain biology research

## External resources

These are referenced throughout the tutorial:

- **Think Python** (3rd edition) — free online textbook for learning Python: https://greenteapress.com/wp/think-python-3rd-edition/
- **MIT Missing Semester** — practical computing skills most scientists never learn: https://missing.csail.mit.edu/
- **Anthropic documentation** — prompt engineering, API reference, Claude Code docs: https://docs.anthropic.com/
- Local copies of key Anthropic docs are saved in `resources/references/`
