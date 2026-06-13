# MeetingFlow

> AI agent that turns meeting transcripts into action items in Notion and a follow-up email — drafted by AI, approved by you.

**Live demo:** <img width="755" height="752" alt="image" src="https://github.com/user-attachments/assets/ebbfa652-2bab-46dc-b657-2d4aa407c940" />

**Website Link:** https://meetingflow.streamlit.app/
**Author:** [Paritosh Vyawahare](https://www.linkedin.com/in/paritoshvyawahare)

---

## Why this project

Every meeting ends the same way. Decisions get made, people commit to things, deadlines get thrown around — and within a day, half of it is forgotten. Someone has to listen back, write the action items down, assign owners, set deadlines, and send a follow-up email. It almost never happens consistently.

MeetingFlow exists to close that gap. Paste a transcript or upload a recording, and the agent extracts what actually needs to happen, drafts a follow-up message that matches the tone of the meeting, and — after you approve — creates the tasks directly in your Notion workspace as real, trackable work.

This is not a summarizer. It's an **action-taking agent** — the kind of system that current AI engineering roles are built around. It demonstrates the full agentic loop: reasoning over unstructured input, integrating with external tools, handling multimodal data, and keeping a human in the decision loop where it matters.

---

## What it does

- Accepts either a pasted transcript or an uploaded audio recording (mp3, m4a, wav, mp4, ogg, webm)
- Transcribes audio using Groq's hosted Whisper Large v3 Turbo
- Extracts structured action items — task, owner, due date, priority — using an LLM with strict JSON output
- Resolves vague dates like "Friday" or "next week" into ISO 8601 dates using current-day context
- Infers the meeting type (professional, academic, casual) and writes a tone-matched follow-up email
- Lets the user review and edit every task before any external action is taken
- Creates the approved tasks in a connected Notion database via the official API
- Handles per-task failures gracefully so one bad row never breaks the pipeline

---

## Architecture

┌──────────────────┐
    │   User Input     │
    │  (text or audio) │
    └────────┬─────────┘
             │
             ▼
   ┌──────────────────┐
   │  Audio Agent     │  ← Groq Whisper (if audio)
   │  (transcribe)    │
   └────────┬─────────┘
             │
             ▼
   ┌──────────────────┐
   │ Extraction Agent │  ← Groq LLM (Llama 3.3 70B)
   │  (structure)     │     + date resolution
   └────────┬─────────┘
             │
    ┌────────┴─────────┐
    ▼                  ▼
    ┌──────────────┐   ┌──────────────┐
│ Email Agent  │   │ Human Review │  ← Streamlit UI
│ (tone-match) │   │   & Edit     │     (editable cards)
└──────┬───────┘   └──────┬───────┘
│                  │
▼                  ▼
Email Draft       ┌──────────────┐
│ Notion Agent │  ← Notion API
│ (create)     │     + date validation
└──────────────┘
│
▼


Tasks in Notion

The system is built as a set of focused, single-responsibility agents that coordinate through structured data. Each agent does one thing and does it cleanly — failure in one cannot corrupt the others. The intelligence lives inside the agents; the boundary between the agents and external APIs is treated as untrusted and validated before any irreversible action.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language Model | Llama 3.3 70B Versatile (via Groq) |
| Speech-to-Text | Whisper Large v3 Turbo (via Groq) |
| LLM Orchestration | LangChain |
| External Tool | Notion API |
| UI Framework | Streamlit (custom CSS theming) |
| Deployment | Streamlit Cloud |
| Language | Python |

---

## Design Decisions

**Human-in-the-loop by default.** LLMs are powerful but probabilistic. Creating tasks in someone's real workspace without their approval is the fastest way to lose trust. The review step is what makes this a product, not a demo.

**Validation at the boundary.** LLM output cannot be trusted blindly when it's about to cross into an external system. Dates, in particular, are validated against ISO 8601 format before being sent to Notion — if the model hallucinates a date string like "Friday", the validation layer strips it rather than letting it fail downstream.

**Separate agents over one big prompt.** It's tempting to ask one LLM to "do everything." But splitting extraction, email drafting, and Notion creation into independent agents means I can debug, swap, and improve each one without touching the others. The same extraction output feeds both the email and the Notion paths.

**Tone-adaptive output.** A team meeting and a study group don't deserve the same email. The email agent reads the original transcript (not just the action items) and infers register — formal, casual, or somewhere in between — so the output actually feels appropriate to the context.

---

## What I Learned

- How to design **agentic systems** as coordinated, single-purpose components rather than one giant prompt
- How to build **multimodal pipelines** that mix speech-to-text with downstream LLM reasoning, and the surprising details that come with audio file handling
- How to do **defensive programming around LLMs** — trusting model output internally, but verifying it before it crosses into external APIs
- How **real tool integration** works in production — workspace tokens, per-resource permissions, the difference between authentication and authorization
- How to design **UX for AI uncertainty** — the review step exists because the model will occasionally be wrong, and the user must always be able to correct it before something irreversible happens

---

## Roadmap

- Persistent meeting history
- Visual confidence scores per extracted task
- Slack and Google Calendar integrations
- Optional direct email sending via Gmail OAuth (currently drafts only)

---
