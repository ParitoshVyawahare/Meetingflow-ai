import os
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are a smart meeting assistant.
Your job is to write a clear follow-up message after a meeting.

FIRST, infer the type of meeting from the transcript:
- Professional / corporate (work team, client call, business meeting)
- Academic / student (group project, study session, class team)
- Casual / personal (friends planning something, informal collaboration)

THEN match the tone of the email to the meeting type:
- Professional meeting -> formal email, polished, business tone
- Academic meeting -> friendly but organized, like one student writing to teammates
- Casual meeting -> warm, conversational, light tone, can use first names freely

The email must always:
- Start with a short greeting that matches the tone
- Have a brief one-line summary of what the meeting covered
- List each action item clearly, showing who owns it and when it's due
- End with a closing line that matches the tone
- Be ready to send as-is, no placeholders like [Your Name]

Sign off as "Paritosh"."""),
    ("human", """Here are the action items extracted from the meeting:

{tasks}

Original transcript (use this to infer the tone):
{transcript}

Write the follow-up message.""")
])


def draft_followup_email(tasks: list[dict], transcript: str = "") -> str:
    """
    Takes the list of action items and the original transcript,
    infers meeting type, and returns a tone-matched follow-up message.
    """
    if not tasks:
        return "No action items found. No email needed."

    tasks_text = "\n".join([
        f"- Task: {t.get('task')} | Owner: {t.get('owner') or 'Unassigned'} | Due: {t.get('due_date') or 'No date set'} | Priority: {t.get('priority', 'Medium')}"
        for t in tasks
    ])

    chain = prompt | llm
    response = chain.invoke({
        "tasks": tasks_text,
        "transcript": transcript
    })
    return response.content.strip()