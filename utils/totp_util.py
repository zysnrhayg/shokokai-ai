import base64
import hmac
import hashlib
import struct
import time


def _hotp(key, counter):
    digest = hmac.new(key, struct.pack(">Q", counter), hashlib.sha1).digest()
    offset = digest[-1] & 0x0F
    binary = struct.unpack(">I", digest[offset:offset + 4])[0] & 0x7FFFFFFF
    return "%06d" % (binary % 1000000)


def verify_totp(secret, code, window=1):
    code = str(code or "").strip().replace(" ", "")
    secret = str(secret or "").strip().replace(" ", "").upper()
    if not secret or not code.isdigit() or len(code) != 6:
        return False
    try:
        key = base64.b32decode(secret, casefold=True)
    except Exception:
        return False
    timestep = int(time.time()) // 30
    for delta in range(-window, window + 1):
        if hmac.compare_digest(_hotp(key, timestep + delta), code):
            return True
    return False
