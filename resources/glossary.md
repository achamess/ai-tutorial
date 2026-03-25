# Glossary of Terms

A searchable reference for all technical terms used throughout the AI Power-User Tutorial. Definitions are written for biologists, not computer scientists. Module references point to where each term is covered in depth.

---

## A

**Absolute path** — The full address of a file starting from the root of your filesystem (e.g., `/Users/alex/data/experiment1.csv`). Unlike a relative path, it works the same no matter where you are in your directory structure. *Module: 04-mastering-claude-code*

**Agent** — An AI system that can take multiple steps autonomously to accomplish a goal, such as reading files, running code, and deciding what to do next without being told each step. Claude Code operates as an agent when it searches your codebase and makes edits on its own. *Module: 04-mastering-claude-code, 07-ai-research-workflows*

**Alignment** — The field of research focused on making AI systems behave according to human values and intentions. When an LLM refuses to help synthesize a dangerous compound, that is alignment at work. *Module: 02-how-llms-work, 08-ai-landscape*

**API (Application Programming Interface)** — A structured way for one program to talk to another. When you send a prompt to Claude from a Python script (instead of typing in a chat window), you are using the Claude API. *Example: A script that sends your RNA-seq gene list to Claude and gets back pathway analysis suggestions.* *Module: 01-python-foundations, 05-claude-api*

**API endpoint** — A specific URL that accepts requests for a particular function of an API. Think of it like a specific counter at a service desk — each endpoint handles a different type of request. *Module: 05-claude-api*

**API key** — A secret password-like string that identifies you when calling an API. You must keep it private — anyone with your key can make requests (and charges) as you. *Module: 05-claude-api*

**Argument** — A value you pass into a function when you call it. In `calculate_fold_change(treated=8.5, control=2.1)`, the numbers 8.5 and 2.1 are arguments. *Module: 01-python-foundations*

**Attention mechanism** — The core innovation of transformer models that lets the AI weigh how important each word is relative to every other word in a passage. This is why an LLM can understand that "it" in "The nociceptor fired because it was sensitized" refers to the nociceptor. *Module: 02-how-llms-work*

**Authentication** — The process of proving your identity to a system, typically with an API key or password. Required before you can use the Claude API or access a private Git repository. *Module: 05-claude-api*

## B

**Benjamini-Hochberg** — A statistical method for controlling the false discovery rate when performing many simultaneous tests. Essential when testing thousands of genes in RNA-seq to avoid drowning in false positives. *Module: 06-data-skills*

**Bias** — In statistics, a systematic error that skews results in one direction. In AI, it can also mean the model reflecting societal prejudices present in its training data. Both senses matter when using AI to analyze pain research. *Module: 02-how-llms-work, 06-data-skills*

**Boolean** — A data type with only two possible values: `True` or `False`. Used for yes/no conditions like `is_nociceptor = True` or `p_value < 0.05`. *Module: 01-python-foundations*

**Boxplot** — A chart that shows the distribution of data using the median, quartiles, and outliers. Commonly used to compare pain behavior scores (e.g., withdrawal thresholds) across treatment groups. *Module: 06-data-skills*

## C

**Chain of thought** — A prompting technique where you ask the AI to show its reasoning step by step before giving a final answer. This dramatically improves accuracy on complex tasks like interpreting experimental designs. *Module: 03-prompt-engineering*

**Class** — A blueprint for creating objects in Python. Think of it like a cell type definition — it specifies what properties and behaviors all instances of that type share. Most beginners use existing classes (like DataFrame) rather than writing their own. *Module: 01-python-foundations*

**Claude** — Anthropic's family of AI assistants. Claude is the LLM you interact with through the chat interface, the API, or Claude Code. *Module: 02-how-llms-work, 03-prompt-engineering, 05-claude-api*

**Claude Code** — Anthropic's command-line tool that lets Claude act as an agent on your computer — reading files, running code, editing scripts, and executing shell commands. *Module: 04-mastering-claude-code*

