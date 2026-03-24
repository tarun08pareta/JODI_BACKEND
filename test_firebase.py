import os
import sys

# Add backend directory to python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.firebase import init_firebase

print("Testing Firebase Init:")
try:
    success = init_firebase()
    print(f"Init Success: {success}")
except Exception as e:
    print(f"Exception during init: {e}")
