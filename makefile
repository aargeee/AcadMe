rn:
	py manage.py runserver

mm:
	py manage.py makemigrations

mg: mm
	py manage.py migrate
