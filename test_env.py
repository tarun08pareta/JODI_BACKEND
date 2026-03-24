import os
from dotenv import load_dotenv

load_dotenv()
cred_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
print(f"GOOGLE_APPLICATION_CREDENTIALS: {cred_path}")

if cred_path:
    print(f"Absolute path: {os.path.abspath(cred_path)}")
    print(f"Exists: {os.path.exists(cred_path)}")
else:
    print("Not found in environment variables.")
