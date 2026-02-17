import os
import subprocess
from dotenv import load_dotenv

# Force load
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path, override=True)

auth = os.getenv("X_AUTH_TOKEN", "")
ct0 = os.getenv("X_CT0", "")

print(f"--- Debug Bird Auth ---")
print(f"AUTH_TOKEN length: {len(auth)}")
print(f"CT0 length: {len(ct0)}")
print(f"CT0 Start: {ct0[:10]}...")
print(f"CT0 End: ...{ct0[-10:]}")

# Manually verify headers format
headers = {
    "authorization": "Bearer AAAAAAAAAAAAAAAAAAAAANRILgAAAAAAnNwIzUejRCOuH5E6I8xnZz4puTs%3D1Zv7ttfk8LF81IUq16cHjhLTvJu4FA33AGWWjCpTnA",
    "x-csrf-token": ct0,
    "cookie": f"auth_token={auth}; ct0={ct0}"
}

print("\n--- Constructing Headers ---")
print(f"x-csrf-token: {headers['x-csrf-token'][:10]}... (len={len(headers['x-csrf-token'])})")
print(f"cookie len: {len(headers['cookie'])}")

# Try a direct curl call to verify if Twitter accepts this long token
# This bypasses 'bird' to see if it's a tool issue or a credential issue.
# We will query the "Am I" endpoint (verify_credentials)
print("\n--- Testing Direct Curl (verify_credentials) ---")
cmd = [
    "curl", "-s", "-I", "https://api.twitter.com/1.1/account/verify_credentials.json",
    "-H", f"authorization: {headers['authorization']}",
    "-H", f"x-csrf-token: {ct0}",
    "-H", f"cookie: auth_token={auth}; ct0={ct0}",
    "-H", "user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
]

result = subprocess.run(cmd, capture_output=True, text=True)
print(result.stdout)
if "200 OK" in result.stdout:
    print("✅ Twitter accepted the credentials!")
elif "403 Forbidden" in result.stdout:
    print("❌ Twitter rejected (403). CSRF mismatch or invalid token.")
elif "401 Unauthorized" in result.stdout:
    print("❌ Twitter rejected (401). Invalid auth_token.")
else:
    print(f"⚠️ Unexpected response:\n{result.stdout[:200]}")
