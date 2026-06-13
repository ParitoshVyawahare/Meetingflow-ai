import re
from utils.notion_client import create_task


def is_valid_iso_date(date_str) -> bool:
    """Returns True only if date_str matches YYYY-MM-DD format exactly."""
    if not date_str:
        return False
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}$", str(date_str).strip()))


def create_tasks_in_notion(tasks: list[dict]) -> list[dict]:
    """
    Takes a list of action item dicts and creates each one in Notion.
    Returns a list of results showing which succeeded and which failed.
    Sanitizes due_date — only passes it if it's a valid ISO date.
    """
    results = []

    for task in tasks:
        raw_date = task.get("due_date")
        safe_date = raw_date if is_valid_iso_date(raw_date) else None

        try:
            response = create_task(
                task=task.get("task", ""),
                owner=task.get("owner", ""),
                due_date=safe_date,
                priority=task.get("priority", "Medium"),
                status="Not started"
            )
            results.append({
                "success": True,
                "task": task.get("task"),
                "url": response.get("url")
            })
        except Exception as e:
            results.append({
                "success": False,
                "task": task.get("task"),
                "error": str(e)
            })

    return results