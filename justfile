shell:
    python manage.py shell

migrate:
    python manage.py migrate

runserver:
    python manage.py runserver

startapp app:
    python manage.py startapp {{ app }}

makemigrations app:
    python manage.py makemigrations {{ app }}


