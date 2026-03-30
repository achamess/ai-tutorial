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
    # Pre-Flight Check

    **What this notebook does:** Before diving into the tutorial, we need to make sure your environment is set up correctly. This notebook runs a series of checks — Python version, installed packages, virtual environment, API key — and reports what passed and what needs attention.

    Run every cell from top to bottom. Green checkmarks mean you are good to go. Red X marks mean something needs fixing before you proceed.

    **Why this matters:** Nothing kills momentum like a broken setup. In pain biology, you would never start a patch-clamp recording without checking your rig. Same principle here — five minutes of pre-flight saves hours of debugging later.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Complete Setup Guide](01-complete-setup-guide.py) | [Module Index](../README.md) | [Next: Your First Code \u2192](../01-python-foundations/01-your-first-code.py)
    """)
    return


@app.cell
def _():
    # We'll collect results as we go, then summarize at the end
    results = []
    return (results,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check 1: Python version

    The tutorial was built with Python 3.14. Older versions may work for early modules, but later notebooks depend on 3.14 features.
    """)
    return


@app.cell
def _(results):
    import sys

    major, minor = sys.version_info.major, sys.version_info.minor
    full_version = sys.version.split()[0]

    if major == 3 and minor >= 14:
        print(f"  Python {full_version} — correct!")
        results.append(("Python version", True))
    else:
        print(f"  Python {full_version} — expected 3.14+")
        print("   Fix: make sure you activated the .venv before launching marimo")
        results.append(("Python version", False))
    return (sys,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check 2: Key packages installed

    These are the core libraries used throughout the tutorial.
    """)
    return


@app.cell
def _(results):
    required_packages = {
        "marimo":     "marimo",       # Notebook infrastructure
        "pandas":     "pandas",       # Data manipulation (Modules 09-10)
        "numpy":      "numpy",        # Numerical computing
        "matplotlib": "matplotlib",   # Plotting
        "seaborn":    "seaborn",      # Statistical visualization
        "anthropic":  "anthropic",    # Claude API client (Modules 08-10)
    }

    all_found = True
    for display_name, import_name in required_packages.items():
        try:
            __import__(import_name)
            print(f"  {display_name}")
        except ImportError:
            print(f"  {display_name} — NOT FOUND")
            print(f"   Fix: pip install {display_name}")
            all_found = False

    results.append(("Key packages", all_found))
    if all_found:
        print("\nAll packages installed.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check 3: marimo installation

    The tutorial uses marimo notebooks. marimo runs using the Python from your active virtual environment — no separate kernel registration needed.
    """)
    return


