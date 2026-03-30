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
    # 02: Techniques That Work

    Now that you know the anatomy of a prompt, let's fill your toolbox with specific techniques. For each one, we'll run a before/after comparison so you can see the difference yourself.

    > **Requires:** `ANTHROPIC_API_KEY` set as an environment variable.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Anatomy of a Prompt](01-anatomy-of-a-prompt.py) | [Module Index](../README.md) | [Next: Prompts for Research \u2192](03-prompts-for-research.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Chain-of-thought prompting is how you get Claude to actually reason through your calcium imaging results instead of giving a surface-level summary. Without it, you get pattern-matched answers; with it, you get step-by-step analysis that mirrors how you'd think at the bench.
    > - Few-shot examples are the most reliable way to get consistent, structured output — critical when you're batch-processing 50 paper abstracts for a literature review or extracting data from screening results. Show the format once, get it right every time.
    > - Prompt chaining (breaking complex tasks into steps) is how you'll build real research workflows: evaluate experimental design, then plan analysis, then generate biological questions. Each step feeds the next, and you can review intermediates.
    > - These techniques directly reduce the time you spend re-prompting. Instead of sending the same request five times hoping for a better answer, you engineer the prompt once and get what you need.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Chain-of-thought prompting

    When you need Claude to reason through a problem — not just retrieve an answer — ask it to think step by step. This is especially useful for:

    - Interpreting experimental results
    - Evaluating whether a conclusion follows from the data
    - Planning multi-step analyses

    The key phrase: **"Think through this step by step"** (or more specifically, tell Claude *what* steps to think through).
    """)
    return


@app.cell
def _(ask_claude):
    # Scenario: Interpreting unexpected calcium imaging results
    experiment_description = """
    We performed calcium imaging on cultured mouse DRG neurons to test our de novo binder
    DNB-Nav17-003 (designed to bind the NaV1.7 DII-III linker). Protocol:
    - Loaded neurons with Fura-2 AM
    - Baseline recording: 5 min
    - Applied 100 nM DNB-Nav17-003 in bath solution
    - Stimulated with 50 mM KCl at 10 min

    Results:
    - 68% of neurons showed reduced calcium transient amplitude after binder application
      (mean reduction: 34%, p<0.01 vs vehicle)
    - BUT: 12% of neurons showed INCREASED transient amplitude (mean increase: 52%)
    - The "increased" population was enriched for large-diameter neurons (>35 um)
    """

    # WITHOUT chain of thought
    response_no_cot = ask_claude(f"""
    What might explain these calcium imaging results?

    {experiment_description}""")

    print("=== WITHOUT chain of thought ===")
    print(response_no_cot)
    return (experiment_description,)


@app.cell
def _(ask_claude, experiment_description):
    # WITH chain of thought — guide the reasoning
    response_cot = ask_claude(f"""
    Interpret these calcium imaging results. Think through this step by step:

    1. First, consider what the expected result should be if the binder works as designed
    2. Evaluate whether the 68% responder population supports the intended mechanism
    3. Consider possible explanations for the paradoxical 12% "increased" population,
       especially given their large diameter
    4. Assess whether this could be a NaV1.7 selectivity issue (what other channels
       are expressed in large-diameter DRG neurons?)
    5. Suggest the most likely explanation and what experiment would test it

    Experimental data:
    {experiment_description}""")

    print("=== WITH chain of thought ===")
    print(response_cot)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    The chain-of-thought version doesn't just list possibilities — it *reasons through* them. And because you told it what steps to follow, the reasoning follows a logical path that mirrors how you'd think about this at the bench.

    **When to use it:** Any time you need reasoning, interpretation, or evaluation — not just retrieval.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** Which prompting technique for which task?
    >
    > | Technique | How it works | Pros | Cons | Use when... |
    > |-----------|-------------|------|------|-------------|
    > | **Chain-of-thought** ("think step by step") | Guide Claude to reason through intermediate steps before concluding | Dramatically improves reasoning; makes logic transparent and auditable; catches errors in reasoning | Longer responses; costs more tokens; slower | You need *interpretation* or *evaluation*: analyzing experimental results, comparing approaches, planning multi-step analyses |
    > | **Few-shot examples** (show 1-3 input/output pairs) | Demonstrate the exact format and style you want | Most reliable formatting technique; no ambiguity about what you expect; scales to batch processing | Costs extra tokens for the examples; requires having good examples | You need *consistent, structured output*: data extraction, batch processing, any task where format matters more than creativity |
    > | **Role prompting** (assign an expert persona) | Tell Claude to think as a specific expert | Changes what Claude pays attention to; reveals different facets of the same data | Can bias the response; expert role may not be calibrated | You want a *specific perspective*: reviewer, protein engineer, translational scientist; or to stress-test results through multiple lenses |
    > | **Prompt chaining** (break task into steps) | Feed output of step N as input to step N+1 | Handles complex tasks; reviewable intermediates; different roles per step | More API calls; must design the pipeline; error can propagate between steps | The task is too complex for one prompt: "evaluate design, then plan analysis, then generate questions" |
    >
    > **Combinations are powerful.** The best prompts often use role + chain-of-thought + output format together.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Few-shot examples

    Instead of explaining what you want, *show* Claude what you want. Give it 1-3 input/output examples, and it will match the pattern. This approach, known as **few-shot prompting**, was demonstrated at scale by [Brown et al. (2020)](https://arxiv.org/abs/2005.14165) in the GPT-3 paper.

    This is the single most effective technique for getting consistent, formatted output.
    """)
    return


