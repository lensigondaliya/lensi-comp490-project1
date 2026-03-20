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

### Deployed Application (Sprint 4)

Live server: http://104.236.239.10:8000/

## Important URLs

Admin Panel: http://104.236.239.10:8000/admin/

API Endpoints:

/api/v1/member/

/api/v1/meeting-rooms/

## Environment Variables

SERVER_URL=http://104.236.239.10:8000
EMAIL=user@gmail.com
USERNAME=user
PASSWORD=lensi1110

### CI/CD Pipeline

GitHub Actions runs tests automatically on every push

If tests pass, deployment is triggered

The server is updated automatically via SSH

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


### 👤 Author

Lensi Gondaliya
COMP 490 – Spring 2026
---

# 🎯 Final checklist 

✅ Remove backup folder  
✅ Update README  
✅ Push final changes  

```bash
git add .
git commit -m "Final submission update"
git push origin sprint4