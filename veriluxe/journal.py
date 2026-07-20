"""The Michael Protocol Journal — private, structured incident documentation.

Entries live only in the browser session (Streamlit session state) and in
files the user chooses to download. Nothing is stored on a server.
"""

import json
from datetime import date, datetime

import pandas as pd
import streamlit as st

from veriluxe import ai, framework

STATE_KEY = "journal_entries"


def _entries() -> list[dict]:
    return st.session_state.setdefault(STATE_KEY, [])


def _export_json() -> str:
    return json.dumps(
        {
            "app": "Michael Protocol Journal",
            "exported": datetime.now().isoformat(timespec="seconds"),
            "entries": _entries(),
        },
        indent=2,
    )


def _export_markdown() -> str:
    lines = [
        "# Michael Protocol Journal — Documentation Record",
        f"_Exported {datetime.now().strftime('%B %d, %Y at %H:%M')}. "
        "Prepared by the record's author; entries listed chronologically._",
        "",
    ]
    for i, e in enumerate(sorted(_entries(), key=lambda x: x["date"]), start=1):
        lines += [
            f"## Entry {i} — {e['date']}",
            f"**Pattern tags:** {', '.join(e['tags']) or '—'}",
            "",
            e["text"],
            "",
            "---",
            "",
        ]
    return "\n".join(lines)


def render() -> None:
    st.subheader("📓 The Michael Protocol Journal")
    st.caption(
        "Log incidents with pattern tags, build your timeline, and export a "
        "clean record. Entries exist only in this browser session and in the "
        "files you download — nothing is sent to a server. **Download a "
        "backup before closing the tab**, and store it somewhere the other "
        "party cannot access."
    )

    # ---- restore from backup ----
    with st.expander("Restore from a backup file"):
        uploaded = st.file_uploader("Upload a journal JSON backup", type="json")
        if uploaded is not None and st.button("Restore entries"):
            try:
                data = json.load(uploaded)
                st.session_state[STATE_KEY] = data["entries"]
                st.success(f"Restored {len(data['entries'])} entries.")
                st.rerun()
            except (KeyError, json.JSONDecodeError):
                st.error("That file doesn't look like a journal backup.")

    # ---- new entry ----
    st.markdown("### New entry")
    entry_date = st.date_input("Date of incident", value=date.today())
    tags = st.multiselect("Pattern tags", framework.PATTERN_TAGS)
    raw = st.text_area(
        "What happened?",
        height=180,
        placeholder=(
            "Write freely — what was said, what was done, who was there, "
            "how it affected you. You can structure it with AI before saving."
        ),
    )

    col_a, col_b = st.columns(2)
    structured = st.session_state.get("journal_structured")

    with col_a:
        if st.button("✨ Structure with AI", disabled=not raw.strip()):
            with st.spinner("Structuring your record…"):
                try:
                    result = ai.chat(
                        framework.MODULES["documentation"]["prompt"],
                        [{"role": "user", "content": raw}],
                    )
                    st.session_state["journal_structured"] = result
                    st.rerun()
                except Exception as exc:
                    st.error(str(exc))
    with col_b:
        save_what = st.radio(
            "Save which version?",
            ["My original text", "AI-structured version"],
            horizontal=True,
            disabled=structured is None,
        )

    if structured:
        st.markdown("**AI-structured version (review and edit before saving):**")
        structured = st.text_area(
            "Structured record", value=structured, height=260, label_visibility="collapsed"
        )
        st.session_state["journal_structured"] = structured

    if st.button("💾 Save entry", type="primary", disabled=not raw.strip()):
        text = (
            structured
            if (structured and save_what == "AI-structured version")
            else raw
        )
        _entries().append(
            {
                "date": entry_date.isoformat(),
                "tags": tags,
                "text": text,
                "logged": datetime.now().isoformat(timespec="seconds"),
            }
        )
        st.session_state.pop("journal_structured", None)
        st.success("Entry saved to this session. Download a backup below.")
        st.rerun()

    entries = _entries()
    if not entries:
        st.info("No entries yet. Your first record starts your timeline.")
        return

    # ---- timeline & patterns ----
    st.markdown(f"### Timeline — {len(entries)} entries")
    tag_counts: dict[str, int] = {}
    for e in entries:
        for t in e["tags"]:
            tag_counts[t] = tag_counts.get(t, 0) + 1
    if tag_counts:
        st.markdown("**Pattern frequency**")
        st.bar_chart(pd.Series(tag_counts).sort_values(ascending=False))

    for e in sorted(entries, key=lambda x: x["date"], reverse=True):
        with st.expander(f"{e['date']} — {', '.join(e['tags']) or 'untagged'}"):
            st.markdown(e["text"])
            st.caption(f"Logged {e['logged']}")

    # ---- export ----
    st.markdown("### Export")
    col1, col2 = st.columns(2)
    stamp = date.today().isoformat()
    with col1:
        st.download_button(
            "⬇️ Backup (JSON — can be restored here)",
            _export_json(),
            file_name=f"michael-protocol-journal-{stamp}.json",
            mime="application/json",
        )
    with col2:
        st.download_button(
            "⬇️ Clean report (Markdown — for you, an advocate, or counsel)",
            _export_markdown(),
            file_name=f"michael-protocol-report-{stamp}.md",
            mime="text/markdown",
        )
