# Class 5 password audit

Run from the NoteApp folder, or run either script directly in PyCharm:

```powershell
E:\Python\python.exe .\crack\make_dump.py
E:\Python\python.exe .\crack\crack.py
```

Both scripts resolve their files relative to their own folder. The bundled
`wordlist.txt` is the course's public common-password list, unchanged:
[source](https://kristenpire.github.io/epita-security-labs/class5/assets/common-passwords.txt).
The dump contains six fictional accounts for the offline MD5 experiment; it is
separate from the real app's legacy plaintext password storage.

With the HTTPS stack running, measure hashing speed inside the web container:

```powershell
docker compose -f docker-compose.yml -f docker-compose.https.yml exec -T web python /host/crack/benchmark.py
```

The web app now upgrades a legacy plaintext password to Argon2id after a correct
login. Log out and log back in to check the Argon2 verification branch. Accounts
that have not logged in yet retain their legacy value until their next correct
login. Default parameters are 64 MiB of memory, three passes and four lanes.

The course deliberately leaves the other planted vulnerabilities for later labs.
