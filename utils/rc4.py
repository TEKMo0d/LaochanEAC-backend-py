import hashlib
from arc4 import ARC4

EAMUSE_RC4_KEY = '69D74627D985EE2187161570D08D93B12455035B6DF0D8205DF5'

def rc4_transform(key_hex: str, data: bytes) -> bytes:
    combined_key_bytes = bytes.fromhex(key_hex + EAMUSE_RC4_KEY)
    
    md5_key = hashlib.md5(combined_key_bytes).digest()
    
    cipher = ARC4(md5_key)
    return cipher.encrypt(data)