**CLI (Command Line Interface)** — A text-based way to interact with your computer by typing commands, as opposed to clicking in a graphical interface. The Terminal app on your Mac is a CLI. *Module: 01-python-foundations, 04-mastering-claude-code*

**Command line** — See *CLI*. The text prompt where you type commands in a terminal window. *Module: 04-mastering-claude-code*

**Conditional** — Code that runs only when a certain condition is met, using `if`, `elif`, and `else`. Example: `if p_value < 0.05: print("Significant")`. *Module: 01-python-foundations*

**Confidence interval** — A range of values that likely contains the true population value. A 95% CI for a pain threshold means that if you repeated the experiment many times, 95% of the intervals would contain the true mean. *Module: 06-data-skills*

**Container** — A lightweight, self-contained package that bundles code with all its dependencies so it runs the same on any computer. Docker is the most common tool for creating containers. *Module: 07-ai-research-workflows*

**Context window** — The maximum amount of text (measured in tokens) that an LLM can process at once, including both your input and its response. If your document exceeds the context window, the model cannot "see" all of it simultaneously. *Module: 02-how-llms-work, 03-prompt-engineering*

**Correlation** — A statistical measure of how two variables move together. A correlation between TRPV1 expression and pain score does not prove one causes the other. *Module: 06-data-skills*

**Cron** — A scheduler on Unix/macOS that runs scripts at specified times. You could use it to automatically pull new PubMed results every morning. *Module: 07-ai-research-workflows*

**CSV (Comma-Separated Values)** — A simple text file format where each line is a row of data and values are separated by commas. The most universal format for tabular data like behavioral assay results or gene expression matrices. *Module: 01-python-foundations, 06-data-skills*

## D

**Daemon** — A background program that runs continuously without user interaction, like a web server or a scheduled task runner. *Module: 07-ai-research-workflows*

**DataFrame** — The central data structure in pandas — a table with labeled rows and columns. Think of it as a programmable spreadsheet. *Example: Loading your calcium imaging traces into a DataFrame with columns for `neuron_id`, `time`, and `fluorescence`.* *Module: 01-python-foundations, 06-data-skills*

**Data type** — The category of a value that determines what operations are valid on it. Common types include integers, floats, strings, and booleans. Python will not let you subtract a string from a number. *Module: 01-python-foundations*

**Decorator** — A special annotation (starting with `@`) placed above a function to modify its behavior. You may encounter these in frameworks but rarely need to write your own as a beginner. *Module: 01-python-foundations*

**Dictionary** — A Python data structure that stores key-value pairs, like a lookup table. *Example: `gene_info = {"name": "TRPV1", "chromosome": 17, "function": "heat sensing"}`.* *Module: 01-python-foundations*

**Directory** — A folder in your filesystem that can contain files and other directories. *Module: 01-python-foundations, 04-mastering-claude-code*

**Distribution** — The pattern of how values in a dataset are spread out. Knowing whether your pain scores follow a normal distribution determines which statistical tests are appropriate. *Module: 06-data-skills*

**DNS (Domain Name System)** — The system that translates human-readable web addresses (like `api.anthropic.com`) into numerical IP addresses that computers use. You rarely interact with it directly, but DNS failures explain why "the internet is down" sometimes. *Module: 07-ai-research-workflows*

**Dotfile** — A file whose name starts with a period (e.g., `.env`, `.gitignore`). These are hidden by default on macOS/Linux and typically store configuration settings. *Module: 04-mastering-claude-code*

## E

**Effect size** — A measure of the magnitude of a difference between groups, independent of sample size. A statistically significant but tiny effect size on a pain assay may not be biologically meaningful. *Module: 06-data-skills*

**Embedding** — A way of representing text (or images, or other data) as a list of numbers (a vector) so that similar meanings are close together in mathematical space. Used for semantic search — finding papers related to "nociceptor sensitization" even if they use different wording. *Module: 02-how-llms-work, 07-ai-research-workflows*

**Environment variable** — A named value stored in your operating system's settings, accessible to programs. API keys are commonly stored this way (e.g., `ANTHROPIC_API_KEY`) to avoid putting secrets in your code. *Module: 01-python-foundations, 05-claude-api*

