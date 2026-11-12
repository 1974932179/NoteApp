# HMAC CSV Verification

**Name 1:** Siyuan Wu

**Name 2:** Congwen Liu

**Date:** 25 October 2026

We tested `hmac_csv.py` and `verify_csv.py` using a temporary copy of the existing
721-byte NotesApp CSV export. The signing script generated a fresh temporary key
and appended an HMAC-SHA256 footer. The original export and project key were not
modified.

| Check | Change | Result |
| --- | --- | --- |
| Original signed CSV | None | `CHECK PASSED` |
| Modified CSV | Alice's grade changed from 10.5 to 18.0; original HMAC retained | `CHECK FAILED` |
| Restored CSV | Original signed bytes restored | `CHECK PASSED` |

**Conclusion:** Changing a grade changes the recomputed HMAC, so the original tag
no longer matches. HMAC detects changes to the CSV bytes when the verifier has the
correct secret key. It does not encrypt the grades; the key must remain private.

Two automated regression tests also passed: an unchanged CSV is accepted, and a
changed grade is rejected with the original HMAC. The tests use fictional data
and temporary files. Run them from the NoteApp folder:

```powershell
python -m unittest discover -s tests -p test_hmac_csv.py -v
```

Test code: [test_hmac_csv.py](../../tests/test_hmac_csv.py).

## Web export verification

The teacher export now signs the CSV bytes inside `/export.csv` before returning
`grades_signed.csv`. The existing verifier reads that download directly using
the same `HMAC_KEY`.

The regression test uses the actual Flask route, a test session, a fictional
grade from a simulated database, and temporary keys. It exercises both full and
class-filtered downloads, and runs `verify_csv.py` on the response bytes.

| Check | Result |
| --- | --- |
| Original download | HTTP 200, `CHECK PASSED`, exit code 0 |
| Grade changed with the original HMAC retained | `CHECK FAILED`, exit code 1 |
| Export with an absent or invalid key | HTTP 503 |

Test code: [test_csv_export.py](../../tests/test_csv_export.py).
