import os
import sys
from pathlib import Path

# Add src to path for mypackage
sys.path.insert(0, str(Path(__file__).parent / "src"))

import streamlit as st

from mypackage.ollama_client import OllamaClient


st.set_page_config(page_title="Local Ollama Chat", page_icon="🤖", layout="centered")

st.title("Local Ollama Chat Interface")
st.markdown(
    "Use this interface to send prompts to your locally running Ollama server. "
    "Configure the endpoint and model with environment variables if needed."
)

ollama_url = st.text_input("Ollama URL", value=os.environ.get("OLLAMA_URL", "http://localhost:11434/api/chat"))
ollama_model = st.text_input("Ollama Model", value=os.environ.get("OLLAMA_MODEL", "qwen2.5-coder:7b"))
ollama_timeout = st.number_input("Timeout (seconds)", min_value=1, max_value=120, value=int(os.environ.get("OLLAMA_TIMEOUT", "30")))

client = OllamaClient(ollama_url=ollama_url, model=ollama_model, timeout=ollama_timeout)

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "system_prompt" not in st.session_state:
    st.session_state.system_prompt = os.environ.get(
        "OLLAMA_SYSTEM_PROMPT",
        "You are a helpful assistant answering user questions honestly and concisely.",
    )

st.sidebar.header("Session settings")
st.sidebar.text_area("System prompt", value=st.session_state.system_prompt, height=140, key="system_prompt_input")
if st.sidebar.button("Save system prompt"):
    st.session_state.system_prompt = st.session_state.system_prompt_input
    st.sidebar.success("System prompt saved.")

user_input = st.text_area("Your message", height=120, key="user_input")
if st.button("Send"):
    if user_input.strip():
        st.session_state.chat_history.append({"role": "user", "content": user_input.strip()})
        with st.spinner("Sending to Ollama..."):
            try:
                response_text = client.chat(
                    prompt=user_input.strip(),
                    system_prompt=st.session_state.system_prompt,
                    history=st.session_state.chat_history[:-1],
                )
                st.session_state.chat_history.append({"role": "assistant", "content": response_text})
            except Exception as exc:
                st.error(f"Ollama request failed: {exc}")

if st.session_state.chat_history:
    st.markdown("---")
    for turn in st.session_state.chat_history:
        if turn["role"] == "user":
            st.markdown(f"**You:** {turn['content']}")
        else:
            st.markdown(f"**Assistant:** {turn['content']}")
