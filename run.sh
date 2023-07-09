#!/bin/bash
echo "start migrate"
python manage.py migrate
echo "run server"
gunicorn python3 manage.py runserver --noreload
