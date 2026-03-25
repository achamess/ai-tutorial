# AI Power-User Tutorial for Pain Biology

## Project purpose
Interactive tutorial teaching Alex (pain biologist) to become a master AI user.
Not about building AI — about leveraging AI tools effectively for research.

## Structure
11 modules (35 notebooks total) in numbered directories:
- 01-python-foundations/ (3 notebooks)
- 02-your-computer/ (4 notebooks — includes AI toolkit guide)
- 03-how-llms-work/ (3 notebooks)
- 04-prompt-engineering/ (3 notebooks)
- 05-mastering-claude-code/ (3 notebooks)
- 06-systems-thinking/ (3 notebooks)
- 07-math-you-need/ (3 notebooks)
- 08-claude-api/ (3 notebooks)
- 09-data-skills/ (4 notebooks — includes databases intro)
- 10-ai-research-workflows/ (3 notebooks)
- 11-ai-landscape/ (3 notebooks)
- resources/ — cheat sheet, references (downloaded Anthropic docs, external links index)
- sessions/ — session logs tracking engagement and progress

## Python environment
- venv at `.venv/` (Python 3.14)
- Jupyter kernel: "ai-tutorial"
- Core packages: jupyter, pandas, numpy, matplotlib, seaborn, anthropic

## Conventions
- Each module contains numbered .ipynb notebooks
- Notebooks mix explanation (markdown cells) with runnable exercises (code cells)
- Every notebook opens with a "Why this matters" justification tied to Alex's research
- Use pain biology examples wherever possible (DRG neurons, nociceptors, inflammatory mediators, behavioral assays, calcium imaging, RNA-seq of pain-related tissues)
- Keep code simple — Alex is learning programming as a tool, not becoming a developer
- Every notebook should be self-contained and runnable top-to-bottom
- Never use fake citations or author names — use obvious placeholders or real references
- Cross-reference Think Python and MIT Missing Semester throughout
- Commit after substantive changes (new modules, major updates, end of session)

## External references (local copies in resources/references/)
- Anthropic prompt engineering guide
- Anthropic API getting started
- Anthropic tool use guide
- Anthropic Claude Code overview
- Full external links index: resources/references/external-links.md