**Exception** — An error that interrupts normal code execution. Python raises exceptions when something goes wrong, like dividing by zero or opening a file that does not exist. You can handle them with `try`/`except` blocks. *Module: 01-python-foundations*

## F

**FDR (False Discovery Rate)** — The expected proportion of false positives among all results you call significant. When you test 20,000 genes, controlling FDR at 5% means you accept that roughly 5% of your "hits" may be false. See also *Benjamini-Hochberg*. *Module: 06-data-skills*

**Few-shot** — A prompting technique where you provide a few examples of the desired input-output pattern before asking the model to handle a new case. *Example: Showing Claude three gene-summary pairs before asking it to summarize a fourth gene.* *Module: 03-prompt-engineering*

**File permissions** — Settings that control who can read, write, or execute a file. Important when scripts fail with "Permission denied" errors. *Module: 04-mastering-claude-code*

**Filesystem** — The organizational structure of files and directories on your computer. Understanding it is essential for telling Python (and Claude Code) where your data lives. *Module: 04-mastering-claude-code*

**Fine-tuning** — The process of further training a pre-trained model on a specialized dataset to improve its performance on a specific task. Distinct from prompting, which does not change the model itself. *Module: 02-how-llms-work, 08-ai-landscape*

**Firewall** — Software or hardware that blocks unauthorized network connections. Occasionally the reason a script cannot reach an API. *Module: 07-ai-research-workflows*

**Float** — A number with a decimal point, like `3.14` or `-0.05`. P-values, fold changes, and fluorescence intensities are all floats. *Module: 01-python-foundations*

**Fold change** — The ratio of a measurement in one condition versus another. A fold change of 2 means the value doubled. Often reported as log2 fold change in genomics. *Module: 06-data-skills*

**For loop** — Code that repeats an action for each item in a collection. *Example: `for gene in gene_list: print(gene)` prints every gene name.* *Module: 01-python-foundations*

**Foundation model** — A large AI model (like Claude or GPT-4) trained on broad data that can be adapted to many downstream tasks without task-specific training. *Module: 02-how-llms-work, 08-ai-landscape*

**F-string** — A Python string prefixed with `f` that lets you embed variables directly: `f"The gene {gene_name} has p-value {pval:.4f}"`. The most readable way to build strings with data in them. *Module: 01-python-foundations*

**Function** — A reusable block of code that takes inputs, does something, and optionally returns a result. *Example: `def calculate_sem(values): return np.std(values) / np.sqrt(len(values))`.* *Module: 01-python-foundations*

## G

**Git** — A version control system that tracks changes to your files over time. It lets you revert mistakes, see what changed and when, and collaborate with others. *Module: 04-mastering-claude-code*

**Git branch** — A parallel version of your code that lets you experiment without affecting the main version. Like making a copy of your analysis script to try a different normalization method. *Module: 04-mastering-claude-code*

**Git commit** — A saved snapshot of your project at a specific point in time, with a message describing what changed. *Module: 04-mastering-claude-code*

**Git repository** — A project directory tracked by Git, containing all your files plus their full change history. *Module: 04-mastering-claude-code*

**GPT (Generative Pre-trained Transformer)** — OpenAI's family of large language models. "GPT" is sometimes used loosely to mean any LLM, but strictly it refers to OpenAI's models (GPT-4, etc.). *Module: 02-how-llms-work, 08-ai-landscape*

## H

**Hallucination** — When an LLM generates information that sounds confident and plausible but is factually wrong. Particularly dangerous in research contexts — always verify AI-generated claims against primary literature. *Example: Claude might cite a paper that does not actually exist.* *Module: 02-how-llms-work, 03-prompt-engineering*

**Heatmap** — A visualization that uses color intensity to represent values in a matrix. Standard for displaying gene expression patterns across samples in RNA-seq experiments. *Module: 06-data-skills*

**Histogram** — A chart showing the frequency distribution of a single variable by dividing it into bins. Useful for checking whether your pain threshold data is normally distributed before choosing a statistical test. *Module: 06-data-skills*

