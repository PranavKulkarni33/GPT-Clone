from openai import OpenAI
import streamlit as st
import os

st.title("GPT like clone")

chosen_model = st.selectbox("Choose the model provider" ,
             ["OpenAI", "Anyscale", "Together AI"])

if chosen_model == "OpenAI":
    client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])
elif chosen_model == "Anyscale":
    client = OpenAI(api_key=st.secrets["ANYSCALE_API_KEY"],base_url=os.environ.get("ANYSCALE_BASE_URL"))
    st.session_state["openai_model"] = "mistralai/Mixtral-8x7B-Instruct-v0.1"
elif chosen_model == "Together AI":
    client = OpenAI(api_key=st.secrets["TOGETHERAI_API_KEY"],base_url=os.environ.get("TOGETHERAI_BASE_URL"))
    st.session_state["openai_model"] = "mistralai/Mixtral-8x7B-Instruct-v0.1"


if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-3.5-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What's up?"):
    st.session_state.messages.append({"role":"user", "content": prompt})

    with st.chat_message("user"):
        st.markdown(prompt)


    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        for response in client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages],
            stream= True,
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌ ")

        message_placeholder.markdown(full_response)

    st.session_state.messages.append({"role" : "assistant", "content": full_response})
    