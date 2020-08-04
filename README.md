# SchoolERP

## Clone the project to your system

```console
git clone https://github.com/Rajangupta09/School-beta.git
```

## Change into project directory

```console
cd School
```

## Create virtual environment

```python
virtualenv env
./env/Scripts/activate
```

## Install requirements

```python
pip install -r requirements.txt
```

## Create database

<!-- For mysql change engine in settings.py/DATABASES

	'django.db.backends.mysql'

For postgresql change engine in settings.py/DATABASES

	'django.db.backends.postgresql_psycopg2'

Change the user and password according to your database servers

	Create new database and set 'NAME' : <database_name> -->

## Makemigrations and migrate

```python
python manage.py makemigrations
python manage.py migrate
```

## Start the development server

```python
python manage.py runserver
```
## Create Super User
```python
python manage.py createsuperuser
```