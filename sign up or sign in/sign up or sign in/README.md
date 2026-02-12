# Wisdom Connect

A platform where experienced individuals share their work-life stories and build meaningful professional connections.

## Project Overview
Wisdom Connect is a web-based platform built using Django (Python), HTML/CSS, and JavaScript, where experienced professionals—especially seniors or retirees—can share their life's work experiences, inspire others, and form meaningful connections. The platform aims to serve as a bridge between generations by enabling knowledge transfer, social engagement, and community building.

## Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd wisdom-connect
    ```

2.  **Create and activate a virtual environment:**
    ```bash
    python -m venv venv
    # On Windows
    .\venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**
    ```bash
    python manage.py runserver
    ```

Visit `http://127.0.0.1:8000/` in your browser.

## Tech Stack

*   Backend: Django
*   Frontend: HTML, CSS, JavaScript (with Bootstrap)
*   Database: SQLite (Development)

## Key Features (Implemented / Planned)

*   [x] Basic project structure
*   [x] User model (Django built-in)
*   [x] Profile, Experience, Connection models
*   [x] Basic views and templates (Home, Login, Placeholders)
*   [x] Basic routing
*   [ ] User registration
*   [ ] Profile creation/editing
*   [ ] Experience creation/editing form handling
*   [ ] Experience detail view implementation
*   [ ] Connection request sending/accepting logic
*   [ ] Connection page implementation
*   [ ] Styling refinements
*   [ ] Admin interface customization

## Folder Structure

```
wisdom_connect/
├── manage.py
├── wisdom_connect/         # Project directory
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── wisdom_app/             # App directory
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── tests.py
│   ├── views.py
│   ├── urls.py
│   └── migrations/
│   └── templates/
│       └── wisdom_app/
│           ├── base.html
│           ├── home.html
│           ├── profile.html
│           ├── create_experience.html
│           ├── experience_detail.html
│           ├── connections.html
│           └── login.html
├── static/
│   └── css/
│       └── styles.css
├── templates/              # Optional project-level templates
├── requirements.txt
└── db.sqlite3              # Database file (created after migrate)
``` 