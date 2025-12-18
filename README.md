## Manual Test Plan

1. Setup:
- `uv venv -p 3.11`
- `uv pip install -r requirements.txt`

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






