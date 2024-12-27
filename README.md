# theatre-service-api

Project "Theatre Service API". For online management of plays and performances in the current theater and ticket reservations. Built with Django REST Framework.

## Installing

Use this commands for installation of this project on your localhost

* Install PostgreSQL and create a data base
```shell
git clone https://github.com/spa7id/theatre-api-service
cd theatre_service
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
* create .env file in main directory
* set data into it (use .env.sample for reference)
```shell
POSTGRES_HOST=POSTGRES_HOST
POSTGRES_DB=POSTGRES_DB
POSTGRES_USER=POSTGRES_USER
POSTGRES_PASSWORD=POSTGRES_PASSWORD
```
```
python manage.py migrate
python manage.py runserver
```

## Run project with docker

* Download and install [Docker](https://www.docker.com/products/docker-desktop/)
* Run in terminal:

```shell
docker-compose build
docker-compose up
```


## Get access to project

* Download [ModHeader](https://chrome.google.com/webstore/detail/modheader/idgpnmonknjnojddfkpgkljpfnnfcklj?hl=en)
* create user - /api/user/register
* get access token /api/user/token/