import streamlit as st

st.set_page_config(page_title="MU ML Tutor", page_icon="🧑‍🏫")
st.title("MU ML Tutor Chatbot 🧑‍🏫")


if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "auth" not in st.session_state:
    st.session_state["auth"] = False


if not st.session_state["auth"]:
    username = st.text_input("username")
    password = st.text_input("password", type="password")
    openai_key = st.text_input("openAI key", type="password")


    for valid_username, valid_password in st.secrets.credentials.users:
        if valid_username == username and valid_password == password:
            if openai_key:
                st.session_state["openai_key"] = openai_key
            else:
                if valid_username == "admin" :
                    st.session_state["openai_key"] = st.secrets.openai.api_key
                else:
                    st.stop()
            st.session_state["auth"] = True


if st.session_state["auth"]:
    st.write("you may now use the the chatbot!")







