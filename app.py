import streamlit as st


if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "auth" not in st.session_state:
    st.session_state["auth"] = False


if not st.session_state["auth"]:
    username = st.text_input("username")
    password = st.text_input("password", type="password")
    auth = True

    for valid_username, valid_password in st.secrets.credentials.users:
        if valid_username == username and valid_password == password:
            st.session_state["auth"] = True
            break


if st.session_state["auth"]:
    st.write("you may now use the the chatbot!")







