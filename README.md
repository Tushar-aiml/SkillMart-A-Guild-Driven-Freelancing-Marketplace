# Skill Mart

Skill Mart is a service marketplace where clients can hire skilled workers for both physical and virtual work.

## Tech Stack

- Backend: Django (Python) with SQLite
- Frontend: HTML, CSS, Vanilla JavaScript
- Authentication: Django's built-in authentication system
- APIs: Django views returning JSON (REST-style) and HTML templates

## Features

- User registration and login for two roles:
  - Client (hires workers)
  - Service Provider / Worker (offers services)
- Separate dashboards for clients and workers
- Quest (job) posting and acceptance workflow
- Ranking and EXP system for workers
- Premium membership with quest limits and bonuses
- Simple payment confirmation flow (no real payment gateway)
- Ratings and reviews for completed quests

## Getting Started

1. Create and activate a virtual environment (recommended).
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run database migrations:

```bash
python manage.py migrate
```

4. Create a superuser to access the admin:

```bash
python manage.py createsuperuser
```

5. Start the development server:

```bash
python manage.py runserver
```

6. Open the site in your browser at `http://127.0.0.1:8000/`.

