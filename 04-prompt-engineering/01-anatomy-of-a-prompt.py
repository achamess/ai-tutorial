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
    # 01: Anatomy of a Prompt

    You already use Claude for grant writing and literature synthesis — so you know that *how* you ask matters. This notebook takes that intuition and makes it systematic.

    We'll break every prompt into its component parts, then build one up piece by piece so you can see exactly how each addition changes the output.

    > **Requires:** `ANTHROPIC_API_KEY` set as an environment variable. All code cells call the Claude API.
    >
    > **Key reference:** [Anthropic's Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) covers these same concepts — and a local copy is available at `resources/references/anthropic-prompt-engineering-guide.md`. Also see the [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) for worked examples.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: How Claude "Thinks"](../03-how-llms-work/03-how-claude-thinks.py) | [Module Index](../README.md) | [Next: Techniques That Work \u2192](02-techniques-that-work.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Prompt quality is the highest-leverage skill in AI use. A 30-second improvement to your prompt can save 30 minutes of re-prompting and manual editing. This notebook teaches you the systematic framework to get it right the first time.
    > - The difference between a generic NaV1.7 overview and a targeted analysis of binder-accessible epitopes on VSD-II comes down to adding the right components: role, context, constraints, and output format. Each component is a dial you can turn.
    > - When Claude gives you a mediocre response, you need a diagnostic framework: is the problem missing context? Wrong role? No output format specified? This notebook gives you that framework.
    > - Every prompt you write for the API (Module 05) and every CLAUDE.md instruction (Module 04) uses these same components. This is the foundation for all your AI interactions going forward.
    """)
    return


@app.cell
def _():
    import anthropic
    import os

    # Initialize the client — picks up ANTHROPIC_API_KEY from your environment
    client = anthropic.Anthropic()

    # Helper function we'll reuse throughout this notebook
    def ask_claude(user_prompt, system_prompt=None, model="claude-sonnet-4-20250514", max_tokens=1024, temperature=0.0):
        """Send a prompt to Claude and return the text response."""
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "user", "content": user_prompt}],
        }
        if system_prompt:
            kwargs["system"] = system_prompt
        response = client.messages.create(**kwargs)
        return response.content[0].text

    print("Client ready.")
    return (ask_claude,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The six components of a prompt

    Every effective prompt is built from some combination of these parts:

    | Component | What it does | Example |
    |-----------|-------------|--------|
    | **System prompt / Role** | Sets the persona and ground rules | "You are an expert in voltage-gated sodium channel pharmacology" |
    | **Context** | Background information Claude needs | A paper abstract, dataset description, or experimental protocol |
    | **Instruction** | The actual task — what you want Claude to do | "Summarize the key findings" |
    | **Examples** | Demonstrations of the desired input/output format | A sample summary you've written |
    | **Constraints** | Guardrails: length limits, what to include/exclude, tone | "Keep it under 200 words. Do not speculate beyond the data." |
    | **Output format** | The structure you want the response in | "Return a markdown table with columns: Gene, Mutation, Effect" |

    You don't need all six every time. But knowing they exist means you can reach for the right one when a prompt isn't giving you what you want.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🔑 **Key concept:** The quality of your prompt determines the quality of the output. This isn't a platitude — it's a measurable fact. A vague prompt ("tell me about NaV1.7") produces a generic Wikipedia-style response. A structured prompt with role, context, constraints, and output format produces exactly what you need, first try. The difference is 30 seconds of prompt investment that saves 30 minutes of re-prompting and manual editing. The rest of this notebook shows you this progression step by step.

    > 💡 **Tip:** Start with the simplest prompt and iterate. Don't try to write a perfect prompt on the first attempt. Start with just your instruction, see what comes back, then add components one at a time: context, then role, then constraints, then output format. Each addition is a dial you turn. The progressive build-up demo below shows exactly this workflow.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.mermaid(
        """
        graph TD
            subgraph "The 6 Components of an Effective Prompt"
                ROLE["1. <b>ROLE / System Prompt</b><br/>'You are an ion channel<br/>pharmacology expert'"]
                CTX["2. <b>CONTEXT</b><br/>Paper abstract, dataset,<br/>experimental protocol"]
                INST["3. <b>INSTRUCTION</b><br/>'Summarize the key findings<br/>relevant to binder design'"]
                EX["4. <b>EXAMPLES</b><br/>Input/output demonstrations<br/>showing the format you want"]
                CON["5. <b>CONSTRAINTS</b><br/>'Under 150 words,<br/>no speculation, exact numbers'"]
                FMT["6. <b>OUTPUT FORMAT</b><br/>'Return a markdown table<br/>with columns: Gene, Mutation, Effect'"]
            end
        
            ROLE --> CTX --> INST --> EX --> CON --> FMT
        
            subgraph "When output isn't right, diagnose:"
                P1["Too generic?"] -.-> CTX
                P2["Misses what matters?"] -.-> ROLE
                P3["Too long/vague?"] -.-> CON
                P4["Inconsistent format?"] -.-> FMT
                P5["Doesn't understand task?"] -.-> EX
                P6["Task too complex?"] -.-> CHAIN["Break into a<br/>prompt chain"]
            end
        
            style ROLE fill:#aa44aa,color:#fff
            style CTX fill:#cc8844,color:#fff
            style INST fill:#4488cc,color:#fff
            style EX fill:#44aa88,color:#fff
            style CON fill:#cc4444,color:#fff
            style FMT fill:#448888,color:#fff
        """
    ),
    mo.md(r"""

    You don't need all six every time. But when a prompt isn't working, this map tells you which dial to turn.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Demo: Building a prompt piece by piece

    Let's start with a bare-bones prompt and progressively improve it. Our task: ask Claude to summarize findings about NaV1.7 gain-of-function mutations in inherited pain disorders.

    Here's a realistic abstract we'll use as context:
    """)
    return


@app.cell
def _():
    # A representative abstract about NaV1.7 gain-of-function mutations
    paper_abstract = """
    Gain-of-function mutations in SCN9A, encoding the voltage-gated sodium channel NaV1.7,
    are responsible for three human pain syndromes: inherited erythromelalgia (IEM),
    paroxysmal extreme pain disorder (PEPD), and small fiber neuropathy (SFN). We performed
    whole-cell patch-clamp recordings on HEK293 cells expressing wild-type and mutant NaV1.7
    channels (I848T, L858H, A863P, V400M, and S241T). All five mutations shifted the voltage
    dependence of activation in the hyperpolarizing direction (range: -5.2 to -12.7 mV),
    lowering the threshold for action potential firing. Three mutations (I848T, L858H, A863P)
    also slowed fast inactivation by 1.5- to 3.2-fold. When expressed in DRG neurons derived
    from NaV1.7-null mice, mutant channels produced spontaneous firing at rates of 2.4-8.1 Hz,
    compared with 0.1 Hz for wild-type. Molecular dynamics simulations suggest that IEM
    mutations destabilize the S4-S5 linker in domain III, facilitating outward movement of
    the S4 voltage sensor. These findings establish a biophysical framework linking specific
    NaV1.7 mutations to distinct pain phenotypes through quantifiable shifts in channel gating.
    """

    print("Abstract loaded.")
    return (paper_abstract,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Attempt 1: Instruction only (minimal prompt)
    """)
    return


