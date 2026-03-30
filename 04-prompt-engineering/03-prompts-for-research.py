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
    # 03: Prompts for Research

    This notebook is your personal prompt library — battle-tested templates for the tasks you do every day. Each one is ready to use as-is or customize for your specific needs.

    We'll cover:
    1. Literature review and synthesis
    2. Grant writing assistance
    3. Data analysis planning
    4. Critical evaluation of arguments
    5. Building your own reusable prompt templates

    > **Requires:** `ANTHROPIC_API_KEY` set as an environment variable.
    >
    > **Key references:**
    > - [Anthropic's Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — also available as a local copy at `resources/references/anthropic-prompt-engineering-guide.md`
    > - [Anthropic Cookbook](https://github.com/anthropics/anthropic-cookbook) — worked examples of prompt patterns for the Claude API
    > - See `resources/references/external-links.md` for the full curated list of external references
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Techniques That Work](02-techniques-that-work.py) | [Module Index](../README.md) | [Next: Claude Code Basics \u2192](../05-mastering-claude-code/01-claude-code-basics.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Generic prompting advice ("be specific!") doesn't address research-specific challenges: maintaining scientific accuracy when summarizing across papers, extracting quantitative data without hallucinated numbers, or getting grant feedback that sounds like an actual study section reviewer.
    > - The prompt templates in this notebook are directly usable for your daily work — multi-paper synthesis for literature reviews, Specific Aims critique before submission, structured data extraction from abstracts, and troubleshooting experimental problems.
    > - A well-maintained prompt library saves hours per week. Instead of crafting a new prompt every time you need to summarize a paper or critique an experimental plan, you use a tested template and get reliable results immediately.
    > - The reviewer simulation technique lets you stress-test your grants and papers before submission — getting study-section-quality feedback on demand, from multiple expert perspectives, at any hour.
    """)
    return


@app.cell
def _():
    import anthropic
    import json
    from datetime import date
    client = anthropic.Anthropic()

    def ask_claude(user_prompt, system_prompt=None, model='claude-sonnet-4-20250514', max_tokens=2000, temperature=0.0):
        """Send a prompt to Claude and return the text response."""
        kwargs = {'model': model, 'max_tokens': max_tokens, 'temperature': temperature, 'messages': [{'role': 'user', 'content': user_prompt}]}
        if system_prompt:
            kwargs['system'] = system_prompt
        _response = client.messages.create(**kwargs)
        return _response.content[0].text
    LAB_SYSTEM_PROMPT = "You are a research assistant for a pain neuroscience lab.\nThe lab focuses on:\n- De novo protein binder design for NaV1.7, NaV1.8, and KCNQ2/3 ion channels\n- Targeted protein degradation (PROTACs, molecular glues)\n- DRG neuron electrophysiology and calcium imaging\n- Behavioral pain assays (von Frey, Hargreaves, formalin, CFA, SNI)\n- Single-cell and bulk RNA-seq of pain-related tissues\n\nThe PI's background: pain biology, ion channel pharmacology, protein engineering.\nThey read these outputs between experiments — be concise and lead with findings."
    # Your standing system prompt — reused across all templates
    print('Client ready. Lab system prompt loaded.')
    return LAB_SYSTEM_PROMPT, ask_claude, client


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ```mermaid
    graph TD
        subgraph "Research Workflow: Where Prompt Templates Fit"
            LIT["<b>Literature</b><br/>Multi-paper synthesis<br/>Daily research digest"] --> PLAN["<b>Planning</b><br/>Analysis plans<br/>Experimental design"]
            PLAN --> EXEC["<b>Execution</b><br/>Data extraction (JSON)<br/>Code generation"]
            EXEC --> EVAL["<b>Evaluation</b><br/>Critical analysis<br/>Reviewer simulation"]
            EVAL --> WRITE["<b>Writing</b><br/>Results paragraphs<br/>Grant sections"]
            WRITE --> REVIEW["<b>Review</b><br/>Specific Aims feedback<br/>Argument stress-testing"]
            REVIEW -.->|"iterate"| LIT
        end

        subgraph "Prompt Templates in This Notebook"
            T1["summarize_paper()"]
            T2["generate_research_digest()"]
            T3["analysis_plan_prompt"]
            T4["results_paragraph_prompt"]
            T5["critique_aim()"]
            T6["simulate_reviewer()"]
            T7["brainstorm()"]
        end

        LIT -.- T1
        LIT -.- T2
        PLAN -.- T3
        EXEC -.- T4
        EVAL -.- T6
        WRITE -.- T4
        REVIEW -.- T5
        PLAN -.- T7

        style LIT fill:#4488cc,color:#fff
        style PLAN fill:#44aa88,color:#fff
        style EXEC fill:#cc8844,color:#fff
        style EVAL fill:#aa44aa,color:#fff
        style WRITE fill:#cc4444,color:#fff
        style REVIEW fill:#448888,color:#fff
    ```

    Each stage of your research has corresponding prompt templates. The templates in this notebook are ready to use -- customize them with your specific data and context.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 🤔 **Decision point:** When should you use AI vs. do it yourself for each research task?
    >
    > | Research task | AI-assisted (Claude) | Do it yourself | Recommendation |
    > |--------------|---------------------|----------------|----------------|
    > | **Literature review** | Fast synthesis of 10+ papers, identifies themes, generates structured comparisons | You catch nuances AI misses, can assess methodology quality, know your field's debates | Use Claude for first-pass synthesis and structure, then add your expert judgment. Always verify citations. |
    > | **Writing** (grants, papers) | Excellent first drafts, consistent style, overcomes blank-page paralysis | Your scientific voice, original arguments, precise claims | Use Claude for drafts and editing. Write the core scientific arguments yourself. |
    > | **Data analysis** | Generates analysis code, suggests statistical approaches, creates visualizations | You understand your data's quirks, know what controls matter, catch biological implausibility | Use Claude to write the code, but you interpret the results. Never let AI make scientific conclusions from your data unsupervised. |
    > | **Experimental design** | Suggests controls you might miss, brainstorms alternative approaches, identifies confounds | You know your system, your equipment, your budget, what's actually feasible | Use Claude as a brainstorming partner and reviewer. The experimental decisions are yours. |
    > | **Citation lookup** | Can describe the general literature landscape | Cannot reliably generate specific, real citations | Never trust AI-generated citations without verification. Use PubMed for actual references. |

    > ⚠️ **Warning:** Never trust AI-generated citations without verification. This is the single most common and consequential error researchers make with LLMs. Claude will generate plausible-looking citations — correct-sounding author names, real journal names, reasonable years — that simply do not exist. Always look up every citation in PubMed or Google Scholar before including it in any document. A fabricated citation in a grant application or publication is a career-damaging mistake.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 1. Literature review and synthesis

    ### Template: Multi-paper synthesis

    The hardest part of literature review isn't summarizing one paper — it's synthesizing across several to find patterns, contradictions, and gaps. Here's a template for that.
    """)
    return


@app.cell
def _(LAB_SYSTEM_PROMPT, ask_claude):
    # Sample abstracts to synthesize (all authors and data below are fictional mock data)
    abstracts = {'Paper A (Researcher 1 et al. 2025)': '\n    Cryo-EM structure of human NaV1.7 bound to a peptide toxin ProTx-II at 2.8A\n    resolution reveals the toxin binds to the S3-S4 loop in voltage-sensing domain II\n    (VSD-II). The binding site overlaps with the aryl sulfonamide site but extends\n    further into the membrane-facing surface. Key interactions: R996 (salt bridge),\n    F960 (pi-stacking), and a hydrophobic pocket formed by L929, I932, V936.\n    ProTx-II traps VSD-II in the resting state, preventing S4 outward movement.\n    Mutagenesis of F960A reduced toxin potency 340-fold.\n    ', 'Paper B (Researcher 2 et al. 2025)': '\n    We solved the structure of NaV1.7 in complex with a clinical-stage inhibitor\n    (GX-936 analog) at 3.1A resolution. The compound binds in the central cavity\n    near the selectivity filter. Unexpectedly, we also observe a secondary binding\n    site at the DII-DIII intracellular linker, with electron density consistent\n    with a second inhibitor molecule. Mutations at the DII-DIII site (K1237A,\n    E1240A) reduced inhibition 5-fold, suggesting this site contributes to potency.\n    ', 'Paper C (Researcher 3 et al. 2025)': '\n    Hydrogen-deuterium exchange mass spectrometry (HDX-MS) of full-length NaV1.7\n    in lipid nanodiscs reveals that gain-of-function mutations (I848T, L858H)\n    increase solvent exposure in the DIII S4-S5 linker by 23-41%, consistent with\n    destabilization of the linker-pore domain interface. Binding of the selective\n    blocker PF-05089771 reduced exchange in both the VSD-II S3-S4 loop (28% reduction)\n    and the DIII S4-S5 linker (19% reduction), suggesting allosteric coupling between\n    these regions.\n    '}
    abstracts_text = '\n\n'.join((f'### {k}\n{v}' for k, v in abstracts.items()))
    synthesis_prompt = f"""Synthesize these three papers about NaV1.7 structure.\n\n{abstracts_text}\n\nProvide your synthesis in this format:\n\n**Convergent findings:** What do these papers agree on? What structural regions\nkeep appearing as important?\n\n**Contradictions or tensions:** Any findings that seem to conflict or require\nreconciliation?\n\n**Novel insight from combining these papers:** What can we conclude by reading\nthese together that we couldn't from any one alone?\n\n**Implications for our binder program:** Given that we design de novo protein\nbinders, what target sites or strategies do these papers collectively support?\nBe specific about which structural regions and why.\n\n**Key knowledge gap:** What's the most important unanswered question that would\nhelp our binder design?\n\nConstraints:\n- Cite which paper supports each claim (e.g., "Paper A")\n- Distinguish between structural data and functional inference\n- Total response under 500 words"""
    _response = ask_claude(synthesis_prompt, system_prompt=LAB_SYSTEM_PROMPT)
    print(_response)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Template: Daily research digest

    This template takes a batch of abstracts and produces a scannable digest you could read on your phone.
    """)
    return


@app.cell
def _(LAB_SYSTEM_PROMPT, ask_claude):
    def generate_research_digest(abstracts_dict, focus_areas=None):
        """Generate a daily research digest from a dictionary of {title: abstract} pairs."""
    
        if focus_areas is None:
            focus_areas = ["NaV1.7/NaV1.8 pharmacology", "protein binder design",
                           "targeted protein degradation", "pain mechanisms"]
    
        abstracts_text = "\n\n---\n\n".join(
            f"**{title}**\n{abstract}" for title, abstract in abstracts_dict.items()
        )
    
        prompt = f"""Create a research digest from these paper abstracts.

    {abstracts_text}

    Focus areas for relevance scoring: {', '.join(focus_areas)}

    For EACH paper, provide:
    1. **Relevance:** [High/Medium/Low] and one-phrase reason
    2. **One-liner:** Single sentence capturing the key finding
    3. **So what:** One sentence on why this matters for our lab
    4. **Key number:** The single most important quantitative result

    Then at the end:
    **Today's top takeaway:** One sentence synthesizing the most important insight
    across all papers.

    Sort papers by relevance (highest first). Be ruthlessly concise."""
    
        return ask_claude(prompt, system_prompt=LAB_SYSTEM_PROMPT)

    # Test it
    test_abstracts = {
        "Researcher 4 et al. — NaV1.7 splice variant in human nociceptors": """
        A novel splice variant of SCN9A expressed selectively in human peptidergic
        nociceptors produces a NaV1.7 channel with a 15-residue insertion in the
        DII-DIII linker. This variant shows a -7.2 mV shift in activation threshold
        and 2.3-fold slower inactivation compared to the canonical isoform.
        Single-cell RNA-seq confirms this variant represents 34% of SCN9A transcripts
        in human DRG nociceptors but is absent from mouse.
        """,
        "Researcher 5 et al. — Oral PROTAC for TRPV1": """
        We developed an orally bioavailable PROTAC (TVD-301) targeting TRPV1 via
        recruitment of cereblon. TVD-301 achieved 82% TRPV1 degradation in DRG
        cultures (DC50 = 45 nM) and reversed CFA-induced thermal hyperalgesia
        for 48h after single oral dose (30 mg/kg) in rats.
        """,
        "Researcher 6 et al. — KCNQ2 structure with opener bound": """
        Cryo-EM structure of KCNQ2 at 2.6A resolution with the opener retigabine
        bound reveals the drug occupies a fenestration between S5 and S6 helices.
        The binding pocket is lined by W236, L243, L299, and F305. Molecular dynamics
        simulations show retigabine stabilizes the open state by 2.8 kcal/mol.
        """,
        "Researcher 7 et al. — Machine learning for pain biomarkers": """
        Random forest classifier trained on DRG single-cell RNA-seq from 200 patients
        identifies a 12-gene signature that predicts chronic pain persistence with
        AUC = 0.89. Top features: SCN10A, KCNQ2, CALCA, ATF3, BDNF. The model
        generalizes across inflammatory and neuropathic pain subtypes.
        """
    }

    digest = generate_research_digest(test_abstracts)
    print(digest)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 2. Grant writing assistance

    ### Template: Specific Aims feedback

    This template gives you structured, actionable feedback on a Specific Aims page draft.
    """)
    return


