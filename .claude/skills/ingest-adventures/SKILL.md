---
name: ingest-adventures
description: Full ingest workflow — process downloaded DM's Guild HTML files into _dc/ JSON, verify the results, rebuild catalog.json, run tests, then commit and push. Use when the user has downloaded HTML files into dmsguildinfo/ and wants to publish them.
disable-model-invocation: true
---

# Ingest Adventures Workflow

You are running the full adventure ingest pipeline for the AL adventure catalog.

## Step 1: Preflight Check

Run this PowerShell command to list waiting HTML files:
```
Get-ChildItem maintaindb\dmsguildinfo -Filter 'dmsguildinfo-*.html' | Select-Object -ExpandProperty Name
```

If no files are returned, stop and tell the user there's nothing to process.

Otherwise, list the files found and proceed.

## Step 2: Run process_downloads

Run:
```
uv run python -m maintaindb.process_downloads
```

Report the full output. Note which files were successfully processed and any errors.

## Step 3: Verify the New/Changed JSON Files

Run `git diff --name-only` and `git status --short` to find which `_dc/*.json` files were created or modified.

For each changed file, read it and display a compact summary table:

| Field | Value |
|-------|-------|
| title | ... |
| code | ... |
| authors | ... |
| tiers | ... |
| hours | ... |
| campaigns | ... |
| season | ... |
| needs_review | ... |

Flag any file where `needs_review` is `true` with a warning — these are missing author/tier/hour data and need manual follow-up.

Also flag any file where:
- `code` is null or empty
- `tiers` is null
- `hours` is null
- `is_adventure` is false (worth confirming these are intentionally included)

## Step 4: Ask for Confirmation

Present the summary and ask the user: **"Do these look correct? Should I proceed with rebuilding catalog.json and pushing?"**

Wait for explicit confirmation before continuing. If the user says no or asks to fix something, stop and help them address the issue first.

## Step 5: Rebuild Catalog

Run:
```
uv run python -m maintaindb.aggregator
```

Report the output.

## Step 6: Run Tests

Run:
```
uv run pytest
```

If tests fail, stop and report the failures. Do not commit or push with failing tests.

## Step 7: Commit

Stage the changed files:
- All modified/new `maintaindb/_dc/*.json` files
- `assets/data/catalog.json`

Do NOT stage HTML files in `dmsguildinfo/` — those are not committed.

Write the commit message based on what was processed. Use this format:
- New only: `Add N new adventures: [codes/titles]`
- Mixed: `Add X new / update Y existing adventures: [codes/titles]`

**PowerShell syntax for multiline commit messages** (the closing `'@` must be at column 0):
```powershell
git commit -m @'
Add 2 new adventures: FR-DC-MCG-INN02, FR-DC-LCO-05

Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>
'@
```

## Step 8: Push

Push to origin:
```
git push
```

Report success and the commit hash.
