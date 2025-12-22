# AI Assistant Guidelines for Windows Environment

This project runs on **Windows with PowerShell**. When working with this codebase, follow these guidelines to avoid common command-line and path issues.

## Critical Windows Environment Notes

### 1. Use PowerShell Commands, NOT Unix Commands

**❌ DO NOT USE:**
- `grep` (use `Select-String` instead)
- `cat` (use `Get-Content` instead)
- `head`/`tail` (use `Select-Object -First`/`-Last` instead)
- `find` (use `Get-ChildItem` or `Select-String` instead)
- Unix-style pipes with backticks (`` ` ``)

**✅ USE INSTEAD:**
- `Select-String` for text searching: `Select-String -Pattern "pattern" file.txt`
- `Get-Content` for reading files: `Get-Content file.txt`
- `Select-Object` for limiting output: `command | Select-Object -First 10`
- PowerShell pipes (`|`) work fine

### 2. Quoting and String Handling

**❌ DO NOT USE:**
- Single quotes for literal strings with special chars: `'pattern (test)'` 
- Backticks for escaping: `` `$var `` 
- Unix-style command substitution: `` `command` ``

**✅ USE INSTEAD:**
- Double quotes for strings: `"pattern (test)"`
- Backticks only for escaping in PowerShell: `` `$var `` (to prevent variable expansion)
- For command output: `$(command)` or PowerShell's `-Command` syntax

### 3. Check Current Working Directory (CWD)

**ALWAYS check CWD before running commands that reference paths.**

```powershell
# Check CWD first
pwd

# Or use Get-Location
Get-Location

# The project root is where pyproject.toml exists
# Most commands should be run from project root, not from maintaindb/ subdirectory
```

**Common mistake**: Assuming you're in `maintaindb/` when you're actually in project root, or vice versa.

### 4. Path Handling

- Use **forward slashes** (`/`) or **backslashes** (`\`) - both work in PowerShell for paths
- When in doubt, use **relative paths from project root**
- Don't use `cd` unnecessarily - use relative paths instead

**Examples:**
```powershell
# Good: Relative path from project root
Get-Content maintaindb/_dc/some_file.json

# Good: Check if file exists
Test-Path maintaindb/_dc/some_file.json

# Avoid: Changing directory unnecessarily
cd maintaindb
# ... do something
cd ..  # Easy to forget or get lost
```

### 5. Running Python Scripts

All Python scripts should be run from **project root** using module syntax:

```powershell
# From project root (where pyproject.toml is)
uv run python -m maintaindb.stats
uv run python -m maintaindb.process_downloads
uv run python -m maintaindb.aggregator
```

**DO NOT:**
- Change directory into `maintaindb/` and try to run scripts directly
- Use Unix-style paths or assumptions about directory structure

### 6. Command Output Filtering Examples

**Searching output:**
```powershell
# ✅ PowerShell way
uv run python -m maintaindb.process_downloads --force 2>&1 | Select-String -Pattern "510014"

# ❌ Don't use Unix grep
uv run python -m maintaindb.process_downloads --force 2>&1 | grep "510014"
```

**Limiting output:**
```powershell
# ✅ PowerShell way
uv run python -m maintaindb.stats | Select-Object -First 20

# ❌ Don't use Unix head
uv run python -m maintaindb.stats | head -20
```

### 7. Testing File Paths

Before running commands that reference files, verify they exist:

```powershell
# Check if file exists
Test-Path maintaindb/_dc/FR-DC-BTW-01-Fathers-Conscience.json

# List files
Get-ChildItem maintaindb/_dc/*.json | Select-Object -First 5
```

### 8. Common Pitfalls

1. **Assuming bash/shell environment**: This is Windows PowerShell, not Unix shell
2. **Not checking CWD**: Always verify current directory before path-based operations
3. **Unix command syntax**: Use PowerShell equivalents, not Unix commands
4. **Complex quoting**: Simplify command strings; create temporary test scripts if needed
5. **Path assumptions**: Use relative paths from project root; don't assume subdirectory context

### 9. When in Doubt

- Create a small test script (`.py` or `.ps1`) to test complex operations
- Use simple, explicit paths relative to project root
- Check CWD with `pwd` or `Get-Location`
- Test commands incrementally rather than chaining complex pipelines
- Use PowerShell's built-in help: `Get-Help Select-String` or `Select-String -?`

---

**Remember**: This is a Windows PowerShell environment. When writing or suggesting commands, think "PowerShell" 
not "bash" or "Unix shell".

