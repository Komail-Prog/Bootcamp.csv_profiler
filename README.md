## Manual Test Plan

- What can it do?
    `Automatic Profiling: Calculates total rows, columns, and data types.`

    `Data Summarization: Identifies unique values and provides data samples for every column.`

    `Dual Interface: Run it via a terminal (CLI) for automation or a web browser (GUI) for      interactive use.`

    `Flexible Exports: Saves results in both JSON (for machines) and Markdown (for humans).`

- How do I install dependencies?
1. Setup:
- `uv venv -p 3.11`
- `uv pip install -r requirements.txt`

- How do I run it?
2. CLI:
- `Windows (CMD): set PYTHONPATH=src`

- `Windows (PowerShell): $env:PYTHONPATH="src"`

- `macOS / Linux: export PYTHONPATH=src`

- `uv run python -m csv_profiler.cli data/sample.csv --out-dir outputs`


3. Verify:
- `outputs/report.json` and `outputs/report.md` exist

4. GUI:

- `Windows (CMD): set PYTHONPATH=src`

- `Windows (PowerShell): $env:PYTHONPATH="src"`

- `macOS / Linux: export PYTHONPATH=src`

- `uv run streamlit run app.py`


5. Export:
- `Download JSON and Markdown from the UI`
- `Click "Save to outputs/" to save directly to the local project folder`

- What does output look like?
    `The tool generates two files in the outputs/ folder:`

    `report.json: A structured file containing all statistical metrics.`

    `report.md: A clean, formatted table showing column details and unique counts.`




