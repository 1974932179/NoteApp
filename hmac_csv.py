from pathlib import Path
import secrets
import hmac
import hashlib

data = Path("grades.csv").read_bytes()
print(type(data),len(data))

key_file = Path("hmac.key")

if not key_file.exists():
    key_file.write_bytes(secrets.token_bytes(32))

key = key_file.read_bytes()
print("key length", len(key))

tag = hmac.new(key,data,hashlib.sha256).hexdigest()
print("HMAC:", tag)

output = Path("grades_signed.csv")
footer = f"\n# HMAC: {tag}\n".encode("ascii")

output.write_bytes(data + footer)