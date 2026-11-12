import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import Mock, patch


REPO = Path(__file__).resolve().parents[1]
TEST_KEY = "ab" * 32


class CsvExportTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        folder = tempfile.TemporaryDirectory(prefix="notesapp-export-")
        cls.addClassCleanup(folder.cleanup)
        cls.folder = Path(folder.name)
        comment_key = cls.folder / "comment_key"
        comment_key.write_bytes(bytes(range(32)))
        (cls.folder / ".env").write_text(f"HMAC_KEY={TEST_KEY}\n", encoding="utf-8")

        fixture_env = {
            "COMMENT_KEY_FILE": str(comment_key),
            "JWT_SECRET": "test-jwt-key",
        }
        with patch.dict(os.environ, fixture_env):
            with patch.object(sys, "path", [str(REPO / "web"), *sys.path]):
                import app

        cls.notes_app = app

    def setUp(self):
        config = patch.dict(
            self.notes_app.app.config,
            {"TESTING": True, "SECRET_KEY": "test-session-key"},
        )
        self.addCleanup(config.stop)
        config.start()
        self.client = self.notes_app.app.test_client()
        with self.client.session_transaction() as session:
            session.update(user_id=1, username="fixture", role="teacher")

    def verify_download(self, data):
        (self.folder / "grades_signed.csv").write_bytes(data)
        return subprocess.run(
            [sys.executable, "-B", str(REPO / "verify_csv.py")],
            cwd=self.folder,
            env={**os.environ, "PYTHONIOENCODING": "utf-8"},
            capture_output=True,
            text=True,
            encoding="utf-8",
        )

    def test_download_verifies_and_grade_tampering_fails(self):
        db = Mock()
        db.cursor.return_value.fetchall.return_value = [
            {
                "student": "fixture",
                "class": "Security",
                "grade": 14,
                "comment": self.notes_app.encrypt_comment("Tr\u00e8s bien"),
            }
        ]

        with patch.object(self.notes_app, "get_db", return_value=db):
            with patch.dict(os.environ, {"HMAC_KEY": TEST_KEY}):
                for path in ("/export.csv", "/export.csv?class_id=1"):
                    with self.subTest(path=path):
                        response = self.client.get(path)
                        self.assertEqual(response.status_code, 200)
                        self.assertEqual(response.mimetype, "text/csv")
                        self.assertEqual(
                            response.headers["Content-Disposition"],
                            "attachment; filename=grades_signed.csv",
                        )
                        self.assertIn("fixture,Security,14,Tr\u00e8s bien".encode(), response.data)

                        valid = self.verify_download(response.data)
                        self.assertEqual((valid.returncode, valid.stdout.strip()), (0, "CHECK PASSED"))

                        changed = response.data.replace(b",14,", b",18,", 1)
                        invalid = self.verify_download(changed)
                        self.assertNotEqual(invalid.returncode, 0)
                        self.assertEqual(invalid.stdout.strip(), "CHECK FAILED")

    def test_export_without_a_valid_key_does_not_send_csv(self):
        with patch.object(self.notes_app, "get_db") as get_db:
            for key in ("", "invalid"):
                with self.subTest(key_configured=bool(key)):
                    with patch.dict(os.environ, {"HMAC_KEY": key}):
                        response = self.client.get("/export.csv")
                    self.assertEqual(response.status_code, 503)
                    self.assertNotIn("Content-Disposition", response.headers)
            get_db.assert_not_called()
