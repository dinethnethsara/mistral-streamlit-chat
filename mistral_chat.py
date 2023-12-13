from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
import streamlit as st
import os

st.title("Mistral Chat")

# Get the API key from the environment variables or the user
api_key = os.getenv("MISTRAL_API_KEY")
if not api_key:
    api_key = st.text_input("Enter your Mistral API key", type="password", key="api_key_input")
    if api_key:
        st.session_state["api_key"] = api_key

if "api_key" in st.session_state:
    client = MistralClient(api_key=st.session_state["api_key"])
else:
    st.warning("Enter your Mistral API key to use the app.")
    st.stop()

# Initialize the model in session state if it's not already set
if "mistral_model" not in st.session_state:
    st.session_state["mistral_model"] = 'mistral-tiny'

# Always display the dropdown
model_options = ('mistral-tiny', 'mistral-small', 'mistral-medium')
st.session_state["mistral_model"] = st.selectbox('Select a model', model_options, index=model_options.index(st.session_state["mistral_model"]), key="model_select")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message.role):  # Use dot notation here
        st.markdown(message.content)  # And here

if prompt := st.chat_input("What is up?"):
    new_message = ChatMessage(role="user", content=prompt)
    st.session_state.messages.append(new_message)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        for response in client.chat_stream(
            model=st.session_state["mistral_model"],
            messages=st.session_state.messages,  # Pass the entire messages list
        ):
            full_response += (response.choices[0].delta.content or "")
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    st.session_state.messages.append(ChatMessage(role="assistant", content=full_response))