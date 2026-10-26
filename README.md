# Name:Siyuan Wu 吴思远
# StudentID: 2023905932

# NotesApp

A small grades application used throughout the Computer Security course. Teachers
record grades and comments for their classes, students read their own grades, and an
admin manages users and classes.

## Run it

You need Docker with the Compose plugin.

```
git clone https://github.com/1974932179/NoteApp.git notesapp
cd notesapp
```

For this fork, follow the AES-GCM setup below and generate the local HTTPS
certificate using the command in the Class 5 section. Then open
`https://localhost`. PostgreSQL loads the seed data on its first start;
the migration encrypts its plaintext comments before the web service starts.

## Test accounts

| Role    | Username      | Password   |
|---------|---------------|------------|
| Student | `alice`       | `alicepw`  |
| Teacher | `prof.turing` | `teach123` |
| Admin   | `admin`       | `admin123` |

(There are ~30 students in total; each student's password is their username + `pw`,
e.g. `bob` / `bobpw`.)

## Stack

- Python 3.11 + Flask (server-rendered Jinja2 pages and a small JSON API)
- PostgreSQL 15
- Docker Compose (`web` and `db` services)

## Reset

```
docker compose down -v   # wipes the database volume
```

After a reset, repeat the database startup, build, migration and HTTPS startup
commands in the AES-GCM section. Keep the existing key if any encrypted data
or database backups still need to be read.

## Updating your fork

The course repository is sometimes updated. Your fork does **not** update by itself.
To pull the latest changes into your fork:

**Easiest (GitHub website):** open your fork, and if it says *"This branch is behind
KristenPire/NoteApp"*, click **Sync fork → Update branch**. Then, in your local clone:

```
git pull
```

**Command line (keeps your own commits):**

```
git remote add upstream https://github.com/KristenPire/NoteApp.git   # once
git fetch upstream
git merge upstream/main
git push
```

Then **rebuild**, because the app code is baked into the Docker image:

```
docker compose up --build
```

A plain `docker compose up` would keep running the old image.


## Project 1: threat model (group contribution)

| Part | Material in this fork |
|---|---|
| 1. Numbered data-flow diagram and every trust boundary | [Group diagram](flow_img.jpg), with [Flow_List.md](Flow_List.md) as the F01–F44 numbering reference. |
| 2. STRIDE table | [threat.md](threat.md): TH01–TH17, covering all six categories. |
| 3. Likelihood × impact ratings | [Risk_Assessment.md](Risk_Assessment.md): scale, scores and reasons for every threat. |
| 4. Top three risks and a fix for each | [Top3_Risks_and_Fixes.md](Top3_Risks_and_Fixes.md): TH01, TH02 and TH03, with proposed fixes and acceptance checks. |

The course asks for a group submission on GitHub before 20 October and a
3-minute group presentation that day (Session 03, page 31). The four deliverable
files are now present in this fork.

The Project 1 reports describe the original teaching baseline and proposed fixes.
Later lab changes and their measured results are documented separately below.
AI assistance for review, proposed ratings and wording is disclosed in the reports.
Local drafts, private keys and editor files are excluded from version control.

## Session 3: AES-GCM comment storage

Comments are encrypted before insertion or update and decrypted for the teacher
page, student page, note API and CSV export. The database stores
`aesgcm:v1:` followed by Base64 of a 12-byte nonce, ciphertext and a 16-byte
authentication tag. The key is 32 random bytes; the authenticated context is
`notes.comment:v1`. Each encryption generates a fresh nonce.

For a new clone, create a local key once from the NoteApp folder:

```powershell
New-Item -ItemType Directory -Force secrets
python -c "from pathlib import Path; import secrets; p=Path('secrets/comment.key'); f=p.open('xb'); f.write(secrets.token_bytes(32)); f.close(); print('Key created')"
```

The command refuses to overwrite an existing key. Keep this key for the lifetime
of the encrypted data. It is ignored by Git and mounted as
`/run/secrets/comment_key`; it is not part of the web image. An existing encrypted
database requires its original key, not a newly generated one.

After generating the HTTPS certificate described below, run:

```powershell
docker compose -f docker-compose.yml -f docker-compose.https.yml stop nginx web
docker compose -f docker-compose.yml -f docker-compose.https.yml up -d --wait db
docker compose -f docker-compose.yml -f docker-compose.https.yml build web
docker compose -f docker-compose.yml -f docker-compose.https.yml run --rm --no-deps web python migrate_comments.py
docker compose -f docker-compose.yml -f docker-compose.https.yml up -d
```

Back up an existing database before migration. The migration commits all changes
together, rolls back on failure and validates already encrypted comments before
skipping them. Repeating it after a successful migration reports zero migrated
comments.

Run the encryption checks with:

```powershell
docker compose -f docker-compose.yml -f docker-compose.https.yml exec -T web python /host/tests/test_comment_crypto.py
```

The tests cover Unicode round trips, different ciphertexts for repeated input,
empty and NULL comments, tamper rejection and plaintext rejection. Exported CSV
files contain readable comments. Existing authorization flaws remain part of the
teaching application; comment encryption does not fix them.

## Class 4: CSV integrity with HMAC

`hmac_csv.py` signs a local `grades.csv`; `verify_csv.py` checks the resulting
`grades_signed.csv`. The [HMAC verification report](reports/hmac/HMAC_Verification.md)
records acceptance of the original export, rejection after a grade edit, and
acceptance after restoring the original bytes. Keys and exported grades stay local.

## Class 5: HTTPS and password storage

[Combined report and screenshots](reports/class5/NotesApp_Class5_Report.md)
cover the HTTP/HTTPS comparison, certificate trust, MD5 wordlist experiment and
Argon2id migration. [Password experiment instructions](crack/README.md) explain
how to repeat the local scripts and benchmark.

For the HTTPS lab, generate a local certificate once from the NoteApp folder:

```powershell
New-Item -ItemType Directory -Force nginx/certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout nginx/certs/notesapp.key -out nginx/certs/notesapp.crt -subj "/CN=localhost"
docker compose -f docker-compose.yml -f docker-compose.https.yml up -d --build
```

Open `https://localhost`. The certificate is self-signed for this local lab.
The HTTPS override removes the web service's published port 8080. Existing
plaintext passwords are upgraded to Argon2id after a correct login; subsequent
logins verify the stored hash. Other planted flaws remain for later classes.
