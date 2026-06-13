import os
import json
import re
from datetime import date
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

prompt = ChatPromptTemplate.from_messages([
    ("system", """You are an expert meeting analyst.
Your job is to read a meeting transcript and extract clear, actionable tasks.

Return ONLY a valid JSON array, nothing else. No explanation, no markdown, no code fences.

Each task should have this exact format:
[
    {{
        "task": "short clear description of what needs to be done",
        "owner": "name of the person responsible, or empty string if unclear",
        "due_date": "YYYY-MM-DD if mentioned, otherwise null",
        "priority": "High, Medium, or Low based on urgency cues in the transcript"
    }}
]

Rules:
- Extract only real action items, not general discussion
- Be concise but specific in the task description
- If no clear owner is mentioned, use empty string
- For due_date: ONLY return a strict YYYY-MM-DD date (ISO 8601 format).
- If the transcript says something vague like "Friday", "next week", "soon", you MUST resolve it to an exact YYYY-MM-DD date using today's date as reference, OR return null.
- Never return free text like "Friday" or "next week" in the due_date field.
- Today's date is {today}.
- Default priority is Medium unless urgency is clearly stated"""),
    ("human", "Meeting transcript:\n\n{transcript}\n\nExtract all action items.")
])


def extract_action_items(transcript: str) -> list[dict]:
    """
    Reads a meeting transcript and returns a list of structured action items.
    Each item is a dict with: task, owner, due_date, priority.
    """
    today_str = date.today().isoformat()
    chain = prompt | llm
    response = chain.invoke({"transcript": transcript, "today": today_str})

    raw = response.content.strip()
    raw = re.sub(r'^```json|^```|```$', '', raw, flags=re.MULTILINE).strip()

    try:
        tasks = json.loads(raw)
        return tasks
    except json.JSONDecodeError:
        print("LLM did not return valid JSON. Raw output:")
        print(raw)
        return []