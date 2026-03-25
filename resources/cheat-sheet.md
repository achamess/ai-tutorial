# AI Power-User Cheat Sheet

Quick reference for everything covered in this tutorial.

---

## Python Basics

### Variables and types

```python
channel = "NaV1.7"          # str — text
num_neurons = 45             # int — whole number
threshold = -35.2            # float — decimal
is_nociceptor = True         # bool — True/False
```

### Lists (ordered collections)

```python
targets = ["NaV1.7", "NaV1.8", "KCNQ2"]

targets[0]             # "NaV1.7" (first item, 0-indexed)
targets[-1]            # "KCNQ2" (last item)
targets.append("CaV2.2")  # add to end
len(targets)           # 4

# List comprehension
nav_only = [t for t in targets if t.startswith("NaV")]
```

### Dictionaries (key-value pairs)

```python
experiment = {
    "target": "NaV1.8",
    "approach": "de novo binder",
    "kd_nm": 12.5
}

experiment["target"]           # "NaV1.8"
experiment["status"] = "done"  # add new key
experiment.keys()              # all keys
experiment.values()            # all values
experiment.items()             # key-value pairs
```

### Loops

```python
# For loop
for channel in ["NaV1.7", "NaV1.8", "KCNQ2"]:
    print(f"Targeting {channel}")

# Loop with index
for i, channel in enumerate(channels):
    print(f"{i}: {channel}")

# Loop over dictionary
for key, value in experiment.items():
    print(f"{key}: {value}")
```

### Conditionals

```python
if kd < 10:
    print("High affinity")
elif kd < 100:
    print("Moderate affinity")
else:
    print("Low affinity")
```

### Functions

```python
def calculate_hill(concentration, ec50, n=1):
    """Hill equation for dose-response."""
    return concentration**n / (ec50**n + concentration**n)

# Call it
response = calculate_hill(100, 50, n=1.5)
```

### f-strings

```python
name = "DNB-001"
kd = 8.3
print(f"{name} has Kd = {kd:.1f} nM")        # DNB-001 has Kd = 8.3 nM
print(f"Percentage: {7/48*100:.1f}%")          # Percentage: 14.6%
print(f"{'NaV1.7':>10}")                       # right-aligned, width 10
```

### File I/O

```python
# Read a text file
with open("data.txt", "r") as f:
    content = f.read()

# Write a text file
with open("output.txt", "w") as f:
    f.write("Results here\n")

# Read lines into a list
with open("data.txt", "r") as f:
    lines = f.readlines()
```

---

## pandas Essentials

### Reading data

```python
import pandas as pd

df = pd.read_csv("data.csv")
df = pd.read_excel("data.xlsx")
df = pd.read_csv("data.tsv", sep="\t")
```

### Inspecting

```python
df.head()           # first 5 rows
df.shape            # (rows, columns)
df.columns          # column names
df.dtypes           # data types
df.describe()       # summary statistics
df.info()           # overview of the DataFrame
df.value_counts("column")  # frequency counts
```

### Selecting and filtering

```python
# Select columns
df["channel"]                    # single column (Series)
df[["channel", "kd_nm"]]        # multiple columns (DataFrame)

# Filter rows
high_affinity = df[df["kd_nm"] < 10]
nav_only = df[df["channel"].str.startswith("NaV")]
combined = df[(df["kd_nm"] < 10) & (df["channel"] == "NaV1.7")]
```

### Groupby and aggregation

```python
df.groupby("channel")["kd_nm"].mean()
df.groupby("channel")["kd_nm"].agg(["mean", "std", "count"])
df.groupby(["channel", "region"]).size()
```

### Creating columns

```python
df["affinity_class"] = df["kd_nm"].apply(
    lambda x: "high" if x < 10 else "low"
)
df["log_kd"] = np.log10(df["kd_nm"])
```

### Sorting

```python
df.sort_values("kd_nm")                      # ascending
df.sort_values("kd_nm", ascending=False)      # descending
df.sort_values(["channel", "kd_nm"])          # multi-column
```

