import os
from notion_client import Client
from dotenv import load_dotenv

load_dotenv()

notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("NOTION_DATABASE_ID")


def create_task(task: str, owner: str = "", due_date: str = None, priority: str = "Medium", status: str = "Not started") -> dict:
    """
    Creates a single task row in the Notion Meeting Tasks database.
    Returns the created page object.
    """
    properties = {
        "task": {
            "title": [
                {"text": {"content": task}}
            ]
        },
        "owner": {
            "rich_text": [
                {"text": {"content": owner}}
            ]
        },
        "Priority": {
            "select": {"name": priority}
        },
        "Status": {
            "select": {"name": status}
        },
    }

    if due_date:
        properties["Due Date"] = {
            "date": {"start": due_date}
        }

    response = notion.pages.create(
        parent={"database_id": DATABASE_ID},
        properties=properties
    )

    return response