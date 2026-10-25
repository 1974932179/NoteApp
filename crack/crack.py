import hashlib, time
from pathlib import Path

def load_dump(path):
    # read the leaked file into {username: md5_digest}
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            u, d = line.strip().split(":")   # each line is "username:digest"
            out[u] = d
    return out

folder = Path(__file__).resolve().parent
accounts = load_dump(folder / "leaked_users.txt")
with (folder / "wordlist.txt").open(encoding="utf-8-sig") as f:
    wordlist = [w.strip() for w in f if w.strip()]

start = time.perf_counter()
cracked = {}
for candidate in wordlist:                       # for each guess in the wordlist...
    cd = hashlib.md5(candidate.encode()).hexdigest()   # hash the guess the SAME way the app did
    for u, d in accounts.items():                # ...compare it to every leaked digest
        if u not in cracked and d == cd:         # same digest => that guess IS the password
            cracked[u] = candidate
elapsed = time.perf_counter() - start

# the attack never "reverses" a hash - it just hashes guesses until one matches.
print(f"cracked {len(cracked)} / {len(accounts)} in {elapsed*1000:.3f} ms")
for u, p in cracked.items():
    print(f"  {u} : {p}")
