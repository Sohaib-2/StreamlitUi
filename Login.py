import streamlit as st
from functions import *
import sqlite3

# Create a connection to SQLite database
conn = sqlite3.connect('users.db')
c = conn.cursor()

# Create a table to store user information
c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        email TEXT,
        password TEXT
    )
''')


def main():
    st.title("Login/Signup")

    menu = st.sidebar.selectbox("Login/Signup", ("Login", "Signup"))

    if menu == "Signup":
        with st.form("signup_form"):
            st.subheader("SignUp")
            username = st.text_input('Username')
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Sign Up")

        if submitted:
            result = signup(username, email, password, c=c, conn=conn)
            if result == "Signup successful":
                st.success("Signup successful. Please login.")
            else:
                st.error(result)

    elif menu == "Login":
        with st.form("login_form"):
            st.subheader("Login")
            username = st.text_input('Username')
            password = st.text_input('Password', type="password")
            submitted = st.form_submit_button("Login")

        if submitted:
            result = login(username, password, c)
            if result == "Login successful":
                st.success("Login successful!")
                st.session_state['username'] = username
            else:
                st.error(result)


if __name__ == '__main__':
    main()
