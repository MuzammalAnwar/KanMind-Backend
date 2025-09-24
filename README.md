# KanMind – Backend (Django + DRF)

Django REST backend for **KanMind**.  
Manages boards, tasks, and auth (token-based login via **email + password**).

## Deployment

The backend is deployed on a Google Cloud VM using the following stack:

Gunicorn – WSGI server for running Django

Nginx – reverse proxy handling client requests and SSL termination

Supervisor – process manager to keep Gunicorn running

Certbot (Let’s Encrypt) – automatic HTTPS certificates

The Admin panel is accessible
👉 [here](https://kanmind-api.muzammal-anwar.at/admin/)
---

## Tech Stack

- Python 3.12
- Django 5.x
- Django REST Framework
- DRF Token Authentication
- SQLite (default)

---

## Quick Start

### 1) Clone the repository
```bash
git clone https://github.com/MuzammalAnwar/KanMind-Backend.git
```
```bash
cd KanMind-Backend
```
### 2) Create and activate a virtual environment
```bash
python -m venv .venv
```

### Windows (PowerShell)
```bash
venv\Scripts\Activate
```
### macOS/Linux:
```bash
source .venv/bin/activate
```

### 3) Install dependencies
```bash
pip install -r requirements.txt
```

### 4) Apply database migrations
```bash
python manage.py migrate
python manage.py createsuperuser  # optional
```

### 5) Run the development server
```bash
python manage.py runserver
# http://127.0.0.1:8000/
```

