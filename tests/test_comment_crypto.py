import base64
import sys
import unittest
from pathlib import Path

from cryptography.exceptions import InvalidTag

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "web"))

from comment_crypto import PREFIX, decrypt_comment, encrypt_comment


class CommentCryptoTests(unittest.TestCase):
    def test_round_trip(self):
        text = "Good work — 评论测试"
        self.assertEqual(decrypt_comment(encrypt_comment(text)), text)

    def test_fresh_nonce(self):
        first = encrypt_comment("Same comment")
        second = encrypt_comment("Same comment")
        self.assertNotEqual(first, second)
        self.assertEqual(decrypt_comment(first), decrypt_comment(second))

    def test_empty_and_null(self):
        self.assertEqual(decrypt_comment(encrypt_comment("")), "")
        self.assertIsNone(decrypt_comment(encrypt_comment(None)))

    def test_tampering_is_rejected(self):
        encrypted = encrypt_comment("Original comment")
        payload = bytearray(base64.b64decode(encrypted[len(PREFIX):]))
        payload[-1] ^= 1
        tampered = PREFIX + base64.b64encode(payload).decode("ascii")

        with self.assertRaises(InvalidTag):
            decrypt_comment(tampered)

    def test_plaintext_is_rejected(self):
        with self.assertRaises(ValueError):
            decrypt_comment("Unencrypted comment")


if __name__ == "__main__":
    unittest.main(verbosity=2)