import streamlit as st

from call_openai import get_ai_gateway_access_token
from ai_gateway import DeereAIGatewayOpenAI
import os

# Show title and description.
st.title("💬 Agentic Land Dashboard")
st.write(
    "This is a simple chatbot that uses DeereAI's OpenAI GPT-4o-mini gateway to generate responses. "
    "It references the various Land tables in the EDL to respond to queries, with dynamic outputs."
    "The outputs include dashboards and text."
)

# try/except?
access_token = get_ai_gateway_access_token()

client = DeereAIGatewayOpenAI(
    access_token=access_token,
    base_url=os.getenv("AI_GATEWAY_BASE_URL"),
    deere_ai_gateway_registration_id=os.getenv("AI_GATEWAY_REGISTRATION_ID")
)

# Create a session state variable to store the chat messages. This ensures that the
# messages persist across reruns.
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "developer", # initial instructions for LLM behavior, thus leave as developer ; != assistant
            "content": "You are an awesome assistant here to help users.",
        },
        {
            "role": "user",
            "content": "Hello, Deere AI!"
        },
    ]

# this loops 
# Display the existing chat messages via `st.chat_message`.
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        if message["role"] != 'developer':
            st.markdown(message["content"])

# Create a chat input field to allow the user to enter a message. This will display
# automatically at the bottom of the page.
if prompt := st.chat_input("Hello, Deere AI!"):

    # Store and display the current prompt.
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate a new response using the DeereAI gateway bearer token
    stream = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=[
            {"role": m["role"], "content": m["content"]}
            for m in st.session_state.messages
        ],
        stream=True,
    )

    # stream?

    # Stream the response to the chat using `st.write_stream`, then store it in 
    # session state.
    with st.chat_message("assistant"):
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})