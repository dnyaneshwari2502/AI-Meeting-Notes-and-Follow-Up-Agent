# AI Meeting Notes and Follow-Up Agent

## Overview
In many teams, not everyone can attend every meeting. Important decisions, action items, and follow-ups often get buried in long transcripts or meeting recordings, making it difficult for team members to stay aligned.

I built this AI Meeting Notes and Follow-Up Agent to automate the process of converting meeting transcripts into structured meeting notes, identifying action items, and sending follow-up emails automatically.

The goal was not just to summarize meetings, but to create a system that can understand what happened during a meeting, determine what actions need to be taken, and perform those actions automatically.

---

## What the Agent Does
The agent takes a meeting transcript as input and performs the following tasks:

1. Generates a structured meeting summary
2. Extracts decisions and action items
3. Identifies task owners and deadlines
4. Creates follow-up plans for each task owner
5. Sends a summary email to the team
6. Schedules reminder emails for upcoming deadlines
7. Runs automatically using GitHub Actions

---

## My Approach

While building this project, I intentionally separated the workflow into multiple stages instead of asking the LLM to do everything at once.

### Stage 1: Meeting Understanding

The transcript is sent to Gemini, which extracts:

* Meeting summary
* Action items
* Blockers
* Next meeting agenda

The output is stored in a structured JSON format.

I chose JSON because it acts as a source of truth that can later be used for emails, dashboards, chatbots, reminders, or reporting systems without repeatedly calling the LLM.

### Stage 2: Agent Decision Layer

After generating meeting notes, a second reasoning step is performed.

Instead of simply summarizing the meeting, the agent determines:

* Who owns each task
* Task priority
* Whether reminders are needed
* When reminders should be sent
* Whether escalation may be required

This creates a decision plan that the system can execute automatically.

### Stage 3: Action Execution

Once decisions are made, the system performs actions such as:

* Sending meeting summaries
* Creating personalized follow-ups
* Checking for reminders
* Sending reminder emails automatically

This separation between understanding, reasoning, and execution makes the system easier to maintain and extend.

---

## Workflow

```text
Meeting Transcript
        ↓
Gemini Meeting Analysis
        ↓
Structured Meeting Notes (JSON)
        ↓
Agent Decision Engine
        ↓
Action Plan (JSON)
        ↓
Email Generation
        ↓
Gmail API
        ↓
Team Summary Emails
        ↓
Reminder Emails
```

---

## Technologies Used

* Python
* Gemini API
* Gmail API
* GitHub Actions
* JSON
* OAuth 2.0 Authentication

---

## Project Structure

```text
AI Meeting Assistant Agent
│
├── data/
│   ├── team_members.json
│   └── meeting_001.txt
│
├── outputs/
│   ├── meeting_001_summary.json
│   ├── meeting_001_email.txt
│   └── meeting_001_agent_decision.json
│
├── src/
│   ├── generate_notes.py
│   ├── generate_email.py
│   ├── agent_decision.py
│   ├── send_email.py
│   ├── send_reminders.py
│   └── run_agent.py
│
└── .github/workflows/
    └── meeting_agent.yml
```

---

## Automated Scheduling

GitHub Actions is used to run the workflow automatically.

Current automation:

* Manual workflow execution
* Daily reminder checks
* Automatic reminder email delivery

This allows the agent to continue operating even when the local machine is turned off.

---

## Real-World Implementation

This project uses sample transcripts and a simulated team environment.

In a production setting, the workflow would typically look like:

```text
Microsoft Teams / Zoom Meeting
            ↓
Meeting Ends
            ↓
Transcript Stored in SharePoint or OneDrive
            ↓
Webhook / Power Automate Trigger
            ↓
AI Agent
            ↓
Meeting Summary
            ↓
Action Items
            ↓
Follow-Ups and Reminders
```

Additional production features could include:

* Team-specific access control
* User authentication
* Slack and Teams integration
* Escalation workflows
* Manager notifications
* Audit logging
* Analytics dashboards

---

## Future Enhancements

The next major enhancement is a team knowledge assistant.

Instead of only sending emails, all meeting notes and action items could be stored in a searchable knowledge base.

Team members would be able to ask questions such as:

* What decisions were made last month?
* What tasks are assigned to me?
* What blockers have been discussed recently?
* Summarize all meetings related to a project.

This would transform the system from a meeting automation tool into a complete AI-powered team assistant.

---

## Key Takeaways

One of the biggest lessons from this project was understanding the difference between automation and agents.

A workflow simply follows predefined steps.

An agent analyzes information, makes decisions, and determines which actions should be executed.

By separating meeting understanding, decision-making, and action execution, I was able to move beyond a simple meeting summarization workflow and build the foundation of a practical AI agent that can support real team operations.
