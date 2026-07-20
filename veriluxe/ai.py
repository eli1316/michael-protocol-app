"""Thin wrapper around the OpenAI API for the VeriLuxe Guardian."""

import os

import streamlit as st
from openai import OpenAI

DEFAULT_MODEL = "gpt-4o"


def _secret(name: str, default: str | None = None) -> str | None:
    # Streamlit Cloud provides secrets.toml; Docker hosts (Render, Railway,
    # Fly, Cloud Run) provide environment variables. Support both.
    # st.secrets raises StreamlitSecretNotFoundError when no secrets.toml
    # exists at all, so a plain .get() is not enough.
    try:
        value = st.secrets.get(name)
    except Exception:
        value = None
    return value or os.environ.get(name) or default


def get_client() -> OpenAI | None:
    api_key = _secret("OPENAI_API_KEY")
    if not api_key:
        return None
    return OpenAI(api_key=api_key)


def get_model() -> str:
    return _secret("OPENAI_MODEL", DEFAULT_MODEL)


def chat(system_prompt: str, history: list[dict]) -> str:
    """Send the module's system prompt plus conversation history; return the reply."""
    client = get_client()
    if client is None:
        raise RuntimeError(
            "No OPENAI_API_KEY found. Add it in Streamlit Cloud under "
            "Settings → Secrets, e.g.\n\nOPENAI_API_KEY = \"sk-...\""
        )
    messages = [{"role": "system", "content": system_prompt}] + history
    response = client.chat.completions.create(
        model=get_model(),
        messages=messages,
    )
    return response.choices[0].message.content
