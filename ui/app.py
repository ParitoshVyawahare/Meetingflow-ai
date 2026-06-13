import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import streamlit as st
from agents.extraction_agent import extract_action_items
from agents.notion_agent import create_tasks_in_notion
from agents.email_agent import draft_followup_email
from agents.audio_agent import transcribe_audio


# ---------- Page config ----------
st.set_page_config(
    page_title="MeetingFlow",
    page_icon="◆",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ---------- Custom styling ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: radial-gradient(ellipse at top, #fdfdfd 0%, #f6f7f9 60%, #eef0f4 100%);
    color: #1a1d24;
}

#MainMenu, footer, header { visibility: hidden; }

.block-container {
    padding-top: 3rem;
    padding-bottom: 3rem;
    max-width: 780px;
}

.brand-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 0.9rem;
    margin-bottom: 0.6rem;
    width: 100%;
    text-align: center;
}

.brand-mark {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: linear-gradient(135deg, #4f9cf9 0%, #2d7dd2 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 6px 18px rgba(45, 125, 210, 0.28);
}

.brand-header h1.app-title {
    margin: 0 !important;
    font-size: 2.2rem;
    font-weight: 600;
    letter-spacing: -0.025em;
    color: #0f1115;
    text-align: center;
    width: 100%;
}
.brand-tag {
    margin: 0;
    color: #8a8f99;
    font-size: 0.78rem;
    font-weight: 500;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    text-align: center;
    width: 100%;
}

p.app-subtitle {
    color: #5c6370;
    font-size: 0.95rem;
    font-weight: 400;
    margin-bottom: 2.5rem;
    letter-spacing: 0.01em;
    line-height: 1.5;
    text-align: center;
    max-width: 560px;
    margin-left: auto;
    margin-right: auto;
}

.stTextArea textarea {
    background-color: #ffffff !important;
    color: #1a1d24 !important;
    border: 1px solid #e2e5ea !important;
    border-radius: 12px !important;
    padding: 1rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    line-height: 1.6 !important;
    transition: all 0.2s ease;
    box-shadow: 0 1px 2px rgba(15, 17, 21, 0.03);
}

.stTextArea textarea:focus {
    border: 1px solid #2d7dd2 !important;
    box-shadow: 0 0 0 3px rgba(45, 125, 210, 0.12) !important;
}

.stTextArea textarea::placeholder {
    color: #9ca2ad !important;
}

.stTextInput input {
    background-color: #ffffff !important;
    color: #1a1d24 !important;
    border: 1px solid #e2e5ea !important;
    border-radius: 8px !important;
    padding: 0.55rem 0.8rem !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.9rem !important;
}

.stTextInput input:focus {
    border: 1px solid #2d7dd2 !important;
    box-shadow: 0 0 0 3px rgba(45, 125, 210, 0.12) !important;
}

.stSelectbox > div > div {
    background-color: #ffffff !important;
    border: 1px solid #e2e5ea !important;
    border-radius: 8px !important;
}

.stButton button {
    background: linear-gradient(135deg, #4f9cf9 0%, #2d7dd2 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 1.6rem !important;
    font-weight: 500 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.01em !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 14px rgba(45, 125, 210, 0.22) !important;
}

.stButton button:hover {
    transform: translateY(-1px);
    box-shadow: 0 6px 20px rgba(45, 125, 210, 0.32) !important;
}

.task-card {
    background: #ffffff;
    border: 1px solid #e8ebf0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.75rem;
    box-shadow: 0 1px 3px rgba(15, 17, 21, 0.04);
}

.section-label {
    color: #6b7280;
    font-size: 0.78rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.09em;
    margin-bottom: 0.7rem;
    margin-top: 2rem;
}

.email-box {
    background: #ffffff;
    border: 1px solid #e8ebf0;
    border-radius: 12px;
    padding: 1.5rem 1.75rem;
    font-family: 'Inter', sans-serif;
    font-size: 0.93rem;
    line-height: 1.75;
    color: #2c3038;
    white-space: pre-wrap;
    box-shadow: 0 1px 3px rgba(15, 17, 21, 0.04);
}

.success-banner {
    background: linear-gradient(135deg, #ecfdf5 0%, #f0fdf4 100%);
    border: 1px solid #a7f3d0;
    border-radius: 12px;
    padding: 1rem 1.25rem;
    color: #047857;
    font-size: 0.92rem;
    font-weight: 500;
    margin-bottom: 1rem;
}

.stCaption, .caption {
    color: #8a8f99 !important;
    font-size: 0.85rem !important;
}

a {
    color: #2d7dd2 !important;
    text-decoration: none !important;
    font-weight: 500 !important;
}
a:hover {
    text-decoration: underline !important;
}
</style>
""", unsafe_allow_html=True)


# ---------- Session state ----------
if "tasks" not in st.session_state:
    st.session_state.tasks = []
if "email" not in st.session_state:
    st.session_state.email = ""
if "transcript" not in st.session_state:
    st.session_state.transcript = ""
if "submitted_to_notion" not in st.session_state:
    st.session_state.submitted_to_notion = False
if "notion_results" not in st.session_state:
    st.session_state.notion_results = []


# ---------- Header ----------
st.markdown("""
<div class="brand-header">
    <div class="brand-mark">
        <svg width="22" height="22" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M4 6L12 14L20 6" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>
            <path d="M4 14L12 22L20 14" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" opacity="0.5"/>
        </svg>
    </div>
    <h1 class="app-title">MeetingFlow</h1>
    <p class="brand-tag">AI agent for action items</p>
</div>
""", unsafe_allow_html=True)


# ---------- Input: audio or text ----------
st.markdown('<div class="section-label">Meeting Input</div>', unsafe_allow_html=True)

input_tab1, input_tab2 = st.tabs(["Paste Transcript", "Upload Audio"])

with input_tab1:
    transcript = st.text_area(
        label="transcript",
        value=st.session_state.transcript,
        placeholder="Paste the full meeting transcript here. Could be a Zoom export, Google Meet captions, or your own notes — any format works.",
        height=240,
        label_visibility="collapsed"
    )

with input_tab2:
    audio_file = st.file_uploader(
        "Upload a meeting recording",
        type=["mp3", "m4a", "wav", "webm", "ogg", "mp4"],
        label_visibility="collapsed",
        help="Max 25MB. Supports most common audio formats."
    )
    st.caption("The audio will be transcribed using Whisper, then analyzed.")

col1, col2, col3 = st.columns([1, 1, 1])
with col2:
    extract_btn = st.button("Extract Action Items", use_container_width=True)


# ---------- Extraction (handles both text and audio inputs) ----------
if extract_btn:
    final_transcript = ""

    # Path 1: audio uploaded
    if audio_file is not None:
        with st.spinner("Transcribing audio with Whisper..."):
            try:
                final_transcript = transcribe_audio(audio_file)
            except Exception as e:
                st.error(f"Audio transcription failed: {str(e)}")
                final_transcript = ""

    # Path 2: text pasted
    elif transcript.strip():
        final_transcript = transcript

    # Run extraction if we got a transcript from either path
    if final_transcript:
        with st.spinner("Analyzing transcript..."):
            st.session_state.transcript = final_transcript
            st.session_state.tasks = extract_action_items(final_transcript)
            st.session_state.email = draft_followup_email(st.session_state.tasks, final_transcript)
            st.session_state.submitted_to_notion = False
            st.session_state.notion_results = []
    elif audio_file is None:
        st.warning("Please either paste a transcript or upload an audio file.")


# ---------- Review & edit ----------
if st.session_state.tasks:
    st.markdown('<div class="section-label">Review Action Items</div>', unsafe_allow_html=True)
    st.caption("Edit any field before sending to Notion. Remove tasks you don't want.")

    updated_tasks = []
    for i, task in enumerate(st.session_state.tasks):
        with st.container():
            st.markdown('<div class="task-card">', unsafe_allow_html=True)
            c1, c2 = st.columns([5, 1])
            with c1:
                new_task = st.text_input(f"Task", value=task.get("task", ""), key=f"task_{i}")
            with c2:
                remove = st.button("Remove", key=f"remove_{i}")

            c3, c4, c5 = st.columns(3)
            with c3:
                new_owner = st.text_input("Owner", value=task.get("owner", ""), key=f"owner_{i}")
            with c4:
                new_date = st.text_input("Due Date (YYYY-MM-DD)", value=task.get("due_date") or "", key=f"date_{i}")
            with c5:
                new_priority = st.selectbox(
                    "Priority",
                    ["High", "Medium", "Low"],
                    index=["High", "Medium", "Low"].index(task.get("priority", "Medium")),
                    key=f"priority_{i}"
                )
            st.markdown('</div>', unsafe_allow_html=True)

            if not remove:
                updated_tasks.append({
                    "task": new_task,
                    "owner": new_owner,
                    "due_date": new_date if new_date.strip() else None,
                    "priority": new_priority
                })

    st.session_state.tasks = updated_tasks


# ---------- Email preview ----------
if st.session_state.email:
    st.markdown('<div class="section-label">Follow-up Email Draft</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="email-box">{st.session_state.email}</div>', unsafe_allow_html=True)


# ---------- Final approve & send ----------
if st.session_state.tasks and not st.session_state.submitted_to_notion:
    st.write("")
    col1, col2, col3 = st.columns([1, 1.2, 1])
    with col2:
        approve_btn = st.button("Approve & Send to Notion", use_container_width=True)

    if approve_btn:
        with st.spinner("Creating tasks in Notion..."):
            results = create_tasks_in_notion(st.session_state.tasks)
            st.session_state.notion_results = results
            st.session_state.submitted_to_notion = True
            st.rerun()


# ---------- Success state ----------
if st.session_state.submitted_to_notion and st.session_state.notion_results:
    success_count = sum(1 for r in st.session_state.notion_results if r["success"])
    total = len(st.session_state.notion_results)
    st.markdown(f'<div class="success-banner">{success_count} of {total} tasks successfully created in Notion.</div>', unsafe_allow_html=True)

    for r in st.session_state.notion_results:
        if r["success"]:
            st.markdown(f"[{r['task']}]({r['url']})")
        else:
            st.error(f"Failed: {r['task']} — {r['error']}")