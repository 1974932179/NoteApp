# Class 8 — NoteApp grade access control

**Name:** Siyuan Wu

**Test date:** 12 November 2026

**Fix commit:** `9b47eb8` (`Enforce note ownership in the grades API`)

## Before the fix

I signed in to the local NoteApp at `https://localhost` as the student `alice`.
Using the same session, I requested two note IDs from the grades API.

| Request as Alice | HTTP status | Returned record |
| --- | --- | --- |
| `GET /api/notes/1` | 200 | Alice's Mathematics grade, 16.2 |
| `GET /api/notes/3` | 200 | Bob's Mathematics grade, 12.6. Comment: “Solid work, keep it up.” |

Changing the note ID exposed another student's record. The handler authenticated
Alice and fetched the requested record by ID, but it did not check whether she
was authorized to read that record. This was an insecure direct object reference
(IDOR), NoteApp flaw #7.

## Fix

After fetching a note, [`api_notes()`](../../web/app.py) compares the note's
`student_id` with the authenticated caller's `user_id`. The owner can read the
note. Callers with the `teacher` or `admin` role can read any note, as specified
in the lab. Other authenticated callers receive HTTP 404 before the comment is
decrypted and the grade is returned.

I chose **404 Not Found** so that a refused request has the same status and JSON
body as a request for a missing note. This avoids confirming that the requested
ID exists.

## After the fix

I rebuilt the web service and repeated the student requests over local HTTPS.
I used a separate login session for `prof.turing` to check teacher access.

| Caller | Request | Observed result |
| --- | --- | --- |
| `alice` | `GET /api/notes/3` | HTTP 404, `{"error":"not found"}` |
| `alice` | `GET /api/notes/1` | HTTP 200, Alice's Mathematics grade, 16.2 |
| `prof.turing` | `GET /api/notes/3` | HTTP 200, Bob's Mathematics grade, 12.6, with the original comment |

These checks used the seeded lab accounts and data. They confirm that the
cross-student request is refused and that the tested owner and teacher requests
still work.

Lab instructions: [Class 8 — Read anyone's grade](https://kristenpire.github.io/epita-security-labs/class8/read-anyones-grade/).