@app.cell
def _(ask_claude):
    # Attempt 1: Just the instruction — no context, no role, no constraints
    response_v1 = ask_claude("Summarize NaV1.7 gain-of-function mutations in pain.")

    print("=== ATTEMPT 1: Instruction only ===")
    print(response_v1)
    return (response_v1,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice what happens: Claude gives a *general* answer drawn from its training data. It's not wrong, but it's generic — it doesn't reference the specific mutations or data from the paper you care about.

    ### Attempt 2: Add context
    """)
    return


@app.cell
def _(ask_claude, paper_abstract):
    # Attempt 2: Instruction + context
    prompt_v2 = f"""Here is a paper abstract:

    {paper_abstract}

    Summarize the key findings of this paper."""

    response_v2 = ask_claude(prompt_v2)

    print("=== ATTEMPT 2: Instruction + context ===")
    print(response_v2)
    return (response_v2,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Better — now it's grounded in the actual paper. But it's probably too long, and it may not emphasize the aspects you care about as a binder designer.

    ### Attempt 3: Add a role via the system prompt
    """)
    return


@app.cell
def _(ask_claude, paper_abstract):
    # Attempt 3: Instruction + context + role (system prompt)
    system_v3 = """You are an expert in ion channel biophysics and pain neuroscience.
    You work with a team designing de novo protein binders targeting NaV1.7 and NaV1.8
    for pain therapeutics. When summarizing papers, focus on findings that are relevant
    to therapeutic targeting — especially structural insights, druggable mechanisms,
    and any quantitative data on channel gating."""

    prompt_v3 = f"""Here is a paper abstract:

    {paper_abstract}

    Summarize the key findings of this paper."""

    response_v3 = ask_claude(prompt_v3, system_prompt=system_v3)

    print("=== ATTEMPT 3: + Role (system prompt) ===")
    print(response_v3)
    return response_v3, system_v3


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The role changes *what Claude pays attention to*. With the binder-designer framing, it should now emphasize the structural mechanism (S4-S5 linker destabilization) and the quantitative gating shifts — the stuff that matters for your work.

    ### Attempt 4: Add constraints
    """)
    return


@app.cell
def _(ask_claude, paper_abstract, system_v3):
    # Attempt 4: + Constraints
    prompt_v4 = f"""Here is a paper abstract:

    {paper_abstract}

    Summarize the key findings of this paper.

    Constraints:
    - Maximum 150 words
    - Focus on quantitative results (voltage shifts, firing rates, fold-changes)
    - Do not restate the methods — only findings and their implications
    - Highlight any structural insights relevant to drug/binder design"""

    response_v4 = ask_claude(prompt_v4, system_prompt=system_v3)

    print("=== ATTEMPT 4: + Constraints ===")
    print(response_v4)
    print(f"\n[Word count: {len(response_v4.split())}]")
    return (response_v4,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Constraints are where you get precision. The word limit forces conciseness, and the explicit instructions about what to include/exclude shape the content.

    ### Attempt 5: Add output format
    """)
    return