**Hook** — A script that runs automatically at a specific point in a workflow — most commonly Git hooks that run before or after commits. *Module: 04-mastering-claude-code*

**HTTP/HTTPS** — The protocol used to transfer data on the web. HTTPS is the encrypted version. Every time your script calls the Claude API, it sends an HTTPS request. *Module: 05-claude-api*

**Hypothesis testing** — A statistical framework for deciding whether observed data provides enough evidence to reject a null hypothesis. The backbone of inferential statistics in pain research. *Module: 06-data-skills*

## I

**IDE (Integrated Development Environment)** — A software application that provides tools for writing code, such as a text editor, debugger, and terminal in one window. VS Code and PyCharm are popular examples. *Module: 01-python-foundations*

**Import** — The Python statement that loads a library or module so you can use its functions. `import pandas as pd` makes the pandas library available as `pd`. *Module: 01-python-foundations*

**Index** — The position number of an item in a sequence. Python uses zero-based indexing, so the first element is at index 0. In a DataFrame, the index labels each row. *Module: 01-python-foundations, 06-data-skills*

**Inference** — In ML, the process of using a trained model to generate predictions or outputs from new input. When you send a prompt to Claude and get a response, that is inference. *Module: 02-how-llms-work*

**Integer** — A whole number without a decimal point, like `42` or `-3`. Used for counts (number of neurons, sample sizes). *Module: 01-python-foundations*

**Interquartile range (IQR)** — The range between the 25th and 75th percentiles of your data. It captures the middle 50% and is more robust to outliers than the full range. *Module: 06-data-skills*

**IP address** — A numerical label (like `192.168.1.1`) assigned to each device on a network. `127.0.0.1` (localhost) always refers to your own computer. *Module: 07-ai-research-workflows*

## J

**JSON (JavaScript Object Notation)** — A lightweight text format for structured data, used heavily in APIs. It looks like nested Python dictionaries and lists. API responses from Claude arrive as JSON. *Module: 01-python-foundations, 05-claude-api*

**Jupyter notebook** — An interactive document (`.ipynb` file) that mixes code cells you can run with text cells for explanation. This entire tutorial is built with Jupyter notebooks. *Module: 01-python-foundations*

## K

**Kernel** — In Jupyter, the background process that actually executes your code. If your notebook hangs, restarting the kernel is the equivalent of rebooting the computational engine. *Module: 01-python-foundations*

**Key-value pair** — A pairing of a name (key) with its associated data (value), the building block of dictionaries and JSON. *Example: `{"gene": "SCN9A", "role": "pain signaling"}`.* *Module: 01-python-foundations*

## L

**Library** — A collection of pre-written Python code you can use in your own programs. pandas, numpy, matplotlib, and anthropic are all libraries. Using libraries means you do not have to write everything from scratch. *Module: 01-python-foundations*

**List** — An ordered, changeable collection of items in Python, written with square brackets. *Example: `pain_genes = ["TRPV1", "SCN9A", "OPRM1"]`.* *Module: 01-python-foundations*

**LLM (Large Language Model)** — An AI model trained on massive amounts of text that can generate, summarize, translate, and reason about language. Claude and GPT-4 are LLMs. *Module: 02-how-llms-work*

**Localhost** — The hostname that refers to your own computer (`127.0.0.1`). When you run a Jupyter server, it is typically accessible at `localhost:8888`. *Module: 07-ai-research-workflows*

**Log2 fold change** — The base-2 logarithm of a fold change. A log2FC of 1 means the value doubled; -1 means it halved. Standard in differential expression analysis because it makes up- and down-regulation symmetric. *Module: 06-data-skills*

**Loop** — Code that repeats a block of instructions. See *for loop* and *while loop*. *Module: 01-python-foundations*

## M

**MCP (Model Context Protocol)** — An open protocol that lets AI models connect to external tools and data sources. Think of it as giving Claude the ability to use specialized software (databases, APIs, lab tools) through a standardized interface. *Module: 04-mastering-claude-code, 07-ai-research-workflows*

