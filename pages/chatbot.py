import time

import streamlit as st
import openai


st.set_page_config(page_title="MU ML Tutor", page_icon="🧑‍🏫")
st.title("MU ML Tutor Chatbot 🧑‍🏫")

if "auth" not in st.session_state:
    st.session_state["auth"] = False

if "openai_key" not in st.session_state:
    st.session_state["openai_key"] = None

if not st.session_state["auth"] or not st.session_state["openai_key"]:
    st.error("unauthorized")
    st.markdown(f"Please login in the app!")

    st.stop()


if "messages" not in st.session_state:
    st.session_state["messages"] = []

openai.api_key = st.session_state["openai_key"]

for msg in st.session_state["messages"]:
    st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    with st.spinner("generating response..."):
        if "thread_id" not in st.session_state:
            st.session_state["thread_id"] = openai.beta.threads.create().id
        thread_id = st.session_state["thread_id"]

        try:
            message = openai.beta.threads.messages.create(
                thread_id=thread_id,
                role="user",
                content=prompt,
            )

            run = openai.beta.threads.runs.create(
                thread_id=thread_id,
                assistant_id=st.secrets.openai.assistant_id,
            )

            total_time = 0
            while (run_status := openai.beta.threads.runs.retrieve(thread_id=thread_id,
                                                                  run_id=run.id).status) not in ["cancelled", "failed", "completed", "expired"]:
                total_time += 2
                time.sleep(2)

                if total_time > 10:
                    break

            if run_status == "completed":
                response = openai.beta.threads.messages.list(
                    thread_id=thread_id
                )
                response = response.data[0]
                for r in response.content:
                    st.session_state.messages.append({"role": "assistant", "content": r.text.value})
                    st.chat_message("assistant").write(r.text.value)
            else:
                st.chat_message("assistant").write("oops something went wrong, please try again!")
        except openai.AuthenticationError:
            st.error("Invalid OpenAI API, please refresh page and login with valid openai key.")
        except Exception as err:
            st.error(err)

