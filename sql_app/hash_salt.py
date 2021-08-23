import hashlib
from typing import Optional

HASH_SALT = "{%s}f9ca99e5d5c361b893da2ca49acd5f78152c20a128c8447de05823384e59834d"


def password_hash_sha256(password: str) -> Optional[str]:
    if isinstance(password, str):
        return hashlib.sha256((HASH_SALT % password).encode()).hexdigest()


print(password_hash_sha256("123123123"))