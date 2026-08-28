---
name: audit-adventures
description: Audit DM's Guild browse-list exports against ingested _dc/ files to find missing adventures. Run after capturing browse pages with the bookmarklet. Produces a list of missing adventures with clickable DM's Guild links.
disable-model-invocation: true
---

# Audit Adventures Workflow

You are auditing the AL adventure catalog to find products captured in browse-list exports that have not yet been ingested into `_dc/`.

Browse-list files are captured using the bookmarklet in `dmsguild_browse_bookmarklet.js`. Each page produces an `aldc-page-NNN.json` file saved into `maintaindb/dmsguildinfo/`.

## Step 1: Check for Browse List Files

Run:
```powershell
Get-ChildItem maintaindb\dmsguildinfo -Filter 'aldc-*.json' | Select-Object -ExpandProperty Name
```

If no files are found, stop and tell the user they need to capture browse pages first using the bookmarklet — it saves `aldc-page-NNN.json` files into `maintaindb/dmsguildinfo/`.

Otherwise, list the files found and continue.

## Step 2: Run the Audit

Run the audit script, writing JSON output to the stats directory:
```powershell
uv run python -m maintaindb.audit_browse_lists --category adventure --exclude-roll20 --exclude-fantasy-grounds --json maintaindb\_stats\browse_audit.json 2>&1
```

Report the summary text it prints (pages covered, unique products, ingested count, missing by category).

## Step 3: Read and Present Results

Read `maintaindb\_stats\browse_audit.json`.

**If the `missing` array is empty:** tell the user the catalog is fully up to date for the captured pages — no actionable missing adventures.

**Otherwise:** display a numbered table of missing adventures. Construct the DM's Guild link from each entry's `id` field using the pattern `https://www.dmsguild.com/en/product/{id}`.

| # | ID | Title | Link |
|---|----|-------|------|
| 1 | 123456 | Some Adventure Title | https://www.dmsguild.com/en/product/123456 |

After the table, note:
- How many entries are in the `excluded` array (curated exclusions — known non-adventures, bundles handled elsewhere, etc.)
- Any entries that have a `note` field set — surface those individually

## Step 4: Offer Next Steps

Ask the user which (if any) of the listed adventures they want to download and ingest. Remind them that clicking a DM's Guild link will open the product page, and they should use the bookmarklet on each product page to save the `dmsguildinfo-{id}.html` file, then run `/ingest-adventures` when done.

## Step 5: Clean Up Browse List Files

Ask the user: **"Should I delete the `aldc-*.json` browse list files now that we're done with them?"**

If they say yes (or words to that effect), run:
```powershell
Get-ChildItem maintaindb\dmsguildinfo -Filter 'aldc-*.json' | Remove-Item -Confirm:$false; Write-Output "Done"
```

Report how many files were deleted.