@app.cell
def _(results):
    import subprocess
    import json

    try:
        output = subprocess.run(
            ["marimo", "--version"],
            capture_output=True, text=True, timeout=15
        )
        if output.returncode == 0:
            version = output.stdout.strip()
            print(f"  marimo {version} is installed.")
            results.append(("marimo", True))
        else:
            print("  marimo NOT found.")
            print("   Fix: pip install marimo")
            results.append(("marimo", False))
    except Exception as e:
        print(f"  Could not check marimo: {e}")
        results.append(("marimo", False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check 4: Virtual environment is active

    The `.venv/` virtual environment keeps this tutorial's packages separate from your system Python. If it is not active, you might be using the wrong Python or missing packages.
    """)
    return


@app.cell
def _(results, sys):
    import os
    executable = sys.executable
    venv_marker = os.path.join(os.path.dirname(os.path.dirname(executable)), 'pyvenv.cfg')
    if os.path.exists(venv_marker):
        print(f'  Virtual environment is active.')
        print(f'   Python executable: {executable}')
        results.append(('Virtual environment', True))
    else:
        print(f'  Virtual environment does NOT appear active.')
        print(f'   Python executable: {executable}')
        print("   Fix: run 'source .venv/bin/activate' in your terminal before launching marimo")
        results.append(('Virtual environment', False))
    return (os,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check 5: Anthropic API key

    Several modules (08-Claude API, 10-AI Research Workflows, and parts of 04-Prompt Engineering and 05-Mastering Claude Code) send requests to the Claude API. For that, you need an `ANTHROPIC_API_KEY` environment variable.

    This is **not** required for the early modules — you can start without it and add it later.
    """)
    return


@app.cell
def _(os, results):
    api_key = os.environ.get('ANTHROPIC_API_KEY')
    if api_key:
        masked = api_key[:8] + '...' + api_key[-4:]
        print(f'  ANTHROPIC_API_KEY is set ({masked})')
        results.append(('API key', True))
    else:  # Show only the first 8 characters for confirmation, never the full key
        print('  ANTHROPIC_API_KEY is NOT set.')
        print('   This is fine for Modules 01-07. You will need it for Modules 08-10.')
        print('   When ready, add to your shell profile:')
        print('   export ANTHROPIC_API_KEY="sk-ant-..."')
        results.append(('API key', False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Check 6: Quick smoke test

    Let's make sure Python actually runs code, creates variables, and can produce a plot. Think of this as the "electrode test pulse" before you start recording.
    """)
    return


@app.cell
def _(results):
    try:
        import numpy as np
        import matplotlib.pyplot as plt

        # Simulate a simple calcium imaging trace — fluorescence over time
        np.random.seed(42)
        time = np.linspace(0, 10, 200)  # 10 seconds
        baseline = 1.0
        # A calcium transient peaking around t=4s (like a nociceptor responding to capsaicin)
        signal = baseline + 2.5 * np.exp(-0.5 * ((time - 4) / 0.8) ** 2)
        noise = np.random.normal(0, 0.08, len(time))
        trace = signal + noise

        fig, ax = plt.subplots(figsize=(8, 3))
        ax.plot(time, trace, color="steelblue", linewidth=1)
        ax.set_xlabel("Time (s)")
        ax.set_ylabel("F/F₀")
        ax.set_title("Simulated calcium transient — nociceptor response to capsaicin")
        ax.axvline(x=2, color="red", linestyle="--", alpha=0.5, label="capsaicin application")
        ax.legend(frameon=False)
        plt.tight_layout()
        plt.show()

        print("\n  Variables, numpy, and matplotlib all work.")
        results.append(("Smoke test", True))

    except Exception as e:
        print(f"  Smoke test failed: {e}")
        results.append(("Smoke test", False))
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Summary
    """)
    return


@app.cell
def _(results):
    print("=" * 50)
    print("  PRE-FLIGHT CHECK RESULTS")
    print("=" * 50)

    passed = 0
    failed = 0
    for name, ok in results:
        status = "PASS" if ok else "FAIL"
        marker = "[x]" if ok else "[ ]"
        print(f"  {marker} {name}: {status}")
        if ok:
            passed += 1
        else:
            failed += 1

    print("-" * 50)
    print(f"  {passed}/{passed + failed} checks passed")
    print()

    if failed == 0:
        print("  You're ready! Everything looks good.")
        print("  Next step: open 01-python-foundations/01-your-first-code.py")
    elif failed == 1 and not dict(results).get("API key", True):
        # Only the API key is missing — that's fine for now
        print("  Almost there! The only thing missing is the API key,")
        print("  which you won't need until Module 08.")
        print("  You're clear to start: open 01-python-foundations/01-your-first-code.py")
    else:
        print("  Some checks failed. Fix the items marked [ ] above before continuing.")
        print("  If you're stuck, ask Claude Code for help — that's what it's here for.")
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Next steps

    If everything passed (or only the API key is missing), you are ready to begin:

    **[Module 01: Python Foundations — Your First Code](../01-python-foundations/01-your-first-code.py)**

    That notebook will introduce variables, data types, and your first real Python program — using pain biology examples throughout.

    ---

    ## Further Reading

    - **Python virtual environments:** https://docs.python.org/3/library/venv.html — explains what `.venv/` is and why it matters
    - **marimo:** https://docs.marimo.io/ — marimo notebook documentation
    - **Anthropic API quickstart:** https://docs.anthropic.com/en/docs/initial-setup — getting your API key and making your first call

    ---

    ## Edit Log

    | Date | Change |
    |------|--------|
    | 2026-03-25 | Created pre-flight check notebook |
    | 2026-03-25 | Added cross-module navigation links |
    | 2026-03-25 | Renumbered to 02; added link to setup guide |
    - 2026-03-25: Updated navigation links for new module numbering
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    > **Navigation:** [\u2190 Previous: Complete Setup Guide](01-complete-setup-guide.py) | [Module Index](../README.md) | [Next: Your First Code \u2192](../01-python-foundations/01-your-first-code.py)
    """)
    return


if __name__ == "__main__":
    app.run()

