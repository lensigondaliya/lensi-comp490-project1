# COMP490 Project – Sprint 3
## Voice-Enabled AI Meeting Room Agent

---

## Overview

This project implements a voice-enabled AI agent that interacts with a Meeting Room Booking REST API.

The system combines:

- **Sprint 1:** Voice recording and speech-to-text  
- **Sprint 2:** REST API client skills  
- **Sprint 3:** LangChain AI agent integration  

The agent can answer questions such as:

- “When is my next reservation?”
- “Do I have a booking tomorrow?”
- “What rooms are free at 11am?”
- “Do I have a reservation in Room 1 today?”

For Sprint 3, the agent only answers questions about reservations.  
It does not create or delete reservations interactively (creation/deletion is used only in automated tests).

## Features

- Login to booking server and retrieve JWT token  
- List current reservations  
- Get available rooms for a time window  
- Voice recording and speech-to-text transcription  
- LangChain agent with tools  
- End-to-end integration test  
- GitHub Actions CI support  

## Project Structure

skills.py → API client functions ("AI skills")
agent.py → LangChain agent entry point
src/stt.py → Voice recording and transcription
tests/test_integration.py → End-to-end integration test
requirements.txt → Python dependencies

## Setup Instructions

### 1. Clone Repository

git clone https://github.com/lensigondaliya/lensi-comp490-project1.git
cd lensi-comp490-project1

### 2. Create Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Environment Configuration (.env File)

Create a file named `.env` in the project root directory:

```env
OPENAI_API_KEY=openai_api_key_here
SERVER_URL=http://server-url
EMAIL=email
PASSWORD=password
```

### Variable Explanation

- **SERVER_URL** – Base URL of the booking server
- **EMAIL** – Login email
- **PASSWORD** – Login password
- **OPENAI_API_KEY** – Required for the LangChain AI agent

⚠️ Do NOT commit the `.env` file to GitHub.

## Running the AI Agent

Start the agent:

```bash
python agent.py
```

You can:

- Type a question
- Type `voice` to record audio input
- Type `quit` to exit

---

## Running Tests

Run all tests:

```bash
pytest
```

Run only the integration test:

```bash
pytest -m integration
```

---

## Integration Test Behavior

The Sprint 3 integration test performs:

1. Login  
2. Find available rooms  
3. Create reservation  
4. Verify reservation exists  
5. Cancel reservation  

This ensures complete end-to-end functionality and proper cleanup.


## Notes for Grading

- Python skills include type hints and docstrings
- Agent uses LangChain tools
- Integration test creates and deletes reservations
- Secrets stored in `.env` and excluded from version control
- CI runs automated tests

## Summary

Sprint 3 integrates:

- Voice input  
- REST API skills  
- AI agent tool usage  
- Automated end-to-end testing  
