# maintaindb/cli.py
from . import process_downloads

def main() -> None:
    # delegate to your existing script’s main (whatever it is)
    # If your script is pure top-level execution, extract it:
    # e.g., process_downloads.main()
    process_downloads.main()
