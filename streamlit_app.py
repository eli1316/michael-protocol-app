"""Veriluxe — The Michael Protocol
AI assistant built on the VERILUX Conscious AGI Framework whitepaper.
"""

import streamlit as st

from veriluxe import ai, framework, journal

st.set_page_config(
    page_title="Veriluxe — The Michael Protocol",
    page_icon="🛡️",
    layout="centered",
)

# ---------------------------------------------------------------- sidebar
st.sidebar.title("VERILUXE")
st.sidebar.caption("Protect the truth. Document your reality. Reclaim your power.")

PAGES = {
    "🛡️ Guardian Chat": ("chat", "guardian"),
    "👁️ Detection — Seeing Clearly": ("chat", "detection"),
    "📓 Journal — Proving Truth": ("journal", None),
    "⚖️ Defense — Taking Action": ("chat", "defense"),
    "🧭 Grounding — Activation Guide": ("grounding", None),
    "📜 The Framework": ("framework", None),
}
choice = st.sidebar.radio("Modules", list(PAGES.keys()), label_visibility="collapsed")
kind, module_key = PAGES[choice]

st.sidebar.markdown("---")
st.sidebar.markdown(framework.CRISIS_NOTE)


# ---------------------------------------------------------------- chat pages
def render_chat(key: str) -> None:
    module = framework.MODULES[key]
    st.subheader(module["title"])
    st.caption(module["tagline"])

    # Axiom 5 — Transparent Logic: the full instruction set is auditable.
    with st.expander("🔍 Transparent Logic — see this module's full instructions"):
        st.code(module["prompt"], language=None)

    state_key = f"history_{key}"
    history = st.session_state.setdefault(state_key, [])

    for msg in history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Speak your truth…"):
        history.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                with st.spinner("Running the Conscious Decision Loop…"):
                    reply = ai.chat(module["prompt"], history)
                st.markdown(reply)
                history.append({"role": "assistant", "content": reply})
            except Exception as exc:
                st.error(str(exc))

    if history and st.button("Clear this conversation"):
        st.session_state[state_key] = []
        st.rerun()


# ---------------------------------------------------------------- grounding
def render_grounding() -> None:
    g = framework.ACTIVATION_GUIDE
    st.subheader("🧭 The Michael Protocol — Activation Guide")
    st.caption(g["purpose"])

    st.markdown("### Core Pillars")
    cols = st.columns(3)
    for col, (name, desc) in zip(cols, g["pillars"]):
        with col:
            st.markdown(f"**{name}**")
            st.caption(desc)

    st.markdown("### Activation Sequence")
    for i, step in enumerate(g["sequence"], start=1):
        st.markdown(f"{i}. {step}")

    st.markdown("### Grounding Statements")
    for s in g["grounding_statements"]:
        st.markdown(f"> “{s}”")

    st.markdown("### Energetic Shield Practice")
    for s in g["shield"]:
        st.markdown(f"- {s}")

    st.info(
        "For best results, practice once per day during calm periods. This "
        "builds nervous-system familiarity, making the protocol more "
        "effective during stress or conflict."
    )


# ---------------------------------------------------------------- framework
def render_framework() -> None:
    st.subheader("📜 The VERILUX Conscious AGI Framework")
    st.caption(
        "The whitepaper this AI runs on. Every module's instructions are "
        "assembled from these axioms — nothing hidden (Axiom 5)."
    )

    st.markdown("### Foundational Axioms")
    for i, (name, desc) in enumerate(framework.AXIOMS, start=1):
        st.markdown(f"**{i}. {name}** — {desc}")

    st.markdown("### The Conscious Decision Loop")
    st.markdown(" → ".join(f"**{s}**" for s, _ in framework.DECISION_LOOP))
    for step, desc in framework.DECISION_LOOP:
        st.markdown(f"- **{step}:** {desc}")

    st.markdown("### Core Interaction Rule")
    st.markdown(f"> “{framework.CORE_INTERACTION_RULE}”")

    st.markdown("### The Michael Protocol — Three Layers")
    st.markdown(
        "1. **Detection** — *seeing clearly.* Recognize manipulation "
        "patterns in real time.\n"
        "2. **Documentation** — *proving truth.* Turn experience into "
        "structured, court-ready records.\n"
        "3. **Defense** — *taking action.* Turn your documented pattern "
        "into real-world leverage."
    )
    st.caption(
        "Full whitepaper: docs/VERILUX_Whitepaper.md in this repository."
    )


# ---------------------------------------------------------------- router
if kind == "chat":
    render_chat(module_key)
elif kind == "journal":
    journal.render()
elif kind == "grounding":
    render_grounding()
else:
    render_framework()

st.markdown("---")
st.caption(
    "Veriluxe is an educational and documentation tool — not therapy, not "
    "legal advice, and not a substitute for either. Model in use: "
    f"`{ai.get_model()}`."
)
