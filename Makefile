run:
	python manage.py runserver
migrations:
	python manage.py makemigrations
migrate:
	python manage.py migrate
create-admin:
	python manage.py createsuperuser