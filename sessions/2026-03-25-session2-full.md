# Session 2 — 2026-03-25 (Full Transcript)

## Session Overview
Completion and polish session. Finished all build items from Session 1, added substantial new content (HPC module, philosophy doc, cross-platform setup), ran full QA, published to GitHub. Tutorial now at 13 modules, 41 notebooks.

---

## Conversation Log

### Resuming
**Alex:** "Let's start a new session and resume our work"

**Claude:** Checked session 1 log and progress.md. Identified queued items: external references sweep, QA pass, data structures notebook. Alex at Module 01 notebook 01.

**Alex:** "let's keep building this. Do all the things. Also, as you're appraising what we've built, if you have any other mods/additions feedback, I welcome it"

### External References Sweep
**Claude:** Launched 3 parallel agents adding inline citations and Further Reading sections to all notebooks. Real citations added:
- Vaswani et al. 2017 (Attention Is All You Need)
- Wei et al. 2022 (Chain-of-thought prompting)
- Brown et al. 2020 (GPT-3 / few-shot)
- Wilson et al. 2017 (Good Enough Practices)
- Benjamini & Hochberg 1995 (FDR)
- Love et al. 2014 (DESeq2)
- Jumper et al. 2021 (AlphaFold)
- Watson et al. 2023 (RFdiffusion)
- Dauparas et al. 2022 (ProteinMPNN)
- Rich Sutton's "The Bitter Lesson"
- Joshua Schimel's "Writing Science"
- John Ousterhout's "A Philosophy of Software Design"
- Jay Alammar's "The Illustrated Transformer"
- + official docs for Python, pandas, matplotlib, seaborn, NumPy, SciPy, sqlite3, Anthropic

### Claude's Additional Recommendations
**Claude:** Proposed 5 improvements:
1. README at project root
2. Module 00 preflight check
3. Fix stale notebook counts in progress.md
4. Cross-module navigation (prev/next links)
5. Glossary of 120+ terms

**Alex:** "yes, build all. good ideas"

All built and committed.

### External References Feedback
**Alex:** "I want you to be making many more external references and citations to things. I want to see and know where you're getting your info from."

**Claude:** Saved as permanent feedback. Already running the reference sweep.

### Data Structures Notebook
Created 01-python-foundations/04-data-structures-in-practice.ipynb — "The Five Shapes of Your Data" connecting lists, dicts, JSON, DataFrames with round-trip conversions.

### QA Pass
3 parallel agents across all modules. Found and fixed:
- Duplicate cells in 22 notebooks (most common issue)
- Missing `import json` in prompt engineering module
- Missing `anthropic` client import in LLM module
- Deprecated `scipy.stats.binom_test()` → `binomtest()`
- Undefined variable `interpretation_prompt` in 2 notebooks
- Wrong file paths (`05-claude-api/` → `08-claude-api/`) in 3 cells
- Missing "Why this matters" sections in 6 notebooks
- Outdated Think Python URL in cheat sheet
All 38 notebooks now pass.

### Comprehensive Setup Guide
**Alex:** "I want a complete and comprehensive computer setup in the 00 module. Assume for people who may have little experience setting up computing environments (including me). Be very explicit"

**Claude:** Created 00-getting-started/01-complete-setup-guide.ipynb — 12-part guide: Homebrew, Python, VS Code + extensions, Git, venv, Jupyter kernel, Claude Code, API key, troubleshooting. Existing preflight check renumbered to 02.

### Sharing and GitHub
**Alex:** "I'd like to share this tutorial with others. is there a way to package it up for sharing?"

**Claude:** Recommended GitHub. Alex chose private repo.

**Alex:** did gh auth login

**Claude:** Created private repo at https://github.com/achamess/ai-tutorial, pushed all content.

### GitHub Documentation
**Alex:** "in the github main page, make it explicit how to work with this repo for a non power user"

**Claude:** Rewrote README with Quick Start, lab sharing guide, requirements table, project structure diagram, FAQ.

### Cross-Platform Support
**Alex:** "does this setup also work for windows people? I'll want to share this with my lab members"

**Claude:** Added Windows and Linux instructions alongside Mac in every step of setup guide.

### Tutorial Philosophy
**Alex:** "I want to have a polished overview, the philosophy of this, the design principles of this tutorial, who its for, why we made the choices we made, how to use, etc"

