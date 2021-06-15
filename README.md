# BE Project Backend (oneQshop)
Demo: https://youtu.be/-Psl9HTsxXU
Android Studio Code: https://github.com/dms24081999/oneQshop-AndroidStudio

## Setup auto-formatting with Git Hooks:
```
pip uninstall autopep8
pip install black
pre-commit install
pre-commit run --all-files
```

## Format files before commit:
```
pre-commit run --all-files
```

## Untrack files already added to git repository based on .gitignore:
Commit all Changes and
```
git rm -r --cached .
git add .
git commit -m ".gitignore fix"
```

## Install Python Tools:
```
sudo apt install python3-virtualenv python3-pip
```

## Create Virtual Environment:
```
virtualenv -p python3.8 unix-env
source ./unix-env/bin/activate
```

## Install requirements:
```
pip install -r requirements.txt
```

## Run all migrations:
```
cd src
python manage.py makemigrations
python manage.py migrate
python manage.py showmigrations
```

## Create Super-user:
```
cd src
python manage.py createsuperuser
```
```
email: dms24081999@gmail.com
username: admin
password: 24081999
```

## Reset Migrations:
```
cd src
find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
find . -path "*/migrations/*.pyc"  -delete
python manage.py makemigrations
python manage.py migrate
```

## Populate Database:
```
cd src
python manage.py populate_db \
    --users_file "/mnt/d/Projects/BE Project/main-backend/src/management/csv/users.csv" \
    --categories_file "/mnt/d/Projects/BE Project/main-backend/src/management/csv/categoriesDf.csv" \
    --brands_file "/mnt/d/Projects/BE Project/main-backend/src/management/csv/brandsDf.csv" \
    --product_images_file "/mnt/d/Projects/BE Project/main-backend/src/management/csv/productImagesDf.csv" \
    --products_file "/mnt/d/Projects/BE Project/main-backend/src/management/csv/productsDf.csv" \
    --images_path "/mnt/d/Projects/BE Project/data/final-dataset"
```

## Migrating to another Server:
### export DB to json
```
python manage.py dumpdata > db.json
sudo apt-get update
sudo apt-get install python3-dev default-libmysqlclient-dev build-essential
pip install mysqlclient
```
### Change the database settings to new database such as of MySQL / PostgreSQL.
```
python manage.py migrate
python manage.py shell
```
### Enter the following in the shell:
```
from django.contrib.contenttypes.models import ContentType
ContentType.objects.all().delete()
exit()
```
### Update new DB from json
```
python manage.py loaddata db.json
```

## Manage or move static files to server:
```
python manage.py collectstatic --noinput
```

## Run Project:
```
source ./setup.sh
cd src
python manage.py runserver 8000
```

## AWS MySQL server connect:
```
mysql -h <hostname / ip> -P <port> -u <server-username> -p
```

## Dockerize Project:
```
sudo docker build -t dms24081999/oneqshop-v1 .
sudo docker run -itd -p 8080:8888 dms24081999/oneqshop-v1
```

## Run localhost online:
```
ngrok http 8000
npm install -g localtunnel
lt --port 8000
lt -p 8000 -s dms24-v4
curl -v https://dms24-v2.loca.lt
```
