# Realtime Chat Application 

## Technology Used:
1. Django
2. Django Channels
3. Django Rest Framework

## Setup process 

Create virtual environment

    python3 -m venv <environment_name>

Activate virtual environment

    source <environment_name>/bin/activate

(<environment_name>) path/to/project/

Install project dependencies

    pip install -r requirements.txt

Migrate the database table

    python3 manage.py migrate

Now, Run the server

    python manage.py runserver
