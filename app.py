import streamlit as st
import openai
import streamlit_authenticator as stauth




if "messages" not in st.session_state:
    st.session_state["messages"] = []


for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("generating response..."):
        response = chat_engine.query(prompt)
        msg = response.response
        st.session_state.messages.append({"role": "assistant", "content": msg})
        st.chat_message("assistant").write(msg)