@app.cell
def _(ask_claude):
    # A draft Specific Aims page (abbreviated for the tutorial)
    specific_aims_draft = """
    SPECIFIC AIMS

    Chronic pain affects over 50 million Americans and current treatments are inadequate.
    NaV1.7 is a genetically validated pain target — loss-of-function mutations cause
    congenital insensitivity to pain while gain-of-function mutations cause inherited
    pain disorders. Despite extensive drug development efforts, no NaV1.7-selective
    small molecule has achieved clinical efficacy, likely because achieving sufficient
    selectivity over cardiac NaV1.5 remains challenging.

    We propose a fundamentally different approach: de novo protein binders that achieve
    NaV1.7 selectivity through large, shape-complementary binding interfaces, combined
    with targeted protein degradation to provide sustained efficacy. Our preliminary
    data demonstrate that computationally designed miniproteins can selectively bind
    NaV1.7 with single-digit nanomolar affinity and >50-fold selectivity.

    Aim 1: Design and optimize NaV1.7-selective de novo protein binders targeting the
    VSD-II S3-S4 loop.
    We will use RFdiffusion and ProteinMPNN to generate binder candidates, screen by
    yeast surface display, and validate by electrophysiology in HEK cells and DRG neurons.

    Aim 2: Convert lead binders into bifunctional degraders (protein PROTACs) by
    fusion to E3 ligase-recruiting domains.
    We will fuse binders to VHL and CRBN-recruiting miniproteins, measure degradation
    kinetics in DRG cultures, and assess selectivity.

    Aim 3: Evaluate lead degraders in preclinical pain models.
    We will test efficacy in CFA (inflammatory) and SNI (neuropathic) models via
    intrathecal delivery, measuring behavioral outcomes and NaV1.7 protein levels.
    """

    aims_feedback = ask_claude(f"""
    Review this Specific Aims page draft as an NIH study section reviewer.

    {specific_aims_draft}

    Provide feedback in this format:

    **Overall impression:** [2-3 sentences on the core idea and its significance]

    **Strengths (what an enthusiastic reviewer would highlight):**
    - [bullet points]

    **Weaknesses (what a skeptical reviewer would question):**
    - [bullet points, each with a specific concern and why it matters]

    **Missing elements:**
    - [What a reviewer would expect to see that isn't here]

    **Specific suggestions:**
    For each Aim, provide one concrete improvement.

    **The "killer question" a reviewer will ask:** [The single hardest question
    this proposal will face in study section, and a suggested counter-argument]

    Be tough but constructive. Think like a seasoned R01 reviewer.""",
        system_prompt="""You are an experienced NIH study section reviewer with expertise
        in ion channel pharmacology, protein engineering, and pain neuroscience. You have
        reviewed hundreds of R01 applications and have a reputation for fair but rigorous
        critiques. You focus on scientific rigor, feasibility, and innovation."""
    )

    print(aims_feedback)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Template: Significance section draft

    This generates a first-pass Significance section that you can then edit with your own voice.
    """)
    return


@app.cell
def _(ask_claude):
    significance_prompt = """
    Write a first draft of the Significance section for an R01 proposal on de novo
    protein binders as NaV1.7-targeted degraders for chronic pain.

    Key points to cover:
    - Burden of chronic pain and limitations of current analgesics
    - Genetic validation of NaV1.7 as a pain target
    - Why small molecule approaches have struggled (selectivity)
    - Why protein binders offer a structural solution to the selectivity problem
    - Why degradation may be superior to inhibition for sustained efficacy
    - Innovation: combining de novo protein design with targeted degradation

    Constraints:
    - 1 page, single-spaced (approximately 500 words)
    - NIH grant style: authoritative, evidence-based, no hype
    - Cite evidence by description (e.g., "Loss-of-function mutations in SCN9A..."),
      not by author/year — I'll add the real citations later
    - Each paragraph should make one clear argument
    - End with a sentence that transitions to the Innovation section
    """

    significance = ask_claude(significance_prompt,
        system_prompt="""You are a grant writer with deep expertise in pain neuroscience
        and protein therapeutics. Write in a clear, confident style appropriate for
        an NIH R01 application. Avoid jargon when simpler language works.""",
        temperature=0.3  # Slight creativity for writing, but still grounded
    )

    print(significance)
    print(f"\n[Word count: {len(significance.split())}]")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 3. Data analysis prompts

    ### Template: Dataset description to analysis plan
    """)
    return


