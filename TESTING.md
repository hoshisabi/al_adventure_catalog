
# Running the tests

This project’s ingestion & JSON maintenance lives under `maintaindb/` (see README).
Tests are placed under `maintaindb/tests/` and validate both the legacy and new DMsGuild HTML formats, plus some helper utilities.

## Quickstart (pytest)

```bash
# Using uv (Python 3.13 per pyproject)
uv venv
uv pip install pytest beautifulsoup4 word2number requests python-dotenv
uv run pytest
```

or with plain venv/pip:

```bash
python -m venv .venv
. .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install pytest beautifulsoup4 word2number requests python-dotenv
pytest
```

## HTML fixtures

The tests look for the sample HTML in **either** location:

- `maintaindb/dmsguildinfo/dmsguildinfo-536025.html` and `...---new.html`
- project root fallbacks: `dmsguildinfo-536025.html` and `dmsguildinfo-536025---new.html`

If you keep real snapshots in a private repo, you can symlink or copy them to `maintaindb/dmsguildinfo/` locally.

## unittest alternative

If you prefer `unittest` discovery for parity with other scripts:
```bash
python -m unittest discover maintaindb
```