**MCP server** — A program that implements the MCP protocol to expose specific capabilities (like searching PubMed or querying a database) to AI models. *Module: 04-mastering-claude-code, 07-ai-research-workflows*

**Mean** — The arithmetic average of a set of values. Sensitive to outliers — a single very high pain score can skew the group mean. *Module: 06-data-skills*

**Median** — The middle value when data is sorted. More robust than the mean when your data has outliers or is skewed. *Module: 06-data-skills*

**Method** — A function that belongs to an object. When you write `df.describe()`, `describe()` is a method of the DataFrame object `df`. *Module: 01-python-foundations*

**Model** — In AI, a trained system that takes input and produces output. "The model" usually refers to the LLM itself (e.g., Claude). In statistics, a model is a mathematical representation of a process (e.g., linear regression). *Module: 02-how-llms-work*

**Module** — In Python, a single `.py` file that contains code you can import. Also used informally to mean a section of this tutorial. *Module: 01-python-foundations*

**Multimodal** — An AI model that can process multiple types of input — text, images, audio, or video. Claude can accept both text and images, making it useful for analyzing microscopy figures or gel images. *Module: 02-how-llms-work, 08-ai-landscape*

**Multiple testing correction** — Statistical adjustments applied when performing many hypothesis tests simultaneously to avoid inflating false positives. Bonferroni and Benjamini-Hochberg are common methods. Essential for RNA-seq differential expression. *Module: 06-data-skills*

## N

**Next-token prediction** — The fundamental task LLMs are trained on: given all preceding text, predict the most likely next piece of text (token). All of Claude's capabilities emerge from this deceptively simple training objective. *Module: 02-how-llms-work*

**Normal distribution** — The bell-shaped curve where most values cluster around the mean. Many statistical tests assume your data follows this distribution; checking this assumption matters before running t-tests on pain scores. *Module: 06-data-skills*

**Null hypothesis** — The default assumption in hypothesis testing that there is no effect or no difference. You are testing whether your data provides enough evidence to reject it. *Module: 06-data-skills*

## O

**Object** — In Python, everything is an object — a thing that has data (attributes) and behaviors (methods). A DataFrame is an object; so is a string, a number, or a plot. *Module: 01-python-foundations*

**Operating system (OS)** — The software that manages your computer's hardware and provides services to programs. macOS, Windows, and Linux are operating systems. *Module: 04-mastering-claude-code*

**Outlier** — A data point that is far from the rest of the values. One mouse with an unusually high pain threshold could be an outlier. Deciding whether to include or exclude outliers is a critical analytical choice. *Module: 06-data-skills*

## P

**Package** — A collection of Python modules distributed together. "Package" and "library" are often used interchangeably in practice. You install packages with pip. *Module: 01-python-foundations*

**Pandas** — The most important Python library for data analysis. It provides the DataFrame, tools for reading CSV/Excel files, filtering, grouping, and summarizing data. *Module: 01-python-foundations, 06-data-skills*

**Parameter** — In Python, a variable name listed in a function definition that receives a value when the function is called. In ML, a numerical value inside the model that is adjusted during training — large language models have billions of these. *Module: 01-python-foundations (Python sense), 02-how-llms-work (ML sense)*

**PATH** — An environment variable that tells your operating system where to look for executable programs. When a command is "not found," it is often a PATH issue. *Module: 04-mastering-claude-code*

**Pip** — Python's package installer. `pip install pandas` downloads and installs the pandas library. Always use pip inside a virtual environment to avoid conflicts. *Module: 01-python-foundations*

**Port** — A numbered channel (like 8888 for Jupyter or 443 for HTTPS) that allows multiple network services to run on the same computer simultaneously. *Module: 07-ai-research-workflows*

**Pre-training** — The initial phase of training an LLM on a massive text corpus to learn language patterns, facts, and reasoning abilities. Fine-tuning and RLHF come after pre-training. *Module: 02-how-llms-work*

**Process** — A running instance of a program on your computer. When you start a Jupyter server, it becomes a process. *Module: 04-mastering-claude-code*

