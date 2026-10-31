\# LOGIN FIX — NotesApp flaw #4



\*\*Name:\*\* Siyuan Wu  

\*\*Test date:\*\* 30 October 2026



\- \*\*Fix 1:\*\* `verify\_jwt` rejects `alg:none` and accepts only HS256, checking the signature with `hmac.compare\_digest`.

\- \*\*Fix 2:\*\* `JWT\_SECRET` was replaced with a long random value and is read from the environment without a default.

\- \*\*Proof:\*\*

&#x20; - Unsigned `alg:none` token → `unauthorized`.

&#x20; - Token signed with the old `s3cr3t` secret → `unauthorized`.

&#x20; - Real Alice login → succeeds; the dashboard displays Alice’s grades.



!\[Unsigned token rejected](none\_rejected.png)



!\[Old-secret token rejected](old\_secret\_rejected.png)



!\[Real Alice login succeeds](real\_login.png)



!\[Alice dashboard](dashboard.png)

