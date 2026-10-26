import base64
import os
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

PREFIX = "aesgcm:v1:"
AAD = b"notes.comment:v1"

key_path = Path(
    os.environ.get("COMMENT_KEY_FILE", "/run/secrets/comment_key")
)
key = key_path.read_bytes()

if len(key) != 32:
    raise ValueError("Comment key must contain exactly 32 bytes")

aesgcm = AESGCM(key)


def encrypt_comment(value):
    if value is None:
        return None

    nonce = os.urandom(12)
    ciphertext = aesgcm.encrypt(nonce, value.encode("utf-8"), AAD)
    payload = base64.b64encode(nonce + ciphertext).decode("ascii")
    return PREFIX + payload


def decrypt_comment(value):
    if value is None:
        return None

    if not value.startswith(PREFIX):
        raise ValueError("Comment is not encrypted")

    payload = base64.b64decode(value[len(PREFIX):], validate=True)

    if len(payload) < 28:
        raise ValueError("Invalid encrypted comment")

    nonce = payload[:12]
    ciphertext = payload[12:]
    plaintext = aesgcm.decrypt(nonce, ciphertext, AAD)
    return plaintext.decode("utf-8")