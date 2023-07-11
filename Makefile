PYTHON_BIN = python3

include .env
dependencies:
	sudo apt update
	sudo apt install -y python3 python3-venv python3-dev python3-pip 

setup:
	python3 -m venv env
	sed -i "s/^DOMAIN = .*$$/DOMAIN = '$(DOMAIN)'/g" simple_ap/settings.py 
	env/bin/pip install -r requirements.txt
	env/bin/python manage.py makemigrations activitypub
	env/bin/python manage.py migrate
	env/bin/python manage.py loaddata fixture/setup.json

supervisor_setup:
	cp sample/config/simple_ap.conf.example simple_ap.conf
	echo directory=$(PWD) >> simple_ap.conf
	echo command=$(PWD)/env/bin/uwsgi --ini flask.ini >> simple_ap.conf
	echo user=$(USER) >> simple_ap.conf

supervisor_enable:
	sudo cp simple_ap.conf /etc/supervisor/conf.d/
	sudo supervisorctl reload

systemd_setup:
	cp sample/config/simple_ap.service.example simple_ap.service
	echo WorkingDirectory=$(PWD) >> simple_ap.service
	echo ExecStart=$(PWD)/env/bin/uwsgi --ini flask.ini >> simple_ap.service
	echo User=$(USER) >> simple_ap.service

systemd_enable:
	sudo cp simple_ap.service /etc/systemd/system/
	sudo systemctl daemon-reload
	sudo systemctl enable simple_ap.service
	sudo systemctl start simple_ap.service

nginx_setup:
	cp sample/config/nginx_simple_ap.conf.example nginx_simple_ap.conf
	sed -i "s/DOMAIN/$(DOMAIN)/g" nginx_simple_ap.conf

nginx_enable:
	sudo cp nginx_simple_ap.conf /etc/nginx/sites-available/$(DOMAIN)/
	sudo ln -s /etc/nginx/sites-available/$(DOMAIN) /etc/nginx/sites-enabled/
	sudo systemctl restart nginx

superuser:
	env/bin/python manage.py createsuperuser

run_standalone:
	env/bin/python run_flask.py

run_standalone_admin:
	env/bin/python manage.py runserver
