# Class 10 — NotesApp stored XSS fix

**Name:** Siyuan Wu

**Test date:** 19 November 2026

**Scope:** Local NotesApp at `https://localhost`, using the seeded grade record
#2 for `alice` in Computer Science (10.5).

## Before the fix

The [student dashboard](../../web/templates/dashboard.html) and [teacher grades
page](../../web/templates/teacher.html) both disabled Jinja autoescaping around
`n.comment`. This gave the browser stored teacher comments as raw HTML. A
comment therefore remained in the database and could be interpreted as markup
when another user opened a grades page.

I used `<b>Class 10 preview</b>` as a harmless formatting check on record #2.
Before the teacher template was fixed, **All grades** showed the comment in
bold. This demonstrated that the browser interpreted the stored markup. The
lab's script execution check remains unverified.

The original template and browser screenshots show the behavior before the
fix. [Student template](screenshots/dashboard-before-template.png) ·
[Teacher template](screenshots/teacher-before-template.png) ·
[Teacher page](screenshots/teacher-before-escaping.png)

## Fix

I removed the `autoescape false` blocks from both templates and kept the
comment cell as `<td>{{ n.comment }}</td>`. Flask's Jinja autoescaping then
encodes HTML special characters as it renders the page.

## After the fix

| Check | Observed result | Evidence |
| --- | --- | --- |
| Student **My grades** | Record #2 showed the complete `<b>Class 10 preview</b>` string as text. | [Student page](screenshots/dashboard-after-escaping.png) |
| Teacher **All grades** | After fixing the teacher template, record #2 showed the same string as text. | [Teacher page](screenshots/teacher-after-escaping.png) |
| Normal comment | The student page displayed `Score < 10 & retry` with the original characters. The teacher page also displayed that comment during the earlier browser check. | [Student page](screenshots/dashboard-after-normal-comment.png), [earlier teacher check](screenshots/teacher-normal-comment-initial.png) |

I also rendered both final templates with Flask and checked the generated HTML.
All four checks passed. Both pages encoded the angle brackets in the formatting
example and encoded `<` and `&` in the normal comment.

AI assistance was used to draft this report and check the final template
output. The browser evidence comes from my local screenshots.

[Class 10 lab instructions](https://github.com/KristenPire/epita-security-labs/blob/main/docs/class10/stored-xss.md)
