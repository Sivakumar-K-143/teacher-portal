# Teacher Portal

## Setup

1. Clone the repo
2. Install dependencies: `pip install django`
3. Run migrations: `python manage.py migrate`
4. Create superuser: `python manage.py createsuperuser`
5. Run server: `python manage.py runserver`

## Features

- Teacher login
- Student listing, add, edit, delete
- Inline editing and modal for add/edit
- Marks update if student+subject exists

## Security

- CSRF protection enabled
- Authentication required for all actions
