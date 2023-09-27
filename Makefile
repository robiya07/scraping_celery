mig:
	python3 manage.py makemigrations
	python3 manage.py migrate
	python manage.py migrate django_celery_results



run:
	python3 manage.py runserver $(PORT)

celery:
	celery -A root worker -l INFO -B

admin:
	python3 manage.py createsuperuser