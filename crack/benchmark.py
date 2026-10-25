import hashlib
import time

from argon2 import PasswordHasher

N = 100_000
start = time.perf_counter()
for _ in range(N):
    hashlib.md5(b"guess").hexdigest()
md5_rate = N / (time.perf_counter() - start)

ph = PasswordHasher()
start = time.perf_counter()
ph.hash("guess")
argon2_seconds = time.perf_counter() - start
argon2_rate = 1 / argon2_seconds

print(f"MD5    : {md5_rate:,.0f} guesses/second")
print(f"Argon2 : {argon2_seconds * 1000:.1f} ms for ONE guess "
      f"({argon2_rate:.1f} guesses/second)")
print(f"MD5/day: {md5_rate * 86400:,.0f}")
print(f"Argon2/day: {argon2_rate * 86400:,.0f}")
print(f"Argon2 is about {md5_rate / argon2_rate:,.0f} times slower per guess.")
print("Single-process lab estimate; not a measurement of a GPU cracking rig.")