@app.cell
def _(ask_claude):
    # Task: Extract structured data from a paper title+abstract
    # WITHOUT examples — Claude has to guess the format

    abstract_to_parse = """
    Title: Selective PROTAC-mediated degradation of NaV1.7 reverses inflammatory
    and neuropathic pain in mice

    Abstract: We developed a heterobifunctional degrader (NVD-992) linking a NaV1.7-selective
    peptide binder to a cereblon (CRBN) E3 ligase recruiter. NVD-992 induced dose-dependent
    degradation of NaV1.7 in DRG neurons (DC50 = 8.3 nM, Dmax = 89%) with >50-fold
    selectivity over NaV1.8 and NaV1.6. In the CFA inflammatory pain model, a single
    intrathecal injection of NVD-992 (10 ug) reversed thermal hyperalgesia for 72 hours
    (Hargreaves latency: 12.1 +/- 1.3s vs 5.4 +/- 0.8s vehicle, p<0.001). In the SNI
    neuropathic model, mechanical allodynia was reduced for 96 hours (von Frey threshold:
    1.4 +/- 0.2g vs 0.3 +/- 0.1g, p<0.001). Immunostaining confirmed NaV1.7 protein
    reduction of 78% in DRG at 48h post-injection. No motor deficits were observed.
    """

    response_no_examples = ask_claude(f"""Extract the key data from this paper:

    {abstract_to_parse}""")

    print("=== WITHOUT few-shot examples ===")
    print(response_no_examples)
    return (abstract_to_parse,)