@app.cell
def _(ask_claude, paper_abstract, system_v3):
    # Attempt 5: + Output format
    prompt_v5 = f"""Here is a paper abstract:

    {paper_abstract}

    Summarize the key findings in the following format:

    **One-sentence takeaway:** [Single sentence capturing the main finding]

    **Mutations studied:** [Markdown table with columns: Mutation | Syndrome | Activation shift (mV) | Inactivation effect]

    **Structural insight:** [1-2 sentences on the structural mechanism]

    **Relevance to binder design:** [1-2 sentences on what this means for targeting NaV1.7]

    Constraints:
    - Stick strictly to data reported in the abstract
    - Use exact numbers where available
    - If information is not in the abstract, write "Not reported" in the table cell"""

    response_v5 = ask_claude(prompt_v5, system_prompt=system_v3)

    print("=== ATTEMPT 5: + Output format ===")
    print(response_v5)
    return (response_v5,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Now you're getting a structured, scannable summary that you could paste straight into your lab notes or a Slack channel.

    ### Side-by-side comparison
    """)
    return


@app.cell
def _(response_v1, response_v2, response_v3, response_v4, response_v5):
    # Let's compare lengths and see the progression
    versions = {
        "V1 — Instruction only": response_v1,
        "V2 — + Context": response_v2,
        "V3 — + Role": response_v3,
        "V4 — + Constraints": response_v4,
        "V5 — + Output format": response_v5,
    }

    print("Prompt version                | Words | First 80 chars")
    print("-" * 80)
    for name, text in versions.items():
        word_count = len(text.split())
        preview = text.replace("\n", " ")[:80]
        print(f"{name:<30}| {word_count:>5} | {preview}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.mermaid(
        """
        graph LR
            subgraph "System Prompt (standing rules)"
                SP["Your role, domain,<br/>team conventions<br/><i>Doesn't change between requests</i>"]
            end
        
            subgraph "User Prompt (specific task)"
                UP["Context + instruction +<br/>constraints + format<br/><i>Changes every time</i>"]
            end
        
            SP --> |"combined for<br/>each API call"| CALL["Claude<br/>API Call"]
            UP --> CALL
            CALL --> OUT["Tailored<br/>Response"]
        
            style SP fill:#aa44aa,color:#fff
            style UP fill:#4488cc,color:#fff
            style CALL fill:#44aa88,color:#fff
            style OUT fill:#44aa88,color:#fff
        """
    ),
    mo.md(r"""

    **Think of it like a lab protocol:** The system prompt is the standing protocol (always the same). The user prompt is today's specific experiment (what sample, what conditions, what measurements).
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The component map

    Here's a mental model for when to reach for each component:

    | Problem | Fix |
    |---------|-----|
    | Response is too generic | Add **context** (paste in the actual data/text) |
    | Response misses what matters to you | Add a **role/system prompt** that reflects your expertise |
    | Response is too long or too vague | Add **constraints** (word limits, include/exclude rules) |
    | Response format is inconsistent | Specify **output format** explicitly |
    | Claude doesn't understand the task | Add **examples** (we'll cover this in depth in notebook 02) |
    | Task is too complex for one pass | Break it into a **prompt chain** (also notebook 02) |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use a system prompt vs. a user prompt?
    >
    > | Put in the... | What goes here | Pros | Cons | Use when... |
    > |---------------|---------------|------|------|-------------|
    > | **System prompt** | Your role, domain expertise, standing conventions, style rules | Persists across all turns in a conversation; sets consistent behavior; separates "who Claude is" from "what to do" | Can't change mid-conversation without starting a new one; invisible in some interfaces | You have standing context that applies to many different requests: your research area, your lab's conventions, formatting preferences |
    > | **User prompt** | The specific task, context data (paper abstracts, datasets), constraints for this task, output format | Can change every message; carries the actual data and instructions | Must be re-specified each time; can get long if you repeat standing context | You have a specific task with specific data: "summarize this abstract," "extract data from this table," "debug this code" |
    >
    > **Think of it like a lab protocol:** The system prompt is the standing protocol (always the same). The user prompt is today's specific experiment (what sample, what conditions, what measurements).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## System prompt vs. user prompt: when to use which

    The **system prompt** is like the lab protocol — it sets the standing rules. The **user prompt** is the specific request for today's experiment.

    Put things in the **system prompt** when:
    - They apply to many different requests (your role, your domain, your team's conventions)
    - They're about *how* Claude should behave, not *what* to do right now

    Put things in the **user prompt** when:
    - They're specific to this one task (the abstract, the dataset, the question)
    - They change from request to request

    Let's see the difference:
    """)
    return


@app.cell
def _(ask_claude, paper_abstract):
    # A reusable system prompt — this captures your standing context
    my_system_prompt = """You are a research assistant for a pain neuroscience lab that designs
    de novo protein binders for ion channels (NaV1.7, NaV1.8, KCNQ2/3). The lab also works
    on targeted protein degradation (PROTACs, molecular glues). When analyzing papers or data,
    always consider relevance to these therapeutic approaches.

    Style rules:
    - Be concise — the PI reads these on their phone between experiments
    - Lead with the finding, not the background
    - Flag anything that suggests a new binder target site or degradation strategy
    - Use exact numbers from the source material"""

    # Now we can use this same system prompt for very different tasks:
    response_a = ask_claude(
        f"Summarize this abstract for our lab meeting:\n\n{paper_abstract}",
        system_prompt=my_system_prompt
    )

    print("=== Task A: Summarize for lab meeting ===")
    print(response_a)
    print()
    return (my_system_prompt,)


@app.cell
def _(ask_claude, my_system_prompt, paper_abstract):
    # Same system prompt, completely different task
    response_b = ask_claude(
        f"""Based on this abstract, what are the top 3 regions of NaV1.7 that
    our lab should consider as binder target sites? For each, explain why.

    Abstract:
    {paper_abstract}""",
        system_prompt=my_system_prompt
    )

    print("=== Task B: Identify binder target sites ===")
    print(response_b)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The system prompt stays the same, but the output changes dramatically because the instruction changes. This is the power of separating the *standing context* from the *specific task*.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Common pitfalls

    **1. Stuffing everything into one paragraph**

    Bad:
    ```
    You are an ion channel expert and I need you to summarize this paper about NaV1.7 mutations and make it short and in a table format and also mention what it means for drug design.
    ```

    Better: Separate your components with clear headers or line breaks, as we did in Attempt 5.

    **2. Being vague about constraints**

    Bad: "Keep it short."
    Better: "Maximum 150 words."

    Bad: "Focus on the important stuff."
    Better: "Focus on quantitative gating parameters and structural mechanisms."

    **3. Asking Claude to not hallucinate (instead of giving it the data)**

    Bad: "Don't make anything up about NaV1.7 mutations."
    Better: Provide the abstract and say "Stick strictly to data reported in the abstract."

    The best way to prevent hallucination is to give Claude the source material and constrain it to that material.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise 1: Deconstruct and improve a research digest prompt

    Here's a prompt that a researcher might use to create a daily research digest. It works, but it's not great. Your task:

    1. Run it as-is and read the output
    2. Identify which components are present and which are missing
    3. Rewrite it using the component framework from this notebook
    4. Compare the outputs
    """)
    return


