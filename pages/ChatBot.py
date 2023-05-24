import streamlit as st
st.header("ChatBot")
if 'username' in st.session_state:
    st.subheader(f"Welcome, {st.session_state['username']}!")
    if st.button("Logout"):
        del st.session_state['username']
        st.experimental_rerun()

else:
    st.warning("Login to continue")

