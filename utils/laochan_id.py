import hashlib
import mmh3

def token_to_infinitas_id(token):
    key = hashlib.md5(token.encode('utf-8')).hexdigest()
    return ('LCHAN' + key)[:13]

HIGHWAY_KEY = b'LAOCHANID_HIGHWAY_KEY_NOTSECURE!'

def token_to_hash(token):
    seed = int.from_bytes(HIGHWAY_KEY[:4], byteorder='little')
    hash_value = mmh3.hash128(token.encode('utf-8'), seed=seed)
    hash_hex = format(hash_value, 'x').upper()
    return hash_hex

def token_to_card_number(token):
    hash_value = token_to_hash(token)
    return ('LCHAN' + hash_value.upper())[:16]

def token_to_code(token):
    seed = int.from_bytes(HIGHWAY_KEY[:4], byteorder='little')
    hash_value = mmh3.hash(token.encode('utf-8'), seed=seed) & 0xFFFFFFFF
    return 'MOAI' + str(hash_value).zfill(9)[:9]

def token_to_sns_id(token):
    seed = int.from_bytes(HIGHWAY_KEY[:4], byteorder='little')
    hash_value = mmh3.hash(token.encode('utf-8'), seed=seed) & 0xFFFFFFFF
    return str(hash_value).zfill(8)

def token_to_sdvx_id(token):
    sns_id = token_to_sns_id(token)
    return f'SV-{sns_id[:4]}-{sns_id[4:8]}'