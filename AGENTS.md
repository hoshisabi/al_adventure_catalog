# AGENTS.md

Guidance for AI coding assistants (Claude, Codex, Cursor, etc.) working in this
repository.

## Project context

This is a static HTML/JS catalog of D&D Adventurers League adventures, hosted at
https://hoshisabi.com/al_adventure_catalog/. Python scripts under `maintaindb/` scrape
and process DM's Guild product data into JSON files consumed by the frontend.

- `README.md` — user-facing overview
- `CLAUDE.md` — full project guide (structure, data workflow, catalog format, critical
  warnings)
- `TASKS.md` — active roadmap and cross-session communication file; use it to track
  progress and note blockers

## Critical: Windows PowerShell environment

This project runs on **Windows with PowerShell**. Use PowerShell equivalents for Unix
commands (`Select-String` not `grep`, `Get-Content` not `cat`, `Get-ChildItem` not
`find`, etc.). See [AI_ASSISTANT_GUIDELINES.md](AI_ASSISTANT_GUIDELINES.md) for the full
reference.

## Running scripts

Always run from the **project root** (where `pyproject.toml` lives) using module
syntax — never `cd` into `maintaindb/`, since its relative imports break:

```powershell
uv run python -m maintaindb.aggregator          # rebuild catalog.json
uv run python -m maintaindb.process_downloads   # parse HTML in dmsguildinfo/ -> _dc/
uv run python -m maintaindb.process_rss --url <url>  # fetch RSS -> _dc/
uv run python -m maintaindb.stats               # print catalog statistics
uv run pytest                                   # run tests
```

`lp.bat rebuild` regenerates `catalog.json` and serves the site locally.

## Critical warnings

- **Never delete files in `maintaindb/_dc/`** without a backup — some contain manually
  entered data that cannot be regenerated.
- **Never commit DM's Guild HTML** to this public repo — it belongs in the private
  `private-fixtures/` submodule.
- `adventure_extractors.py` and `adventure_normalizers.py` are unused refactoring
  drafts — don't wire them in without checking `maintaindb/REFACTORING_TASKS.md`.
