<<<<<<< HEAD
# Meeting Room Booking System

## Overview
The Meeting Room Booking System that allows users to book meeting rooms, view available meeting rooms, and manage their bookings.

## Features

### 1. Members Login
- Endpoint: `api/v1/member/login/`
- Method: POST
- Members can log in using their email and password. (send json with keys "email" and "password")
- returns a JWT token object with access and refresh if login is successful.
- Self-registration is not permitted; members are created exclusively through Django admin, and only they can access the login functionality.
- 


### 2. List Available Meeting Rooms
- Endpoint: `/api/v1/meeting-rooms/available/`
- Method: GET
- login required
- Parameters sent in json (both optional):
  - `start_time` (str in strftime format):
  - `end_time` (str strftime format):
- Lists all [available] meeting rooms based on the specified time range. (my testing indicates that it will list all rooms even if already booked as of Feb 4)

### 3. Book a Meeting Room
- Endpoint: `/api/v1/meeting-rooms/<int:room_id>/book/`
- Method: POST
- login required
- Parameters:
  - `start_time` (str): Start time of the booking. Time should be in python strftime format. (eg "2026-02-05 11:00 AM")
  - `end_time` (str): End time of the booking. (time in same format as above)
  - `no_of_persons` (int, optional): Number of persons for the booking (default is 1).
- Books a meeting room for the specified time range.
- After Booking mail will send to the one who booked

### 4. List My Bookings
- Endpoint: `api/v1/meeting-rooms/my-bookings/`
- Method: GET
- Lists all booked meeting rooms history for a requested user.

### 5. Cancel Meeting Room Booking
- Endpoint: `api/v1/meeting-rooms/<int:booking_id>/cancel-booking/`
- Method: DELETE
- login required
- Cancels a previously booked meeting room.
- Conditions:
  - The meeting room can be canceled only by the user who made the booking.
  - Cancellation is not allowed if the start time has already passed.
- After Cancellation mail will send to the one who booked


### 6. Mail send after booking and cancel booking Feature added

### 7. Unit Test cases
- To run the tests ```python manage.py test```


## Setup Instructions

### Installation
-  Clone the repository:
   ```bash
   git clone https://github.com/your-username/meeting-room-booking.git
    ```
-  Installation steps
    ```
   cd meeting-room-booking
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python manage.py migrate
   python manage.py loaddata fixtures/data.json
   python manage.py createsuperuser
   ```
- Note - 
  need to create a user in django-admin to use the booking system

=======
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
>>>>>>> 2f3bcc1c3007826557e7a3123caad90bb3064cc5
