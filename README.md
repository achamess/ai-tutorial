# AI Power-User Tutorial for Pain Biology

A hands-on tutorial teaching researchers to become master users of AI tools. Not about building AI — about leveraging tools like Claude, the Claude API, and Claude Code to accelerate real research: literature review, data analysis, figure generation, writing, and experimental design. Every example uses pain biology scenarios (DRG neurons, nociceptors, ion channels, calcium imaging, RNA-seq, behavioral assays).

---

## Quick Start (I just want to get going)

### Step 1: Get the code onto your computer

Open a terminal and run:
```bash
git clone https://github.com/achamess/ai-tutorial.git
cd ai-tutorial
```

> **Don't have `git`?** See the full setup guide below. If you're on a Mac, you can also download the repo as a ZIP from the green "Code" button above → "Download ZIP", then unzip it.

### Step 2: Follow the setup guide

Open `00-getting-started/01-complete-setup-guide.ipynb` — it walks you through installing everything you need step by step, with instructions for **Mac, Windows, and Linux**. No prior experience required.

The setup guide covers: VS Code, Python, Git, virtual environment, Jupyter, Claude Code, and API key configuration.

### Step 3: Run the preflight check

Open `00-getting-started/02-preflight-check.ipynb` and run every cell (`Shift+Enter`). This verifies your environment is ready. Green checks = good to go.

### Step 4: Start learning

Open `01-python-foundations/01-your-first-code.ipynb` and begin. Work through the notebooks in order — each one builds on the last.

---

## What this is

12 modules, 38 interactive Jupyter notebooks that take you from "I've never written code" to "I can build AI-powered research tools." Every example uses pain biology data so the skills transfer directly to the bench.

Each notebook has:
- **"Why this matters"** — concrete justification tied to research work
- **Runnable code** — execute cells with `Shift+Enter` and see results immediately
- **Exercises** — practice problems using your domain (ion channels, binder candidates, behavioral data)
- **Further Reading** — links to official docs, textbooks, and papers
- **Navigation** — prev/next links to flow through the curriculum

## Module map

| # | Module | Notebooks | What you'll learn |
|---|--------|-----------|-------------------|
| 00 | **Getting Started** | 2 | Setup guide + environment verification |
| 01 | **Python Foundations** | 4 | Variables, files, libraries, data structures |
| 02 | **Your Computer** | 4 | Filesystem, processes, networking, AI toolkit |
| 03 | **How LLMs Work** | 3 | What LLMs are, tokens, context windows, how Claude thinks |
| 04 | **Prompt Engineering** | 3 | Prompt anatomy, techniques, research-specific prompts |
| 05 | **Mastering Claude Code** | 4 | Basics, workflows, customization, best practices |
| 06 | **Systems Thinking** | 3 | Decomposition, debugging, reproducibility |
| 07 | **Math You Actually Need** | 3 | Stats, hypothesis testing, probability for AI |
| 08 | **Claude API** | 3 | First API call, structured outputs, research tools |
| 09 | **Data Skills** | 4 | Pandas, visualization, analysis, databases |
| 10 | **AI Research Workflows** | 3 | Literature review, data pipelines, writing with AI |
| 11 | **AI Landscape** | 3 | Models, tools ecosystem, staying current |

## How to use this repo

### If you're a learner:

1. **Clone the repo** (see Quick Start above)
2. **Follow the setup guide** in Module 00
3. **Work through notebooks in order** — `Shift+Enter` to run each cell
4. **Ask Claude Code for help** — highlight code in VS Code and ask questions
5. **Do the exercises** — they're where the learning happens
6. **Track your progress** — update `progress.md` as you complete notebooks

### If you're sharing this with your lab:

1. Add collaborators: **Settings** → **Collaborators** → **Add people** (by GitHub username or email)
2. Each person clones the repo and follows the setup guide
3. Everyone gets their own virtual environment — they won't break each other's setup
4. Each person needs their own Anthropic API key for Modules 08-10 (free tier works for the exercises)

### What you need

| Requirement | When you need it | How to get it |
|------------|-----------------|---------------|
| A computer (Mac, Windows, or Linux) | From the start | You probably have one |
| VS Code | From the start | Free: https://code.visualstudio.com |
| Python 3.14 | From the start | Setup guide covers this |
| Git | From the start | Setup guide covers this |
| Anthropic API key | Module 08 onwards | Free: https://console.anthropic.com |
| Claude Code | Module 05 onwards | Setup guide covers this |

## Project structure

```
ai-tutorial/
├── 00-getting-started/      ← Start here
│   ├── 01-complete-setup-guide.ipynb
│   └── 02-preflight-check.ipynb
├── 01-python-foundations/    ← Then work through these in order
├── 02-your-computer/
├── ...
├── 11-ai-landscape/
├── resources/
│   ├── cheat-sheet.md        ← Quick reference for Python, pandas, API, prompts
│   ├── glossary.md           ← 120+ terms defined for researchers
│   └── references/           ← Downloaded Anthropic docs + external links
├── sessions/                 ← Session logs tracking learning progress
├── progress.md               ← Module completion tracker
├── learnings.md              ← Personal insights journal
└── CLAUDE.md                 ← Instructions for Claude Code (you can ignore this)
```

## External resources

Referenced throughout the tutorial:

- **[Think Python](https://allendowney.github.io/ThinkPython/)** (3rd ed.) — free Python textbook
- **[MIT Missing Semester](https://missing.csail.mit.edu/)** — practical computing skills for scientists
- **[Anthropic docs](https://docs.anthropic.com/)** — Claude API, prompt engineering, Claude Code
- **[Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook)** — code examples and patterns
- Local copies of key Anthropic docs are in `resources/references/`

## FAQ

**Do I need programming experience?**
No. Module 01 starts from zero. If you can pipette, you can code.

**How long does this take?**
The setup takes ~30 minutes. Each notebook takes 20-60 minutes depending on the topic. The full tutorial is roughly 30-40 hours of work spread across multiple sessions.

**Can I skip modules?**
Modules build on each other, but if you already know Python you could start at Module 03. The preflight check in Module 00 will tell you if your setup is ready.

**Do I need to pay for anything?**
VS Code, Python, Git, and the tutorial itself are free. Claude Code and the Claude API require an Anthropic account — the free tier is sufficient for the exercises. A paid Claude Pro subscription is useful but not required.

**I'm stuck / something is broken.**
Open Claude Code in VS Code and describe the problem. That's literally what it's for. You can also check the Troubleshooting section in the setup guide.