### Saving

```python
df.to_csv("output.csv", index=False)
df.to_excel("output.xlsx", index=False)
```

### Plotting with pandas

```python
df["kd_nm"].hist(bins=20)
df.plot.scatter(x="predicted_kd", y="experimental_kd")
df.groupby("channel")["kd_nm"].mean().plot.bar()
```

---

## Plotting with matplotlib/seaborn

```python
import matplotlib.pyplot as plt
import seaborn as sns

# Basic plot
fig, ax = plt.subplots(figsize=(8, 5))
ax.scatter(x_data, y_data)
ax.set_xlabel("Concentration (nM)")
ax.set_ylabel("Response (%)")
ax.set_title("Dose-Response Curve")
plt.tight_layout()
plt.savefig("figure.png", dpi=300)
plt.show()

# Seaborn for statistical plots
sns.boxplot(data=df, x="channel", y="kd_nm")
sns.violinplot(data=df, x="group", y="response")
sns.heatmap(df.corr(), annot=True, cmap="coolwarm")
```

---

## Claude API Patterns

### Setup

```python
import anthropic
client = anthropic.Anthropic()  # reads ANTHROPIC_API_KEY from env
```

### Basic call

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Your question here"}]
)
print(response.content[0].text)
```

### With system prompt

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are an expert pain biologist specializing in ion channels.",
    messages=[{"role": "user", "content": "Your question here"}]
)
```

