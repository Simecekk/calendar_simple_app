# Simple Calendar API

RESTful API for managing calendar events and conference room availability.


Each user can choose his/her timezone (default = UTC) 

All endpoints are timezone-aware and return results in the timezone of the currently logged in user.

## How to start project?

1) Install requirements: ``pip install -r requirements.txt``
2) create and fill .env: ``cp .env.sample .env``
3) Create database schema: ``python manage.py migrate`` (assume you have postgres running)
4) start server: ``python manage.py runserver``
5) access API on: http://127.0.0.1:8000/ (you can use browsable interface from django 
