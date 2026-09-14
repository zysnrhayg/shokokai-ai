import hashlib
import bcrypt
# py_encrypt.vm
# New passwords are hashed with bcrypt. Login still accepts legacy SHA-1 hashes.

def check_password_sha1(plain: str, hashed: str) -> bool:
	"""Verify plaintext against a SHA-1 hex hash (legacy). Returns True if match."""
	if not plain or not hashed:
		return False
	return hashlib.sha1(plain.encode("utf-8")).hexdigest() == hashed

def hash_password(plain: str) -> str:
	"""Hash a plaintext password with bcrypt. Store the return value; never store plain passwords."""
	if not plain:
		raise ValueError("password must be non-empty")
	return bcrypt.hashpw(plain.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

def check_password(plain: str, hashed: str) -> bool:
	"""Verify plaintext against a bcrypt hash. Returns True if match."""
	if not plain or not hashed:
		return False
	try:
		return bcrypt.checkpw(plain.encode("utf-8"), hashed.encode("utf-8"))
	except (ValueError, TypeError):
		return False


def is_bcrypt_hash(hashed: str) -> bool:
	"""Return True if hashed looks like a bcrypt hash ($2a$/$2b$/$2y$)."""
	if not hashed or not isinstance(hashed, str):
		return False
	return hashed.startswith(("$2a$", "$2b$", "$2y$")) and len(hashed) >= 59


def _is_sha1_hex(hashed: str) -> bool:
	if not hashed or len(hashed) != 40:
		return False
	return all(c in "0123456789abcdefABCDEF" for c in hashed)


def verify_password(plain: str, hashed: str) -> bool:
	"""
	Verify plaintext against stored hash.
	Supports bcrypt, SHA-1 hex (legacy), and temporary plaintext (mst_user_account).
	"""
	if not plain or not hashed:
		return False
	hashed = str(hashed).strip()
	if is_bcrypt_hash(hashed):
		return check_password(plain, hashed)
	if _is_sha1_hex(hashed):
		return check_password_sha1(plain, hashed)
	return plain == hashed


def encrypt_for_storage(password: str) -> str:
	"""
	Return bcrypt hash for DB storage.
	Blank stays blank; already-bcrypt values are left unchanged (avoid double-hash).
	"""
	#customized by WFC on 2026/07/24 ei
	if password is None:
		return password
	s = str(password)
	if not s.strip():
		return s
	if is_bcrypt_hash(s.strip()):
		return s.strip()
	return hash_password(s)


class Encrypt:
	def encrypt(self, s_data):
		"""Hash password with bcrypt (used when saving / resetting passwords)."""
		if not s_data:
			raise ValueError("password must be non-empty")
		return hash_password(s_data)

	def hash_byte_to_string(self, hash_bytes):
		# バイト配列を16進数文字列に変換（legacy helper）
		hex_string = ''.join(f'{byte:02x}' for byte in hash_bytes)
		return hex_string

	def encrypt_sha1(self, s_data):
		"""Legacy SHA-1 hash (kept for tests / migration tooling only)."""
		sha = hashlib.sha1()
		sha.update(s_data.encode('utf-8'))
		return self.hash_byte_to_string(sha.digest())
