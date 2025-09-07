# KanMind – Backend (Django + DRF)

Django REST backend for **KanMind**.  
Manages boards, tasks, and auth (token-based login via **email + password**).

---

## Tech Stack

- Python 3.12
- Django 5.x
- Django REST Framework
- DRF Token Authentication
- SQLite (default)

---

## Quick Start

```bash
# 1) Clone
git clone https://github.com/MuzammalAnwar/KanMind-Backend.git
cd KanMind-Backend

# 2) Virtualenv
python -m venv .venv
# Windows (PowerShell)
. .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate

# 3) Install
pip install -r requirements.txt

# 4) Environment
# Create a .env in the project root with at least:

# 5) Database
python manage.py migrate
python manage.py createsuperuser  # optional

# 6) Run
python manage.py runserver
# http://127.0.0.1:8000/

