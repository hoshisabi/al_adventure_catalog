param(
    [Parameter(Mandatory = $true)]
    [string]$Message
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

Write-Host "Running aggregator..."
uv run python -m maintaindb.aggregator
if ($LASTEXITCODE -ne 0) { Write-Error "Aggregator failed."; exit 1 }

Write-Host "Running stats generator..."
uv run python -m maintaindb.stats
if ($LASTEXITCODE -ne 0) { Write-Error "Stats generation failed."; exit 1 }

Write-Host "Staging changes..."
git add .
if ($LASTEXITCODE -ne 0) { Write-Error "Failed to stage changes."; exit 1 }

Write-Host "Committing..."
git commit -m $Message
if ($LASTEXITCODE -ne 0) { Write-Error "Git commit failed."; exit 1 }

Write-Host "Pushing..."
git push
if ($LASTEXITCODE -ne 0) { Write-Error "Git push failed."; exit 1 }

Write-Host "Deploy complete!"
