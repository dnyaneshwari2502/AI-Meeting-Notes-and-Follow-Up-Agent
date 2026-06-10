import subprocess
import sys

python_executable = sys.executable

steps = [
    ("Generating meeting notes", "src/generate_notes.py"),
    ("Generating readable email", "src/generate_email.py"),
    ("Generating agent decision plan", "src/agent_decision.py"),
    ("Sending team summary email", "src/send_email.py"),
    ("Checking and sending due reminders", "src/send_reminders.py"),
]

for step_name, script_path in steps:
    print(f"\n{step_name}...")
    subprocess.run([python_executable, script_path], check=True)

print("\nAI Meeting Assistant Agent completed successfully.")