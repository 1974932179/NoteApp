import hashlib
from pathlib import Path

accounts = {
    "liwei": "123456",
    "sofia": "iloveyou",
    "tomk":  "qwerty123",
    "aisha": "password1",
    "marie": "mariepw",        # not a dictionary word - a predictable pattern
    "raj":   "Gv7#pLm2!xQ",    # long and random
}
output = Path(__file__).resolve().parent / "leaked_users.txt"
with output.open("w", encoding="utf-8", newline="\n") as f:
    for username, password in accounts.items():
        # store "username:md5(password)" - unsalted MD5, exactly like the bad app would
        f.write(f"{username}:{hashlib.md5(password.encode()).hexdigest()}\n")
print(f"wrote {output}")