@app.cell
def _(abstract_to_parse, ask_claude):
    # WITH few-shot examples — show Claude the exact format you want
    response_with_examples = ask_claude(f"""Extract structured data from a paper abstract.
    Follow exactly the format shown in these examples.

    ---
    EXAMPLE 1:
    Input: "A small molecule inhibitor (XQ-42) of KCNQ2/3 channels showed IC50 of 340 nM
    and reduced M-current by 67% in DRG neurons. In the formalin test, XQ-42 (30 mg/kg i.p.)
    increased Phase II pain behaviors by 2.1-fold."

    Output:
    - Compound: XQ-42
    - Target: KCNQ2/3
    - Mechanism: Small molecule inhibitor
    - In vitro potency: IC50 = 340 nM
    - Cellular effect: 67% reduction in M-current (DRG neurons)
    - In vivo model: Formalin test
    - In vivo dose/route: 30 mg/kg i.p.
    - In vivo result: 2.1-fold increase in Phase II behaviors
    - Selectivity: Not reported
    - Duration of effect: Not reported

    ---
    EXAMPLE 2:
    Input: "We designed a peptide toxin analog (MTx-7m) targeting the NaV1.8 voltage sensor.
    MTx-7m inhibited NaV1.8 currents with IC50 of 12 nM and 8-fold selectivity over NaV1.7.
    No in vivo data were reported."

    Output:
    - Compound: MTx-7m
    - Target: NaV1.8
    - Mechanism: Peptide toxin analog (voltage sensor targeting)
    - In vitro potency: IC50 = 12 nM
    - Cellular effect: Not reported
    - In vivo model: Not tested
    - In vivo dose/route: Not tested
    - In vivo result: Not tested
    - Selectivity: 8-fold over NaV1.7
    - Duration of effect: Not reported

    ---
    NOW EXTRACT:
    {abstract_to_parse}""")

    print("=== WITH few-shot examples ===")
    print(response_with_examples)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > ⚠️ **Warning:** Don't over-engineer your prompts. It's tempting to cram every technique into every prompt: chain-of-thought + few-shot + role + constraints + output format. But more complexity isn't always better. An over-engineered prompt can actually confuse Claude by giving conflicting instructions, and it costs more tokens. Start with the simplest prompt that works. Add techniques only when the output isn't good enough — and add them one at a time so you know which one helped.

    > 💡 **Tip:** Test prompts with simple inputs first. Before running your carefully crafted prompt on your real 8,000-token paper, test it on a 2-sentence toy input. This lets you iterate on the prompt structure quickly and cheaply. Once the format and logic are right on the toy input, switch to your real data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Notice:
    - The output format matches your examples exactly
    - Fields that aren't in the abstract say "Not reported" (because your examples taught that pattern)
    - You didn't need to explain the format — you just showed it

    **Rule of thumb:** If you spend more than two sentences explaining a format, you'd be better off showing an example.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Role prompting

    Giving Claude a specific expert role changes not just tone but *what it pays attention to*. Different roles notice different things in the same data.
    """)
    return


@app.cell
def _(ask_claude):
    # Same data, three different expert perspectives
    experimental_finding = """
    Our de novo protein binder (DNB-Q23) targets the KCNQ2 N-terminus and enhances
    M-current by 180% in HEK293 cells (EC50 = 15 nM). However, in cultured DRG neurons,
    M-current enhancement was only 45% at 100 nM, and 30% of neurons showed no response.
    Thermal stability assay showed Tm = 42 degrees C. The binder showed no effect on
    KCNQ3 homomers or KCNQ5.
    """

    roles = {
        "Ion channel pharmacologist": """You are an expert ion channel pharmacologist
            who has spent 20 years studying KCNQ channels. Focus on the channel biology
            and pharmacological implications.""",
        "Protein engineer": """You are an expert protein engineer specializing in
            de novo binder design and optimization. Focus on the binder properties
            and what needs to be improved.""",
        "Translational scientist": """You are a translational pain scientist evaluating
            drug candidates. Focus on whether this has potential as a therapeutic and
            what the path to the clinic looks like."""
    }

    for role_name, role_prompt in roles.items():
        response = ask_claude(
            f"Evaluate this finding and identify the key issues:\n\n{experimental_finding}",
            system_prompt=role_prompt,
            max_tokens=600
        )
        print(f"=== Perspective: {role_name} ===")
        print(response)
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Each expert notices different things:
    - The **pharmacologist** focuses on the HEK-to-DRG discrepancy and subunit selectivity
    - The **protein engineer** focuses on thermal stability and affinity optimization
    - The **translational scientist** focuses on the 30% non-responder rate and what it means for efficacy

    This is a powerful trick for stress-testing your own results: run the same data through multiple expert lenses.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Output formatting — JSON, tables, structured text

    When you need to process Claude's output programmatically (feed it into a spreadsheet, another script, or a database), ask for structured formats.
    """)
    return


