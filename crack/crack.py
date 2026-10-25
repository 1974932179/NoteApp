import hashlib, time
from pathlib import Path

def load_dump(path):

    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            u, d = line.strip().split(":")
            out[u] = d
    return out

folder = Path(__file__).resolve().parent
accounts = load_dump(folder / "leaked_users.txt")
with (folder / "wordlist.txt").open(encoding="utf-8-sig") as f:
    wordlist = [w.strip() for w in f if w.strip()]

start = time.perf_counter()
cracked = {}
for candidate in wordlist:
    cd = hashlib.md5(candidate.encode()).hexdigest()
    for u, d in accounts.items():
        if u not in cracked and d == cd:
            cracked[u] = candidate
elapsed = time.perf_counter() - start


print(f"cracked {len(cracked)} / {len(accounts)} in {elapsed*1000:.3f} ms")
for u, p in cracked.items():
    print(f"  {u} : {p}")
