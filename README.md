# Student Management System

A full-stack **Student Management System** built with **Django**, **Bootstrap 5**, and **SQLite**. It provides a modern, glassmorphism-styled dashboard for managing student records with complete Create, Read, Update, and Delete (CRUD) functionality, including profile photo uploads.

## Project Overview

This project lets an institute (or anyone practicing Django) manage a list of students through a clean web interface:

- A dashboard home page with live stats (total students, courses offered).
- A form to add new students, including a profile photo upload.
- A searchable table listing every student.
- Edit and delete workflows, with a confirmation step before deleting.
- A registered Django admin panel for managing students without the front-end.

The UI uses a dark-blue gradient background with frosted-glass ("glassmorphism") cards, built entirely with Bootstrap 5 and a small custom stylesheet — fully responsive from mobile to desktop.

## Features

- **Dashboard home page** — quick stats + recently added students.
- **Add Student** — validated form (name, roll number, email, phone, course, gender, address, joining date, profile photo).
- **Student List** — table of all students with a live search box (search by name or roll number).
- **Edit Student** — update any field, including replacing the profile photo.
- **Delete Student** — dedicated confirmation page before permanent deletion.
- **Validation**
  - Email format validation (Django's `EmailField`).
  - Required-field validation on every form field except the optional photo.
  - Unique roll number validation, enforced both at the database level (`unique=True`) and with a friendly form-level error message.
  - Phone number and roll number format validation via regex.
- **Image upload** — profile photos are stored via `ImageField`, served from `MEDIA_ROOT`/`MEDIA_URL` during development.
- **Django Admin** — the `Student` model is registered with list display, search, and filters.

## Technologies Used

| Layer      | Technology                                   |
|------------|-----------------------------------------------|
| Backend    | Python 3, Django                              |
| Database   | SQLite (Django's default `db.sqlite3`)        |
| Frontend   | HTML5, CSS3, Bootstrap 5, Bootstrap Icons     |
| Image handling | Pillow (required by Django's `ImageField`) |

## Project Structure

```
student_management_system/
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3                       # created after running migrate
├── media/                           # uploaded profile photos (created at runtime)
├── student_management/              # Django project package
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── students/                        # Django app
    ├── __init__.py
    ├── admin.py                     # Student registered in the admin site
    ├── apps.py
    ├── models.py                    # Student model
    ├── forms.py                     # StudentForm + StudentSearchForm
    ├── views.py                     # home, about, add/edit/delete/list views
    ├── urls.py                      # app-level URL routes
    ├── migrations/
    ├── static/
    │   └── students/
    │       └── style.css            # glassmorphism / dark-blue theme
    └── templates/
        └── students/
            ├── base.html            # navbar, footer, message alerts
            ├── home.html             # dashboard
            ├── add_student.html
            ├── student_list.html
            ├── edit_student.html
            ├── delete_confirm.html
            └── about.html
```

## Installation Steps

1. **Clone / unzip the project**, then move into the folder:
   ```bash
   cd student_management_system
   ```

2. **Create and activate a virtual environment** (recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate      # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## Migration Commands

Create the database tables (SQLite file `db.sqlite3` is created automatically):

```bash
python manage.py makemigrations
python manage.py migrate
```

**(Optional)** create an admin superuser so you can log into `/admin/`:

```bash
python manage.py createsuperuser
```

## Run Server Commands

Start the development server:

```bash
python manage.py runserver
```

Then open your browser at:

- **App:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

## Notes

- `DEBUG = True` and media files are served by Django's dev server for local development only. For production, set `DEBUG = False`, configure `ALLOWED_HOSTS`, and serve `media/` and `static/` through a proper web server or storage service.
- The SECRET_KEY in `settings.py` is a development placeholder — replace it with a securely generated value before deploying.
