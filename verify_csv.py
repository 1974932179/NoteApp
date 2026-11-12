from pathlib import Path
import hmac

from dotenv import dotenv_values

from web.csv_integrity import HMAC_FOOTER, csv_hmac, parse_hmac_key

key = parse_hmac_key(dotenv_values(".env").get("HMAC_KEY"))
content = Path("grades_signed.csv").read_bytes()
data, separator, saved_tag = content.rpartition(HMAC_FOOTER)

if not separator:
    print("CHECK FAILED：没有找到 HMAC")
    raise SystemExit(1)

saved_tag = saved_tag.rstrip(b"\r\n")
if not hmac.compare_digest(saved_tag, csv_hmac(data, key)):
    print("CHECK FAILED")
    raise SystemExit(1)

print("CHECK PASSED")
