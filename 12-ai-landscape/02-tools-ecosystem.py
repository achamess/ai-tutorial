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
    # 02: The AI Tools Ecosystem

    ## Beyond chat — the tools that change how you work

    The previous notebook covered models. This one covers the *tools built on top of them* — the things that actually change your daily workflow.

    We'll organize by what you do, not by what the tool is.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Models and Providers](01-models-and-providers.py) | [Module Index](../README.md) | [Next: Staying Current \u2192](03-staying-current.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - The AI tools landscape is vast and most tools overlap. Understanding the ecosystem means you pick the right tool instead of trying five and abandoning all of them. Your time is the bottleneck, not tool availability.
    > - You need different tools for different parts of your workflow: Claude Code for building pipelines, Semantic Scholar for literature discovery, Elicit for structured paper extraction, and marimo for reproducible analysis. Knowing which tool fits where prevents you from using a hammer for every nail.
    > - Many researchers waste weeks evaluating tools they don't need. The evaluation framework here (does it solve a problem I actually have? can I try it in 10 minutes?) saves you from that trap.
    > - Combining tools is where the real power lives. A single workflow -- Semantic Scholar for discovery, Claude API for extraction, pandas for comparison, Claude for synthesis -- is more powerful than any one tool alone.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## AI coding assistants

    These are tools that help you write, debug, and understand code — critical since you're learning Python alongside AI.

    ### Claude Code (what you're using now)
    - **What:** Command-line AI assistant that reads your codebase and edits files directly
    - **Strengths:** Deep context understanding, can read/write/run files, understands project structure
    - **Best for:** Building scripts, debugging, refactoring, creating notebooks
    - **How you use it:** `claude` in terminal, ask it to create or fix things
    - **Docs:** [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code)

    ### GitHub Copilot
    - **What:** AI autocomplete inside VS Code (and other editors)
    - **Strengths:** Inline suggestions as you type, fast, feels like an upgraded autocomplete
    - **Best for:** Writing code when you roughly know what you want — it fills in the details
    - **Limitation:** Autocomplete-style means it can't do big-picture restructuring
    - **Cost:** ~$10/month (free for academics in some programs)
    - **Docs:** [GitHub Copilot documentation](https://docs.github.com/en/copilot)

    ### Cursor
    - **What:** A fork of VS Code with AI deeply integrated
    - **Strengths:** Chat with your codebase, AI-assisted editing, can reference files in conversation
    - **Best for:** People who want AI woven into their editor experience
    - **How it compares:** Similar to Claude Code but GUI-based instead of terminal-based
    - **Website:** [cursor.com](https://www.cursor.com/)

    ### Which should you use?

    For your stage of learning:
    - **Claude Code** for big tasks ("create a script to process all my RNA-seq files")
    - **GitHub Copilot** for small tasks (autocompleting code as you type in a notebook)
    - They complement each other. Many researchers use both.

    > 🤔 **Decision point: Which tools for which workflow**
    >
    > | Workflow | Primary tool | Supporting tool | Why |
    > |---------|-------------|-----------------|-----|
    > | **Coding** (scripts, pipelines) | Claude Code | GitHub Copilot | Claude Code for architecture, Copilot for line-by-line |
    > | **Writing** (grants, papers) | Claude chat/API | Grammarly | Claude for drafting/revision, Grammarly for final polish |
    > | **Literature review** | Semantic Scholar + Elicit | Claude API | Discovery tools find papers, Claude extracts and synthesizes |
    > | **Data analysis** | marimo + Claude Code | ChatGPT Code Interpreter | marimo for reproducible work, ChatGPT for quick exploration |
    > | **Protein design** | RFdiffusion + ProteinMPNN | Claude Code | Specialized tools compute, Claude helps script and interpret |

    > ⚠️ **Warning: Tool fatigue is real.** The temptation is to try every new AI tool that launches. Resist it. Most tools overlap significantly, and switching between five half-learned tools is worse than mastering two. Pick a small stack and go deep before adding new tools.

    > 💡 **Tip: The "two-tool rule."** For any given task, you need at most one AI assistant plus one specialized tool. For literature review: Claude + Semantic Scholar. For coding: Claude Code + Copilot. For writing: Claude + your brain. If you find yourself juggling three or more tools for one task, you're probably overcomplicating it.

    > **Missing Semester connection:** The [Command-line Environment lecture (Lecture 5)](https://missing.csail.mit.edu/2020/command-line/) covers the terminal skills that make Claude Code powerful. The more comfortable you are in the terminal, the more you get from Claude Code.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## AI for research and literature

    These tools are game-changers for staying on top of the literature — especially in a fast-moving field like pain biology and protein design.

    ### Semantic Scholar ([semanticscholar.org](https://www.semanticscholar.org/))
    - Free academic search engine with AI features
    - **TLDR summaries** — one-sentence paper summaries
    - **Citation context** — see how a paper is cited (positively, critically, etc.)
    - Has a [free API](https://api.semanticscholar.org/) for programmatic access
    - Great for: "Find recent papers on NaV1.7 selective blockers"

    ### Elicit ([elicit.com](https://elicit.com/))
    - AI research assistant that searches and summarizes papers
    - Extracts structured data from papers (methods, sample sizes, results)
    - Great for: systematic reviews, comparing methods across studies
    - Example: "What behavioral assays are used to measure mechanical allodynia in CFA models?"

    ### Consensus ([consensus.app](https://consensus.app/))
    - Searches academic papers and synthesizes findings
    - Shows whether the literature supports or contradicts a claim
    - Great for: "Does NaV1.7 blockade reduce inflammatory pain in rodent models?" -> gives a yes/no meter based on papers

    ### Connected Papers ([connectedpapers.com](https://www.connectedpapers.com/))
    - Visual graph of related papers
    - Enter one paper, see what's connected to it
    - Great for: discovering papers you missed, understanding a sub-field's structure
    - Free for basic use

    ### Google NotebookLM ([notebooklm.google.com](https://notebooklm.google.com/))
    - Upload papers/documents, ask questions across them
    - Good for: reading groups, qualifying exams, grant background sections
    - Limitation: only works with documents you upload (no web search)

    ### Comparison

    | Tool | Best for | Cost | API? |
    |------|----------|------|------|
    | [Semantic Scholar](https://www.semanticscholar.org/) | Finding papers, citation analysis | Free | [Yes](https://api.semanticscholar.org/) |
    | [Elicit](https://elicit.com/) | Structured extraction, systematic reviews | Freemium | No |
    | [Consensus](https://consensus.app/) | Quick claim verification | Freemium | No |
    | [Connected Papers](https://www.connectedpapers.com/) | Visual literature mapping | Free (basic) | No |
    | [NotebookLM](https://notebooklm.google.com/) | Deep Q&A over your documents | Free | No |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## AI for data analysis

    ### Claude (conversation + API)
    - Paste data or describe your dataset, ask for analysis
    - Write pandas code for you
    - Via the API: batch process data programmatically
    - You've learned this throughout the tutorial

    ### ChatGPT Code Interpreter (Advanced Data Analysis)
    - Upload a CSV, ask questions, get plots
    - Runs Python in a sandbox — no setup needed
    - Good for: quick exploratory analysis when you don't want to write code
    - Limitation: sandbox is ephemeral (resets between sessions), limited packages

    ### marimo + AI assistants
    - Your current setup: marimo notebooks + Claude Code
    - Most flexible approach — full Python ecosystem, your data stays local
    - Best for: reproducible analysis, publication-quality figures, complex pipelines

    ### When to use which

    | Scenario | Best approach |
    |----------|---------------|
    | Quick look at a CSV | ChatGPT Code Interpreter or paste into Claude |
    | Reproducible analysis for a paper | marimo notebook (with AI help writing code) |
    | Batch processing many files | Python script via Claude Code |
    | Stats you're unsure about | Ask Claude to explain AND write the code |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Building personal workflows

    The power isn't in any single tool — it's in how you combine them. Here's an example workflow for a real research task:

    ### Example: "Prepare background section for a grant on NaV1.7 binders"

    ```
    Step 1: Literature discovery
       → Semantic Scholar: search "NaV1.7 selective inhibitor protein binder"
       → Connected Papers: map the citation network from 2-3 key papers
       → Elicit: extract key findings across 20 relevant papers

    Step 2: Synthesis
       → Claude: "Here are summaries of 20 papers on NaV1.7 binders.
         Organize the key themes and identify gaps in the literature."

    Step 3: Drafting
       → Claude: "Draft a 2-page background section covering [themes].
         Emphasize the unmet need for selective NaV1.7 inhibitors
         and the promise of de novo protein binders."

    Step 4: Revision
       → You: read critically, add your specific insights, fix any errors
       → Claude: "Revise this paragraph for clarity" (iterate)
       → Grammarly: final polish

    Step 5: Figures
       → marimo + matplotlib: create data figures with Claude Code help
       → Claude: "Write a figure legend for this dose-response curve"
    ```

    Total time: 3-4 hours instead of 2-3 days. And the quality is often better because you explored more literature.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Automation with APIs and scripts

    Once you're comfortable with the Claude API (Module 05), you can automate repetitive tasks.

    Here's a taste of what's possible:
    """)
    return


@app.cell
def _():
    # Example: Automated paper screening
    # You'd run this on a list of paper abstracts to quickly categorize them

    import anthropic

    client = anthropic.Anthropic()

    # Simulated abstracts (in practice, you'd get these from Semantic Scholar API or PubMed)
    abstracts = [
        {
            "title": "Selective NaV1.7 inhibition by a computationally designed protein binder",
            "abstract": "We report the design of a de novo protein that binds the voltage-sensing "
                         "domain of NaV1.7 with sub-nanomolar affinity. The binder shows >100-fold "
                         "selectivity over NaV1.5 and reverses mechanical allodynia in a CFA model."
        },
        {
            "title": "CRISPR-based gene therapy for SCN9A gain-of-function pain disorders",
            "abstract": "We developed an AAV-delivered CRISPR system targeting SCN9A in DRG neurons. "
                         "Intrathecal injection reduced NaV1.7 expression by 60% and attenuated "
                         "thermal hyperalgesia in erythromelalgia model mice."
        },
        {
            "title": "Global analysis of sodium channel expression across human tissues",
            "abstract": "RNA-seq analysis of 50 human tissues reveals tissue-specific sodium channel "
                         "expression patterns. NaV1.7 shows highest expression in DRG and sympathetic "
                         "ganglia. We identify novel splice variants in pain-related tissues."
        }
    ]

    print("Screening papers for relevance to de novo binder design...\n")

    for paper in abstracts:
        response = client.messages.create(
            model="claude-haiku-3-5-20241022",  # Haiku for fast, cheap screening
            max_tokens=150,
            messages=[{
                "role": "user",
                "content": f"""Rate this paper's relevance to DE NOVO PROTEIN BINDER DESIGN 
    for NaV1.7/NaV1.8 ion channels. Reply with exactly one line:
    RELEVANCE: [HIGH/MEDIUM/LOW] — [one sentence explanation]

    Title: {paper['title']}
    Abstract: {paper['abstract']}"""
            }]
        )
    
        print(f"Paper: {paper['title']}")
        print(f"  {response.content[0].text}")
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice we used **Haiku** here — the smallest/cheapest model. For simple classification tasks like this, you don't need a frontier model. Processing 200 abstracts this way would cost about $0.20.

    > **Think Python connection:** Chapter 4 covers functions and code reuse. The pattern above — wrapping an API call in a loop — is a direct application of those concepts. If you wanted to make it reusable, you'd wrap it in a function (Chapter 3 in Think Python).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Map your ideal AI-augmented research workflow

    This is a planning exercise. In the markdown cell below, map out how you'd use AI tools for a specific research task you're actually working on.

    Pick one of these (or choose your own):
    1. Designing a new binder for KCNQ2/3
    2. Writing the methods section of a paper
    3. Analyzing a batch of electrophysiology data
    4. Preparing a conference talk on your de novo binder results

    For each step, note:
    - What tool you'd use
    - What specifically you'd ask it to do
    - What you'd do yourself (the human-in-the-loop parts)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### My AI-augmented workflow plan

    **Task:** *(write your task here)*

    **Step 1:**
    - Tool:
    - AI does:
    - I do:

    **Step 2:**
    - Tool:
    - AI does:
    - I do:

    **Step 3:**
    - Tool:
    - AI does:
    - I do:

    **Step 4:**
    - Tool:
    - AI does:
    - I do:

    **Step 5:**
    - Tool:
    - AI does:
    - I do:

    **What's the bottleneck?** Where is AI most/least helpful in this workflow?
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **AI coding assistants:**
    - [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code) -- setup, usage, and tips for your primary coding assistant
    - [GitHub Copilot documentation](https://docs.github.com/en/copilot) -- official docs including setup for VS Code, JetBrains, and Neovim
    - [Cursor](https://www.cursor.com/) -- AI-native code editor built on VS Code

    **Literature and research tools:**
    - [Semantic Scholar](https://www.semanticscholar.org/) -- free academic search with AI-powered features; [API documentation](https://api.semanticscholar.org/)
    - [Elicit](https://elicit.com/) -- AI research assistant for paper extraction and systematic reviews
    - [Consensus](https://consensus.app/) -- claim verification against the academic literature
    - [Connected Papers](https://www.connectedpapers.com/) -- visual citation graphs for literature mapping
    - [Google NotebookLM](https://notebooklm.google.com/) -- upload documents and ask questions across them

    **Writing and communication:**
    - [Overleaf](https://www.overleaf.com/) -- collaborative LaTeX editor with emerging AI features
    - [Grammarly](https://www.grammarly.com/) -- grammar and style checking across platforms

    **Data analysis:**
    - [marimo documentation](https://docs.marimo.io/) -- official docs for marimo notebooks
    - [ChatGPT Code Interpreter](https://openai.com/index/chatgpt-plugins/) -- upload data and get instant analysis (useful for quick exploration)

    **MIT Missing Semester:**
    - [Lecture 5: Command-line Environment](https://missing.csail.mit.edu/2020/command-line/) -- terminal skills that make Claude Code more powerful
    - [Lecture 6: Version Control (Git)](https://missing.csail.mit.edu/2020/version-control/) -- essential for managing code and collaborating
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
    - 2026-03-25: QA pass — removed duplicate sections (coding assistants, research tools, Edit Log)
    - 2026-03-25: Added callout boxes — decision point (which tools for which workflow), warning (tool fatigue), tip (two-tool rule)
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Models and Providers](01-models-and-providers.py) | [Module Index](../README.md) | [Next: Staying Current \u2192](03-staying-current.py)
    """)
    return


if __name__ == "__main__":
    app.run()

