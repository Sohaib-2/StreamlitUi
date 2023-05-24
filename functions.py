import hashlib


def signup(username, email, password, c, conn):
    # Check if the username already exists
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    if c.fetchone() is not None:
        return False  # Username already exists

    # Hash the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Insert the user into the database
    c.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
    conn.commit()
    return True  # Signup successful


def login(username, password, c):
    # Retrieve the user from the database
    c.execute('SELECT * FROM users WHERE username=?', (username,))
    user = c.fetchone()

    if user is None:
        return False  # User not found

    # Verify the password
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    if user[2] != hashed_password:
        return False  # Incorrect password

    return True  # Login successful