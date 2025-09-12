# in tests/conftest.py (or maintaindb/tests/conftest.py)
import os
import pytest
from pathlib import Path
from bs4 import BeautifulSoup

FIXTURE_DIR = Path(os.getenv("DMSGUILD_FIXTURES_DIR", ""))  # optional external repo

candidates_old = [
    FIXTURE_DIR / "dmsguildinfo-536025.html",
    Path("maintaindb/dmsguildinfo/dmsguildinfo-536025.html"),
    Path("dmsguildinfo-536025.html"),
    ]
candidates_new = [
    FIXTURE_DIR / "dmsguildinfo-536025---new.html",
    Path("maintaindb/dmsguildinfo/dmsguildinfo-536025---new.html"),
    Path("dmsguildinfo-536025---new.html"),
    ]

def _first_existing(paths):
    for p in paths:
        if p and p.exists():
            return p
    return None

@pytest.fixture(scope="session")
def bs_html_old():
    p = _first_existing(candidates_old)
    if not p:
        pytest.skip("Legacy HTML fixture not present; skipping.")
    return BeautifulSoup(p.read_text(encoding="utf-8", errors="ignore"), "html.parser")

@pytest.fixture(scope="session")
def bs_html_new():
    p = _first_existing(candidates_new)
    if not p:
        pytest.skip("New-format HTML fixture not present; skipping parity tests.")
    return BeautifulSoup(p.read_text(encoding="utf-8", errors="ignore"), "html.parser")