@app.cell
def _(LAB_SYSTEM_PROMPT, ask_claude):
    analysis_plan_prompt = """
    I have the following dataset. Propose a complete analysis plan.

    Dataset: Calcium imaging of DRG neurons treated with binder candidates

    Variables per neuron:
    - neuron_id: unique identifier
    - diameter_um: cell body diameter
    - ib4_positive: boolean (IB4 staining for non-peptidergic nociceptors)
    - cgrp_positive: boolean (CGRP staining for peptidergic nociceptors)
    - treatment: one of ["vehicle", "DNB-001_10nM", "DNB-001_100nM", "DNB-001_1uM"]
    - baseline_f340_380: Fura-2 ratio at baseline (average of 60s)
    - peak_f340_380: peak Fura-2 ratio after 50mM KCl stimulation
    - delta_f: peak minus baseline
    - time_to_peak_s: seconds from KCl application to peak
    - decay_tau_s: exponential decay time constant
    - n_spontaneous_events: number of spontaneous calcium transients in 5min baseline

    Total: ~800 neurons across 4 treatment groups, from 6 mice (3M, 3F)

    Provide:
    1. **QC checks:** What to look for before analysis
    2. **Primary analysis:** The main statistical test for "does the binder reduce
       calcium transients?" with justification for the test choice
    3. **Secondary analyses:** Dose-response, cell-type effects, sex differences
    4. **Visualization plan:** What plots to make and why
    5. **Pitfalls:** Common mistakes to avoid with this type of data

    Be specific about statistical tests and parameters. Assume I'll implement this
    in Python with scipy, statsmodels, and seaborn."""

    analysis_plan = ask_claude(analysis_plan_prompt, system_prompt=LAB_SYSTEM_PROMPT)
    print(analysis_plan)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Template: Results paragraph from data summary

    When you have the numbers and need to turn them into a results paragraph for a paper.
    """)
    return


@app.cell
def _(LAB_SYSTEM_PROMPT, ask_claude):
    results_prompt = """
    Write a Results paragraph from these data. This is for a research paper, not a grant.

    Experiment: Effect of DNB-001 on KCl-evoked calcium transients in mouse DRG neurons

    Data summary:
    - Vehicle (n=203 neurons): delta_F = 0.82 +/- 0.04 (mean +/- SEM)
    - DNB-001 10 nM (n=198): delta_F = 0.71 +/- 0.05 (p=0.08 vs vehicle, mixed-effects model)
    - DNB-001 100 nM (n=211): delta_F = 0.48 +/- 0.03 (p<0.001 vs vehicle)
    - DNB-001 1 uM (n=189): delta_F = 0.31 +/- 0.04 (p<0.001 vs vehicle)
    - Hill fit EC50 = 72 nM (95% CI: 48-108 nM), Hill coefficient = 1.1
    - Effect was selective for small-diameter neurons (<25 um): 52% inhibition at 100 nM
      vs 18% in large-diameter neurons (>35 um), p<0.01 for interaction
    - No sex difference detected (p=0.67 for treatment x sex interaction)

    Constraints:
    - One paragraph, approximately 150 words
    - Report exact statistics (p values, confidence intervals)
    - Scientific paper style — precise, measured, no hyperbole
    - Reference figure panels in parentheses (e.g., "Fig. 2A")
      — use Fig. 2A for dose-response curve, 2B for small vs large diameter comparison
    - Do NOT interpret the results — just report them"""

    results_paragraph = ask_claude(results_prompt, system_prompt=LAB_SYSTEM_PROMPT,
                                    temperature=0.0)
    print(results_paragraph)
    print(f"\n[Word count: {len(results_paragraph.split())}]")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 4. Critical evaluation

    ### Template: Find weaknesses in an argument

    This is one of the most valuable uses of Claude — having a rigorous interlocutor who will push back on your reasoning.
    """)
    return


