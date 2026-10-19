# NotesApp numbered flow list

F01–F44 are the reference numbers used by the STRIDE and risk tables. This list supports the group diagram; it does not replace it.

TB1: Browser/Flask. TB2: Flask/PostgreSQL. Shell, files, logs, backups, Docker-host access and spreadsheet interpretation are additional component/deployment scopes.

**`POST /login`**

| Flow | Data flow |
|---|---|
| F01 | Browser -> Flask: `POST /login (username, password)` |
| F02 | Flask -> PostgreSQL: `Query (username, password)` |
| F03 | PostgreSQL -> Flask: `Query result (id, username, role; empty result or query error)` |
| F04 | Flask -> Browser: `HTTP 302 (Location=/, signed session cookie containing identity and JWT); on failure: HTTP 200 HTML (login form, error)` |

**`GET /login`**

| Flow | Data flow |
|---|---|
| F05 | Browser -> Flask: `GET /login (optional session cookie)` |
| F06 | Flask -> Browser: `HTTP 200 HTML (login form)` |

**`GET /logout`**

| Flow | Data flow |
|---|---|
| F07 | Browser -> Flask: `GET /logout (session cookie)` |
| F08 | Flask -> Browser: `HTTP 302 (Location=/login, session-clearing Set-Cookie)` |

**`GET /dashboard`**

| Flow | Data flow |
|---|---|
| F09 | Student -> Flask: `GET /dashboard (session cookie)` |
| F10 | Flask -> PostgreSQL: `Query (session user_id)` |
| F11 | PostgreSQL -> Flask: `Query result (id, grade, comment, class_name)` |
| F12 | Flask -> Student: `HTTP 200 HTML (grades, comments, class names, JWT)` |

**`GET /api/notes/<id>`**

| Flow | Data flow |
|---|---|
| F13 | Student -> Flask: `GET /api/notes/<id> (note_id, Bearer JWT or session cookie)` |
| F14 | Flask -> PostgreSQL: `Query (note_id)` |
| F15 | PostgreSQL -> Flask: `Query result (id, student_id, class_id, grade, comment, student, class_name; or empty result)` |
| F16 | Flask -> Student: `HTTP 200 JSON (id, student_id, class_id, grade, comment, student, class_name); HTTP 404 JSON (error) if absent; HTTP 401 JSON if unauthenticated` |

**`GET /teacher`**

| Flow | Data flow |
|---|---|
| F17 | Teacher -> Flask: `GET /teacher (session cookie)` |
| F18 | Flask -> PostgreSQL: `Query (courses, grades, students)` |
| F19 | PostgreSQL -> Flask: `Query results (courses; grades with student/course details; student IDs and usernames)` |
| F20 | Flask -> Teacher: `HTTP 200 HTML (courses, grades, students, grade form, export links)` |

**`POST /grades`**

| Flow | Data flow |
|---|---|
| F21 | Teacher -> Flask: `POST /grades (session cookie, note_id, student_id, class_id, grade, comment)` |
| F22 | Flask -> PostgreSQL: `Query (update grade: note_id, grade, comment; create grade: student_id, class_id, grade, comment)` |
| F23 | PostgreSQL -> Flask: `Command result (write completion status)` |
| F24 | Flask -> Teacher: `HTTP 302 (Location=/teacher)` |

**`GET /export.csv`**

| Flow | Data flow |
|---|---|
| F25 | Teacher -> Flask: `GET /export.csv (session cookie, optional class_id)` |
| F26 | Flask -> PostgreSQL: `Query (optional class_id)` |
| F27 | PostgreSQL -> Flask: `Query result (student, class, grade, comment)` |
| F28 | Flask -> Teacher: `HTTP 200 CSV (student, class, grade, comment; filename=grades.csv)` |

**`GET /admin`**

| Flow | Data flow |
|---|---|
| F29 | Admin -> Flask: `GET /admin (session cookie, optional ping_result)` |
| F30 | Flask -> PostgreSQL: `Query (users, classes)` |
| F31 | PostgreSQL -> Flask: `Query results (users: id, username, role, teacher_id; classes: id, name, teacher_id)` |
| F32 | Flask -> Admin: `HTTP 200 HTML (users, classes, user forms, ping form, optional ping_result)` |

**`POST /admin/users`**

| Flow | Data flow |
|---|---|
| F33 | Admin -> Flask: `POST /admin/users (session cookie; create: action, username, password, role; delete: action, user_id)` |
| F34 | Flask -> PostgreSQL: `Query (create user: username, password, role; delete user: user_id)` |
| F35 | PostgreSQL -> Flask: `Command result (write completion status)` |
| F36 | Flask -> Admin: `HTTP 302 (Location=/admin)` |

**`POST /admin/ping`**

| Flow | Data flow |
|---|---|
| F37 | Admin -> Flask: `POST /admin/ping (session cookie, host)` |
| F38 | Flask -> Shell/ping process: `Execute command string ("ping -c 1 " + host, shell=True)` |
| F39 | Shell/ping process -> Flask: `Process result (ping output or error)` |
| F40 | Flask -> Admin: `HTTP 200 HTML (ping_result, users, classes)` |

**`GET /static/<path:filename>`**

| Flow | Data flow |
|---|---|
| F41 | Browser -> Flask: `GET /static/<path:filename> (filename, optional cache-validation headers; e.g. style.css)` |
| F42 | Flask -> Static files: `Read/stat file (/app/static/<filename>)` |
| F43 | Static files -> Flask: `File result (content, modification time, size)` |
| F44 | Flask -> Browser: `HTTP 200 file (content, cache headers) or HTTP 304 (cache headers, no body)` |

Browser means a student, teacher, or admin browser.
F40 also reads users/classes through the same queries represented by F30–F31. F42–F43 access static files, not PostgreSQL. PostgreSQL write responses F23 and F35 indicate command completion, not updated rows.
