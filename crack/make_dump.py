import hashlib
from pathlib import Path

accounts = {
    "liwei": "123456",
    "sofia": "iloveyou",
    "tomk":  "qwerty123",
    "aisha": "password1",
    "marie": "mariepw",
    "raj":   "Gv7#pLm2!xQ",
}
output = Path(__file__).resolve().parent / "leaked_users.txt"
with output.open("w", encoding="utf-8", newline="\n") as f:
    for username, password in accounts.items():

        f.write(f"{username}:{hashlib.md5(password.encode()).hexdigest()}\n")
print(f"wrote {output}")
