import streamlit as st
import openai

openai.api_key = st.secrets.openai.api_key

st.title("MU ML Tutor Chatbot" )

@st.cache_resource()
def get_new_thread():
    thread = openai.beta.threads.create()
    return thread.id


thread_id = get_new_thread()

if "messages" not in st.session_state:
    st.session_state["messages"] = []

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if not st.session_state["auth"]:
    st.error("unauthorized")
    st.markdown(f"Please login in the app!")

    st.stop()

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("generating response..."):
        message = openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt,
        )
        run = openai.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=st.secrets.openai.assistant_id,
        )
        response = openai.beta.threads.messages.list(
            thread_id=thread_id, order="desc"
        )
        try:
            response = response.data[1]

            for r in response.content:
                msg = r.text.value
                st.session_state.messages.append({"role": "assistant", "content": msg})
                st.chat_message("assistant").write(msg)
        except:
            st.chat_message("assistant").write("oops something went wrong, please try again!")
