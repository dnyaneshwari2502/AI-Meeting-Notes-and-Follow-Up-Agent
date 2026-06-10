import os
import json
from dotenv import load_dotenv
from google import genai


load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY is missing. Check GitHub Secret or local .env file."
    )

client = genai.Client(api_key=api_key)


def load_meeting_notes(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


def generate_agent_decision(notes):
    prompt = f"""
You are an AI meeting follow-up agent.

Based on the meeting notes below, decide what follow-up actions are needed.

Return ONLY valid JSON with this structure:

{{
  "team_email_required": true,
  "owner_followups": [
    {{
      "owner": "",
      "task": "",
      "deadline": "",
      "priority": "Low / Medium / High",
      "follow_up_message": "",
      "reminder_needed": true,
      "reminder_timing": "",
      "escalation_needed": false,
      "escalation_reason": ""
    }}
  ]
}}

Rules:
- Create one owner follow-up for each action item.
- If the task affects a blocker or project delivery, mark priority as High.
- If the deadline is within 3 days, reminder_needed should be true.
- If the task has no owner, escalation_needed should be true.
- If there are no action items, team_email_required should still be true but owner_followups should be empty.
- Do not invent unrelated tasks.
- Return ONLY JSON.

Meeting notes:
{json.dumps(notes, indent=2)}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text


def save_decision(content, output_path):
    cleaned_content = content.replace("```json", "").replace("```", "").strip()
    data = json.loads(cleaned_content)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return data


if __name__ == "__main__":
    notes = load_meeting_notes("outputs/meeting_001_summary.json")
    decision = generate_agent_decision(notes)
    saved_decision = save_decision(decision, "outputs/meeting_001_agent_decision.json")

    print("Agent decision generated successfully.")
    print(json.dumps(saved_decision, indent=2))