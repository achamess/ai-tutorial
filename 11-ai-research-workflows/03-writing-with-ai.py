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
    # 03: AI-Assisted Scientific Writing

    ## Why this matters

    You spend a huge fraction of your research life writing — grants, papers, reviews, emails to collaborators. AI can help at every stage, but only if you use it the right way.

    This notebook covers:
    1. **Grant writing:** generating first drafts of specific aims and significance sections
    2. **Revision workflows:** improving clarity, flow, and logic
    3. **The structured approach:** outline → draft → revise → polish
    4. **Prompt templates** for common writing tasks
    5. **Style matching:** teaching Claude your writing voice
    6. **Ethics and attribution:** what to use AI for and what to write yourself

    > **Prerequisites:** Claude API basics from Module 05. The prompt engineering principles from Module 03 are essential here — this is where they get their biggest payoff. See also the [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) for techniques directly applicable to writing tasks.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: AI-Assisted Data Analysis Pipeline](02-data-analysis-pipeline.py) | [Module Index](../README.md) | [Next: Models and Providers \u2192](../12-ai-landscape/01-models-and-providers.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Grant writing is high-stakes and time-consuming -- an R01 Specific Aims page can take days to draft from scratch. AI-assisted writing doesn't replace your scientific judgment, but it eliminates blank-page paralysis and accelerates the mechanical parts (first drafts, clarity editing, formatting).
    > - You're writing for multiple audiences simultaneously: NIH study sections, journal reviewers, collaborator emails, and lab presentations. The audience adaptation techniques here let you repurpose the same content efficiently instead of rewriting from scratch each time.
    > - The iterative refinement workflow (outline, draft, revise with specific feedback, polish) mirrors how you'd work with a human writing collaborator -- but it's available at 11 PM the night before a deadline.
    > - Your competitive advantage as a researcher depends on communicating your binder design work clearly to reviewers who may not know protein engineering. These tools help bridge that gap.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Setup
    """)
    return


@app.cell
def _():
    import anthropic
    from IPython.display import display, Markdown
    import textwrap
    client = anthropic.Anthropic()
    MODEL = 'claude-sonnet-4-6'

    def show(text):
        """Display text as formatted Markdown."""
        display(Markdown(text))

    def ask_claude(prompt, system=None, max_tokens=2000):
        """Simple wrapper for Claude API calls."""
        kwargs = {'model': MODEL, 'max_tokens': max_tokens, 'messages': [{'role': 'user', 'content': prompt}]}
        if system:
            kwargs['system'] = system
        _response = client.messages.create(**kwargs)
        return _response.content[0].text
    print(f'Using model: {MODEL}')
    print('Ready.')
    return MODEL, ask_claude, client, show


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 1: The structured writing approach

    The worst way to use AI for writing: paste nothing and say "write me a grant about NaV1.7."

    The best way: **outline → draft → revise → polish**, with you steering at every step.

    ```
    You (the expert)          Claude (the writing assistant)
    ──────────────            ─────────────────────────────
    Define the argument  →    Generate a structured outline
    Approve/edit outline →    Draft each section
    Check facts & logic  →    Revise for clarity & flow
    Final review         →    Polish language
    ```

    You keep scientific ownership. Claude handles the blank-page problem and language polish.

    > 💡 **Tip:** Think of AI as your editor, not your author. The scientific ideas, arguments, and claims must come from you. Claude excels at turning rough notes into polished prose, restructuring paragraphs for flow, and adapting content for different audiences — tasks where the intellectual content is already defined and you need help with execution.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### The structured writing workflow

    """),
    mo.mermaid(
        """
        flowchart TD
            subgraph OUTLINE["1. OUTLINE"]
                direction TB
                O1["YOU: Define argument,<br>aims, key claims"]
                O2["CLAUDE: Generate<br>structured outline"]
                O1 --> O2
            end
        
            subgraph DRAFT["2. DRAFT"]
                direction TB
                D1["YOU: Approve/edit<br>outline"]
                D2["CLAUDE: Write<br>each section"]
                D1 --> D2
            end
        
            subgraph REVISE["3. REVISE"]
                direction TB
                R1["YOU: Check facts,<br>logic, emphasis"]
                R2["CLAUDE: Revise for<br>clarity & flow"]
                R1 --> R2
                R2 -->|"iterate 2-3x"| R1
            end
        
            subgraph POLISH["4. POLISH"]
                direction TB
                P1["CLAUDE: Tighten<br>language, hit<br>word count"]
                P2["YOU: Final review,<br>add citations,<br>verify claims"]
                P1 --> P2
            end
        
            OUTLINE --> DRAFT
            DRAFT --> REVISE
            REVISE --> POLISH
        
            style O1 fill:#e74c3c,color:#fff
            style O2 fill:#8e44ad,color:#fff
            style D1 fill:#e74c3c,color:#fff
            style D2 fill:#8e44ad,color:#fff
            style R1 fill:#e74c3c,color:#fff
            style R2 fill:#8e44ad,color:#fff
            style P1 fill:#8e44ad,color:#fff
            style P2 fill:#e74c3c,color:#fff
        """
    ),
    mo.md(r"""

    **Legend:** Red = you (the scientist). Purple = Claude. You own the science at every step; Claude handles the blank-page problem and language polish.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 2: Grant writing — Specific Aims

    Let's walk through generating a Specific Aims page for an R01. This is arguably the most important page in any NIH grant.

    ### Step 1: Define your project in structured notes

    Before touching the API, write down the key elements. This is your scientific input — the part AI cannot provide.
    """)
    return


