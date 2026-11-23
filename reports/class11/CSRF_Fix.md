# Class 11 — NotesApp CSRF fix

**Name:** Siyuan Wu

**Test date:** 23 November 2026

**Scope:** Local NotesApp at `https://localhost`, using seeded data and a
temporary student account for the admin test.

## Before the fix

The grade update route in [app.py](../../web/app.py) checked that the session
belonged to a teacher. It accepted the submitted fields without checking a
CSRF token. A session cookie identifies the signed-in user, while a CSRF
token lets the server verify that the submission carries the token issued
to that session.

Alice's Computer Science record (note ID 2) started at **10.5**, with the
comment `<b>Class 10 preview</b>`. The baseline screenshot records that
starting state. A browser-based demonstration of an unintended grade
change remains unverified. [Baseline screenshot](screenshots/01-before-grade.png)

## Fix

- The application generates a random token when a session first renders a
  protected form. A Flask request hook validates the token using
  `hmac.compare_digest` on POST requests, with the login endpoint exempt.
  Missing or invalid tokens return **400 Bad Request** before the route
  handler runs. The session cookie also uses `SameSite=Lax`.
- The hidden `csrf_token` field appears in the teacher's Save form and the
  administrator's Delete, Create, and Ping forms. [Teacher template](../../web/templates/teacher.html) · [Admin template](../../web/templates/admin.html)

## After the fix

| Check | Observed result | Evidence |
| --- | --- | --- |
| Teacher saves a grade | The teacher form saved **10.0** and `class 11 form check` on Alice's record (note ID 2). | [All grades after Save](screenshots/02-teacher-save.png) |
| Administrator creates a user | The Users list showed `class11_check` with role **student** (user ID 38). | [Users list](screenshots/03-admin-create.png) |
| Administrator runs Ping | Ping to `127.0.0.1` returned one reply with **0% packet loss**. | [Ping result](screenshots/04-admin-ping.png) |
| CSRF validator | A missing token and an incorrect token returned **400**. A matching token passed validation. | [Terminal check](screenshots/05-csrf-check.png) |

Additional checks on the final app used Flask test sessions with database
access guarded by an assertion. Each of the three protected POST endpoints
rejected a missing session token, a missing form token, an incorrect token,
and a non-ASCII token with **400** before accessing the database. A matching
token passed the request hook on all three endpoints. The checks also
confirmed the login exemption, all four rendered CSRF fields, and distinct
tokens across sessions. These checks verify server-side rejection in
isolation. The browser screenshots document the normal form actions.

AI assistance was used to draft the report and verify the CSRF checks.

[Class 11 lab requirements](https://github.com/KristenPire/epita-security-labs/blob/main/docs/class11/csrf.md#what-you-hand-in)
