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


def read_transcript(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()


def generate_meeting_notes(transcript):
    import time

    prompt = f"""
You are an AI meeting assistant.

Read the meeting transcript and return ONLY valid JSON with this structure:

{{
  "meeting_title": "",
  "date": "",
  "summary": "",
  "decisions": [],
  "action_items": [
    {{
      "task": "",
      "owner": "",
      "deadline": ""
    }}
  ],
  "blockers": [],
  "next_meeting_agenda": []
}}

Rules:
- Use only the information from the transcript.
- Do not invent unrelated action items.
- If there is no deadline, use "TBD".
- Return ONLY valid JSON.

Meeting transcript:
{transcript}
"""

    models = ["gemini-2.5-flash", "gemini-2.0-flash"]

    for model_name in models:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                print(f"{model_name} failed, attempt {attempt + 1}: {e}")
                time.sleep(5)

    raise RuntimeError("All Gemini model attempts failed.")


def save_output(content, output_path):
    cleaned_content = content.replace("```json", "").replace("```", "").strip()
    data = json.loads(cleaned_content)

    with open(output_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return data


if __name__ == "__main__":
    transcript = read_transcript("data/meeting_001.txt")
    notes = generate_meeting_notes(transcript)
    saved_data = save_output(notes, "outputs/meeting_001_summary.json")

    print("Meeting notes generated successfully.")
    print(json.dumps(saved_data, indent=2))