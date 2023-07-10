#!/bin/sh
sudo apt update
sudo apt install -y python3.8 python3.8-venv python3.8-dev python3-pip

python3.8 -m venv env

env/bin/python -m pip install -r requirements.txt
env/bin/python manage.py makemigrations activitypub
env/bin/python manage.py migrate
env/bin/python manage.py loaddata fixture/setup.json

cp simple_ap.conf.example simple_ap.conf
echo directory=$PWD >> simple_ap.conf
echo command=$PWD/env/bin/uwsgi --ini flask.ini >> simple_ap.conf
echo user=$USER >> simple_ap.conf
sudo mv simple_ap.conf /etc/supervisor/conf.d/
sudo supervisorctl reload
