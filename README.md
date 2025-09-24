# KanMind – Backend (Django + DRF)

Django REST backend for **KanMind**.

## Features

- **User Roles**
  - **Regular Users** – can create and manage their own boards, lists, and tasks  
  - **Team Collaboration** – multiple users can be added to boards to collaborate on shared projects  

- **Board & Task Management**
  - Create multiple **boards** to organize projects  
  - Within boards, create **lists/columns** (e.g., "To Do", "In Progress", "Done")  
  - Add and update **tasks** with details such as title, description, due dates, and assigned users  

- **Authentication & Permissions**
  - Secure user registration & login system  
  - Users can only access and edit boards/tasks they are part of  
  - Admin panel for superusers to oversee boards, tasks, and users  

- **Collaboration Tools**
  - Assign tasks to specific users  
  - Add comments to tasks for team communication  
  - Track activity history for accountability

## Deployment

- The backend is deployed on a Google Cloud VM using the following stack:
- Gunicorn – WSGI server for running Django
- Nginx – reverse proxy handling client requests and SSL termination
- Supervisor – process manager to keep Gunicorn running
- Certbot (Let’s Encrypt) – automatic HTTPS certificates

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

