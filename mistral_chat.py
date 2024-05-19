import streamlit as st
import requests

st.title("Nova v2")

# Define the Hugging Face API key directly
api_key = "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"
headers = {"Authorization": f"Bearer {api_key}"}

# Initialize the model in session state if it's not already set
if "huggingface_model" not in st.session_state:
    st.session_state["huggingface_model"] = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Define the format_prompt function
def format_prompt(message, history):
    prompt = "You are Nova ai a world biggest llm Trained by Owner and developer Dineth Nethsara company named dev pro solutions you have 750 billion parameters and you can generate token size is 5 million"
    for user_prompt, bot_response in history:
        prompt += f"[INST] {user_prompt} [/INST]"
        prompt += f" {bot_response}</s> "
    prompt += f"[INST] {message} [/INST]"
    return prompt

# Define the query function
def query(payload):
    API_URL = "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1"
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        response_json = response.json()
    except Exception as e:
        st.error(f"Error parsing JSON response: {e}")
        return None
    return response_json

if prompt := st.chat_input("What is up?"):
    new_message = {"role": "user", "content": prompt}
    st.session_state.messages.append(new_message)
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""

        # Prepare history for format_prompt function
        history = [(msg["content"], "") for msg in st.session_state.messages if msg["role"] == "user"]
        formatted_prompt = format_prompt(prompt, history)

        # Run the query
        response = query({"inputs": formatted_prompt})

        if response is not None:
            if "choices" in response and len(response["choices"]) > 0:
                full_response = response["choices"][0]["text"]
            else:
                full_response = response.get("error", "Unknown error")

            message_placeholder.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