@app.cell
def _(ask_claude):
    import json

    # Getting JSON output you can parse in Python
    compounds_text = """
    We tested five NaV1.7 binder candidates in whole-cell patch clamp:
    - DNB-001: IC50 = 8.3 nM, 45-fold selectivity over NaV1.8, Tm = 58 C
    - DNB-002: IC50 = 23.1 nM, 12-fold selectivity over NaV1.8, Tm = 63 C
    - DNB-003: IC50 = 4.7 nM, 8-fold selectivity over NaV1.8, Tm = 41 C
    - DNB-004: IC50 = 67.2 nM, >100-fold selectivity over NaV1.8, Tm = 71 C
    - DNB-005: IC50 = 11.9 nM, 32-fold selectivity over NaV1.8, Tm = 55 C
    """

    response_json = ask_claude(f"""Extract the compound data from this text into JSON format.

    Return a JSON array where each element has these fields:
    - "name": string
    - "ic50_nm": number
    - "selectivity_over_nav18": number (use -1 if reported as ">X")
    - "selectivity_qualifier": string ("exact" or "greater_than")
    - "tm_celsius": number

    Return ONLY the JSON, no other text.

    {compounds_text}""")

    print("Raw response:")
    print(response_json)
    print()

    # Parse it into Python — now you can work with it programmatically
    # Strip markdown code fences if present
    json_text = response_json.strip()
    if json_text.startswith("```"):
        json_text = json_text.split("\n", 1)[1]  # remove first line
        json_text = json_text.rsplit("```", 1)[0]  # remove last fence

    compounds = json.loads(json_text)
    print(f"Parsed {len(compounds)} compounds.")
    print(f"Most potent: {min(compounds, key=lambda x: x['ic50_nm'])['name']}")
    print(f"Most stable: {max(compounds, key=lambda x: x['tm_celsius'])['name']}")
    return (compounds_text,)


@app.cell
def _(ask_claude, compounds_text):
    # You can also ask for markdown tables — great for lab notebooks and Slack
    import pandas as pd

    response_table = ask_claude(f"""Create a markdown table from this data with columns:
    Compound | IC50 (nM) | Selectivity (vs NaV1.8) | Tm (C) | Verdict

    For Verdict, apply these rules:
    - IC50 < 15 nM AND selectivity > 20-fold AND Tm > 50 C = "Advance"
    - Fails one criterion = "Optimize"
    - Fails two or more = "Deprioritize"

    {compounds_text}

    Return ONLY the markdown table.""")

    print(response_table)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why prompt chaining for research?** Real research tasks are rarely one-shot. Evaluating RNA-seq experimental design, then planning the analysis, then generating biological questions requires different expertise at each step. Chaining lets you review intermediates and course-correct — just like you would in a real collaboration.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.mermaid(
        """
        graph TD
            subgraph "Prompt Chaining: Complex Tasks as a Pipeline"
                INPUT["<b>Input</b><br/>RNA-seq experiment<br/>description"]
        
                STEP1["<b>Step 1: Evaluate Design</b><br/>Role: Bioinformatician<br/>Output: Strengths, weaknesses,<br/>missing controls"]
        
                REVIEW1["You review<br/>intermediate output"]
        
                STEP2["<b>Step 2: Plan Analysis</b><br/>Role: Bioinformatician<br/>Input: Experiment + Step 1 output<br/>Output: Analysis pipeline"]
        
                REVIEW2["You review<br/>intermediate output"]
        
                STEP3["<b>Step 3: Generate Questions</b><br/>Role: Translational scientist<br/>Input: Experiment + Step 2 output<br/>Output: Prioritized questions"]
        
                INPUT --> STEP1 --> REVIEW1 --> STEP2 --> REVIEW2 --> STEP3
            end
        
            NOTE["Each step can use a<br/><b>different role</b> and<br/>feeds its output into<br/>the next step's context"]
        
            style INPUT fill:#cc8844,color:#fff
            style STEP1 fill:#4488cc,color:#fff
            style STEP2 fill:#44aa88,color:#fff
            style STEP3 fill:#aa44aa,color:#fff
            style REVIEW1 fill:#fff,stroke:#999
            style REVIEW2 fill:#fff,stroke:#999
        """
    ),
    mo.md(r"""

    The key advantage of chaining: you can **review intermediates** and course-correct between steps, just like you would in a real collaboration.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Prompt chaining — breaking complex tasks into steps

    When a task is too complex for a single prompt, break it into a chain where each step feeds into the next. This mirrors how you'd approach a complex analysis: you don't jump straight from raw data to conclusions.

    Let's build a three-step chain for analyzing an RNA-seq dataset description.
    """)
    return


