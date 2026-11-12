from pathlib import Path

from dotenv import dotenv_values

from web.csv_integrity import HMAC_FOOTER, parse_hmac_key, sign_csv

key = parse_hmac_key(dotenv_values(".env").get("HMAC_KEY"))
data = Path("grades.csv").read_bytes()
signed = sign_csv(data, key)
Path("grades_signed.csv").write_bytes(signed)
print("HMAC:", signed.rpartition(HMAC_FOOTER)[2].decode("ascii").rstrip())
