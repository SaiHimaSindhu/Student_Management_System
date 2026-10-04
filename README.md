# Student Management System

Django + MySQL + HTML + CSS (no JavaScript). Features: signup/login (email or username),
dashboard, add/view/edit/delete students, search, pagination (5 per page), profile
update and password change.

## Requirements
- Python 3.10+
- MySQL 8.0+ running locally

## Setup

1. **Create a virtual environment**
   ```
   python -m venv venv
   venv\Scripts\activate          # Windows
   source venv/bin/activate       # macOS / Linux
   ```
2. **Install requirements**
   ```
   pip install -r requirements.txt
   ```
3. **Configure MySQL**
   - Create the database: `mysql -u root -p < database_setup.sql`
   - Open `student_management_system/settings.py` and set `USER` and `PASSWORD`
     in `DATABASES` (or set env vars `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`).
4. **Run migrations**
   ```
   python manage.py migrate
   ```
5. **Create a superuser** (for /admin/)
   ```
   python manage.py createsuperuser
   ```
6. **(Optional) Load demo data** - creates user `demo` / `Demo@12345` and 8 students
   ```
   python manage.py seed_demo
   ```
7. **Start the development server**
   ```
   python manage.py runserver
   ```
   Open http://127.0.0.1:8000/

## Quick trial without MySQL
Set `USE_SQLITE=1` before the commands above (`set USE_SQLITE=1` on Windows CMD,
`export USE_SQLITE=1` on macOS/Linux) to use a local SQLite file instead.

## Run the tests
```
python manage.py test
```

## Pages
| URL | Page |
|-----|------|
| /signup/, /login/ | Authentication |
| /dashboard/ | Statistics + quick actions |
| /students/ | List, search, pagination |
| /students/add/ | Add student |
| /students/<id>/edit/ | Edit student |
| /students/<id>/delete/ | Delete confirmation |
| /profile/ | Profile + change password |
| /admin/ | Django admin |

## Notes
- "New Students" = added in the last 7 days.
- Logout is a POST form (CSRF-protected), so no JavaScript is needed.
- "Forgot password?" is a placeholder link.
- Change `SECRET_KEY` and set `DEBUG=0` before any real deployment.
