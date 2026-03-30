# AI Power-User Tutorial for Pain Biology

## Project purpose
Interactive tutorial teaching Alex (pain biologist) to become a master AI user.
Not about building AI — about leveraging AI tools effectively for research.

## Structure
13 modules (42 notebooks total) in numbered directories:
- 00-getting-started/ (3 notebooks — philosophy, setup guide, preflight check)
- 01-python-foundations/ (4 notebooks — includes data structures)
- 02-your-computer/ (4 notebooks — includes AI toolkit guide)
- 03-how-llms-work/ (3 notebooks)
- 04-prompt-engineering/ (3 notebooks)
- 05-mastering-claude-code/ (4 notebooks — includes setup & best practices)
- 06-systems-thinking/ (3 notebooks)
- 07-cloud-and-hpc/ (3 notebooks — SSH, SLURM, cloud computing)
- 08-math-you-need/ (3 notebooks)
- 09-claude-api/ (3 notebooks)
- 10-data-skills/ (4 notebooks — includes databases intro)
- 11-ai-research-workflows/ (3 notebooks)
- 12-ai-landscape/ (3 notebooks)
- resources/ — cheat sheet, glossary, references (downloaded Anthropic docs, external links index)
- sessions/ — session logs with full verbatim conversation capture

## Python environment
- venv at `.venv/` (Python 3.14)
- marimo notebooks (plain `.py` files, no kernel registration needed)
- Core packages: marimo, pandas, numpy, matplotlib, seaborn, anthropic

## Conventions
- Each module contains numbered .py marimo notebooks with cross-module navigation (prev/next)
- Notebooks mix explanation (markdown cells via `mo.md()`) with runnable exercises (code cells)
- Every notebook opens with a "Why this matters" justification tied to Alex's research
- Use pain biology examples wherever possible (DRG neurons, nociceptors, inflammatory mediators, behavioral assays, calcium imaging, RNA-seq of pain-related tissues)
- Keep code simple — Alex is learning programming as a tool, not becoming a developer
- Every notebook should be self-contained and runnable top-to-bottom
- Never use fake citations or author names — use obvious placeholders or real references
- Cite sources liberally — link to docs, papers, books. Add Further Reading sections.
- Cross-reference Think Python, Think Stats, and MIT Missing Semester throughout
- Use standardized callout system: ⚠️ Warning, 💡 Tip, 🔑 Key concept, 🤔 Decision point (with tables), 📖 Deep dive (collapsible)
- Include Mermaid/matplotlib visualizations for system diagrams and data flows
- Edit log at the bottom of every notebook tracking all changes
- Commit after substantive changes (new modules, major updates, end of session)
- Capture full verbatim session logs every session (not summaries)

## External references (local copies in resources/references/)
- Anthropic prompt engineering guide
- Anthropic API getting started
- Anthropic tool use guide
- Anthropic Claude Code overview
- Full external links index: resources/references/external-links.md