### Structured output (JSON)

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": """Extract information from this abstract and return as JSON:
        {"target": "...", "method": "...", "key_finding": "..."}

        Abstract: ..."""
    }]
)

import json
data = json.loads(response.content[0].text)
```

### Batch processing

```python
results = []
for item in items:
    response = client.messages.create(
        model="claude-haiku-3-5-20241022",  # cheap model for batch work
        max_tokens=256,
        messages=[{"role": "user", "content": f"Process this: {item}"}]
    )
    results.append(response.content[0].text)
```

### Check usage and cost

```python
print(f"Input tokens: {response.usage.input_tokens}")
print(f"Output tokens: {response.usage.output_tokens}")
```

### Model selection guide

| Model | Use case | Relative cost |
|-------|----------|---------------|
| `claude-opus-4-20250514` | Complex reasoning, nuanced writing | $$$$$ |
| `claude-sonnet-4-20250514` | Most daily tasks, good balance | $$$ |
| `claude-haiku-3-5-20241022` | Batch processing, simple extraction | $ |

---

## Prompt Engineering Templates

### Literature review

```
System: You are an expert in [field]. Provide accurate, evidence-based analysis.

User: Review the current state of research on [topic]. Organize by:
1. Key findings (last 3 years)
2. Methodological approaches
3. Open questions and controversies
4. Relevance to [your specific work]

Be specific about experimental evidence. Flag where evidence is weak.
```

### Writing assistance

```
System: You are a scientific writing editor. Maintain technical accuracy
while improving clarity. Preserve the author's voice.

User: Revise this [paragraph/section] for clarity and concision.
Maintain all technical claims. Flag any statements that seem unsupported.

[paste your text]
```

### Data analysis

```
System: You are a biostatistics consultant helping a biologist analyze data.
Explain your reasoning and any assumptions.

User: I have [describe dataset]. I want to test whether [hypothesis].
- Independent variable: [what]
- Dependent variable: [what]
- Sample sizes: [what]
- Any concerns: [normality, repeated measures, etc.]

Recommend an appropriate statistical test and explain why.
```

### Code generation

```
Write a Python script that:
1. [Step 1]
2. [Step 2]
3. [Step 3]

Use pandas for data handling. Include error handling.
Add comments explaining each step — I'm learning Python.

Input: [describe input file/data format]
Output: [describe desired output]
```

### Experimental design

```
System: You are an expert in [pain biology / protein engineering / etc.].

User: I'm planning an experiment to [goal].

Current approach: [describe]
Target: [NaV1.7 / NaV1.8 / etc.]
Available tools: [list]
Constraints: [budget, time, equipment]

Suggest an experimental design including:
- Controls (positive and negative)
- Sample size considerations
- Potential pitfalls
- Alternative approaches if primary plan fails
```

---

## VS Code Shortcuts for Notebooks

| Action | Mac | Windows/Linux |
|--------|-----|---------------|
| Run cell | `Shift+Enter` | `Shift+Enter` |
| Run cell, stay in place | `Ctrl+Enter` | `Ctrl+Enter` |
| Insert cell below | `B` (command mode) | `B` |
| Insert cell above | `A` (command mode) | `A` |
| Delete cell | `DD` (command mode) | `DD` |
| Cell to markdown | `M` (command mode) | `M` |
| Cell to code | `Y` (command mode) | `Y` |
| Command palette | `Cmd+Shift+P` | `Ctrl+Shift+P` |
| Toggle sidebar | `Cmd+B` | `Ctrl+B` |
| Open terminal | `` Ctrl+` `` | `` Ctrl+` `` |
| Find in file | `Cmd+F` | `Ctrl+F` |
| Save | `Cmd+S` | `Ctrl+S` |

**Tip:** Press `Escape` to enter command mode (cell border turns blue), `Enter` to edit.

---

## Terminal / Command Line Basics

```bash
# Navigation
pwd                    # print working directory
ls                     # list files
ls -la                 # list all files with details
cd dirname             # change directory
cd ..                  # go up one level
cd ~                   # go to home directory

# Files
cp source dest         # copy file
mv source dest         # move or rename
rm filename            # delete file (careful!)
mkdir dirname          # create directory
cat filename           # print file contents
head -20 filename      # first 20 lines
wc -l filename         # count lines

# Python environment
python --version       # check Python version
pip install package    # install a package
pip list               # see installed packages
source .venv/bin/activate  # activate virtual environment

# Git basics
git status             # see what's changed
git add filename       # stage a file
git commit -m "msg"    # commit with message
git log --oneline      # see recent commits
git diff               # see unstaged changes

# Jupyter
jupyter notebook       # launch notebook server
jupyter kernelspec list  # see available kernels

# Claude Code
claude                 # start Claude Code
claude "do something"  # one-shot command
```

> **Missing Semester reference:** Lectures 1 (Shell), 2 (Shell Tools), and 6 (Version Control) cover these topics in depth. Highly recommended: https://missing.csail.mit.edu/

---

## Key Links

### Learning resources
- **Think Python** (free): https://allendowney.github.io/ThinkPython/
- **Missing Semester** (MIT): https://missing.csail.mit.edu/
- **Python Data Science Handbook**: https://jakevdp.github.io/PythonDataScienceHandbook/

### Anthropic / Claude
- **Anthropic docs**: https://docs.anthropic.com/
- **Claude API reference**: https://docs.anthropic.com/en/api/
- **Anthropic cookbook** (examples): https://github.com/anthropics/anthropic-cookbook
- **Prompt engineering guide**: https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering/overview

### Biology AI tools
- **AlphaFold Server**: https://alphafoldserver.com/
- **ColabFold**: https://colab.research.google.com/github/sokrypton/ColabFold
- **RFdiffusion**: https://github.com/RosettaCommons/RFdiffusion
- **ProteinMPNN**: https://github.com/dauparas/ProteinMPNN
- **ESM** (Meta): https://github.com/facebookresearch/esm

### Research AI tools
- **Semantic Scholar**: https://www.semanticscholar.org/
- **Elicit**: https://elicit.com/
- **Consensus**: https://consensus.app/
- **Connected Papers**: https://www.connectedpapers.com/

### Staying current
- **Anthropic blog**: https://www.anthropic.com/news
- **The Batch** (Andrew Ng newsletter): https://www.deeplearning.ai/the-batch/
- **Import AI** (Jack Clark): https://importai.substack.com/
