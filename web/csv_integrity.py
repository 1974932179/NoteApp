import hashlib
import hmac


HMAC_FOOTER = b"\n# HMAC: "


def parse_hmac_key(value: str | None) -> bytes:
    if not value:
        raise ValueError("HMAC_KEY is missing")
    error = "HMAC_KEY must be a 64-character hexadecimal string"
    if len(value) != 64:
        raise ValueError(error)
    try:
        key = bytes.fromhex(value)
    except ValueError as exc:
        raise ValueError(error) from exc
    if len(key) != 32:
        raise ValueError(error)
    return key


def csv_hmac(data: bytes, key: bytes) -> bytes:
    return hmac.new(key, data, hashlib.sha256).hexdigest().encode("ascii")


def sign_csv(data: bytes, key: bytes) -> bytes:
    return data + HMAC_FOOTER + csv_hmac(data, key) + b"\n"
