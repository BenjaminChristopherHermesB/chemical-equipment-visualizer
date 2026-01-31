#!/bin/bash

# Build script for Render deployment

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate
