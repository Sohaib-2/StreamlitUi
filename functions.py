import hashlib
import re


def validate_username(username):
    if not re.match(r"^\w+$", username):
        return False
    return True


def validate_email(email):
    if not re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email):
        return False
    return True


def validate_password(password):
    if len(password) < 8:
        return False
    return True


def signup(username, email, password, c, conn):
    if not validate_username(username):
        return "Invalid username format"

    if not validate_email(email):
        return "Invalid email format"

    if not validate_password(password):
        return "Password should be at least 8 characters long"

    c.execute('SELECT * FROM users WHERE username=?', (username,))
    if c.fetchone() is not None:
        return "Username already exists"

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Insert data in db
    c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
    conn.commit()
    return "Signup successful"


def login(username, password, c):
    if not validate_username(username):
        return "Invalid username format"

    # Retrieve user
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()

    if user is None:
        return "User not found"

    # Verify the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user[2] != hashed_password:
        return "Incorrect password"

    return "Login successful"
