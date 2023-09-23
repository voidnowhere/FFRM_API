#!/bin/bash

pip install -r requirements.txt

sed -i "s/^SECRET_KEY=$/SECRET_KEY=$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')/" /app/.env

python manage.py runserver 0.0.0.0:8000