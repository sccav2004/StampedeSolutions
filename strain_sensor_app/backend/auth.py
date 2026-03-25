import hashlib

USERS = {
    "admin": hashlib.sha256("password123".encode()).hexdigest()
}

def authenticate(username, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()

    if username in USERS and USERS[username] == hashed:
        return True

    return False
