from pathlib import Path
import hashlib
import hmac

from dotenv import dotenv_values

key_hex = dotenv_values(".env").get("HMAC_KEY")

if not key_hex:
    raise ValueError("HMAC_KEY is missing from .env")

key = bytes.fromhex(key_hex)

if len(key) != 32:
    raise ValueError("HMAC_KEY must represent 32 bytes")

content = Path("grades_signed.csv").read_bytes()
data, separator, saved_tag = content.rpartition(b"\n# HMAC: ")

if not separator:
    print("CHECK FAILED：没有找到 HMAC")
else:
    current_tag = hmac.new(
        key, data, hashlib.sha256
    ).hexdigest().encode("ascii")

    saved_tag = saved_tag.rstrip(b"\r\n")

    if hmac.compare_digest(saved_tag, current_tag):
        print("CHECK PASSED")
    else:
        print("CHECK FAILED")