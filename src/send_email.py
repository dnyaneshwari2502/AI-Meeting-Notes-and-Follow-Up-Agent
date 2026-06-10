import os
import json
import base64
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


def load_team_members(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def load_email_body(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def create_message(sender, recipients, subject, body):
    message = MIMEText(body)
    message["to"] = ", ".join(recipients)
    message["from"] = sender
    message["subject"] = subject

    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    return {"raw": raw_message}


def send_email(service, message):
    sent_message = service.users().messages().send(
        userId="me",
        body=message
    ).execute()

    return sent_message


if __name__ == "__main__":
    service = get_gmail_service()

    team_members = load_team_members("data/team_members.json")
    recipients = [member["email"] for member in team_members]

    email_body = load_email_body("outputs/meeting_001_email.txt")

    subject = "Weekly Product Analytics Meeting - Meeting Notes"

    message = create_message(
        sender="me",
        recipients=recipients,
        subject=subject,
        body=email_body
    )

    result = send_email(service, message)

    print("Email sent successfully.")