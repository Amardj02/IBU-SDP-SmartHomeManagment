# SmartHomeManagement
Web application

## Python 3.11

python manage.py runserver 8080

python manage.py migrate

python manage.py createsuperuser --username=amar --email=amar@gmail.com

python manage.py dumpdata auth.User --indent 4 > users.json

python manage.py loaddata users.json

python manage.py dumpdata manage_devices.Room --indent 4 > rooms.json

python manage.py loaddata rooms.json

## Docker
docker run --name smart-home -e MYSQL_ROOT_PASSWORD=root -d mysql