import json


def load_notes(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def format_action_item(item):
    owner = item.get("owner", "Unassigned")
    task = item.get("task", "")
    deadline = item.get("deadline", "")

    if deadline and deadline.strip().upper() not in ["TBD", "N/A", ""]:
        return f"- {owner}: {task} ({deadline})"

    return f"- {owner}: {task}"


def generate_email(notes):
    email = f"""Subject: {notes['meeting_title']} - Meeting Notes

Hi Team,

Here is a summary of today's meeting.

SUMMARY
{notes['summary']}

ACTION ITEMS
"""

    for item in notes.get("action_items", []):
        email += f"\n{format_action_item(item)}"

    email += "\n\nBLOCKERS\n"

    blockers = notes.get("blockers", [])
    if blockers:
        for blocker in blockers:
            email += f"\n- {blocker}"
    else:
        email += "\n- None"

    email += "\n\nNEXT MEETING AGENDA\n"

    agenda_items = notes.get("next_meeting_agenda", [])
    if agenda_items:
        for agenda in agenda_items:
            email += f"\n- {agenda}"
    else:
        email += "\n- None"

    email += "\n\nThanks,\nAI Meeting Assistant"

    return email


if __name__ == "__main__":
    notes = load_notes("outputs/meeting_001_summary.json")
    email = generate_email(notes)

    with open("outputs/meeting_001_email.txt", "w", encoding="utf-8") as file:
        file.write(email)

    print(email)
    print("\nEmail saved to outputs/meeting_001_email.txt")