**Claude:** Created 00-getting-started/00-tutorial-philosophy.ipynb covering: who it's for, what it is/isn't, 6 core philosophy points, design choice justifications (why Python, why Jupyter, why VS Code, why Claude, why this order, why pain biology), how to use the tutorial, 10 design principles, what success looks like.

### Notebook Interaction
**Alex:** Previously asked about interacting with notebook content — covered in Session 1 transcript.

### HPC and Cloud Computing
**Alex:** "Do you think there is any utility in learning how to interact with cloud or remote high performance computing?"

**Claude:** Yes — directly relevant. RFdiffusion/ProteinMPNN need GPUs. RNA-seq can exceed laptop RAM. WashU has RIS/CHPC cluster.

**Alex:** "Yes. Do it. Make it deep enough and explicit enough that we could use it well. Also discuss tradeoffs, decision making about when to use certain tools. You can use callouts and other devices to highlight particular things, or folded text to go deeper"

**Claude:** Created 07-cloud-and-hpc/ with 3 notebooks:
- 01: SSH, file transfer, remote filesystems, software management
- 02: SLURM job scheduling, arrays, interactive sessions, practical workflows
- 03: Cloud computing decision frameworks, containers, cost management

### Callout System and Decision Frameworks
**Alex:** "you can go back throughout all tutorials as well and consider good places for examples, callouts, deep dives, etc. Let's make that actually part of a global design architecture so we're consistent throughout. Capture that thought. I think it's really important to have a 'when to use this tool' or 'deciding when to do this vs that' with clear guidance"

**Claude:** Saved as permanent design standard:
- ⚠️ Warning — things that can go wrong
- 💡 Tip — practical advice
- 🔑 Key concept — foundational ideas
- 🤔 Decision point — with comparison tables
- 📖 Deep dive — collapsible for optional depth

Retroactive sweep across all existing modules queued for next session.

### Think Stats Reference
**Alex:** "for the stats and math part, some linkable material that you should weave in aggressively https://allendowney.github.io/ThinkStats/"

**Claude:** Saved to reference resources. Will weave into Module 08 (Math) during the retroactive callouts pass.

---

## Decisions Made This Session
1. External references with real citations in all notebooks
2. Data structures connecting notebook in Module 01
3. README rewritten for GitHub onboarding
4. Module 00 expanded: philosophy + setup guide + preflight
5. Cross-module navigation in all notebooks
6. Glossary of 120+ terms
7. Full QA pass with fixes
8. Cross-platform setup (Mac/Windows/Linux)
9. Published to private GitHub repo
10. HPC/Cloud module added (07-cloud-and-hpc)
11. Standardized callout system (⚠️💡🔑🤔📖) as global design standard
12. Think Stats added as core reference for math module
13. Tutorial now 13 modules, 41 notebooks

## What Was Built This Session
- 00-getting-started/00-tutorial-philosophy.ipynb (new)
- 00-getting-started/01-complete-setup-guide.ipynb (new, cross-platform)
- 00-getting-started/02-preflight-check.ipynb (renumbered)
- 01-python-foundations/04-data-structures-in-practice.ipynb (new)
- 07-cloud-and-hpc/01-remote-computing-fundamentals.ipynb (new)
- 07-cloud-and-hpc/02-job-schedulers-and-slurm.ipynb (new)
- 07-cloud-and-hpc/03-cloud-computing-and-when-to-use-what.ipynb (new)
- README.md (rewritten for GitHub)
- resources/glossary.md (new)
- External references added to all 38 prior notebooks
- QA fixes across 22 notebooks
- Navigation links in all notebooks
- Windows/Linux setup instructions

## Queued for Next Session
- Retroactive callout/decision-framework sweep across all existing modules
- Weave Think Stats references into Module 08
- Continue learning through notebooks interactively (Alex at Module 01, notebook 02)
- Navigation links need updating for new module numbering (07-12 shifted)
- Consider JupyterBook for web-hosted version

## Observations About Alex
- Thinks about sharing and accessibility from the start (lab members, cross-platform)
- Values decision frameworks over exhaustive instructions — "when to use this vs that"
- Wants the tutorial to serve as a reference, not just a one-time read-through
- Appreciates polished presentation (philosophy doc, consistent design system)
- Keeps pushing for more depth and rigor (citations, callouts, HPC module)
- Good instinct for what's missing — every suggestion improved the tutorial
