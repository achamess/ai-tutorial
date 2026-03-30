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
    # Module 6.2: Evaluating and Debugging Code

    ## How to Read, Evaluate, and Fix Code You Didn't Write

    Claude (and other AI tools) will write most of your code. But **you are still responsible for the results**. Just like you'd never trust a core facility's output without checking it, you should never trust AI-generated code without evaluation.

    This notebook teaches you:
    1. How to read code and understand what it does
    2. Red flags that signal problems
    3. How to systematically check if code is correct
    4. How to debug when things go wrong

    The goal isn't to become an expert programmer. It's to become an **informed evaluator** — like being a PI who can critically evaluate a postdoc's experimental protocol even if you haven't run that exact assay yourself.

    **References:** [Missing Semester Lecture 7: Debugging and Profiling](https://missing.csail.mit.edu/2020/debugging-profiling/) | [Python docs: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Decomposition and Design](01-decomposition-and-design.py) | [Module Index](../README.md) | [Next: Reproducibility and Project Structure \u2192](03-reproducibility-and-project-structure.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Why this matters for your work**
    >
    > - Claude generates code that looks correct but may have subtle bugs -- wrong column names, off-by-one errors, inverted filtering logic. If you can't evaluate and debug AI-generated code, you can't trust your screening results or statistical analyses.
    > - A 2024 study found that developers using AI coding assistants introduced more security vulnerabilities when they couldn't evaluate the generated code. The same principle applies to scientific code: unchecked errors propagate silently into your figures and conclusions.
    > - When Claude writes a function to rank your NaV1.7 binder candidates by composite score, you need to verify it's weighting Kd, selectivity, and thermostability correctly -- not just that it runs without errors.
    > - Debugging is also how you learn. Every bug you fix in AI-generated code teaches you something about Python that makes your next prompt better.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 1. How to Read Code You Didn't Write

    Reading code is like reading a methods section. You don't need to understand every detail — you need to understand:
    1. **What goes in** (inputs, parameters)
    2. **What comes out** (return values, files created)
    3. **What the key decisions are** (thresholds, filters, transformations)

    ### Strategy: Start from the outside, work inward

    Don't read code line by line from the top. Instead:
    1. Read the **function/variable names** — what do they suggest?
    2. Read the **docstrings/comments** — what does the author say it does?
    3. Look at the **inputs and outputs** — what data flows through?
    4. Only then read the **logic** — how does it transform input to output?
    """)
    return


@app.cell
def _():
    # Practice: Read this function using the outside-in strategy
    # Don't try to understand every line — answer the questions below it

    import pandas as pd
    import numpy as np

    def classify_drg_neurons(traces_df, capsaicin_window, kcl_window,
                              response_threshold=0.20, baseline_frames=30):
        """
        Classify DRG neurons as nociceptors vs non-nociceptors based on
        calcium imaging responses to capsaicin and KCl.
    
        Nociceptor = responds to capsaicin (TRPV1+)
        Non-nociceptor = responds to KCl but not capsaicin
        Non-neuronal = no response to KCl
    
        Parameters:
            traces_df: DataFrame, rows=frames, columns=cell_IDs, values=fluorescence
            capsaicin_window: tuple (start_frame, end_frame) for capsaicin application
            kcl_window: tuple (start_frame, end_frame) for KCl application
            response_threshold: delta-F/F0 threshold for calling a response
            baseline_frames: number of initial frames for baseline calculation
    
        Returns:
            DataFrame with columns: cell_id, classification, capsaicin_response, kcl_response
        """
        results = []
    
        for cell_id in traces_df.columns:
            trace = traces_df[cell_id].values
        
            # Calculate baseline
            f0 = np.mean(trace[:baseline_frames])
            delta_f = (trace - f0) / f0
        
            # Check responses in each window
            cap_response = np.max(delta_f[capsaicin_window[0]:capsaicin_window[1]])
            kcl_response = np.max(delta_f[kcl_window[0]:kcl_window[1]])
        
            # Classify
            if cap_response > response_threshold:
                classification = "nociceptor"
            elif kcl_response > response_threshold:
                classification = "non-nociceptor"
            else:
                classification = "non-neuronal"
        
            results.append({
                "cell_id": cell_id,
                "classification": classification,
                "capsaicin_response": round(cap_response, 3),
                "kcl_response": round(kcl_response, 3),
            })
    
        return pd.DataFrame(results)

    print("Function loaded. Answer the questions in the next cell.")
    return classify_drg_neurons, np, pd


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Questions (answer without re-reading the code line by line)

    1. What does this function take as input?
    2. What does it return?
    3. What are the three possible classifications?
    4. What threshold determines if a cell "responds"?
    5. Is a cell that responds to BOTH capsaicin and KCl classified as a nociceptor or non-nociceptor?

    If you could answer all 5 questions from the function name, docstring, and a quick skim — you can read code.
    """)
    return


