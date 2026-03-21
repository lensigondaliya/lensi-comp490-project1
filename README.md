# Room Booking System (Sprint 4)

## Overview
This project is a Django-based Room Booking System that allows users to:
- View meeting rooms
- Create and manage bookings
- Track booking history
- Use REST APIs for room operations
- Access an admin dashboard

---

## Features
- Django backend with REST API
- Admin panel for managing rooms and bookings
- Booking history tracking
- Automated testing with GitHub Actions
- Continuous deployment to DigitalOcean server

---

## Local Setup Instructions

### 1. Clone Repository
```bash
git clone https://github.com/lensigondaliya/lensi-comp490-project1.git
cd lensi-comp490-project1
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
pip install -r Room_booking_serve/requirements.txt
```

### 4. Run Migrations
```bash
cd Room_booking_serve
python manage.py migrate
```

### 5. Run Server
```bash
python manage.py runserver
```

Server runs at: http://127.0.0.1:8000/

### TUI Interface

This project includes a Text User Interface (TUI) that allows users to manage rooms directly from the terminal.

Features:
Add a room
Remove a room
Change room capacity
Automatically remove reservations when a room is deleted
Display affected usernames
Save cancellation report to cancellation_report.txt

### Run TUI (Sprint 4)
python main.py


### Deployed Application (Sprint 4)

Live server: http://104.236.239.10:8000/

### Important URLs

Admin Panel: http://104.236.239.10:8000/admin/

API Endpoints:

/api/v1/member/

/api/v1/meeting-rooms/

## Environment Variables

SERVER_URL=http://104.236.239.10:8000
EMAIL=user@gmail.com
USERNAME=user

### CI/CD Pipeline

GitHub Actions runs tests automatically on every push

If tests pass, deployment is triggered

The server is updated automatically via SSH

### Test Coverage

The following tests validate core functionality:

Add Room → verifies room creation
Remove Room → verifies room deletion and affected users
Change Capacity → verifies capacity updates

Tests ensure database operations behave correctly rather than just checking outputs.

### Running Tests
```bash
pytest
```

### Technologies Used

Python
Django
Django REST Framework
SQLite
GitHub Actions (CI/CD)
DigitalOcean (Deployment)

### Separation of Concerns

The project follows the requirement to separate interface from database logic:

main.py → handles user input (TUI interface)
apps/booking/utils.py → handles database operations:
add room
remove room
change capacity


# Author

Lensi Gondaliya
COMP 490 – Spring 2026
---

# Final Checklist

- TUI interface implemented  
- Add room functionality working  
- Remove room and reservation cleanup working  
- Cancellation report saved to file  
- Change room capacity working  
- Interface separated from database logic  
- README updated  
- Final changes pushed to GitHub  

## Submission

The final version of the project has been pushed to the `sprint4` branch on GitHub.