@app.cell
def _(ask_claude):
    # A description of an RNA-seq experiment
    rnaseq_description = """
    RNA-seq experiment: Profiling DRG transcriptomes after CFA-induced inflammatory pain

    Design:
    - Species: Mouse (C57BL/6J), 8-10 weeks, male and female
    - Groups: CFA-injected left hindpaw (n=6) vs. saline vehicle (n=6)
    - Timepoint: 72 hours post-injection
    - Tissue: L3-L5 DRG, ipsilateral
    - Library: Bulk RNA-seq, polyA-selected, paired-end 150bp
    - Sequencing: NovaSeq 6000, ~30M reads per sample
    - Behavioral confirmation: CFA group showed thermal hyperalgesia
      (Hargreaves: 4.2 +/- 0.8s vs 11.3 +/- 1.1s baseline, p<0.001)
      and mechanical allodynia (von Frey: 0.4 +/- 0.1g vs 1.2 +/- 0.2g baseline, p<0.001)
    """

    # STEP 1: Evaluate the experimental design
    step1_response = ask_claude(f"""
    Evaluate this RNA-seq experimental design for a pain study. Identify:
    1. Strengths of the design
    2. Potential confounds or limitations
    3. Missing controls or information

    Be specific — reference details from the description.

    {rnaseq_description}""",
        system_prompt="You are a bioinformatician with expertise in pain transcriptomics."
    )

    print("=== STEP 1: Design evaluation ===")
    print(step1_response)
    print()
    return rnaseq_description, step1_response


@app.cell
def _(ask_claude, rnaseq_description, step1_response):
    # STEP 2: Feed step 1 output into an analysis planning step
    step2_response = ask_claude(f"""
    Given this RNA-seq experiment and the design evaluation below, propose a
    bioinformatics analysis plan. For each step, specify the tool/method and
    explain why it's appropriate for this dataset.

    Experiment:
    {rnaseq_description}

    Design evaluation from previous review:
    {step1_response}

    Format the plan as a numbered pipeline with these sections:
    1. QC and preprocessing
    2. Alignment and quantification
    3. Differential expression
    4. Downstream analysis (pathway, network, etc.)
    5. Validation priorities

    Focus on analyses relevant to identifying pain-related targets for protein binder design.""",
        system_prompt="You are a bioinformatician with expertise in pain transcriptomics."
    )

    print("=== STEP 2: Analysis plan ===")
    print(step2_response)
    print()
    return (step2_response,)


