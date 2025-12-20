# maintaindb/cli.py
from . import process_downloads

def main() -> None:
    # Delegate to process_downloads function (not main, as the function is named process_downloads)
    process_downloads.process_downloads()