@app.cell
def _(ask_claude):
    argument_to_evaluate = """
    We propose that NaV1.7-targeted protein degraders will be superior to NaV1.7
    inhibitors for chronic pain because:

    1. Degradation provides sustained efficacy beyond the compound's half-life,
       since the cell must re-synthesize the channel protein
    2. Complete elimination of the protein removes both conducting and non-conducting
       functions of NaV1.7 (the channel may have scaffolding roles)
    3. Protein binders can achieve selectivity through shape complementarity that
       small molecules cannot, solving the NaV1.5 selectivity problem
    4. Unlike gene therapy, degradation is reversible — stopping dosing allows
       channel levels to recover, providing a safety valve
    5. Our preliminary data show that intrathecal delivery of our lead degrader
       reverses pain behavior for 5 days vs 8 hours for the parent blocker
    """

    critique = ask_claude(f"""
    Critically evaluate this argument. For each point, do three things:

    1. **Steel-man it:** State the strongest version of the argument
    2. **Attack it:** What's the most compelling counterargument or weakness?
    3. **What data would resolve it:** What experiment or evidence would
       determine who's right?

    Then provide an overall assessment: is the core thesis sound even if
    individual points have weaknesses?

    The argument:
    {argument_to_evaluate}""",
        system_prompt="""You are a rigorous scientist who excels at finding logical
        gaps and unstated assumptions. You are fair — you acknowledge strong points
        before attacking weak ones. You focus on scientific substance, not style."""
    )

    print(critique)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Template: Reviewer simulation

    Before submitting a paper or grant, simulate the toughest reviewer.
    """)
    return


@app.cell
def _(ask_claude):
    def simulate_reviewer(text, reviewer_type="tough_but_fair"):
        """Simulate a peer reviewer's response to a manuscript section."""
    
        reviewer_personas = {
            "tough_but_fair": """You are Reviewer 2 — thorough, skeptical, but ultimately
                fair. You focus on experimental rigor and alternative explanations.
                You write detailed critiques with specific suggestions.""",
            "methods_focused": """You are a reviewer obsessed with methodological
                rigor. You focus on sample sizes, controls, statistical tests, and
                reproducibility. You want to see power analyses and effect sizes.""",
            "big_picture": """You are a senior reviewer who focuses on significance
                and novelty. You ask "so what?" and "how does this advance the field?"
                You care less about methods details and more about the story."""
        }
    
        prompt = f"""Review this text as if you're reviewing it for a top-tier
    neuroscience journal (e.g., Neuron, Nature Neuroscience).

    {text}

    Provide your review in standard journal format:

    **Major concerns** (issues that must be addressed):
    1. [numbered, each with rationale]

    **Minor concerns:**
    1. [numbered]

    **Questions for the authors:**
    - [specific questions]

    **Missing experiments or controls:**
    - [what you'd want to see]

    **Overall recommendation:** [Accept / Minor revisions / Major revisions / Reject]
    and one-sentence justification."""
    
        return ask_claude(prompt, system_prompt=reviewer_personas.get(reviewer_type, reviewer_personas["tough_but_fair"]))

    # Test it with a methods-focused reviewer
    test_text = """
    We tested our NaV1.7 degrader (DNB-PROTAC-7) in the CFA model of inflammatory pain.
    Mice received intrathecal injections of DNB-PROTAC-7 (10 ug) or vehicle 24 hours
    after CFA injection into the left hindpaw. Thermal withdrawal latencies were
    measured using the Hargreaves apparatus at 2, 24, 48, 72, and 96 hours
    post-treatment. DNB-PROTAC-7 fully reversed thermal hyperalgesia by 24 hours
    post-treatment and the effect persisted for 72 hours (p<0.001, two-way ANOVA
    with Bonferroni correction). Western blot of ipsilateral L3-L5 DRG confirmed
    NaV1.7 protein reduction of 81% at 48 hours.
    """

    review = simulate_reviewer(test_text, "methods_focused")
    print(review)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > 💡 **Tip:** Build a personal prompt template library. The most effective prompt engineers don't write new prompts from scratch — they maintain a library of tested templates and adapt them. The `PromptLibrary` class below is a starting point. Every time you craft a prompt that works well, save it as a function with clear parameters. After a few weeks, you'll have a toolkit that handles 80% of your research tasks with minimal effort.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## 5. Building your prompt template library

    The most effective prompt engineers don't write new prompts from scratch every time — they maintain a library of tested templates that they customize.

    Here's a pattern for creating reusable, parameterized templates.
    """)
    return


@app.cell
def _(LAB_SYSTEM_PROMPT, client):
    # A template library — each template is a function with clear parameters
    class PromptLibrary:
        """A collection of reusable prompt templates for pain research."""

        def __init__(self, client, system_prompt=None):
            self.client = client
            self.system_prompt = system_prompt or LAB_SYSTEM_PROMPT

        def _ask(self, prompt, system=None, temperature=0.0, max_tokens=1500):
            kwargs = {'model': 'claude-sonnet-4-20250514', 'max_tokens': max_tokens, 'temperature': temperature, 'messages': [{'role': 'user', 'content': prompt}]}
            sys = system or self.system_prompt
            if sys:
                kwargs['system'] = sys
            _response = self.client.messages.create(**kwargs)
            return _response.content[0].text

        def summarize_paper(self, abstract, focus='general'):
            """One-page summary of a paper abstract."""
            focus_instructions = {'general': 'Provide a balanced summary of all findings.', 'binder_design': 'Focus on structural insights and target sites relevant to protein binder design.', 'degradation': 'Focus on findings relevant to targeted protein degradation strategies.', 'clinical': 'Focus on translational potential and clinical implications.'}
            return self._ask(f'Summarize this paper abstract.\n\n{abstract}\n\nFocus: {focus_instructions.get(focus, focus)}\n\nFormat:\n- **One-liner:** [key finding in one sentence]\n- **What they did:** [2-3 sentences]\n- **Key results:** [bullet points with numbers]\n- **Why it matters for us:** [1-2 sentences]')

        def compare_compounds(self, compounds_text):
            """Compare binder/drug candidates and recommend which to advance."""
            return self._ask(f'Compare these compounds and recommend a path forward.\n\n{compounds_text}\n\nFor each compound, evaluate: potency, selectivity, stability, and any red flags.\n\nProvide a ranked recommendation with clear rationale. Identify the top candidate\nand what its biggest remaining risk is.\n\nFormat as a markdown table followed by a 3-sentence recommendation.')

        def critique_aim(self, aim_text):
            """Get study-section-style feedback on a Specific Aim."""
            return self._ask(f'Critique this Specific Aim as an NIH reviewer.\n\n{aim_text}\n\nProvide:\n- Top 3 strengths\n- Top 3 weaknesses (with specific suggestions to fix each)\n- The hardest question a reviewer will ask\n- Suggested rewrite of the Aim statement (one sentence) if you think it can be stronger', system='You are a veteran NIH study section reviewer in pain and\n            neuroscience with 15 years of review experience.')

        def experimental_troubleshoot(self, problem_description):
            """Troubleshoot an experimental problem."""
            return self._ask(f"Help me troubleshoot this experimental problem.\n\n{problem_description}\n\nThink through this step by step:\n1. What are the most likely causes? (rank by probability)\n2. For each cause, what diagnostic experiment would confirm it?\n3. What's the quickest fix to try first?\n4. What controls should I add to rule out artifacts?\n\nBe specific to the techniques mentioned.")

        def brainstorm(self, topic, n_ideas=5):
            """Generate research ideas with higher temperature."""
            return self._ask(f'Brainstorm {n_ideas} creative but scientifically\ngrounded ideas for: {topic}\n\nFor each idea:\n- One-sentence description\n- Why it might work (scientific rationale)\n- Biggest risk or unknown\n- How to test it quickly (cheapest experiment)\n\nAim for a mix of safe bets and moonshots.', temperature=0.8)
    prompts = PromptLibrary(client)
    print('Prompt library loaded with templates:')
    print("  prompts.summarize_paper(abstract, focus='binder_design')")
    print('  prompts.compare_compounds(compounds_text)')
    print('  prompts.critique_aim(aim_text)')
    print('  prompts.experimental_troubleshoot(problem)')
    # Create your library instance
    print('  prompts.brainstorm(topic, n_ideas=5)')
    return (prompts,)


@app.cell
def _(prompts):
    # Try it out: troubleshoot an experimental problem
    _response = prompts.experimental_troubleshoot("\nProblem: My calcium imaging experiment with Fura-2 in DRG neurons is showing\nvery high baseline fluorescence ratios (F340/F380 > 1.5) before any stimulation.\nNormally baseline should be ~0.3-0.5. This is happening in all wells, including\nvehicle controls. The neurons look healthy under brightfield. I'm using the same\nFura-2 AM lot as last month when things worked fine. The only thing that changed\nis we got a new batch of poly-D-lysine coated coverslips.\n")
    print(_response)
    return


@app.cell
def _(prompts):
    # Try brainstorming
    _response = prompts.brainstorm('New approaches to deliver our NaV1.7 protein binder-PROTAC to DRG neurons without intrathecal injection')
    print(_response)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Create your own prompt template

    Think about a task you do regularly — something you've already been using Claude for, or wish you could automate. Build a template for it.

    Some ideas:
    - **Journal club prep:** Given an abstract, generate discussion questions and key figures to focus on
    - **Experiment planner:** Given a hypothesis, generate a complete experimental plan with controls
    - **Bioinformatics translator:** Convert an analysis description into a step-by-step Python/R code plan
    - **Collaboration email:** Draft a clear, professional email proposing a collaboration based on a shared interest

    Add your template as a new method on the `PromptLibrary` class, or just write it as a standalone function.
    """)
    return


