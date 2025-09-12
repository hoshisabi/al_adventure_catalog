Project-specific development guidelines for al_adventure_catalog/maintaindb

Audience: Advanced developers contributing to the data extraction/normalization tooling for DMsGuild/WP data. This document captures the conventions and steps that are specific to this repo, so you can be productive quickly.

1) Environment and Build/Configuration
- Python: The repository is actively used on Windows with PowerShell and a modern CPython (tested with 3.13 locally). 3.10+ should be fine. Prefer a virtual environment.
- Dependencies: Install runtime dependencies from requirements.txt. Note that pytest is NOT listed there (see Testing section).
  PowerShell:
    python -m venv .venv
    .venv\Scripts\Activate.ps1
    python -m pip install -U pip
    python -m pip install -r requirements.txt
- Path conventions: Scripts often assume Windows paths. When using the CLI or PowerShell, prefer backslashes (\). Some tests and scripts add paths manually; see tests/conftest.py.
- Network access: Some scripts fetch remote pages (requests). For tests in this repo, we avoid network and use local HTML fixtures when present.
- Data directories in-repo:
  - _dc: JSON outputs shaped like Adventure JSONs (normalized metadata for adventures). Many tooling tasks read/write here.
  - dmsguildinfo/: HTML snapshots used for parsing (includes processed/ and newformat/ variants). Tests can optionally use files from here.
  - _stats, rewards, assets/: Aggregated outputs and supporting data (do not assume stable schemas without checking the specific generator).
- Key modules and flow:
  - adventure.py: parsing helpers (e.g., sanitize_filename, str_to_int, pattern helpers, plus higher-level extractors used by scrapers/normalizers).
  - adventure_model.py: dataclass model for Adventure objects with to_json serialization.
  - adventure_normalizers.py and adventure_extractors.py: turn extracted raw fields (or RSS snippets) into normalized model fields.
  - dmsguild_rss_parser.py: RSS-only path that either writes minimal JSONs or, when normalization modules are available, produces Adventure-shaped JSONs with a review flag.
  - dmsguild_rss_parser_new.py, process_downloads(_new).py, generate_* scripts: alternative or newer pipelines; verify parity before adopting.

2) Testing: How to configure and run
- Frameworks:
  - pytest is used for tests under tests/ (e.g., tests/test_units_misc.py and tests/test_parser_equivalence.py).
  - There is also a legacy unittest module test_adventure.py at repo root, which assumes the parent directory is on sys.path (see notes below).
- Install pytest (not in requirements.txt by design):
    python -m pip install pytest
- Running tests (recommended):
    # From the repository root: maintaindb
    python -m pytest -q tests
  This uses tests/conftest.py to provide fixtures. You will likely see some tests skipped (s markers) if local HTML fixtures are not present—that is expected.
- Optional fixtures location:
  The parity tests (tests/test_parser_equivalence.py) can use HTML files from either:
    - maintaindb/dmsguildinfo/dmsguildinfo-536025.html and maintaindb/dmsguildinfo/dmsguildinfo-536025---new.html
    - An external directory if you set the environment variable DMSGUILD_FIXTURES_DIR.
  PowerShell example:
    $env:DMSGUILD_FIXTURES_DIR = "F:\\Users\\decha\\Documents\\Projects\\al_adventure_catalog\\maintaindb\\dmsguildinfo"
    python -m pytest -q tests
  If neither location is available, those tests are skipped with a helpful message.
- Running the legacy unittest file (optional):
  test_adventure.py imports from maintaindb.adventure. Because the repo root is the maintaindb package directory, python -m unittest from this directory will not find the package unless you add the parent directory to PYTHONPATH or run from the parent folder.
  Options:
    # Option A: set PYTHONPATH to the parent of this repo
    $env:PYTHONPATH = (Resolve-Path ..).Path
    python -m unittest -q
    # Option B: run from the parent directory of maintaindb
    cd ..
    python -m unittest -q maintaindb.test_adventure

3) Adding and executing new tests
- Where to put tests:
  - Prefer pytest tests under tests/ following the existing patterns (see tests/test_units_misc.py). Keep tests self-contained and avoid network calls.
  - When importing the code under test, mimic the existing approach so the project can be importable regardless of the current working directory:
      PROJECT_ROOT = Path(__file__).resolve().parents[2]
      sys.path.insert(0, str(PROJECT_ROOT)) if needed
      try:
          import adventure
      except ModuleNotFoundError:
          from maintaindb import adventure
