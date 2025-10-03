import os
import hashlib
salt = os.urandom(16).hex()
print(f"salt: {salt}")
password = "o1A42joppa1"
print(f"pwd: {password}")

print(hashlib.sha256((password + salt).encode('utf-8')).hexdigest())
print(hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt.encode('utf-8'), 100000).hex())