@app.cell
def _(classify_drg_neurons, np, pd):
    # Let's test it to confirm our understanding

    np.random.seed(42)
    n_frames = 300
    n_cells = 8

    # Simulate calcium imaging data
    simulated_traces = pd.DataFrame({
        f"cell_{i}": 500 + np.random.normal(0, 10, n_frames)
        for i in range(n_cells)
    })

    # Capsaicin applied at frames 100-130, KCl at frames 200-230
    capsaicin_window = (100, 130)
    kcl_window = (200, 230)

    # Make some cells nociceptors (respond to capsaicin)
    for cell in ["cell_0", "cell_3", "cell_5"]:
        simulated_traces.loc[105:120, cell] += 200  # capsaicin response
        simulated_traces.loc[205:220, cell] += 150  # also respond to KCl

    # Make some cells non-nociceptors (respond to KCl only)
    for cell in ["cell_1", "cell_6"]:
        simulated_traces.loc[205:220, cell] += 180  # KCl response only

    # cells 2, 4, 7 = non-neuronal (no response to either)

    results = classify_drg_neurons(simulated_traces, capsaicin_window, kcl_window)
    print(results.to_string(index=False))
    print()
    print("Classification counts:")
    print(results["classification"].value_counts().to_string())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 2. Red Flags in Code

    When you're evaluating code that Claude (or anyone) wrote, here are warning signs — like seeing contamination in a culture dish or inconsistent controls.

    ### Red Flag Checklist

    | Red Flag | Why It's Bad | Lab Analogy |
    |---|---|---|
    | Hardcoded file paths (`/Users/john/data/...`) | Won't work on your machine | Protocol that references specific equipment by room number |
    | No error handling on file/API operations | Crashes silently or gives misleading results | No positive/negative controls |
    | Magic numbers with no explanation | Can't tell if thresholds are appropriate | Unlabeled reagent bottles |
    | Commented-out code left in | Confusing — is it needed or not? | Crossed-out steps in a protocol |
    | `except: pass` (catch all errors, do nothing) | Hides problems completely | Throwing away failed samples without noting it |
    | Variable named `data`, `x`, `temp`, `stuff` | Can't tell what it contains | Unlabeled tubes |

    Let's look at examples:
    """)
    return


@app.cell
def _(pd):
    # RED FLAG DEMO: Spot the problems in this code

    import json

    def analyze(f):
        data = pd.read_csv(f)
        data = data[data["value"] > 3.7]          # Why 3.7? What does "value" mean?
        data["result"] = data["value"] * 0.0821    # What is 0.0821? Where does it come from?
        # data = data.dropna()                      # Was this important? Why is it commented out?
        data.to_csv("/Users/someone/results.csv")  # Hardcoded path — won't work for you
        return data

    print("Can you spot all the red flags? (See markdown cell below)")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Red flags in the code above:

    1. **`def analyze(f)`** — function name is vague, parameter `f` is unclear
    2. **`data["value"] > 3.7`** — magic number. What is 3.7? Why that threshold?
    3. **`* 0.0821`** — another magic number. Is this a conversion factor? For what units?
    4. **Commented-out `dropna()`** — are there NaN values? Does dropping them matter?
    5. **Hardcoded output path** — will crash on any other machine
    6. **No error handling** — what if the file doesn't exist? What if "value" column is missing?
    7. **Variable named `data`** — reused multiple times for different things

    Here's how you'd ask Claude to fix it:
    """)
    return


