from pathlib import Path
import hmac
import hashlib

from dotenv import dotenv_values

key_hex = dotenv_values(".env").get("HMAC_KEY")

if not key_hex:
    raise ValueError("HMAC_KEY is missing from .env")

key = bytes.fromhex(key_hex)

if len(key) != 32:
    raise ValueError("HMAC_KEY must represent 32 bytes")

data = Path("grades.csv").read_bytes()

tag = hmac.new(key, data, hashlib.sha256).hexdigest()
print("HMAC:", tag)

footer = f"\n# HMAC: {tag}\n".encode("ascii")
Path("grades_signed.csv").write_bytes(data + footer)