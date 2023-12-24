
#Packages

Django==4.2.8
djangorestframework==3.14.0
python-dotenv==1.0.0
pytest==7.4.3
pytest-django==4.7.0
black==23.12.0
flake8==6.1.0
django-mptt==0.15.0
drf-spectacular==0.27.0


#Commands
django-admin startproject drfecomm

python .\manage.py runserver 

 python .\manage.py shell 

from django.core.management.utils import get_random_secret_key 
print(get_random_secret_key())

python .\manage.py createsuperuser

python .\manage.py spectacular --file schema.yml #To create yaml file with schema


#pytest

pytest -h #prints options and config file setting

