# AGENTS.md

## Cursor Cloud specific instructions

This is a small, single-product Python batch project (see `README.md`). It loads
`data/clients.json` and `data/sales.csv`, computes metrics, and writes
`final_report.json`. There are no long-running services, databases, ports, or UI.

- Use `python3` (the VM has Python 3.12; CI targets 3.10, but the code runs fine on 3.12). There is no `python` alias on PATH.
- `pytest` is installed to `~/.local/bin`, which may not be on PATH. Run tests via `python3 -m pytest -q` to avoid PATH issues.
- Run the app with `python3 src/analyze.py` (from the repo root). It overwrites the tracked `final_report.json` in place; regenerating it with the committed input data reproduces the same file (no diff).
- No linter is configured (no ruff/flake8/black); there is no lint step to run.
- Dependencies (`pandas`, `pytest`) are installed by the startup update script; no extra setup is needed.
