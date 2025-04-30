import hashlib

def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()