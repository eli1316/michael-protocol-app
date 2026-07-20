# Veriluxe — The Michael Protocol

**Protect the truth. Document your reality. Reclaim your power.**

An AI assistant built on the [VERILUX Conscious AGI Framework](docs/VERILUX_Whitepaper.md).
The whitepaper's six axioms and Conscious Decision Loop are encoded directly
into every module's instructions (`veriluxe/framework.py`), and the full
instruction set is visible in-app under **Transparent Logic** — nothing hidden.

## Modules

| Module | Michael Protocol Layer | What it does |
|--------|------------------------|--------------|
| 🛡️ Guardian Chat | — | General assistant, fully framework-aligned |
| 👁️ Detection | Layer 01 — Seeing clearly | Names manipulation patterns with evidence, and teaches you to spot them |
| 📓 Journal | Layer 02 — Proving truth | Structured incident logging with pattern tags, timeline, pattern-frequency view, and clean exports. Entries stay in your browser session and your downloaded files — nothing stored on a server |
| ⚖️ Defense | Layer 03 — Taking action | Structure for affidavits, complaints, and preparation (not legal advice) |
| 🧭 Grounding | — | The Michael Protocol Activation Guide: presence, alignment, direction |
| 📜 The Framework | — | The whitepaper the AI runs on |

## Running it

```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
```

Add your API key to `.streamlit/secrets.toml` locally, or in Streamlit Cloud
under **Settings → Secrets**:

```toml
OPENAI_API_KEY = "sk-..."
# optional — defaults to gpt-4o
OPENAI_MODEL = "gpt-4o"
```

## Important

Veriluxe is an educational and documentation tool. It is **not** therapy,
legal advice, or an emergency service. If you are in immediate danger, call
911 (US) or your local emergency number. National Domestic Violence Hotline:
**1-800-799-7233** · text **START** to **88788** · [thehotline.org](https://www.thehotline.org)
