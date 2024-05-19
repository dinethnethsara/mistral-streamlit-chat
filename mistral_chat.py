import streamlit as st
import requests
import os
import asyncio

st.title("Hugging Face Chat")

# Function to reset the state
def reset_state():
    for key in st.session_state:
        del st.session_state[key]

# Get the API key from the environment variables or the user
api_key = os.getenv("HUGGINGFACE_API_KEY")
if not api_key:
    if "api_key" not in st.session_state:
        st.session_state["api_key"] = st.text_input("Enter your Hugging Face API key", type="password")
    api_key = st.session_state["api_key"]
else:
    if expected_password := os.getenv("PASSWORD"):
        password = st.text_input("What's the secret password?", type="password")
        # Check if the entered key matches the expected password
        if password != expected_password:
            api_key = ''
            st.error("Unauthorized access.")
            reset_state()  # This line will reset the script
        else:
            api_key = os.getenv("Bearer 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")

headers = {"Authorization": f"Bearer {api_key}"}

# Initialize the model in session state if it's not already set
if "huggingface_model" not in st.session_state:
    st.session_state["huggingface_model"] = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

# Add system prompt input
if "system_prompt" not in st.session_state:
    st.session_state["system_prompt"] = ''
st.text_input('System Prompt', value=st.session_state["system_prompt"], key="system_prompt")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Add system prompt as a message if it doesn't exist
if st.session_state["system_prompt"] and not any(message["role"] == "system" for message in st.session_state.messages):
    st.session_state.messages.insert(0, {"role": "system", "content": st.session_state["system_prompt"]})

for message in st.session_state.messages:
    if message["role"] != "system":  # Skip system messages for UI
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

# Define the async query function
async def query(data):
    response = await fetch(
        "https://api-inference.huggingface.co/models/mistralai/Mixtral-8x7B-Instruct-v0.1",
        {
            "headers": { "Authorization": f"Bearer {"Bearer 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" },
            "method": "POST",
            "body": JSON.stringify(data),
        }
    )
    result = await response.json()
    return result

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

        # Use asyncio to run the query asynchronously
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        response = loop.run_until_complete(query({"inputs": formatted_prompt}))

        if "choices" in response and len(response["choices"]) > 0:
            full_response = response["choices"][0]["text"]
        else:
            full_response = "Error: " + response.get("error", "Unknown error")

        message_placeholder.markdown(full_response)
    
    st.session_state.messages.append({"role": "assistant", "content": full_response})
