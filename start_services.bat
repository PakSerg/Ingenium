@echo off


call venv\Scripts\activate.bat

start cmd /k "python manage.py runserver"

start cmd /k "celery -A ingenium worker -l info -P eventlet"

start cmd /k "celery -A ingenium beat -l info" 

start cmd /k "celery -A ingenium flower -l info"