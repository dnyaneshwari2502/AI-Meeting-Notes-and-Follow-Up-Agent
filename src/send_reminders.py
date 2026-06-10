import json
import base64
from datetime import datetime
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service():
    creds = Credentials.from_authorized_user_file("token.json", SCOPES)

    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return build("gmail", "v1", credentials=creds)


def load_json(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def save_json(data, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def find_email_by_name(team_members, owner_name):
    for member in team_members:
        if member["name"].lower() == owner_name.lower():
            return member["email"]
    return None


def create_message(recipient, subject, body):
    message = MIMEText(body)
    message["to"] = recipient
    message["from"] = "me"
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    return {"raw": raw_message}


def send_email(service, message):
    return service.users().messages().send(
        userId="me",
        body=message
    ).execute()


def send_due_reminders():
    today = datetime.today().strftime("%B %d, %Y")

    decision = load_json("outputs/meeting_001_agent_decision.json")
    team_members = load_json("data/team_members.json")

    service = get_gmail_service()

    reminders_sent = 0

    for followup in decision.get("owner_followups", []):
        if followup.get("reminder_sent") is True:
            continue

        if followup.get("reminder_needed") is not True:
            continue

        if followup.get("reminder_timing") != today:
            continue

        recipient = find_email_by_name(team_members, followup["owner"])

        if not recipient:
            print(f"No email found for {followup['owner']}")
            continue

        subject = f"Reminder: {followup['task']}"

        body = f"""Hi {followup['owner']},

This is a reminder for your action item from the meeting.

Task: {followup['task']}
Deadline: {followup['deadline']}
Priority: {followup['priority']}

{followup['follow_up_message']}

Thanks,
AI Meeting Assistant
"""

        message = create_message(recipient, subject, body)
        send_email(service, message)

        followup["reminder_sent"] = True
        reminders_sent += 1

    save_json(decision, "outputs/meeting_001_agent_decision.json")

    print(f"Reminders sent: {reminders_sent}")


if __name__ == "__main__":
    send_due_reminders()