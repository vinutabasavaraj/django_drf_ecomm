
#Packages

Django==4.2.8
djangorestframework==3.14.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-django==4.7.0


#Commands
django-admin startproject drfecomm

python .\manage.py runserver 

 python .\manage.py shell 

from django.core.management.utils import get_random_secret_key 
print(get_random_secret_key())


#pytest

pytest -h #prints options and config file setting