@app.cell
def _():
    # YOUR TEMPLATE HERE
    #
    # def my_template(input_text):
    #     """Describe what this template does."""
    #     prompt = f"""
    #     [Your carefully crafted prompt here]
    #     
    #     {input_text}
    #     """
    #     return ask_claude(prompt, system_prompt=LAB_SYSTEM_PROMPT)
    #
    # # Test it:
    # result = my_template("your test input")
    # print(result)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Improve the daily digest template

    Take the `generate_research_digest` function from earlier in this notebook and improve it:

    1. Add a parameter for `output_style` ("quick_scan" for phone reading, "detailed" for lab meeting, "email" for sharing with collaborators)
    2. Add a "connections" section that identifies links between papers (shared targets, complementary methods, etc.)
    3. Add an "action items" section that suggests concrete follow-ups for your lab

    Test your improved version on the sample abstracts above.
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

    - [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) — Anthropic's comprehensive guide to prompt design; also available locally at `resources/references/anthropic-prompt-engineering-guide.md`
    - [Anthropic Cookbook — Prompt Engineering](https://github.com/anthropics/anthropic-cookbook/tree/main/misc/prompt_engineering) — worked code examples showing prompt chaining, structured output, and real-world patterns
    - [Anthropic Cookbook — Full Repository](https://github.com/anthropics/anthropic-cookbook) — the complete collection of examples including tool use, embeddings, and multimodal prompts
    - [Anthropic docs: System Prompts](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/system-prompts) — best practices for system prompt design
    - [Full External Links Reference](../resources/references/external-links.md) — the curated master list of all external resources referenced across this tutorial
    - **Chain-of-Thought Prompting** ([Wei et al., 2022](https://arxiv.org/abs/2201.11903)) — the technique used in the critical evaluation and prompt chaining templates
    - **Few-Shot Prompting** ([Brown et al., 2020](https://arxiv.org/abs/2005.14165)) — the technique behind the `summarize_paper()` and data extraction templates
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
    - 2026-03-25: QA pass — removed duplicate 'What you just learned' and embedded Further Reading sections
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

