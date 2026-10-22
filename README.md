# Name:Siyuan Wu 吴思远
# StudentID: 2023905932

# NotesApp

A small grades application used throughout the Computer Security course. Teachers
record grades and comments for their classes, students read their own grades, and an
admin manages users and classes.

## Run it

You need Docker with the Compose plugin.

```
git clone git@github.com:KristenPire/NoteApp.git notesapp
cd notesapp
docker compose up
```

The first start builds the image, launches PostgreSQL, and loads the seed data
automatically. When it is ready, open:

```
http://localhost:8080
```

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
docker compose up        # reloads the seed data
```

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
| 1. Numbered data-flow diagram and every trust boundary | The complete group diagram is held by another group member and still needs to be merged into the final hand-in repository. [Flow_List.md](Flow_List.md) provides the F01–F44 numbering reference. |
| 2. STRIDE table | [threat.md](threat.md): TH01–TH17, covering all six categories. |
| 3. Likelihood × impact ratings | [Risk_Assessment.md](Risk_Assessment.md): scale, scores and reasons for every threat. |
| 4. Top three risks and a fix for each | [Top3_Risks_and_Fixes.md](Top3_Risks_and_Fixes.md): TH01, TH02 and TH03, with proposed fixes and acceptance checks. |

The course asks for a group submission on GitHub before 20 October and a
3-minute group presentation that day (Session 03, page 31). Choose one repository
for the complete hand-in and merge the diagram there. This fork currently contains
the written contribution, not the full four-part submission.

The application remains the original teaching baseline. Fixes in the report are
proposals, not implemented changes. The review uses source inspection; it does not
claim new exploit or load-test results. AI assistance for review, proposed ratings
and wording is disclosed in the reports. Local drafts, test traces and editor
files are excluded from version control.
