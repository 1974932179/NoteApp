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
