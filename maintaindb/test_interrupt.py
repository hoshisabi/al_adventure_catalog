import time
import sys

print("This script will run for a long time.")
print("Press Ctrl-C to interrupt it.")

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nScript interrupted by user.")
    sys.exit(0)