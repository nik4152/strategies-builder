from typing import Any


def run(chat_id: str, template: str, context: dict[str, Any]) -> dict[str, Any]:
    message = template.format(**context)
    # Placeholder: just return message
    return {"chat_id": chat_id, "message": message}
