# social-backend
Django backend for social media project

This project is built using Django REST Framework to provide the backend API for social media project. The deployed API is available on [Heroku](https://social-backend-django.herokuapp.com/). The frontend is available [here](https://github.com/kkosiba/social-frontend). 

Features
--------
...

Main requirements
------------

1. `python` 3.5, 3.6, 3.7
2. `Django` 2.1.9
3. `PostgreSQL` 11.1

This project also uses other packages (see `requirements.txt` file for details).
For instance, tag support is provided by [django-taggit](https://github.com/alex/django-taggit) and image processing is thanks to [Pillow](https://github.com/python-pillow/Pillow).

## How to set up

### Setup using Docker

The easiest way to get backend up and running is via [Docker](https://www.docker.com/). See [docs](https://docs.docker.com/get-started/) to get started. Once set up run the following command:

`docker-compose up`

This command takes care of populating website with sample data.

It may take a while for the process to complete, as Docker needs to pull required dependencies. Once it is done, the application should be accessible at `0.0.0.0:8000`.

### Manual setup

Firstly, create a new directory and change to it:

`mkdir social-backend && cd social-backend`

Then, clone this repository to the current directory:

`git clone https://github.com/kkosiba/social-backend.git .`


For the backend to work, one needs to setup database like SQLite or PostgreSQL on a local machine. This project uses PostgreSQL by default (see [Django documentation](https://docs.djangoproject.com/en/2.1/ref/settings/#databases) for different setup). This process may vary from one OS to another, eg. on Arch Linux one can follow a straightforward guide [here](https://wiki.archlinux.org/index.php/PostgreSQL).

The database settings are specified in `src/settings/local.py`. In particular the default database name is `SocialDjango`, which can be created from the PostgreSQL shell by running `createdb SocialDjango`.

Next, set up a virtual environment and activate it:

`python3 -m venv env && source env/bin/activate`

Install required packages:

`pip3 install -r requirements.txt`

Next, perform migration:

`python3 manage.py migrate --settings=src.settings.local`

The backend is now ready. Run a local server with

`python3 manage.py runserver --settings=src.settings.local`

The backend should be available at `localhost:8000`.