@app.cell
def _(ask_claude, rnaseq_description, step2_response):
    # STEP 3: Generate specific questions to ask of the data
    step3_response = ask_claude(f"""
    Given this RNA-seq experiment, design evaluation, and analysis plan, generate
    a prioritized list of 5 specific biological questions we should ask of this data.

    Context: Our lab designs de novo protein binders for NaV1.7, NaV1.8, and KCNQ2/3.
    We're also interested in targeted protein degradation approaches.

    Experiment:
    {rnaseq_description}

    Analysis plan:
    {step2_response}

    For each question:
    - State the question
    - Why it matters for our binder program
    - What analysis from the plan would answer it
    - What result would change our priorities""",
        system_prompt="""You are a translational pain scientist who bridges computational
        and experimental research. You think about how transcriptomic data can inform
        drug design decisions."""
    )

    print("=== STEP 3: Biological questions ===")
    print(step3_response)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 6. Temperature: when to adjust it

    Temperature controls randomness in Claude's responses (see the [Anthropic API docs](https://docs.anthropic.com/en/api/messages) for the parameter specification):
    - **0.0** — Deterministic. Same input gives (nearly) the same output. Best for data extraction, analysis, factual tasks.
    - **0.5** — Moderate variety. Good for writing tasks where you want some creativity but still grounded.
    - **1.0** — Maximum variety. Good for brainstorming, generating diverse ideas.

    Let's see the difference on a brainstorming task.
    """)
    return


@app.cell
def _(ask_claude):
    brainstorm_prompt = """Suggest 5 unconventional approaches to targeting NaV1.7 for pain
    relief that go beyond traditional small molecule inhibitors and antibodies.
    For each, give a one-sentence description."""

    print("=== Temperature 0.0 (deterministic) ===")
    print(ask_claude(brainstorm_prompt, temperature=0.0))
    print()
    print("=== Temperature 0.0 again (should be nearly identical) ===")
    print(ask_claude(brainstorm_prompt, temperature=0.0))
    return (brainstorm_prompt,)


@app.cell
def _(ask_claude, brainstorm_prompt):
    print("=== Temperature 1.0 — Run 1 ===")
    print(ask_claude(brainstorm_prompt, temperature=1.0))
    print()
    print("=== Temperature 1.0 — Run 2 (different ideas!) ===")
    print(ask_claude(brainstorm_prompt, temperature=1.0))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    **Quick reference:**

    | Task | Recommended temperature |
    |------|------------------------|
    | Data extraction, JSON output | 0.0 |
    | Paper summaries, analysis | 0.0 |
    | Grant writing first draft | 0.3 - 0.5 |
    | Brainstorming, hypothesis generation | 0.7 - 1.0 |
    | Experimental design ideas | 0.5 - 0.7 |

    Default to 0.0 and only increase when you want variety.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Putting it all together: technique combinations

    These techniques aren't mutually exclusive. The most powerful prompts combine several. Here's an example that uses role + chain-of-thought + output formatting + few-shot:
    """)
    return


