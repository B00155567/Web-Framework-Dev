# Training Management System

A Django-based web application for managing training modules, student enrollment, and course progress tracking.

## Features

- Module Management
- Student Enrollment
- Progress Tracking
- Resource Upload
- Forum Discussions
- Certificate Generation

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Load initial data:
```bash
python manage.py loaddata fixtures/*.json
```

6. Run the development server:
```bash
python manage.py runserver
```

## Testing

To run the BDD tests:
```bash
python manage.py behave
```

## Default Users

- Admin: admin@admin.com / password
- User: user1@user1.com / password
- Instructor: instructor@instructor.com / password
- Student: student@student.com / password 