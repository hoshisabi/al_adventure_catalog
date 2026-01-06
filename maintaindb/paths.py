"""
Path configuration module for maintaindb scripts.

This module provides path resolution that works regardless of whether scripts
are run from the project root or the maintaindb/ directory. It detects the
project root by looking for pyproject.toml.
"""
import os
from pathlib import Path


def find_project_root(start_path: Path = None) -> Path:
    """
    Find the project root directory by looking for pyproject.toml.
    
    Starts from the current file's directory and walks up until pyproject.toml
    is found. If not found, falls back to assuming the parent of maintaindb/
    is the root.
    
    Args:
        start_path: Optional starting path (defaults to this file's directory)
        
    Returns:
        Path to project root directory
    """
    if start_path is None:
        start_path = Path(__file__).parent
    
    current = start_path.resolve()
    
    # Walk up the directory tree looking for pyproject.toml
    for parent in [current] + list(current.parents):
        if (parent / 'pyproject.toml').exists():
            return parent
    
    # Fallback: if we're in maintaindb/, assume parent is root
    if current.name == 'maintaindb':
        return current.parent
    
    # Last resort: return current directory
    return current


# Project root (where pyproject.toml is located)
PROJECT_ROOT = find_project_root()

# Maintaindb directory (where this file is located)
MAINTAINDB_DIR = Path(__file__).parent.resolve()

# Data directories (all relative to PROJECT_ROOT)
DC_DIR = PROJECT_ROOT / 'maintaindb' / '_dc'
DMSGUILDINFO_DIR = PROJECT_ROOT / 'maintaindb' / 'dmsguildinfo'
DMSGUILDINFO_PROCESSED_DIR = DMSGUILDINFO_DIR / 'processed'
STATS_DIR = PROJECT_ROOT / 'maintaindb' / '_stats'
ASSETS_DATA_DIR = PROJECT_ROOT / 'assets' / 'data'
DATA_DIR = PROJECT_ROOT / '_data'

# Specific file paths
CATALOG_JSON = ASSETS_DATA_DIR / 'catalog.json'
STATS_JSON = ASSETS_DATA_DIR / 'stats.json'


def ensure_directories():
    """Create all data directories if they don't exist."""
    directories = [
        DC_DIR,
        DMSGUILDINFO_DIR,
        DMSGUILDINFO_PROCESSED_DIR,
        STATS_DIR,
        ASSETS_DATA_DIR,
        DATA_DIR,
    ]
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)


# Ensure directories exist when module is imported
ensure_directories()