- Using local HTML fixtures:
  - Parity/HTML parsing tests use BeautifulSoup on local files. Consider adding minimal, sanitized fixtures under dmsguildinfo/processed or dmsguildinfo/newformat to keep tests deterministic and offline.
  - If you maintain fixtures externally, set DMSGUILD_FIXTURES_DIR to point at that location.
- Example: minimal test (verified)
  We verified the following pattern by creating tests/test_demo_simple.py and running it with pytest.
    python -m pip install pytest
    # From repo root
    python -m pytest -q tests\\test_demo_simple.py
  Example content (uses existing helper sanitize_filename):
    import sys
    from pathlib import Path
    PROJECT_ROOT = Path(__file__).resolve().parents[2]
    if str(PROJECT_ROOT) not in sys.path:
        sys.path.insert(0, str(PROJECT_ROOT))
    try:
        import adventure
    except ModuleNotFoundError:
        from maintaindb import adventure
    def test_demo_sanitize_filename_roundtrip():
        name = "My Demo: Adventure?"
        out = adventure.sanitize_filename(name)
        assert out.endswith(".json")
        assert ":" not in out and "?" not in out and "/" not in out
        assert out.startswith("My-Demo-")
  The test passed locally. After verification, remove the file to keep the repository clean.

4) Development tips and project-specific conventions
- Parsing and normalization boundaries:
  - adventure.extract_data_from_html returns either a dict of raw/derived fields or an object depending on the path; check call sites. Normalization into the Adventure model is done by AdventureDataNormalizer.
  - dmsguild_rss_parser.py has two operating modes:
    1) Minimal RSS → JSON (when normalization modules are not importable), saving only RSS-derived fields.
    2) RSS → normalize → Adventure model → JSON with is_adventure heuristic and needs_review=True.
  This is intentional to keep the pipeline operational even with partial environments.
- Filename safety:
  - Use adventure.sanitize_filename for all generated filenames. It enforces .json extension and strips/normalizes special characters consistently; several tests exercise it.
- Hours, tier, APL extraction:
  - Tests cover numeric and word ranges (e.g., "two-to-four-hour"). If you change regexes, update tests accordingly (test_adventure.py and tests/test_units_misc.py). Be careful with hyphen/dash variants and Unicode spaces in descriptions.
- Import paths in tests and scripts:
  - Because the repo root is also the Python package directory (maintaindb), imports differ depending on CWD. The tests prefer a dual import strategy (adventure or maintaindb.adventure) and adjust sys.path at runtime. Follow this pattern to keep tests runnable from various contexts and IDEs without an install step.
- Windows-specific notes:
  - Prefer PowerShell examples and backslashes in docs. When setting environment variables for a single command: $env:NAME = "value"; subsequent commands see it in the same session. Use quotes and escape backslashes when embedding paths in strings.

5) Common commands (tested locally)
- Create and activate venv:
    python -m venv .venv
    .venv\Scripts\Activate.ps1
- Install runtime deps:
    python -m pip install -r requirements.txt
- Install test deps:
    python -m pip install pytest
- Run pytest-based tests:
    python -m pytest -q tests
- Run a single pytest file:
    python -m pytest -q tests\test_units_misc.py
- Run legacy unittest (ensure PYTHONPATH or parent CWD):
    $env:PYTHONPATH = (Resolve-Path ..).Path
    python -m unittest -q

6) When adding new functionality
- Prefer implementing parsing logic in adventure.py or dedicated extractor modules; keep side effects (I/O) in scripts.
- Extend Adventure model fields deliberately; update normalizers and any JSON writers accordingly.
- If adding new external dependencies, update requirements.txt for runtime and document any optional test-only dependencies here.
- For new parsers, provide a minimal HTML fixture and a pytest with deterministic assertions; mark network-dependent tests as skipped unless an explicit opt-in is provided via env var.

Appendix: Known optional environment variables
- DMSGUILD_FIXTURES_DIR: Path to a directory containing dmsguildinfo-*.html fixtures for tests/test_parser_equivalence.py parity checks.