@app.cell
def _():
    # Your project definition — this is YOUR scientific thinking
    project = {
        "title": "De novo protein binders for selective degradation of pain-related sodium channels",
    
        "long_term_goal": (
            "Develop a new class of pain therapeutics based on targeted protein degradation "
            "of voltage-gated sodium channels in nociceptive DRG neurons."
        ),
    
        "problem": (
            "NaV1.7 and NaV1.8 are genetically validated pain targets, but small-molecule "
            "inhibitors have failed in clinical trials due to insufficient subtype selectivity. "
            "Blocking channel conductance requires sustained receptor occupancy, leading to "
            "off-target effects on cardiac NaV1.5."
        ),
    
        "innovation": (
            "Instead of blocking channels, we will degrade them using de novo protein binders "
            "conjugated to E3 ligase recruiters (PROTAC approach). Computational design via "
            "RFdiffusion enables binders with programmable selectivity. Degradation is catalytic, "
            "requiring lower doses than occupancy-based inhibitors."
        ),
    
        "aims": [
            {
                "number": 1,
                "title": "Design and validate de novo protein binders for NaV1.7 and NaV1.8",
                "approach": "RFdiffusion design, AlphaFold2 filtering, SPR binding validation, selectivity panel",
                "key_milestone": "3+ binders per target with Kd < 10 nM and >100x selectivity over NaV1.5"
            },
            {
                "number": 2,
                "title": "Engineer binder-PROTAC conjugates for targeted NaV degradation in DRG neurons",
                "approach": "CRBN and VHL E3 ligase recruiters, DC50 optimization, degradation kinetics in cultured DRG neurons, calcium imaging to confirm functional knockdown",
                "key_milestone": "DC50 < 50 nM with >80% target degradation at 24h"
            },
            {
                "number": 3,
                "title": "Evaluate analgesic efficacy in preclinical pain models",
                "approach": "CFA inflammatory and SNI neuropathic models, behavioral assays (von Frey, Hargreaves, conditioned place preference), pharmacokinetics",
                "key_milestone": "Significant reversal of mechanical allodynia with no cardiac or motor side effects"
            }
        ],
    
        "significance": (
            "Chronic pain affects 50 million Americans. Current treatments (opioids, gabapentinoids) "
            "have serious side effects. A selective, long-acting approach to silence pain-specific "
            "sodium channels could transform pain management."
        )
    }

    print("Project definition ready.")
    print(f"Title: {project['title']}")
    print(f"Number of aims: {len(project['aims'])}")
    return (project,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Step 2: Generate the outline
    """)
    return


@app.cell
def _(ask_claude, project, show):
    outline_prompt = f"""I'm writing an NIH R01 Specific Aims page. Generate a detailed outline \n(not prose) with the standard structure:\n\n1. Opening paragraph (hook + problem + gap)\n2. "The long-term goal... the objective... the central hypothesis... the rationale..."\n3. Specific Aim 1, 2, 3 (one sentence each with hypothesis and approach)\n4. Closing impact statement\n\nUse ONLY the information I provide below. Do not invent claims or citations.\n\nProject information:\n- Title: {project['title']}\n- Problem: {project['problem']}\n- Innovation: {project['innovation']}\n- Long-term goal: {project['long_term_goal']}\n- Significance: {project['significance']}\n\nAims:\n"""
    for _aim in project['aims']:
        outline_prompt += f"- Aim {_aim['number']}: {_aim['title']}\n  Approach: {_aim['approach']}\n  Milestone: {_aim['key_milestone']}\n"
    outline = ask_claude(outline_prompt)
    show(outline)
    return (outline,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Review the outline. Does the logic flow? Are the aims properly scoped? Edit the `project` dictionary above and re-run if needed.

    ### Step 3: Draft the full Specific Aims page
    """)
    return


@app.cell
def _(ask_claude, outline, project, show):
    draft_prompt = f"""Write a complete NIH R01 Specific Aims page (1 page, approximately 500 words) \nbased on this outline and project information.\n\nRequirements:\n- Formal scientific writing style, appropriate for NIH review\n- Start with a compelling opening sentence about the clinical problem\n- Include the standard R01 framing: long-term goal, objective, central hypothesis, rationale\n- Each aim gets 2-3 sentences: hypothesis, approach, expected outcome\n- End with a strong impact statement\n- Do NOT invent specific citations — use phrases like "recent studies have shown" or \n  "genetic evidence demonstrates" where you'd normally cite\n- Do NOT use bullet points in the body — this should be flowing prose with bold aim titles\n\nOutline:\n{outline}\n\nProject details:\n- Title: {project['title']}\n- Problem: {project['problem']}\n- Innovation: {project['innovation']}\n- Long-term goal: {project['long_term_goal']}\n- Significance: {project['significance']}\n"""
    for _aim in project['aims']:
        draft_prompt += f"\n- Aim {_aim['number']}: {_aim['title']}\n  Approach: {_aim['approach']}\n  Milestone: {_aim['key_milestone']}"
    draft = ask_claude(draft_prompt, max_tokens=2000)
    show(draft)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    That's a first draft. It's not final — you'll need to:
    - Verify every scientific claim
    - Add real citations
    - Adjust emphasis based on reviewer panel
    - Make sure it fits on one page

    But you're editing, not staring at a blank page. That's the value.

    > ⚠️ **Warning: AI writing ethics — disclosure requirements.** Major funders and journals now have explicit policies on AI-assisted writing:
    > - **NIH:** AI tools may be used to assist with writing grant applications, but the PI is responsible for all content. AI tools must not be used in peer review. [NIH FAQ on AI](https://grants.nih.gov/faqs#/use-of-generative-ai-in-peer-review.htm)
    > - **Nature:** Authors must disclose AI use in the Methods or Acknowledgments section. AI tools cannot be listed as authors. [Nature AI policy](https://www.nature.com/nature-portfolio/editorial-policies/ai)
    > - **Science:** Similar to Nature — disclosure required, AI cannot be an author, authors take responsibility for AI-assisted content. [Science editorial policies](https://www.science.org/content/page/science-journals-editorial-policies)
    >
    > **Bottom line:** Using AI for writing is fine and increasingly common. Not disclosing it is an ethics violation. When in doubt, add a sentence to your Methods: "Claude (Anthropic) was used to assist with drafting and editing text. All scientific content was generated and verified by the authors."

    > 🤔 **Decision point: What to use AI for vs write yourself**
    >
    > | Writing task | Use AI? | Why |
    > |-------------|---------|-----|
    > | **First drafts** from detailed notes | Yes | Eliminates blank-page paralysis, fast iteration |
    > | **Editing** for clarity and flow | Yes | AI catches wordiness, passive voice, logical gaps |
    > | **Formatting** (references, tables, figure legends) | Yes | Mechanical work, AI is fast and accurate |
    > | **Adapting** for different audiences | Yes | Efficient repurposing of content |
    > | **Scientific claims and arguments** | **No** | Must come from your expertise and data |
    > | **Interpreting your own results** | **No** | You know the caveats, limitations, and context |
    > | **Citation selection** | **No** | AI may hallucinate citations or miss key papers |
    > | **Novel ideas and hypotheses** | **No** | This is your intellectual contribution |
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 3: Improving existing text

    Often you have a rough paragraph and need Claude to improve it. This is where AI writing assistance shines — revision is less risky than generation because you're starting from your own ideas.

    ### The revision prompt template
    """)
    return


@app.cell
def _():
    # A rough paragraph you might write quickly in Obsidian
    rough_paragraph = """\
    Nav1.7 is really important for pain. People who don't have it can't feel pain 
    at all which is why pharma has been trying to make drugs that block it. But the 
    drugs haven't worked well in clinical trials, probably because they also hit other 
    sodium channels especially the heart one Nav1.5. Our idea is instead of just 
    blocking the channel we want to completely get rid of it using PROTACs. We use 
    RFdiffusion to design protein binders that specifically grab Nav1.7 and then attach 
    a thing that recruits the cell's own protein disposal system. This should work 
    better than regular drugs because you only need a little bit of the PROTAC since 
    it works catalytically.
    """

    print("Rough paragraph:")
    print(rough_paragraph)
    return (rough_paragraph,)


@app.cell
def _(ask_claude, rough_paragraph, show):
    revision_prompt = f"""\
    Revise this paragraph for an NIH R01 Significance section. 

    Instructions:
    - Maintain the same scientific content and argument structure
    - Improve to formal scientific writing style
    - Fix any vague language ("really important" → specific claim)
    - Ensure logical flow between sentences
    - Keep roughly the same length (don't pad it)
    - Use proper gene/protein nomenclature (NaV1.7, SCN9A, etc.)

    Return ONLY the revised paragraph, no commentary.

    Original:
    {rough_paragraph}"""

    revised = ask_claude(revision_prompt)
    show("### Revised:\n\n" + revised)
    return (revised,)


@app.cell
def _(ask_claude, revised, rough_paragraph, show):
    # Now ask Claude to explain what it changed and why — a learning tool
    explain_prompt = f"""\
    Compare these two paragraphs and explain each change you would make to 
    convert the original into the revised version. Format as a numbered list.
    Focus on: word choice, sentence structure, scientific precision, and logical flow.

    Original:
    {rough_paragraph}

    Revised:
    {revised}"""

    explanation = ask_claude(explain_prompt)
    show(explanation)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    This explain-the-changes pattern is great for learning. Over time, you'll internalize these improvements and your first drafts will get better.

    ---

    ## Part 4: Prompt templates for common writing tasks

    Here are reusable templates for the writing tasks you do most often. Each one is a function you can call with your content.
    """)
    return


@app.cell
def _(ask_claude):
    def improve_clarity(text: str) -> str:
        """Revise text for clarity and conciseness while preserving meaning."""
        prompt = f"""\
    Revise this text for clarity and conciseness. Rules:
    - Preserve the exact scientific meaning
    - Remove filler words and redundancy
    - Prefer active voice
    - Keep the same approximate length
    - Return ONLY the revised text

    Text:
    {text}"""
        return ask_claude(prompt)


    def strengthen_argument(text: str) -> str:
        """Identify logical gaps and suggest improvements to an argument."""
        prompt = f"""\
    Analyze this scientific argument. Identify:
    1. Any logical gaps or unsupported claims
    2. Where evidence or citations would strengthen the argument
    3. Whether the conclusion follows from the premises
    4. Specific suggestions for improvement

    Text:
    {text}"""
        return ask_claude(prompt)


    def adapt_for_audience(text: str, audience: str) -> str:
        """Rewrite text for a specific audience."""
        prompt = f"""\
    Rewrite this text for the following audience: {audience}

    Adjust technical depth, jargon, and emphasis appropriately.
    Preserve the core scientific content.
    Return ONLY the rewritten text.

    Text:
    {text}"""
        return ask_claude(prompt)


    def generate_abstract(title: str, background: str, methods: str, 
                          results: str, conclusion: str, word_limit: int = 250) -> str:
        """Generate a structured abstract from key components."""
        prompt = f"""\
    Write a scientific abstract ({word_limit} words max) from these components:

    Title: {title}
    Background: {background}
    Methods: {methods}
    Results: {results}
    Conclusion: {conclusion}

    Use standard abstract structure (background, methods, results, conclusions).
    Be specific and quantitative. Return ONLY the abstract text."""
        return ask_claude(prompt)


    print("Writing templates defined:")
    print("  - improve_clarity(text)")
    print("  - strengthen_argument(text)")
    print("  - adapt_for_audience(text, audience)")
    print("  - generate_abstract(title, background, methods, results, conclusion)")
    return (adapt_for_audience,)


@app.cell
def _(adapt_for_audience, show):
    # Demo: adapt the same content for different audiences

    technical_text = """\
    We designed de novo protein binders targeting the voltage-sensing domain of NaV1.7 
    using RFdiffusion, achieving sub-nanomolar binding affinity (Kd = 0.8 nM by SPR). 
    Conjugation to a CRBN-recruiting moiety yielded a heterobifunctional degrader with 
    DC50 = 15 nM in cultured DRG neurons, resulting in >90% NaV1.7 depletion at 24 hours 
    without affecting NaV1.5 or NaV1.8 levels."""

    # For a study section (NIH reviewers — experts but maybe not in your exact subfield)
    study_section = adapt_for_audience(technical_text, 
        "NIH study section reviewers with expertise in neuroscience and pharmacology, "
        "but not necessarily protein engineering")

    show("### For NIH Study Section:\n\n" + study_section)
    return (technical_text,)


@app.cell
def _(adapt_for_audience, show, technical_text):
    # For a department seminar (broad biology audience)
    seminar = adapt_for_audience(technical_text,
        "a broad biology department audience including grad students and faculty "
        "from diverse fields — minimize jargon, emphasize the 'so what'")

    show("### For Department Seminar:\n\n" + seminar)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 5: Style matching

    You can teach Claude your writing style by providing examples. This is useful when you want AI-generated text to blend with your existing writing.

    The technique: include 1-2 paragraphs of your own writing as examples, then ask Claude to match that style.
    """)
    return


@app.cell
def _(ask_claude, show):
    # Example: two paragraphs in "your" style
    style_examples = """\
    Example 1 (from a previous grant):
    "The selective engagement of NaV1.7 in nociceptive circuits remains a formidable 
    challenge. While loss-of-function mutations in SCN9A unequivocally demonstrate that 
    NaV1.7 is dispensable for cardiac function but essential for pain perception, no 
    clinical inhibitor has achieved the selectivity window needed to exploit this biology. 
    We propose a fundamentally different strategy: rather than competing for the channel 
    pore, we will eliminate the target protein entirely through engineered degradation."

    Example 2 (from a manuscript introduction):
    "Targeted protein degradation has transformed drug discovery for oncology targets, 
    yet its application to integral membrane proteins — including the ion channels that 
    drive pathological pain — remains largely unexplored. The principal barrier is not 
    conceptual but practical: heterobifunctional degraders require a target-binding moiety 
    with both high affinity and exquisite selectivity, properties that conventional small 
    molecules struggle to achieve against the conserved pore domains of voltage-gated 
    sodium channels."
    """

    style_prompt = f"""\
    I want you to match my writing style. Here are two examples of my scientific writing:

    {style_examples}

    Key characteristics of my style:
    - I use em dashes for parenthetical asides
    - I prefer longer, complex sentences with subordinate clauses
    - I frame innovations as contrasts with existing approaches ("rather than X, we Y")
    - I use strong, specific verbs ("eliminate", "exploit", "transformed")
    - I tend to address limitations directly before pivoting to the solution

    Now write a paragraph IN MY STYLE about this topic:
    KCNQ2/3 potassium channels control neuronal excitability via the M-current. 
    Dysfunction causes both epilepsy and pain hypersensitivity. Existing modulators 
    (retigabine) lack subtype selectivity and have dose-limiting side effects. De novo 
    protein binders designed by RFdiffusion could target the KCNQ2/3 heteromer interface 
    with programmable selectivity.

    Write exactly ONE paragraph. Return ONLY the paragraph."""

    styled = ask_claude(style_prompt)
    show("### Style-matched paragraph:\n\n" + styled)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Compare that output with your examples. Does it capture the sentence rhythm? The use of dashes? The contrast structure? The more examples you provide, the better the match.

    > **Tip for Obsidian users:** Keep a note called "My Writing Style" with 3-4 of your best paragraphs. Paste it into the prompt whenever you want style-matched output.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Part 6: The iterative refinement loop

    Real writing is iterative. Here's how to use multi-turn conversations for progressive refinement — the same technique from Module 05, applied to writing.
    """)
    return


@app.cell
def _(MODEL, client, show):
    # Start with your specific aim and iterate toward a significance section
    aim_description = 'We will design de novo protein binders targeting NaV1.7 and NaV1.8 using \nRFdiffusion, then conjugate them to E3 ligase recruiters to create targeted \ndegraders (PROTACs) for pain-related sodium channels in DRG nociceptors.'
    messages = [{'role': 'user', 'content': f"I'm writing the Significance section of an R01 grant. Here's my specific aim:\n\n{aim_description}\n\nWrite a first draft of the Significance section (200-250 words). Cover:\n1. The burden of chronic pain and limitations of current treatments\n2. NaV1.7/1.8 as validated targets (genetic evidence)\n3. Why current inhibitors have failed (selectivity)\n4. Why targeted degradation is a promising alternative\n\nUse formal scientific writing style. Don't invent specific citations."}]
    _response = client.messages.create(model=MODEL, max_tokens=1500, messages=messages)
    draft_1 = _response.content[0].text
    # Round 1: Generate a first draft of the Significance section
    show('### Draft 1:\n\n' + draft_1)
    return draft_1, messages


@app.cell
def _(MODEL, client, draft_1, messages, show):
    # Round 2: Ask for specific improvements
    messages.append({'role': 'assistant', 'content': draft_1})
    messages.append({'role': 'user', 'content': "Good start. Three revisions:\n1. The opening is too generic — start with a more specific hook about the opioid crisis and unmet need for mechanism-based analgesics.\n2. Add a sentence about how targeted degradation is catalytic (sub-stoichiometric dosing) which reduces off-target risk.\n3. The transition from 'why inhibitors failed' to 'why degradation works' is abrupt — smooth it out.\n\nRewrite the full section with these changes. Same length."})
    _response = client.messages.create(model=MODEL, max_tokens=1500, messages=messages)
    draft_2 = _response.content[0].text
    show('### Draft 2:\n\n' + draft_2)
    return (draft_2,)


@app.cell
def _(MODEL, client, draft_2, messages, show):
    # Round 3: Final polish
    messages.append({'role': 'assistant', 'content': draft_2})
    messages.append({'role': 'user', 'content': "Much better. Final pass:\n1. Tighten to exactly 200 words (it's probably over).\n2. Make sure every sentence earns its place — cut anything that's just filler or restates something already said.\n3. End with a forward-looking sentence about the potential impact.\n\nReturn ONLY the final paragraph."})
    _response = client.messages.create(model=MODEL, max_tokens=1500, messages=messages)
    final = _response.content[0].text
    show('### Final Version:\n\n' + final)
    print(f'\nWord count: ~{len(final.split())}')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    Three rounds. Each one you gave specific, actionable feedback. That's the pattern:

    1. **Generate** with clear constraints
    2. **Evaluate** (you read it critically)
    3. **Direct** specific changes
    4. **Repeat** until satisfied

    This is exactly how you'd work with a human writing collaborator.

    <details><summary>Click to expand: When iterative revision helps most (and when it doesn't)</summary>

    **High value:**
    - Grant Specific Aims pages (high stakes, needs tight logic)
    - Paper introductions (argument structure matters)
    - Response to reviewers (tone and completeness matter)
    - Abstracts (every word counts at 250-word limit)

    **Diminishing returns after 2-3 rounds:**
    - Methods sections (factual, less about style)
    - Figure legends (formulaic)
    - Email drafts (quick and disposable)

    **Rule of thumb:** If the document will be read by more than 10 people or decides funding/publication, invest in 3+ revision rounds. Otherwise, one pass is usually enough.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Build your own Significance section

    Use the iterative approach to draft a Significance section for this project:

    **Project:** Using single-cell RNA-seq of human DRG neurons to identify co-expression patterns of NaV1.7 with druggable targets, enabling rational combination therapy for chronic pain.

    Steps:
    1. Define your project in a dictionary (like we did in Part 2)
    2. Generate a first draft
    3. Give at least 2 rounds of revision feedback
    4. Produce a final ~200-word Significance section
    """)
    return


@app.cell
def _(MODEL, client, show):
    # Define your project
    exercise_project = {'title': 'Single-cell transcriptomic atlas of NaV1.7 co-expression in human DRG for combination pain therapy', 'problem': 'NaV1.7-targeted monotherapies have failed clinically. Single-cell RNA-seq can reveal which druggable targets are co-expressed with NaV1.7 in specific nociceptor subtypes, enabling rational combination strategies.', 'significance': 'Chronic pain remains inadequately treated. Understanding the molecular context of NaV1.7 expression at single-cell resolution could identify synergistic drug combinations and explain why NaV1.7 inhibitors alone are insufficient.'}
    exercise_messages = [{'role': 'user', 'content': f"Write a first draft of an NIH R01 Significance section (200-250 words) for this project:\n\nTitle: {exercise_project['title']}\nProblem: {exercise_project['problem']}\nSignificance: {exercise_project['significance']}\n\nCover: the unmet need in pain treatment, why NaV1.7 monotherapy has failed, \nwhat single-cell RNA-seq uniquely enables, and the potential for rational \ncombination therapy. Use formal scientific writing style."}]
    _response = client.messages.create(model=MODEL, max_tokens=1500, messages=exercise_messages)
    ex_draft_1 = _response.content[0].text
    # Round 1: Generate first draft
    show('### Exercise Draft 1:\n\n' + ex_draft_1)
    return ex_draft_1, exercise_messages


@app.cell
def _(MODEL, client, ex_draft_1, exercise_messages, show):
    # Round 2: Your revision feedback
    # Edit this feedback to match what YOU think needs improvement
    exercise_messages.append({'role': 'assistant', 'content': ex_draft_1})
    exercise_messages.append({'role': 'user', 'content': 'Revisions needed:\n1. Be more specific about which co-expressed targets are interesting — mention TRPV1, P2RX3, and NTRK1 as examples of druggable co-expressed genes.\n2. Add a sentence about how human DRG data is critical because mouse-to-human translation of nociceptor subtypes is poor.\n3. Make the clinical impact more concrete — mention specific patient populations (post-surgical pain, diabetic neuropathy).\n\nRewrite the full section.'})
    _response = client.messages.create(model=MODEL, max_tokens=1500, messages=exercise_messages)
    ex_draft_2 = _response.content[0].text
    show('### Exercise Draft 2:\n\n' + ex_draft_2)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **Prompt engineering for writing:**
    - [Anthropic Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview) -- official guide covering system prompts, few-shot examples, chain-of-thought, and structured output. Directly applicable to the writing prompts in this notebook.
    - [Anthropic API Documentation](https://docs.anthropic.com/) -- complete reference for the Claude API

    **Scientific writing:**
    - *Writing Science* by Joshua Schimel -- the best book on structuring scientific narratives. Covers the OCAR framework (Opening, Challenge, Action, Resolution), paragraph structure, and how to build arguments that reviewers find compelling. Highly recommended for grant writing.
    - *The Elements of Style* by Strunk & White -- classic reference for clear, concise English prose

    **AI use policies in research:**
    - [NIH guidance on AI use in grant applications](https://grants.nih.gov/faqs#/use-of-generative-ai-in-peer-review.htm) -- current NIH policy on disclosure of AI-assisted writing in grants and peer review
    - [Nature editorial policies on AI-assisted writing](https://www.nature.com/nature-portfolio/editorial-policies/ai) -- Nature's requirements for disclosure and author responsibility when using AI writing tools
    - [Science editorial policies on AI](https://www.science.org/content/page/science-journals-editorial-policies) -- Science family journals' AI policies

    **Grant writing resources:**
    - [NIH grant writing tips](https://grants.nih.gov/grants/how-to-apply-application-guide/format-and-write/write-your-application.htm) -- official NIH advice on writing Specific Aims, Significance, and other sections
    - The Specific Aims page format used in Part 2 follows the standard NIH R01 structure: hook, long-term goal, objective, central hypothesis, rationale, aims, and impact statement
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
    - 2026-03-25: Added cross-module navigation links
    - 2026-03-25: QA pass — removed duplicate Part 7 section (code cell with markdown), removed duplicate Edit Log
    - 2026-03-25: Added callout boxes — warning (AI writing ethics and disclosure policies), decision point (what to use AI for vs write yourself), tip (AI as editor not author), collapsible deep-dive (when iterative revision helps most)
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: AI-Assisted Data Analysis Pipeline](02-data-analysis-pipeline.py) | [Module Index](../README.md) | [Next: Models and Providers \u2192](../12-ai-landscape/01-models-and-providers.py)
    """)
    return


if __name__ == "__main__":
    app.run()