@app.cell
def _(pd):
    # CLEANED VERSION — same logic, but you can actually evaluate it

    from pathlib import Path

    # Configuration
    FLUORESCENCE_BASELINE_THRESHOLD = 3.7  # AU — cells below this are likely dead/debris
    AU_TO_DELTA_F_FACTOR = 0.0821          # Conversion: arbitrary units to delta-F (calibration from 2025-01-15)


    def filter_and_convert_traces(input_csv_path, output_csv_path,
                                   baseline_threshold=FLUORESCENCE_BASELINE_THRESHOLD,
                                   conversion_factor=AU_TO_DELTA_F_FACTOR):
        """
        Filter calcium imaging traces by baseline fluorescence and convert units.
    
        Removes cells with low baseline fluorescence (likely dead or debris),
        then converts arbitrary fluorescence units to delta-F values.
    
        Parameters:
            input_csv_path: Path to CSV with columns including 'fluorescence_au'
            output_csv_path: Path where filtered results will be saved
            baseline_threshold: minimum fluorescence (AU) to keep a cell
            conversion_factor: multiplier to convert AU to delta-F
    
        Returns:
            DataFrame with filtered cells and converted values
        """
        input_path = Path(input_csv_path)
        if not input_path.exists():
            raise FileNotFoundError(f"Input file not found: {input_path}")
    
        raw_traces = pd.read_csv(input_path)
    
        if "fluorescence_au" not in raw_traces.columns:
            raise ValueError(f"Expected column 'fluorescence_au' not found. "
                            f"Available columns: {list(raw_traces.columns)}")
    
        # Filter out dead cells / debris
        viable_cells = raw_traces[raw_traces["fluorescence_au"] > baseline_threshold].copy()
        n_removed = len(raw_traces) - len(viable_cells)
        print(f"Removed {n_removed}/{len(raw_traces)} cells below baseline threshold ({baseline_threshold} AU)")
    
        # Handle missing values
        n_missing = viable_cells["fluorescence_au"].isna().sum()
        if n_missing > 0:
            print(f"Warning: dropping {n_missing} rows with missing fluorescence values")
            viable_cells = viable_cells.dropna(subset=["fluorescence_au"])
    
        # Convert units
        viable_cells["delta_f"] = viable_cells["fluorescence_au"] * conversion_factor
    
        # Save
        output_path = Path(output_csv_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        viable_cells.to_csv(output_path, index=False)
        print(f"Saved {len(viable_cells)} cells to {output_path}")
    
        return viable_cells

    print("Clean version defined. Compare with the messy version above.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 3. The "What Could Go Wrong?" Checklist

    Before running any code on real data, walk through this checklist. It's like doing a dry run of an experiment.

    ### For any data analysis code:

    - [ ] **Wrong input**: What if the file format is slightly different? (extra columns, different delimiter, different encoding)
    - [ ] **Missing data**: What happens with NaN/empty values? Does the code handle them or crash?
    - [ ] **Unexpected values**: What if numbers are negative when you expect positive? What if strings have extra whitespace?
    - [ ] **Empty results**: What if filtering removes ALL rows? Does the code handle an empty DataFrame?
    - [ ] **Scale issues**: What if you have 10 samples instead of 10,000? Or 10,000,000?

    ### For code that calls external services (APIs, databases):

    - [ ] **Service down**: What if the API returns an error? (PubMed is down, Claude API times out)
    - [ ] **Rate limits**: What if you hit usage limits? Does the code retry or crash?
    - [ ] **Changed format**: What if the API changes its response format?

    ### For code that writes output:

    - [ ] **Overwriting**: Will it overwrite previous results without warning?
    - [ ] **Disk space**: Will output files be unexpectedly large?
    - [ ] **Permissions**: Can it write to the specified directory?

    Let's practice:
    """)
    return


@app.cell
def _():
    # What could go wrong with this function?
    # Read it and think about failure modes before running the test cases below

    def compute_response_rate(traces_df, stimulus_frame, threshold=0.2):
        """
        Compute the fraction of cells that respond to a stimulus.
    
        Parameters:
            traces_df: DataFrame where each column is a cell's delta-F/F0 trace
            stimulus_frame: frame number when stimulus was applied
            threshold: delta-F/F0 above which a cell is "responsive"
    
        Returns:
            float: fraction of cells that responded (0.0 to 1.0)
        """
        n_responsive = 0
        n_total = len(traces_df.columns)
    
        for cell_id in traces_df.columns:
            # Look at the 20 frames after stimulus
            post_stimulus = traces_df[cell_id].iloc[stimulus_frame:stimulus_frame + 20]
            if post_stimulus.max() > threshold:
                n_responsive += 1
    
        return n_responsive / n_total

    print("Function loaded. Let's test failure modes...")
    return (compute_response_rate,)


@app.cell
def _(compute_response_rate, np, pd):
    # Test case 1: Normal case — should work fine
    np.random.seed(42)
    normal_traces = pd.DataFrame({f'cell_{i}': np.random.normal(0, 0.05, 100) for i in range(10)})
    normal_traces.loc[55:65, 'cell_3'] += 0.5
    _rate = compute_response_rate(normal_traces, stimulus_frame=50)
    print(f'Test 1 (normal): Response rate = {_rate:.1%}  (expected ~10%)')  # One responsive cell
    return (normal_traces,)


@app.cell
def _(compute_response_rate, normal_traces):
    # Test case 2: What if stimulus_frame is near the end of the recording?
    # The function looks at 20 frames after stimulus, but what if there aren't 20 frames left?
    try:
        _rate = compute_response_rate(normal_traces, stimulus_frame=95)
        print(f'Test 2 (near end): Response rate = {_rate:.1%}')
        print("  Hmm, it didn't crash but it only checked 5 frames instead of 20.")
        print('  This could cause false negatives — a silent error!')
    except Exception as e:
        print(f'Test 2 (near end): ERROR — {e}')
    return


@app.cell
def _(compute_response_rate, pd):
    # Test case 3: What if the DataFrame is empty (no cells)?
    empty_traces = pd.DataFrame()
    try:
        _rate = compute_response_rate(empty_traces, stimulus_frame=50)
        print(f'Test 3 (empty): Response rate = {_rate:.1%}')
    except ZeroDivisionError:
        print('Test 3 (empty): CRASHED with ZeroDivisionError (division by zero)')
        print('  The function divides by n_total, which is 0 for an empty DataFrame.')
    except Exception as e:
        print(f'Test 3 (empty): ERROR — {type(e).__name__}: {e}')
    return


@app.cell
def _(compute_response_rate, normal_traces, np):
    # Test case 4: What if traces contain NaN values? (common with dropped frames)
    nan_traces = normal_traces.copy()
    nan_traces.loc[55:60, 'cell_3'] = np.nan
    _rate = compute_response_rate(nan_traces, stimulus_frame=50)  # Dropped frames right during the response!
    print(f'Test 4 (NaN values): Response rate = {_rate:.1%}')
    print('  Cell 3 had a real response, but NaN values may mask it.')
    print('  np.max of a series with NaN depends on the implementation — could be wrong.')
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### What we found:

    This simple, reasonable-looking function has at least 3 failure modes:
    1. **Near-end stimulus**: silently checks fewer frames than expected
    2. **Empty input**: crashes with ZeroDivisionError
    3. **NaN values**: may give incorrect results

    None of these would be caught by just running the function once on normal data. You need to **think about edge cases** — just like you think about what controls you need in an experiment.

    When Claude gives you code, try it with:
    - Normal input (sanity check)
    - Edge cases (empty, very large, very small)
    - Known answers (data where you already know the right result)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 4. The Testing Mindset: "How Do I Know This Is Correct?"

    In the lab, you always run controls. In code, the equivalent is **testing with known answers**.

    | Lab | Code |
    |---|---|
    | Positive control | Input where you know the right answer |
    | Negative control | Input that should give no result / zero |
    | Standard curve | Range of inputs with known outputs |
    | Technical replicate | Run the same input twice, get the same answer |

    You don't need a formal testing framework. Just ask yourself: **"What input would I need to give this code to verify it's doing the right thing?"**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Key concept:** "How do I know this is correct?" is the single most important question you can ask about any piece of code -- AI-generated or otherwise. Before trusting any analysis result, you need an answer to this question. For numerical code, the answer is always the same: test with inputs where you already know the correct output. If `calculate_ec50()` returns a known EC50 for a known dose-response curve, you can trust it on unknown data.

    > **Warning:** Never trust AI-generated code without evaluation. Claude writes code that looks syntactically correct and often runs without errors -- but "runs without errors" is not the same as "produces correct results." A script that silently drops 30% of your binder candidates due to a wrong merge key is far more dangerous than one that crashes with a KeyError. Always check outputs against your domain knowledge: does the number of rows make sense? Are the values in a reasonable range? Do the top hits match your intuition from looking at the raw data?
    """)
    return


@app.cell
def _(np):
    # Example: Testing a dose-response curve fitting function

    from scipy.optimize import curve_fit

    def hill_equation(concentration, ec50, hill_coefficient, bottom, top):
        """Standard 4-parameter Hill equation for dose-response curves."""
        return bottom + (top - bottom) / (1 + (ec50 / concentration) ** hill_coefficient)


    def fit_dose_response(concentrations, responses):
        """Fit a Hill equation to dose-response data.
    
        Returns dict with ec50, hill_coefficient, bottom, top.
        """
        try:
            popt, _ = curve_fit(
                hill_equation, concentrations, responses,
                p0=[np.median(concentrations), 1.0, min(responses), max(responses)],
                maxfev=10000
            )
            return {
                "ec50": popt[0],
                "hill_coefficient": popt[1],
                "bottom": popt[2],
                "top": popt[3],
            }
        except RuntimeError as e:
            return {"error": str(e)}


    # ---- TESTING WITH KNOWN ANSWERS ----

    # "Positive control": Generate data FROM the Hill equation with known parameters
    known_ec50 = 100  # nM
    known_hill = 1.5
    known_bottom = 0.0
    known_top = 1.0

    test_concentrations = np.array([1, 3, 10, 30, 100, 300, 1000, 3000])
    # Generate "perfect" data (no noise)
    perfect_responses = hill_equation(test_concentrations, known_ec50, known_hill, known_bottom, known_top)

    fit_result = fit_dose_response(test_concentrations, perfect_responses)

    print("Positive control (known parameters, no noise):")
    print(f"  Expected EC50:  {known_ec50} nM")
    print(f"  Fitted EC50:    {fit_result['ec50']:.1f} nM")
    print(f"  Expected Hill:  {known_hill}")
    print(f"  Fitted Hill:    {fit_result['hill_coefficient']:.2f}")
    print(f"  Match: {'PASS' if abs(fit_result['ec50'] - known_ec50) < 1 else 'FAIL'}")
    return (
        fit_dose_response,
        known_ec50,
        known_hill,
        perfect_responses,
        test_concentrations,
    )


@app.cell
def _(
    fit_dose_response,
    known_ec50,
    known_hill,
    np,
    perfect_responses,
    test_concentrations,
):
    # Now test with noisy data (more realistic)
    np.random.seed(42)
    noisy_responses = perfect_responses + np.random.normal(0, 0.05, len(test_concentrations))

    fit_noisy = fit_dose_response(test_concentrations, noisy_responses)

    print("Realistic test (known parameters + noise):")
    print(f"  Expected EC50:  {known_ec50} nM")
    print(f"  Fitted EC50:    {fit_noisy['ec50']:.1f} nM")
    print(f"  Expected Hill:  {known_hill}")
    print(f"  Fitted Hill:    {fit_noisy['hill_coefficient']:.2f}")
    print(f"  Close enough: {'PASS' if abs(fit_noisy['ec50'] - known_ec50) < 20 else 'FAIL'}")
    print()
    print("Key insight: With noisy data, the fit isn't perfect but should be close.")
    print("If EC50 came back as 5000 nM, you'd know something was wrong.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Quick Testing Strategy for AI-Generated Code

    When Claude gives you analysis code:

    1. **Create a tiny test case by hand** where you know the answer
    2. **Run the code on the test case** and check the output
    3. **Try an edge case** (empty input, one data point, huge numbers)
    4. **Run it on real data and spot-check** a few results manually

    This takes 5 minutes and can save you from publishing wrong results.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 5. Debugging Strategies

    When code doesn't work, don't panic. Debugging is systematic — like troubleshooting a failed experiment.

    ### Strategy 1: Read the Error Message

    Python error messages are actually quite informative. They tell you:
    - **What** went wrong (the error type)
    - **Where** it went wrong (the file and line number)
    - **Why** (the error message)

    **Reference**: See *The Missing Semester*, Lecture 7 (Debugging and Profiling) for more debugging techniques.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Decision point: When to debug yourself vs ask Claude to debug**
    >
    > | Situation | Debug yourself | Ask Claude | Why |
    > |-----------|---------------|------------|-----|
    > | Clear error message (KeyError, FileNotFoundError) | If you understand it | If you don't | Simple errors are good learning opportunities |
    > | Logic error (wrong results, no crash) | First pass -- check your assumptions | After you've localized the problem | You need domain knowledge to spot wrong biology |
    > | Complex traceback (deep library internals) | Rarely | Almost always | Claude excels at parsing stack traces through unfamiliar libraries |
    > | Performance issue (code is slow) | If you know profiling tools | If you don't | Claude can suggest vectorization, caching, algorithmic improvements |
    > | "It worked yesterday, broke today" | Check what changed (git diff) | If git diff doesn't reveal it | Version/environment changes are common culprits |
    >
    > **Rule of thumb:** Always try to understand *what* went wrong before asking Claude to fix it. Even a 30-second attempt to read the error message builds debugging intuition. But don't spend more than 5-10 minutes stuck -- that's when Claude pays for itself.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.vstack([
    mo.md(r"""
    ### Debugging Decision Tree

    """),
    mo.mermaid(
        """
        flowchart TD
            START["Got an error!"] --> READ["Read the error message<br>(last line first)"]
            READ --> TYPE{"What type<br>of error?"}
        
            TYPE -->|"KeyError /<br>ColumnNotFound"| KEY["Wrong column or<br>dictionary key name"]
            TYPE -->|"FileNotFoundError"| FILE["Wrong file path<br>or missing file"]
            TYPE -->|"TypeError"| TYPEE["Wrong data type<br>passed to function"]
            TYPE -->|"ValueError"| VAL["Right type but<br>invalid value"]
            TYPE -->|"Other / Logic bug<br>(wrong results)"| LOGIC["Code runs but<br>output is wrong"]
        
            KEY --> FIX1["Check: df.columns or<br>dict.keys() to see<br>actual names"]
            FILE --> FIX2["Check: does file exist?<br>Is the path relative<br>or absolute?"]
            TYPEE --> FIX3["Check: type() of each<br>variable in the<br>failing line"]
            VAL --> FIX4["Check: print the value<br>being passed -- is it<br>what you expect?"]
            LOGIC --> ISO["Isolate: add print()<br>at each step boundary<br>to find where data<br>goes wrong"]
        
            FIX1 --> APPLY["Apply fix"]
            FIX2 --> APPLY
            FIX3 --> APPLY
            FIX4 --> APPLY
            ISO --> APPLY
            APPLY --> TEST["Test with<br>known input"]
            TEST --> DONE{"Fixed?"}
            DONE -->|"Yes"| COMMIT["Commit the fix"]
            DONE -->|"No"| READ
        
            style START fill:#E24A33,color:#fff
            style COMMIT fill:#55A868,color:#fff
            style READ fill:#4878CF,color:#fff
            style ISO fill:#8172B2,color:#fff
        """
    ),
    mo.md(r"""

    This flowchart captures the systematic debugging process. The key insight: **always read the error message first** (many beginners skip this!) and **identify the error type** before trying to fix anything. Each error type has a specific diagnostic step.
    """)
    ])
    return


@app.cell
def _(pd):
    # Let's intentionally create some common errors and learn to read them
    try:
    # Error 1: KeyError — you asked for a column that doesn't exist
        _df = pd.DataFrame({'gene_name': ['SCN9A', 'SCN10A'], 'expression': [100, 200]})
        _result = _df['Gene_Name']
    except KeyError as e:  # Note the capitalization difference!
        print('ERROR 1: KeyError')
        print(f'  Message: {e}')
        print(f"  Translation: Column 'Gene_Name' doesn't exist. Available: {list(_df.columns)}")
        print(f'  Fix: Check column name spelling and capitalization.')
        print()
    return


@app.cell
def _(pd):
    # Error 2: FileNotFoundError — the file path is wrong
    try:
        _df = pd.read_csv('my_data/experiment_results.csv')
    except FileNotFoundError as e:
        print('ERROR 2: FileNotFoundError')
        print(f'  Message: {e}')
        print(f"  Translation: The file doesn't exist at that path.")
        print(f'  Fix: Check the file path. Use Path.exists() to verify before reading.')
        print()
    return


@app.cell
def _():
    # Error 3: TypeError — you passed the wrong type of data
    try:
        _result = 'expression level: ' + 42  # Can't add string and integer
    except TypeError as e:
        print('ERROR 3: TypeError')
        print(f'  Message: {e}')
        print(f'  Translation: You tried to combine incompatible types.')
        print(f"  Fix: Convert the number to string first: 'expression level: ' + str(42)")
        print()
    return


@app.cell
def _():
    # Error 4: ValueError — the data doesn't make sense for the operation
    try:
        concentration = float("10 nM")  # Can't convert string with units to float
    except ValueError as e:
        print("ERROR 4: ValueError")
        print(f"  Message: {e}")
        print(f"  Translation: The value '10 nM' can't be converted to a number because of the units.")
        print(f"  Fix: Strip the units first, or check your data for unexpected text in numeric columns.")
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Strategy 2: Isolate the Problem

    If a multi-step pipeline fails, figure out **which step** failed. Check the data at each step boundary.

    This is like troubleshooting a staining protocol — if you get no signal, you check: Did the fixation work? Did the primary antibody bind? Did the secondary work? Did the detection work?
    """)
    return


@app.cell
def _(pd):
    # Debugging a pipeline: add checkpoints

    def debug_pipeline_example():
        """A pipeline with a bug — let's find it."""
    
        # Step 1: Create data
        data = pd.DataFrame({
            "gene": ["SCN9A", "SCN10A", "KCNQ2", "KCNQ3", "TRPV1"],
            "fold_change": [2.5, -1.8, 3.1, 0.5, "N/A"],  # Note: "N/A" is a string!
            "p_value": [0.001, 0.05, 0.003, 0.8, 0.01]
        })
        print("CHECKPOINT 1 — after creating data:")
        print(data.dtypes)  # Check data types!
        print()
    
        # Step 2: Filter significant genes
        significant = data[data["p_value"] < 0.05]
        print(f"CHECKPOINT 2 — after filtering: {len(significant)} significant genes")
        print(significant)
        print()
    
        # Step 3: Try to compute something with fold_change
        try:
            significant["abs_fc"] = significant["fold_change"].apply(lambda x: abs(float(x)))
            print("CHECKPOINT 3 — after computing abs fold change:")
            print(significant)
        except (ValueError, TypeError) as e:
            print(f"CHECKPOINT 3 — ERROR: {e}")
            print(f"  Problem: fold_change column contains non-numeric values")
            print(f"  Values: {data['fold_change'].tolist()}")
            print(f"  Data types: {data['fold_change'].dtype}")
            print(f"  Fix: Clean the data before analysis — convert 'N/A' to NaN")

    debug_pipeline_example()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Strategy 3: Check Your Assumptions

    Most bugs come from **wrong assumptions** about the data. Common ones:

    - "I assumed all values were numeric" (but some are strings)
    - "I assumed the file had headers" (but it didn't)
    - "I assumed the data was sorted" (but it wasn't)
    - "I assumed there were no duplicates" (but there were)
    - "I assumed concentrations were in nM" (but they were in uM)

    **Quick assumption checks in pandas:**
    """)
    return


@app.cell
def _(pd):
    # Assumption-checking toolkit

    # Create some example data
    experiment_data = pd.DataFrame({
        "cell_id": ["c1", "c2", "c3", "c2", "c4"],  # Note: c2 appears twice!
        "response": [0.5, 0.8, None, 0.3, -0.1],        # Note: None and a negative value!
        "condition": ["vehicle", "drug", "drug", "vehicle", "drug"],
    })

    print("=== Assumption Checks ===")
    print()

    # Check 1: Data types
    print("Data types:")
    print(experiment_data.dtypes)
    print()

    # Check 2: Missing values
    print(f"Missing values per column:")
    print(experiment_data.isna().sum())
    print()

    # Check 3: Duplicates
    duplicated_ids = experiment_data[experiment_data["cell_id"].duplicated(keep=False)]
    print(f"Duplicate cell_ids: {len(duplicated_ids)} rows")
    if len(duplicated_ids) > 0:
        print(duplicated_ids)
    print()

    # Check 4: Value ranges
    print(f"Response range: {experiment_data['response'].min()} to {experiment_data['response'].max()}")
    print(f"Negative responses: {(experiment_data['response'] < 0).sum()}")
    print()

    # Check 5: Unique values in categorical columns
    print(f"Conditions: {experiment_data['condition'].unique()}")
    print(f"Condition counts: ")
    print(experiment_data["condition"].value_counts().to_string())
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 6. Common Failure Modes with AI-Generated Code

    After using Claude to write code for a while, you'll notice patterns in what can go wrong:

    ### 1. Plausible but wrong logic
    Claude writes code that runs without errors but gives subtly incorrect results. This is the most dangerous failure mode — like getting a Western blot with bands that look right but are actually non-specific.

    **Defense**: Always test with known answers.

    ### 2. Outdated APIs or syntax
    Claude might use a version of a library that's different from what you have installed.

    **Defense**: Check the error message — if it says a function doesn't exist, check the library documentation.

    ### 3. Overly complex solutions
    Claude sometimes writes elaborate code when a simple approach would work better.

    **Defense**: If you can't follow the logic, ask "Can you simplify this? I need to understand what it does."

    ### 4. Missing error handling
    First-draft code often assumes everything works perfectly.

    **Defense**: Ask "What happens if the input file is missing? What if the API call fails? Add error handling for common failures."

    ### 5. Hardcoded assumptions about your data
    Claude might assume column names, file formats, or data ranges that don't match your actual data.

    **Defense**: Before running on real data, check that column names and data types match what the code expects.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## 7. Exercise: Review This Script

    The following script is supposed to analyze behavioral assay data from a pain experiment — specifically, mechanical withdrawal thresholds (von Frey testing) before and after injecting CFA (Complete Freund's Adjuvant) to model inflammatory pain.

    It has **at least 5 intentional issues**. Your job is to find them.

    For each issue you find, note:
    1. What the problem is
    2. Why it matters (what could go wrong)
    3. How to fix it
    """)
    return


@app.cell
def _(pd):
    # === SCRIPT TO REVIEW ===
    # Analyze von Frey mechanical withdrawal thresholds
    # Compare baseline vs. post-CFA across treatment groups
    def analyze_von_frey(filepath):
        data = pd.read_csv(filepath)
        data['pct_change'] = (data['post_cfa'] - data['baseline']) / data['baseline'] * 100
        results = {}
        for group in ['vehicle', 'drug_low', 'drug_high']:
            group_data = data[data['group'] == group]  # Read data
            results[group] = {'mean_baseline': group_data['baseline'].mean(), 'mean_post_cfa': group_data['post_cfa'].mean(), 'mean_pct_change': group_data['pct_change'].mean(), 'n': len(group_data)}
        vehicle_change = results['vehicle']['mean_pct_change']
        drug_high_change = results['drug_high']['mean_pct_change']  # Calculate percent change from baseline for each mouse
        if drug_high_change > vehicle_change:
            conclusion = 'Drug REVERSES CFA-induced hypersensitivity'
        else:  # Get group means  
            conclusion = 'Drug has NO EFFECT on CFA-induced hypersensitivity'
        output = pd.DataFrame(results).T
        output.to_csv('/Users/someone/Desktop/results.csv')
        return conclusion
    print('Script loaded. Find the issues! (See next cell for hints)')  # Determine if drug is effective  # Save results
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Hints (try finding issues yourself first!)

    <details>
    <summary>Click to reveal hints</summary>

    Look for:
    1. Something wrong with the effectiveness comparison logic (think about which direction mechanical thresholds change with pain)
    2. Hardcoded values that shouldn't be hardcoded
    3. Missing error handling
    4. Statistical rigor issues
    5. Data validation issues
    6. A robustness issue with group names

    </details>
    """)
    return


@app.cell
def _():
    # YOUR REVIEW NOTES
    # Fill in the issues you found:

    issues_found = [
        {
            "issue": "Issue 1: ___",
            "why_it_matters": "___",
            "fix": "___",
        },
        {
            "issue": "Issue 2: ___",
            "why_it_matters": "___",
            "fix": "___",
        },
        {
            "issue": "Issue 3: ___",
            "why_it_matters": "___",
            "fix": "___",
        },
        # Add more as you find them...
    ]

    for i, issue in enumerate(issues_found, 1):
        print(f"Issue {i}: {issue['issue']}")
        print(f"  Why:  {issue['why_it_matters']}")
        print(f"  Fix:  {issue['fix']}")
        print()
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### Answer Key

    <details>
    <summary>Click to reveal answers</summary>

    **Issue 1: Reversed comparison logic**
    - CFA causes *hypersensitivity* (lower thresholds = more pain). So pct_change should be negative (thresholds decrease).
    - An effective drug would make pct_change *less negative* (closer to zero, or positive if it fully reverses).
    - The comparison `drug_high_change > vehicle_change` is checking if the drug group has a HIGHER percent change, but both should be negative. A less negative number IS greater. So the logic might accidentally be correct — but it's confusing and fragile. It would be wrong if thresholds increase (antinociceptive assay).
    - **Fix**: Be explicit about direction. Compare absolute values or use clear variable names like `hypersensitivity_score`.

    **Issue 2: Hardcoded output path**
    - `/Users/someone/Desktop/results.csv` won't work on your machine.
    - **Fix**: Accept output path as a parameter, or save relative to input file.

    **Issue 3: No error handling**
    - File might not exist. Columns might be named differently. Groups might not match.
    - **Fix**: Add try/except, validate column names, check that expected groups exist.

    **Issue 4: No statistical test**
    - The conclusion is based on comparing means with no p-value or confidence interval.
    - A mean difference could easily be due to chance.
    - **Fix**: Add a statistical test (t-test, Mann-Whitney) or at least report standard errors.

    **Issue 5: No data validation**
    - What if baseline is 0? (Division by zero in pct_change)
    - What if there are negative thresholds? (Doesn't make physical sense)
    - What if a group has only 1 mouse?
    - **Fix**: Validate data ranges before computing.

    **Issue 6: Hardcoded group names**
    - The function assumes groups are named exactly "vehicle", "drug_low", "drug_high".
    - If your data says "Vehicle" or "saline" or "10mg/kg", it silently produces empty results.
    - **Fix**: Either accept group names as parameters, or detect them from the data and confirm with the user.

    </details>
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---
    ## Key Takeaways

    1. **Read code outside-in**: function names and docstrings first, logic last
    2. **Watch for red flags**: magic numbers, hardcoded paths, missing error handling, vague names
    3. **Always ask "what could go wrong?"**: empty data, wrong types, missing values, edge cases
    4. **Test with known answers**: create positive and negative controls for your code, just like for experiments
    5. **Debug systematically**: read the error, isolate the step, check your assumptions
    6. **AI-generated code needs review**: it runs doesn't mean it's correct

    ### What to Say to Claude When Something Breaks

    Don't say: *"It doesn't work"*

    Say: *"I'm getting a KeyError on line 15 when I run this on my data. Here's the error message: [paste]. Here's what my data looks like: [paste first few rows]. The column names in my file are: [list them]."*

    The more context you give, the faster Claude can help you fix it.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Decomposition and Design](01-decomposition-and-design.py) | [Module Index](../README.md) | [Next: Reproducibility and Project Structure \u2192](03-reproducibility-and-project-structure.py)
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ---

    ## Further Reading

    - **[Missing Semester Lecture 7: Debugging and Profiling](https://missing.csail.mit.edu/2020/debugging-profiling/)** -- Systematic debugging techniques, logging, profiling tools, and how to diagnose performance issues.
    - **[Python Official Docs: Errors and Exceptions](https://docs.python.org/3/tutorial/errors.html)** -- Understanding Python error types, try/except blocks, and exception handling.
    - **[Real Python: Python Debugging with pdb](https://realpython.com/python-debugging-pdb/)** -- Hands-on guide to Python's built-in debugger, breakpoints, and step-through debugging.
    - **[Python Official Docs: The `assert` Statement](https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement)** -- Using assertions as sanity checks in your code.
    - **[NumPy: Debugging Tips](https://numpy.org/doc/stable/user/troubleshooting-importerror.html)** -- Common NumPy-specific issues and how to resolve them.
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
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


if __name__ == "__main__":
    app.run()

