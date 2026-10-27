from pathlib import Path
import os
import subprocess
import sys
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
CSV = b"student,class,grade,comment\nalice,Security,14,Good work\n"


class HmacCsvTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="notesapp-hmac-")
        self.addCleanup(self.temp.cleanup)
        self.folder = Path(self.temp.name)
        (self.folder / ".env").write_text(
            "HMAC_KEY=" + "ab" * 32 + "\n",
            encoding="utf-8",
        )
        (self.folder / "grades.csv").write_bytes(CSV)
        self.run_script("hmac_csv.py")

    def run_script(self, name):
        result = subprocess.run(
            [sys.executable, str(REPO / name)], cwd=self.folder,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            capture_output=True, text=True, encoding="utf-8", check=True,
        )
        return result.stdout.strip()

    def test_original_csv_passes(self):
        self.assertEqual(self.run_script("verify_csv.py"), "CHECK PASSED")
        self.assertEqual((self.folder / "grades.csv").read_bytes(), CSV)

    def test_changed_grade_fails_with_original_hmac(self):
        signed = self.folder / "grades_signed.csv"
        original = signed.read_bytes()
        changed = original.replace(b",14,", b",18,", 1)
        self.assertNotEqual(changed, original)
        self.assertEqual(changed.rpartition(b"\n# HMAC: ")[2],
                         original.rpartition(b"\n# HMAC: ")[2])
        signed.write_bytes(changed)

        self.assertEqual(self.run_script("verify_csv.py"), "CHECK FAILED")
        signed.write_bytes(original)
        self.assertEqual(self.run_script("verify_csv.py"), "CHECK PASSED")


if __name__ == "__main__":
    unittest.main()
