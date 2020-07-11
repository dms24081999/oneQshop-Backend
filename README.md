# BE Project Backend

## Setup auto-formatting with Git Hooks:
```
pip uninstall autopep8
pip install black
pre-commit install
pre-commit run --all-files
```

## Install Python Tools:
```
sudo apt install python3-virtualenv python3-pip
```

## Create Virtual Environment:
```
virtualenv -p python3.8 unix-env3.8
source ./unix-env3.8/bin/activate
source ./.bashrc
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
```

## Create Super-user:
```
cd src
python manage.py createsuperuser
```

## Run Project:
```
cd src
python manage.py runserver
```
