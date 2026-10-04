# PythonAnywhere deployment instructions

1. Clone this repo to your PythonAnywhere account.
2. Create a virtualenv: `mkvirtualenv --python=/usr/bin/python3.11 mysite`
3. Install requirements: `pip install -r requirements.txt`
4. Run migrations: `python manage.py migrate`
5. Create a superuser: `python manage.py createsuperuser`
6. Set environment variables: `DEBUG=False`, `SECRET_KEY=...`, `ALLOWED_HOSTS=yourusername.pythonanywhere.com`
7. Configure Web app to use the WSGI file.
8. Reload app.

The project is configured to use SQLite for free-tier deployment and WhiteNoise for static files.
