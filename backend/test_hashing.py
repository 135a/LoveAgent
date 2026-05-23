import hashlib
import bcrypt

def _pre_hash_password(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).hexdigest().encode("utf-8")

def hash_password(password: str) -> str:
    pre_hashed = _pre_hash_password(password)
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pre_hashed, salt)
    return hashed.decode("utf-8")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pre_hashed = _pre_hash_password(plain_password)
    return bcrypt.checkpw(pre_hashed, hashed_password.encode("utf-8"))

# Test cases
passwords = [
    "short_pass",
    "a" * 71,
    "a" * 72,
    "a" * 73,
    "a" * 100,
    "very_long_password_" + "x" * 150
]

print("=== Hashing Test ===")
for p in passwords:
    hashed = hash_password(p)
    is_valid = verify_password(p, hashed)
    print(f"Length: {len(p):<3} | Valid: {is_valid} | Hash: {hashed[:30]}...")
    if not is_valid:
        print(f"FAILED for length {len(p)}")
        exit(1)

print("\n=== Cross-Verification Test ===")
p1 = "secret"
h1 = hash_password(p1)
print(f"Correct: {verify_password(p1, h1)}")
print(f"Wrong pass: {verify_password('wrong', h1)}")
print(f"Tampered hash: {verify_password(p1, h1[:-1] + 'x')}")

print("\nSUCCESS: All hashing tests passed.")
