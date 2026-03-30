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
    # 01: Models and Providers

    ## The current AI landscape — and what matters for your research

    You already use Claude daily. But the AI world is bigger than one model, and knowing the landscape helps you:

    1. **Pick the right tool** for each task
    2. **Evaluate claims** when someone says "just use X"
    3. **Stay flexible** — the best model today might not be the best next quarter

    This notebook maps the territory.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: AI-Assisted Scientific Writing](../11-ai-research-workflows/03-writing-with-ai.py) | [Module Index](../README.md) | [Next: The AI Tools Ecosystem \u2192](02-tools-ecosystem.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## The major LLM providers

    As of early 2026, these are the players that matter:

    | Provider | Flagship model(s) | Key strengths | API available? |
    |----------|-------------------|---------------|----------------|
    | **[Anthropic](https://www.anthropic.com/)** | Claude (Opus, Sonnet, Haiku) | Long context, careful reasoning, coding, safety | [Yes](https://docs.anthropic.com/) |
    | **[OpenAI](https://openai.com/)** | GPT-4o, o1, o3 | Broad capabilities, large ecosystem, plugins | [Yes](https://platform.openai.com/docs/) |
    | **[Google](https://deepmind.google/)** | Gemini (Ultra, Pro, Flash) | Multimodal (native image/video), huge context windows | [Yes](https://ai.google.dev/docs) |
    | **[Meta](https://ai.meta.com/)** | Llama 3/4 | Open weights — you can run it locally, fine-tune it | Weights downloadable |
    | **[Mistral](https://mistral.ai/)** | Mistral Large, Mixtral | Strong European alternative, open-weight options | [Yes](https://docs.mistral.ai/) |
    | **[DeepSeek](https://www.deepseek.com/)** | DeepSeek-V3, DeepSeek-R1 | Competitive performance, efficient architecture | Yes |

    > 🤔 **Decision point: Comprehensive model comparison for pain biology research**
    >
    > | Model | Strength | Weakness | Approx. cost (per 1M tokens) | Best for |
    > |-------|----------|----------|------------------------------|----------|
    > | **Claude Opus 4** | Deep reasoning, long context, careful | Most expensive | $15 in / $75 out | Complex analysis, grant writing, experimental design |
    > | **Claude Sonnet 4** | Great balance of quality and cost | Slightly less nuanced than Opus | $3 in / $15 out | Daily research tasks, coding, literature review |
    > | **GPT-4o** | Strong all-around, large plugin ecosystem | Less careful reasoning on edge cases | $2.50 in / $10 out | Multimodal tasks, broad general knowledge |
    > | **Gemini Ultra** | Native multimodal, huge context | Still maturing in reasoning depth | $7 in / $21 out | Processing long documents, image analysis |
    > | **Gemini Flash** | Extremely fast and cheap | Less capable for complex tasks | $0.075 in / $0.30 out | Batch processing, classification, quick summaries |
    > | **Llama 3/4 (open)** | Free, local, private, fine-tunable | Requires GPU hardware, less capable | Compute only | Sensitive data (patient info, unpublished results) |
    > | **DeepSeek-R1** | Strong reasoning, cost-effective | Newer, smaller ecosystem | ~$2 in / $8 out | Budget-conscious reasoning tasks |
    > | **Specialized bio AI** (AlphaFold, RFdiffusion) | Purpose-built for biology | Narrow scope, can't chat | Free-to-compute | Protein structure, binder design, sequence design |
    >
    > **Recommendation:** Start with Claude Sonnet for most tasks. Upgrade to Opus for high-stakes work (grant drafts, complex interpretation). Drop to Haiku/Flash for batch processing. Use specialized tools (AlphaFold, RFdiffusion) for what they're built for — don't ask a chatbot to predict protein structures.

    > ⚠️ **Warning: Vendor lock-in.** If you build all your pipelines around one provider's API, switching later is painful. Mitigate this by: (1) keeping your prompts in separate files (not hardcoded), (2) abstracting the API call into a wrapper function (as we did in Module 09), and (3) periodically testing your most important prompts on a second provider. The API formats are similar enough that switching is feasible if you plan for it.

    ### What "open weights" means

    Meta's Llama and some Mistral models release their weights publicly. This means:
    - You can run them on your own hardware (or a cloud GPU)
    - You can fine-tune them on your own data
    - No API costs — but you pay for compute
    - Important for sensitive data where you can't send it to an external API

    For most day-to-day research tasks, API-based frontier models (Claude, GPT-4o, Gemini) are easier and more capable. But local models matter for privacy-sensitive work (patient data, unpublished results).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Model tiers: frontier vs. smaller models

    Not every task needs the biggest model. Think of it like choosing between a confocal microscope and a benchtop dissecting scope — both are microscopes, but you pick based on the task.

    ### Frontier models (Claude Opus, GPT-4o, Gemini Ultra)
    - Best reasoning and nuance
    - Most expensive (~\$15/M input tokens, ~\$75/M output tokens for Opus-tier)
    - Use for: complex analysis, writing assistance, tricky code, reviewing experimental designs

    ### Mid-tier models (Claude Sonnet, GPT-4o-mini, Gemini Pro)
    - 80-90% of frontier quality at ~1/5 the cost
    - Use for: most daily tasks, literature summaries, data formatting, routine coding

    ### Small/fast models (Claude Haiku, Gemini Flash)
    - Fast and cheap (~\$0.25/M input tokens)
    - Use for: classification, extraction, batch processing hundreds of papers, simple reformatting

    ### Decision framework

    ```
    Does this task require careful reasoning or creativity?
      YES → Frontier model
      NO  → Is it a batch job with hundreds+ of items?
              YES → Small model (Haiku/Flash)
              NO  → Mid-tier model (Sonnet/Pro)
    ```

    > **Think Python connection:** Chapter 1 discusses the idea that computers are fast but not smart. LLMs change this equation — they're slow (compared to regular code) but surprisingly capable at tasks that used to require human judgment. The trick is knowing when to use which.
    """)
    return


@app.cell
def _():
    import matplotlib.pyplot as plt
    import matplotlib.patches as mpatches
    import numpy as np
    _fig, _ax = plt.subplots(figsize=(10, 7))
    models = {'Claude Opus 4': (9.5, 9.5, 'Anthropic', '#8e44ad'), 'GPT-4o': (9.0, 7.0, 'OpenAI', '#2ecc71'), 'Gemini Ultra': (8.8, 8.0, 'Google', '#3498db'), 'Claude Sonnet 4': (8.5, 3.5, 'Anthropic', '#8e44ad'), 'GPT-4o-mini': (7.0, 1.0, 'OpenAI', '#2ecc71'), 'Gemini Pro': (8.0, 4.0, 'Google', '#3498db'), 'Gemini Flash': (6.5, 0.5, 'Google', '#3498db'), 'Claude Haiku 3.5': (7.0, 1.5, 'Anthropic', '#8e44ad'), 'Llama 3 (405B)': (8.0, 0.3, 'Meta', '#e74c3c'), 'DeepSeek-R1': (8.5, 2.0, 'DeepSeek', '#f39c12')}
    for name, (cap, _cost, provider, color) in models.items():
    # Model positions: (capability score 0-10, relative cost 0-10)
        _ax.scatter(_cost, cap, s=200, c=color, alpha=0.8, edgecolors='black', linewidth=0.5, zorder=3)
        _ax.annotate(name, (_cost, cap), xytext=(8, -12), textcoords='offset points', fontsize=8, fontweight='bold')  # (capability, cost, label, color)
    _ax.axhspan(8.5, 10, alpha=0.05, color='red', label='Frontier tier')
    _ax.axhspan(7.0, 8.5, alpha=0.05, color='orange', label='Mid tier')
    _ax.axhspan(5.0, 7.0, alpha=0.05, color='green', label='Small/fast tier')
    _ax.set_xlabel('Relative Cost (per token)', fontsize=12)
    _ax.set_ylabel('Capability (reasoning, coding, writing)', fontsize=12)
    _ax.set_title('LLM Landscape: Capability vs. Cost (early 2026)', fontsize=13)
    _ax.set_xlim(-0.5, 11)
    _ax.set_ylim(5.5, 10.2)
    legend_handles = [mpatches.Patch(color='#8e44ad', label='Anthropic'), mpatches.Patch(color='#2ecc71', label='OpenAI'), mpatches.Patch(color='#3498db', label='Google'), mpatches.Patch(color='#e74c3c', label='Meta (open weights)'), mpatches.Patch(color='#f39c12', label='DeepSeek')]
    _ax.legend(handles=legend_handles, loc='lower right', fontsize=9)
    _ax.annotate('SWEET SPOT\n(best value for\nmost research tasks)', xy=(3.5, 8.5), fontsize=9, fontstyle='italic', color='gray', ha='center', bbox=dict(boxstyle='round,pad=0.3', facecolor='lightyellow', edgecolor='gray', alpha=0.7))
    plt.tight_layout()
    plt.show()
    # Add tier zones
    # Provider legend
    print('The sweet spot: mid-tier models give 80-90% of frontier quality at ~1/5 the cost.')
    return (plt,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Specialized AI tools for biology

    > **Why you need this section especially:** General LLMs like Claude are versatile, but they can't predict protein structures or generate binder backbones. The specialized tools below are the ones that directly produce the computational outputs your binder design pipeline depends on. Understanding what each tool does (and doesn't do) prevents you from asking Claude to do AlphaFold's job or vice versa.

    This is where things get especially relevant for your de novo protein binder work. General LLMs are versatile, but these specialized tools are transformative for structural biology:

    ### AlphaFold / AlphaFold 3
    - **What:** Predicts 3D protein structure from sequence
    - **Key paper:** Jumper, J. et al. (2021). "Highly accurate protein structure prediction with AlphaFold." *Nature* 596:583-589. [DOI: 10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2)
    - **Why it matters for you:** Predicting NaV1.7/1.8 conformations, understanding binding interfaces
    - **Access:** [AlphaFold Server](https://alphafoldserver.com/) (free), [ColabFold](https://github.com/sokrypton/ColabFold) (free), or local install
    - **Limitations:** Less reliable for disordered regions; multimer predictions are improving but not perfect
    - AlphaFold 3 now handles protein-ligand, protein-nucleic acid, and protein-protein complexes

    ### ESM / ESMFold (Meta)
    - **What:** Protein language model trained on millions of sequences
    - **Key paper:** Lin, Z. et al. (2023). "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science* 379:1123-1130. [DOI: 10.1126/science.ade2574](https://doi.org/10.1126/science.ade2574)
    - **Why it matters:** Fast structure prediction, evolutionary understanding, variant effect prediction
    - **Relevance:** Understanding how mutations in NaV channels affect structure and function
    - **Advantage over AlphaFold:** Much faster (single forward pass), good for screening many sequences

    ### RFdiffusion (Baker Lab)
    - **What:** Generates new protein structures using diffusion (like image generation, but for proteins)
    - **Key paper:** Watson, J.L. et al. (2023). "De novo design of protein structure and function with RFdiffusion." *Nature* 620:1089-1100. [DOI: 10.1038/s41586-023-06415-8](https://doi.org/10.1038/s41586-023-06415-8)
    - **Why it matters for you:** This is core to de novo binder design. Generate binder backbones targeting specific epitopes on NaV1.7, NaV1.8, KCNQ2/3
    - **Workflow:** Define target epitope -> RFdiffusion generates binder backbones -> ProteinMPNN designs sequences -> AlphaFold validates

    ### ProteinMPNN (Baker Lab)
    - **What:** Designs amino acid sequences for a given protein backbone
    - **Key paper:** Dauparas, J. et al. (2022). "Robust deep learning-based protein sequence design using ProteinMPNN." *Science* 378:49-56. [DOI: 10.1126/science.add2187](https://doi.org/10.1126/science.add2187)
    - **Why it matters:** Once RFdiffusion gives you a backbone, ProteinMPNN gives you a sequence that folds into it
    - **Your pipeline:** RFdiffusion backbone -> ProteinMPNN sequence -> AlphaFold2/ESMFold validation -> experimental testing

    ### Chai-1 / Boltz / NeuralPLexer
    - **What:** Newer structure prediction models competing with/complementing AlphaFold
    - **Why to watch:** The field is moving fast; these may offer advantages for specific use cases

    ### Your design pipeline in context

    ```
    Target identification (NaV1.7 pain target)
        |
    Structure prediction (AlphaFold 3 -- target + membrane context)
        |
    Epitope selection (which surface to bind -- informed by functional data)
        |
    Binder generation (RFdiffusion -- generate diverse backbones)
        |
    Sequence design (ProteinMPNN -- design sequences for each backbone)
        |
    Validation (AlphaFold 2 / ESMFold -- does the designed protein fold correctly?)
        |
    Filtering (predicted binding affinity, stability, expressibility)
        |
    Experimental testing
    ```

    General LLMs like Claude can help with *every* step of this pipeline — not by running the computations, but by helping you write scripts, interpret results, troubleshoot errors, and think through design decisions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### Protein design pipeline — which AI tool at each step

    """),
    mo.mermaid(
        """
        flowchart TD
            A["Target ID<br>NaV1.7 pain target<br>(Literature + Claude)"] --> B["Structure Prediction<br>AlphaFold 3<br>+ membrane context"]
            B --> C["Epitope Selection<br>Your expertise<br>+ functional data"]
            C --> D["Binder Generation<br>RFdiffusion<br>diverse backbone sampling"]
            D --> E["Sequence Design<br>ProteinMPNN<br>sequence for each backbone"]
            E --> F["Validation<br>AlphaFold 2 / ESMFold<br>does it fold correctly?"]
            F --> G["Filtering<br>Rosetta energy<br>pAE, pLDDT scores"]
            G --> H["Experimental Testing<br>SPR, thermal stability,<br>calcium imaging"]
        
            A -.- Claude1["Claude helps:<br>lit review, planning"]
            D -.- Claude2["Claude helps:<br>script writing,<br>parameter tuning"]
            F -.- Claude3["Claude helps:<br>result interpretation,<br>filtering criteria"]
            H -.- Claude4["Claude helps:<br>data analysis,<br>next-round design"]
        
            style A fill:#bdc3c7,color:#2c3e50
            style B fill:#e74c3c,color:#fff
            style C fill:#f39c12,color:#fff
            style D fill:#9b59b6,color:#fff
            style E fill:#9b59b6,color:#fff
            style F fill:#e74c3c,color:#fff
            style G fill:#3498db,color:#fff
            style H fill:#2ecc71,color:#fff
            style Claude1 fill:#8e44ad,color:#fff,stroke-dasharray: 5 5
            style Claude2 fill:#8e44ad,color:#fff,stroke-dasharray: 5 5
            style Claude3 fill:#8e44ad,color:#fff,stroke-dasharray: 5 5
            style Claude4 fill:#8e44ad,color:#fff,stroke-dasharray: 5 5
        """
    ),
    mo.md(r"""

    **Key insight:** Specialized tools (red/purple) do the computation. Claude (dashed purple) helps you *use* those tools -- writing scripts, interpreting outputs, planning next steps. Neither replaces the other.
    """)
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Cost comparison

    Let's make this concrete. Below is approximate pricing as of early 2026 (check current prices on the [Anthropic pricing page](https://www.anthropic.com/pricing), [OpenAI pricing page](https://openai.com/pricing), and [Google AI pricing page](https://ai.google.dev/pricing) — they only go down).
    """)
    return


@app.cell
def _():
    import pandas as pd
    models_1 = pd.DataFrame({'Model': ['Claude Opus 4', 'Claude Sonnet 4', 'Claude Haiku 3.5', 'GPT-4o', 'GPT-4o-mini', 'Gemini Ultra', 'Gemini Flash'], 'Provider': ['Anthropic', 'Anthropic', 'Anthropic', 'OpenAI', 'OpenAI', 'Google', 'Google'], 'Input_per_1M': [15.0, 3.0, 0.8, 2.5, 0.15, 7.0, 0.075], 'Output_per_1M': [75.0, 15.0, 4.0, 10.0, 0.6, 21.0, 0.3], 'Tier': ['Frontier', 'Mid', 'Small', 'Frontier', 'Small', 'Frontier', 'Small']})
    # Approximate pricing per 1M tokens (early 2026 — check for updates)
    print(models_1.to_string(index=False))
    return (models_1,)


@app.cell
def _(models_1, plt):
    input_tokens = 100000
    output_tokens = 40000
    models_1['Cost_200_abstracts'] = models_1['Input_per_1M'] * input_tokens / 1000000 + models_1['Output_per_1M'] * output_tokens / 1000000
    _fig, _ax = plt.subplots(figsize=(10, 5))
    colors = {'Frontier': '#e74c3c', 'Mid': '#f39c12', 'Small': '#27ae60'}
    bar_colors = [colors[t] for t in models_1['Tier']]
    bars = _ax.barh(models_1['Model'], models_1['Cost_200_abstracts'], color=bar_colors)
    _ax.set_xlabel('Cost (USD)')
    _ax.set_title('Cost to process 200 paper abstracts\n(~100K input + 40K output tokens)')
    for bar, _cost in zip(bars, models_1['Cost_200_abstracts']):
        _ax.text(bar.get_width() + 0.05, bar.get_y() + bar.get_height() / 2, f'${_cost:.3f}', va='center', fontsize=10)
    from matplotlib.patches import Patch
    legend_elements = [Patch(facecolor=c, label=t) for t, c in colors.items()]
    _ax.legend(handles=legend_elements, loc='lower right')
    _ax.set_xlim(0, max(models_1['Cost_200_abstracts']) * 1.4)
    plt.tight_layout()
    plt.show()
    print('\nKey takeaway: even frontier models are cheap for typical research tasks.')
    print('200 abstracts through Claude Opus costs about $4.50.')
    print("Through Haiku, it's about $0.24. Through Gemini Flash, about $0.02.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### When cost actually matters

    For most research tasks (asking questions, writing help, code debugging), you'll spend $5-50/month. That's less than a single antibody.

    Cost becomes relevant when you:
    - Process thousands of papers or sequences through the API
    - Run large batch jobs (e.g., classifying 10,000 gene descriptions)
    - Build applications that serve many users

    In those cases, use the tier framework: prototype with a frontier model, then drop to a smaller model for production.

    > 💡 **Tip:** Use the cheapest model that works. For your literature screening pipeline (Module 11, Notebook 01), the extraction prompt works nearly as well with Sonnet as with Opus — test both and compare output quality before defaulting to the expensive option. For simple classification ("is this paper about NaV1.7?"), Haiku is often sufficient and costs 60x less than Opus.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Exercise: Compare approaches to a pain biology question

    Let's use the Claude API to tackle a real question, then think about how you'd approach it differently with different tools.

    **Question:** "What are the key structural differences between NaV1.7 and NaV1.8 that could be exploited for selective binder design?"

    First, let's ask Claude via the API.
    """)
    return


@app.cell
def _():
    import anthropic

    client = anthropic.Anthropic()  # uses ANTHROPIC_API_KEY from environment

    question = """What are the key structural differences between NaV1.7 (SCN9A) and NaV1.8 (SCN10A) 
    that could be exploited for designing selective de novo protein binders? 
    Focus on extracellular-accessible regions and known structural features 
    from cryo-EM structures. Be specific about domain architecture."""

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": question}]
    )

    print("Claude's analysis:")
    print("=" * 60)
    print(response.content[0].text)
    return (response,)


@app.cell
def _(response):
    # Now let's think about what each tool brings to this question.
    # This is a THINKING exercise — fill in the markdown cell below.

    # First, let's see how much that API call cost:
    input_cost = response.usage.input_tokens * 3.0 / 1_000_000  # Sonnet pricing
    output_cost = response.usage.output_tokens * 15.0 / 1_000_000
    total_cost = input_cost + output_cost

    print(f"Tokens used: {response.usage.input_tokens} input, {response.usage.output_tokens} output")
    print(f"Approximate cost: ${total_cost:.4f}")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Your turn: tool comparison

    For the question "How do I design a selective binder for NaV1.7 over NaV1.8?", think about what each tool category brings:

    **General LLM (Claude/GPT-4o):**
    - Good for: *(your notes here)*
    - Limitations: *(your notes here)*

    **AlphaFold 3:**
    - Good for: *(your notes here)*
    - Limitations: *(your notes here)*

    **RFdiffusion + ProteinMPNN:**
    - Good for: *(your notes here)*
    - Limitations: *(your notes here)*

    **Literature search AI (Elicit/Semantic Scholar):**
    - Good for: *(your notes here)*
    - Limitations: *(your notes here)*

    **Key insight:** No single tool does everything. The skill is in combining them — use Claude to plan your approach, AlphaFold to get structures, RFdiffusion to generate candidates, and Claude again to interpret results and troubleshoot.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    **Provider documentation and pricing:**
    - [Anthropic API docs and pricing](https://docs.anthropic.com/) -- Claude model docs, API reference, and current pricing
    - [OpenAI API docs](https://platform.openai.com/docs/) -- GPT model documentation and usage guides
    - [Google AI for Developers](https://ai.google.dev/docs) -- Gemini model docs and API reference

    **Key papers in biology-specific AI:**
    - Jumper, J. et al. (2021). "Highly accurate protein structure prediction with AlphaFold." *Nature* 596:583-589. [DOI: 10.1038/s41586-021-03819-2](https://doi.org/10.1038/s41586-021-03819-2) -- the breakthrough paper that solved protein structure prediction
    - Lin, Z. et al. (2023). "Evolutionary-scale prediction of atomic-level protein structure with a language model." *Science* 379:1123-1130. [DOI: 10.1126/science.ade2574](https://doi.org/10.1126/science.ade2574) -- ESMFold; single forward pass structure prediction
    - Watson, J.L. et al. (2023). "De novo design of protein structure and function with RFdiffusion." *Nature* 620:1089-1100. [DOI: 10.1038/s41586-023-06415-8](https://doi.org/10.1038/s41586-023-06415-8) -- the core method for your binder design pipeline
    - Dauparas, J. et al. (2022). "Robust deep learning-based protein sequence design using ProteinMPNN." *Science* 378:49-56. [DOI: 10.1126/science.add2187](https://doi.org/10.1126/science.add2187) -- inverse folding for sequence design

    **Tools:**
    - [AlphaFold Server](https://alphafoldserver.com/) -- free web interface for AlphaFold 3 predictions
    - [ColabFold](https://github.com/sokrypton/ColabFold) -- fast, free AlphaFold2 predictions via Google Colab
    - [RFdiffusion GitHub](https://github.com/RosettaCommons/RFdiffusion) -- source code and documentation
    - [ProteinMPNN GitHub](https://github.com/dauparas/ProteinMPNN) -- source code and examples
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
    - 2026-03-25: QA pass — removed duplicate sections (LLM providers, specialized tools, cost comparison, Edit Log)
    - 2026-03-25: Added callout boxes — decision point (comprehensive model comparison table for pain biology), warning (vendor lock-in), tip (use cheapest model that works)
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: AI-Assisted Scientific Writing](../11-ai-research-workflows/03-writing-with-ai.py) | [Module Index](../README.md) | [Next: The AI Tools Ecosystem \u2192](02-tools-ecosystem.py)
    """)
    return


if __name__ == "__main__":
    app.run()