**Prompt** — The text input you give to an LLM. The quality of your prompt largely determines the quality of the response. *Module: 03-prompt-engineering*

**Prompt engineering** — The skill of crafting effective prompts to get the best results from an LLM. Includes techniques like chain of thought, few-shot examples, and role assignment. *Module: 03-prompt-engineering*

**P-value** — The probability of observing results as extreme as yours if the null hypothesis were true. A p-value of 0.01 means there is a 1% chance of seeing this result by random chance alone. It does not tell you the probability that your hypothesis is correct. *Module: 06-data-skills*

## R

**RAG (Retrieval-Augmented Generation)** — A technique that gives an LLM access to external information (like your lab's paper database) by retrieving relevant documents and including them in the prompt. This reduces hallucination and keeps answers grounded in your actual data. *Module: 07-ai-research-workflows*

**Rate limit** — A cap on how many API requests you can make in a given time period. If your script sends too many requests too quickly, the API will temporarily reject them. *Module: 05-claude-api*

**Relative path** — A file path defined relative to your current directory (e.g., `../data/results.csv` means "go up one folder, then into data"). Contrast with *absolute path*. *Module: 04-mastering-claude-code*

**REST API** — A widely used style of web API where you interact with resources using standard HTTP methods (GET, POST, etc.). The Claude API is a REST API. *Module: 05-claude-api*

**Return value** — The output a function gives back when it finishes. In `result = calculate_sem(scores)`, the SEM number is the return value. *Module: 01-python-foundations*

**RLHF (Reinforcement Learning from Human Feedback)** — A training technique where human evaluators rank model outputs, and the model learns to prefer responses humans rate higher. This is a key part of how Claude was trained to be helpful, harmless, and honest. *Module: 02-how-llms-work*

**Root** — The top-level directory of a filesystem (`/` on macOS/Linux). Also refers to the administrative superuser account on Unix systems. *Module: 04-mastering-claude-code*

## S

**Sampling** — In AI, the process of selecting the next token during text generation, often with some randomness controlled by temperature. In statistics, selecting a subset of a population for study. *Module: 02-how-llms-work (AI sense), 06-data-skills (stats sense)*

**Sandbox** — A restricted environment where code can run without affecting the rest of your system. Provides safety when executing untrusted or experimental code. *Module: 04-mastering-claude-code*

**Scatter plot** — A chart plotting individual data points on two axes. Useful for visualizing the relationship between two measurements, such as TRPV1 expression level vs. calcium response amplitude. *Module: 06-data-skills*

**Script** — A file containing Python code (`.py`) that runs from top to bottom when executed. Contrast with a notebook, which runs cell by cell interactively. *Module: 01-python-foundations*

**SEM (Standard Error of the Mean)** — A measure of how precisely you have estimated the population mean. Smaller SEM means more precision. Commonly shown as error bars on bar graphs in pain research papers. *Module: 06-data-skills*

**Shell** — The program that interprets your text commands in the terminal. Bash and zsh are common shells on macOS. *Module: 04-mastering-claude-code*

**Softmax** — A mathematical function that converts a list of numbers into probabilities that sum to 1. It is the final step in how an LLM assigns probabilities to each possible next token. *Module: 02-how-llms-work*

**SSH (Secure Shell)** — A protocol for securely connecting to and running commands on a remote computer. Used to access lab servers or cloud computing resources. *Module: 07-ai-research-workflows*

**Standard deviation** — A measure of how spread out values are from the mean. A high SD in your behavioral data means high variability between animals. *Module: 06-data-skills*

**Statistical significance** — The conclusion that an observed result is unlikely to be due to chance alone, typically when p < 0.05. Significance does not imply biological importance — always consider effect size too. *Module: 06-data-skills*

**Stdin/stdout/stderr** — The three standard data streams for a program: input (stdin), normal output (stdout), and error messages (stderr). When you see error messages in your terminal, they come through stderr. *Module: 04-mastering-claude-code*

**String** — A sequence of text characters in Python, enclosed in quotes. `"TRPV1"`, `'dorsal root ganglion'`, and `"p = 0.003"` are all strings. *Module: 01-python-foundations*

**Sudo** — A command that runs another command with administrator privileges. Use cautiously — it bypasses normal safety restrictions. *Module: 04-mastering-claude-code*

**System prompt** — Hidden instructions given to an LLM that shape its behavior before the user's conversation begins. When you tell Claude "You are an expert neuroscience research assistant," that acts as a system prompt. *Module: 03-prompt-engineering, 05-claude-api*

## T

**Temperature** — A setting that controls how random or creative an LLM's responses are. Temperature 0 gives the most deterministic (consistent) answers; higher values produce more varied and creative output. Use low temperature for data analysis, higher for brainstorming. *Module: 02-how-llms-work, 05-claude-api*

**Terminal** — The application that provides a CLI on your computer. On macOS, it is called Terminal (or you may use iTerm2). *Module: 01-python-foundations, 04-mastering-claude-code*

**Token** — The basic unit an LLM reads and generates. Roughly 3/4 of a word in English — "nociceptor" might be split into "noci" + "ceptor." Token count determines cost and context window usage. *Module: 02-how-llms-work, 05-claude-api*

**Tokenizer** — The component that splits text into tokens before an LLM processes it. Different models use different tokenizers, which is why token counts can vary. *Module: 02-how-llms-work*

**Top-p (nucleus sampling)** — A sampling parameter that limits token selection to the smallest set of tokens whose combined probability exceeds p. Top-p of 0.9 means the model considers only the tokens that make up the top 90% of probability mass. *Module: 02-how-llms-work, 05-claude-api*

**Training** — The process of teaching a model by exposing it to data and adjusting its parameters to improve performance. An LLM is trained on vast amounts of text over weeks or months using enormous computing resources. *Module: 02-how-llms-work*

**Transformer** — The neural network architecture behind all modern LLMs, introduced in the 2017 paper "Attention Is All You Need." Its key innovation is the attention mechanism, which allows the model to consider relationships between all words simultaneously. *Module: 02-how-llms-work*

**T-test** — A statistical test comparing the means of two groups. Used constantly in pain research — e.g., comparing withdrawal thresholds between drug-treated and vehicle groups. Assumes roughly normal distributions and similar variances. *Module: 06-data-skills*

**Tuple** — An ordered, unchangeable collection in Python, written with parentheses. Like a list, but once created it cannot be modified. *Example: `coordinates = (4.2, 7.8)` for an x-y position on a microscopy image.* *Module: 01-python-foundations*

## U

**URL (Uniform Resource Locator)** — A web address like `https://api.anthropic.com/v1/messages`. URLs point to specific resources on the internet. *Module: 05-claude-api*

## V

**Variable** — A named container that stores a value in your program. `threshold = 4.5` creates a variable called `threshold` holding the number 4.5. *Module: 01-python-foundations*

**Venv / Virtual environment** — An isolated Python installation that keeps one project's packages separate from another's. This tutorial uses a venv at `.venv/` so its packages do not interfere with anything else on your system. *Module: 01-python-foundations*

**Volcano plot** — A scatter plot showing statistical significance (-log10 p-value) vs. magnitude of change (log2 fold change) for every gene in a differential expression analysis. Points in the upper corners are both statistically significant and biologically meaningful. *Module: 06-data-skills*

## W

**Webhook** — A mechanism where a server automatically sends data to a URL when a specific event happens. Like a notification system — e.g., getting a message when a long-running analysis finishes. *Module: 07-ai-research-workflows*

**While loop** — Code that repeats as long as a condition remains true. Less common than for loops in data analysis, but useful for things like retrying an API call until it succeeds. *Module: 01-python-foundations*

**Worktree** — A Git feature that lets you check out multiple branches simultaneously in different directories. Useful for comparing two versions of an analysis side by side. *Module: 04-mastering-claude-code*

## Z

**Zero-shot** — Asking an LLM to perform a task without providing any examples. The opposite of few-shot. Works well for straightforward tasks but may need examples for complex or domain-specific formatting. *Module: 03-prompt-engineering*

---

*Last updated: 2026-03-25*
