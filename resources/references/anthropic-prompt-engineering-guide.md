# Anthropic Prompt Engineering Guide
Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview
Source: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/claude-prompting-best-practices
Downloaded: 2026-03-25
Note: This is a local copy for reference. Check the source URL for the most current version.

---

## Overview

### Before prompt engineering

This guide assumes that you have:
1. A clear definition of the success criteria for your use case
2. Some ways to empirically test against those criteria
3. A first draft prompt you want to improve

### When to prompt engineer

Not every success criteria or failing eval is best solved by prompt engineering. For example, latency and cost can sometimes be more easily improved by selecting a different model.

### Prompt engineering tutorial

- [GitHub prompting tutorial](https://github.com/anthropics/prompt-eng-interactive-tutorial) -- An example-filled tutorial that covers the prompt engineering concepts found in the docs.
- [Google Sheets prompting tutorial](https://docs.google.com/spreadsheets/d/19jzLgRruG9kjUQNKtCg1ZjdD6l6weA6qRXG5zLIAhC8) -- A lighter weight version via an interactive spreadsheet.

---

## Prompting Best Practices

This is the single reference for prompt engineering with Claude's latest models. It covers foundational techniques, output control, tool use, thinking, and agentic systems.

## General Principles

### Be clear and direct

Claude responds well to clear, explicit instructions. Being specific about your desired output can help enhance results.

Think of Claude as a brilliant but new employee who lacks context on your norms and workflows. The more precisely you explain what you want, the better the result.

**Golden rule:** Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too.

- Be specific about the desired output format and constraints.
- Provide instructions as sequential steps using numbered lists or bullet points when the order or completeness of steps matters.

**Less effective:**
```text
Create an analytics dashboard
```

**More effective:**
```text
Create an analytics dashboard. Include as many relevant features and interactions as possible. Go beyond the basics to create a fully-featured implementation.
```

### Add context to improve performance

Providing context or motivation behind your instructions can help Claude better understand your goals and deliver more targeted responses.

**Less effective:**
```text
NEVER use ellipses
```

**More effective:**
```text
Your response will be read aloud by a text-to-speech engine, so never use ellipses since the text-to-speech engine will not know how to pronounce them.
```

### Use examples effectively

Examples are one of the most reliable ways to steer Claude's output format, tone, and structure. A few well-crafted examples (few-shot or multishot prompting) can dramatically improve accuracy and consistency.

When adding examples, make them:
- **Relevant:** Mirror your actual use case closely.
- **Diverse:** Cover edge cases and vary enough that Claude doesn't pick up unintended patterns.
- **Structured:** Wrap examples in `<example>` tags so Claude can distinguish them from instructions.

Include 3-5 examples for best results.

### Structure prompts with XML tags

XML tags help Claude parse complex prompts unambiguously. Wrapping each type of content in its own tag (e.g. `<instructions>`, `<context>`, `<input>`) reduces misinterpretation.

Best practices:
- Use consistent, descriptive tag names across your prompts.
- Nest tags when content has a natural hierarchy.

### Give Claude a role

Setting a role in the system prompt focuses Claude's behavior and tone:

```python
import anthropic

client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-opus-4-6",
    max_tokens=1024,
    system="You are a helpful coding assistant specializing in Python.",
    messages=[
        {"role": "user", "content": "How do I sort a list of dictionaries by key?"}
    ],
)
print(message.content)
```

### Long context prompting

When working with large documents or data-rich inputs (20k+ tokens):

- **Put longform data at the top**: Place long documents above your query, instructions, and examples. Queries at the end can improve response quality by up to 30%.
- **Structure document content with XML tags**: Wrap each document in `<document>` tags with `<document_content>` and `<source>` subtags.
- **Ground responses in quotes**: Ask Claude to quote relevant parts of documents first before carrying out its task.

## Output and Formatting

### Communication style and verbosity

Claude's latest models have a more concise and natural communication style:
- More direct and grounded
- More conversational
- Less verbose -- may skip detailed summaries unless prompted

### Control the format of responses

1. **Tell Claude what to do instead of what not to do** -- Instead of "Do not use markdown," try "Your response should be composed of smoothly flowing prose paragraphs."
2. **Use XML format indicators** -- Try: "Write the prose sections in `<smoothly_flowing_prose_paragraphs>` tags."
3. **Match your prompt style to the desired output** -- Formatting style in your prompt may influence Claude's response style.
4. **Use detailed prompts for specific formatting preferences** -- Provide explicit guidance about markdown usage.

## Tool Use

### Tool usage

Claude's latest models benefit from explicit direction to use specific tools. Be explicit about whether you want suggestions or action:

**Less effective (Claude will only suggest):**
```text
Can you suggest some changes to improve this function?
```

**More effective (Claude will make the changes):**
```text
Change this function to improve its performance.
```

### Optimize parallel tool calling

Claude excels at parallel tool execution:
- Run multiple speculative searches during research
- Read several files at once to build context faster
- Execute bash commands in parallel

## Thinking and Reasoning

### Leverage thinking capabilities

Claude's latest models offer thinking capabilities helpful for complex multi-step reasoning. You can guide its thinking:

```text
After receiving tool results, carefully reflect on their quality and determine optimal next steps before proceeding.
```

Tips:
- Prefer general instructions over prescriptive steps
- Multishot examples work with thinking -- use `<thinking>` tags in few-shot examples
- Ask Claude to self-check: "Before you finish, verify your answer against [test criteria]."

## Agentic Systems

### Long-horizon reasoning and state tracking

Claude maintains orientation across extended sessions by focusing on incremental progress. Key practices:

- **Use structured formats for state data**: JSON for tracking test results or task status
- **Use git for state tracking**: Git provides logs and checkpoints across sessions
- **Emphasize incremental progress**: Ask Claude to keep track of progress

### Chain complex prompts

With adaptive thinking and subagent orchestration, Claude handles most multi-step reasoning internally. Explicit prompt chaining is still useful when you need to inspect intermediate outputs or enforce a specific pipeline structure.

The most common pattern is **self-correction**: generate a draft -> review against criteria -> refine based on review.

### Research and information gathering

For optimal research results:
1. Provide clear success criteria
2. Encourage source verification
3. For complex research, use a structured approach with competing hypotheses and confidence tracking

### Minimizing hallucinations

```text
Never speculate about code you have not opened. If the user references a specific file,
you MUST read the file before answering. Investigate and read relevant files BEFORE
answering questions about the codebase.
```
