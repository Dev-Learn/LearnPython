#!/usr/bin/env bash
cd /Users/trannam/LearnPython/practice7/src
django-admin startproject mytest
cd mytest
python manage.py runserver
#python manage.py runserver 1500
#python manage.py runserver 0.0.0.0:5000

#python manage.py startapp blogs ==> Create app
#python manage.py migrate

#python manage.py makemigrations blogs  => python manage.py migrate => python manage.py createsuperuser => import model into admin.py of blogs