@app.cell
def _(ask_claude):
    # The "before" prompt — run this and see what you get
    digest_abstracts = """
    Abstract 1: We identified a novel NaV1.8 splice variant enriched in human DRG nociceptors
    that shows altered voltage-dependent inactivation kinetics. RNAscope confirmed expression
    in TRPV1+ neurons. The variant produces a 4.2 mV depolarizing shift in steady-state
    inactivation and increases persistent current by 34%, suggesting a role in chronic pain
    sensitization. CRISPR deletion of this variant in mice reduced inflammatory pain behavior
    by 41% in the CFA model.

    Abstract 2: Structure-guided design yielded a macrocyclic peptide (MC-771) that binds the
    KCNQ2/3 channel opener site with 2.8 nM affinity. Cryo-EM at 2.9 angstrom resolution
    reveals MC-771 occupies a pocket at the S5-S6 linker interface between KCNQ2 and KCNQ3
    subunits. MC-771 enhanced M-current amplitude by 280% in DRG neurons and reduced
    mechanical allodynia in the SNI model of neuropathic pain (von Frey threshold: 1.2g
    vs 0.4g vehicle, p<0.001).

    Abstract 3: Single-cell RNA-seq of human L4-L5 DRG from chronic pain patients (n=8)
    and controls (n=6) identified 14 neuronal subtypes. Pain patients showed selective
    upregulation of SCN10A, KCNQ2, and CALCA in peptidergic nociceptors (log2FC 1.8, 1.2,
    and 2.1 respectively, FDR<0.01). Trajectory analysis revealed a novel "pain-activated"
    transcriptional state characterized by co-expression of ATF3, NPY, and BDNF.
    """

    # The unoptimized prompt
    basic_prompt = f"""Tell me what's interesting about these papers for someone who works
    on pain and ion channels:

    {digest_abstracts}"""

    response_basic = ask_claude(basic_prompt)

    print("=== BEFORE: Basic prompt ===")
    print(response_basic)
    return (digest_abstracts,)


