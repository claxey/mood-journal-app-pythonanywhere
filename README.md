# Mood Journal App

A Django-based mood journal app optimized for PythonAnywhere free tier.

## Overview

This project uses Django with SQLite for a free-tier-friendly deployment setup. It includes journal tracking, daily tasks, goals, mood analytics, and a lightweight sentiment analysis flow.

## Deploying on PythonAnywhere free tier

1. Create a PythonAnywhere account.
2. Clone this repo in Bash.
3. Create a virtual environment and install dependencies:
   ```bash
   mkvirtualenv --python=/usr/bin/python3.11 mysite
   pip install -r requirements.txt
   ```
4. Run migrations:
   ```bash
   python manage.py migrate
   ```
5. Create a superuser:
   ```bash
   python manage.py createsuperuser
   ```
6. Configure the web app with the WSGI file pointing to `journal_project.wsgi.application`.
7. Set environment variables:
   - `SECRET_KEY`
   - `DEBUG=False`
   - `ALLOWED_HOSTS=yourusername.pythonanywhere.com`
8. Reload the app.

See `PYTHONANYWHERE_DEPLOYMENT.md` for the full guide.