@app.cell
def _(ask_claude):
    combined_system = """You are a medicinal chemist and protein engineer evaluating
    de novo binder candidates for ion channel targets. You think systematically
    about structure-activity relationships and developability."""

    combined_prompt = """Evaluate this binder candidate. Think through the assessment
    step by step, then provide a structured verdict.

    Candidate: DNB-Q23-v2
    Target: KCNQ2/3 (heteromeric opener site)
    Format: 62-residue de novo miniprotein, 3 disulfide bonds
    Binding: EC50 = 15 nM (KCNQ2/3 heteromer), no activity on KCNQ3 or KCNQ5 homomers
    Functional: Enhances M-current by 180% in HEK cells, 45% in DRG neurons
    Stability: Tm = 42 C, aggregation at > 10 uM
    In vivo: Not yet tested

    Assessment steps:
    1. Evaluate potency and selectivity
    2. Assess the HEK-to-DRG translation gap
    3. Evaluate developability (stability, aggregation)
    4. Consider the path to in vivo testing
    5. Prioritize what to fix first

    EXAMPLE OUTPUT FORMAT:
    ## Assessment
    [Step-by-step reasoning here]

    ## Verdict
    - Overall: [Advance / Optimize / Deprioritize]
    - Top issue: [single most important problem]
    - Recommended next experiments: [bulleted list]
    - Risk level: [Low / Medium / High] for [specific risk]
    """

    response_combined = ask_claude(combined_prompt, system_prompt=combined_system)
    print(response_combined)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Build a multi-step prompt chain for data extraction

    Here's a realistic abstract from a pain study. Build a **three-step prompt chain** that:

    1. **Step 1:** Extracts all quantitative data points from the abstract into a structured JSON format
    2. **Step 2:** Takes the JSON from step 1 and generates a plain-English summary suitable for a lab meeting slide
    3. **Step 3:** Takes the original abstract + the summary and identifies any claims NOT supported by the data shown

    Use whatever techniques from this notebook are appropriate for each step.
    """)
    return


@app.cell
def _():
    exercise_abstract = """
    Title: Dual-mechanism PROTAC targeting NaV1.8 for chronic neuropathic pain

    We report a bifunctional degrader (NPD-114) that simultaneously blocks NaV1.8 sodium
    current and induces channel degradation via the VHL E3 ligase pathway. In whole-cell
    patch clamp, NPD-114 inhibited NaV1.8 peak current with IC50 = 34 nM (n=12 cells).
    Western blot showed 73% protein reduction at 100 nM after 6h treatment in DRG cultures.
    The compound showed 28-fold selectivity over NaV1.7 and >100-fold over NaV1.5.
    In the spared nerve injury (SNI) model of neuropathic pain, intrathecal NPD-114
    (3 ug) reversed mechanical allodynia for 5 days (von Frey: 1.3 +/- 0.3g vs
    0.2 +/- 0.1g vehicle, p<0.001, n=10 per group). Duration of effect was 3-fold
    longer than the parent NaV1.8 blocker alone (NPB-22, same dose). No cardiac
    effects were detected by ECG monitoring. These results demonstrate that combining
    acute channel blockade with sustained degradation provides superior efficacy
    compared to either mechanism alone.
    """

    # STEP 1: Extract quantitative data into JSON
    # Hint: use temperature=0.0, ask for specific JSON fields, give an example if needed

    # step1 = ask_claude("""...""")  # TODO: write your prompt
    # print("=== Step 1: Data extraction ===")
    # print(step1)
    return


@app.cell
def _():
    # STEP 2: Generate a lab-meeting-ready summary from the extracted data
    # Hint: feed step1 output as context, use role prompting

    # step2 = ask_claude(f"""...{step1}...""")  # TODO: write your prompt
    # print("=== Step 2: Lab meeting summary ===")
    # print(step2)
    return


@app.cell
def _():
    # STEP 3: Critical evaluation — find unsupported claims
    # Hint: use chain-of-thought, ask Claude to compare claims to data

    # step3 = ask_claude(f"""...{exercise_abstract}...{step2}...""")  # TODO
    # print("=== Step 3: Critical evaluation ===")
    # print(step3)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## What you just learned

    - **Chain of thought** — guide Claude's reasoning with explicit steps; essential for interpretation tasks
    - **Few-shot examples** — show the format you want instead of describing it; the most reliable formatting technique
    - **Role prompting** — different expert roles notice different things; use this to stress-test your results
    - **Output formatting** — request JSON for code, markdown for humans; always specify structure explicitly
    - **Prompt chaining** — break complex tasks into steps where each feeds the next; review intermediates
    - **Temperature** — 0.0 for precision, higher for creativity; default to 0.0

    Next up: **03-prompts-for-research.py** — a library of ready-to-use prompt templates for the tasks you do every day.
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
    - 2026-03-25: QA pass — added missing `import json`; removed duplicate section cells for chain-of-thought, few-shot, and temperature
    - 2026-03-25: Added standardized callouts and decision frameworks
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **Chain-of-Thought Prompting** ([Wei et al., 2022](https://arxiv.org/abs/2201.11903)) — the paper that formalized "let's think step by step" prompting and demonstrated dramatic improvements on reasoning tasks
    - **Few-Shot Prompting** ([Brown et al., 2020](https://arxiv.org/abs/2005.14165)) — the GPT-3 paper that demonstrated how in-context examples enable LLMs to perform new tasks without fine-tuning
    - [Anthropic: Prompt Engineering Techniques](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Anthropic's official guide covering chain-of-thought, examples, role prompting, and output formatting
    - [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — worked code examples for prompt chaining, structured output, and tool use with the Claude API
    - [Anthropic docs: System Prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) — guidance on system prompt design for role prompting
    - [Anthropic API: Messages](https://docs.anthropic.com/en/api/messages) — API reference for `temperature`, `system`, and other parameters
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
    - 2026-03-25: QA pass — added missing `import json`; removed duplicate section cells for chain-of-thought, few-shot, and temperature
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