@app.cell
def _(digest_abstracts):
    # YOUR TURN: Rewrite the prompt using the component framework
    # Think about: what role should Claude have? What constraints matter?
    # What output format would make this most useful as a daily digest?

    # Hint: Consider using a system prompt + a structured user prompt
    # with explicit output formatting instructions.

    improved_system = """
    # TODO: Write a system prompt that captures your role and standing instructions
    """

    improved_prompt = f"""
    # TODO: Write the user prompt with context, instruction, constraints, and output format
    # Use the abstracts: {digest_abstracts}
    """

    # Uncomment these lines once you've written your prompts:
    # response_improved = ask_claude(improved_prompt, system_prompt=improved_system)
    # print("=== AFTER: Improved prompt ===")
    # print(response_improved)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise 2: Build a prompt from scratch

    Pick one of these tasks and build a prompt using all the components that make sense:

    1. **Binder design review:** Given a description of a de novo protein binder candidate, ask Claude to evaluate its strengths, weaknesses, and suggest modifications
    2. **Experimental protocol check:** Paste in a calcium imaging protocol and ask Claude to identify potential issues and suggest controls
    3. **Grant aim critique:** Paste a Specific Aim and ask Claude to find logical gaps and suggest improvements

    For whichever you choose, write:
    - A system prompt
    - A user prompt with context, instruction, constraints, and output format

    Then run it and iterate — try removing a component to see how the output changes.
    """)
    return


@app.cell
def _():
    # Your prompt-from-scratch exercise

    exercise_system = """
    # TODO: Your system prompt here
    """

    exercise_prompt = """
    # TODO: Your user prompt here — include context, instruction, constraints, output format
    """

    # Uncomment to run:
    # response_exercise = ask_claude(exercise_prompt, system_prompt=exercise_system)
    # print(response_exercise)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - Every prompt has up to six components: **role, context, instruction, examples, constraints, output format**
    - Adding components incrementally and observing the change is the fastest way to improve a prompt
    - **System prompts** hold your standing context; **user prompts** hold the specific task
    - Constraints should be **specific and measurable** ("150 words" not "short")
    - The best defense against hallucination is providing source material and constraining Claude to it

    Next up: **02-techniques-that-work.py** — chain-of-thought, few-shot examples, prompt chaining, and temperature.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created notebook with initial content
    - 2026-03-25: Added "Why this matters" rationale section
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: Added standardized callouts and decision frameworks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Anthropic's official guide covering all prompt components; a local copy is also available at `resources/references/anthropic-prompt-engineering-guide.md`
    - [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — a collection of worked examples and code recipes for using the Claude API effectively
    - [Anthropic: System Prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) — best practices for writing system prompts
    - [Anthropic docs: Temperature](https://docs.anthropic.com/en/api/messages) — API reference for the `temperature` parameter and how it affects output variability
    - [Anthropic: Give Claude a Role](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/give-claude-a-role) — specific guidance on role prompting
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Edit Log

    - 2026-03-25: Created notebook with initial content
    - 2026-03-25: Added "Why this matters" rationale section
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: Added external references and Further Reading section
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

