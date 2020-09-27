# The Wall App

This is the backend of the Wall app which is handled using Django Rest Framework while frontend is handled in React.
This backend handles User Registration  & then allowing them to Login using token authentication.
The backend also allow the registred user to Post & View the Posts from other users as well.



## Project setup
### Requirements
- Python 3.6+

### Setting up Python3 Virtual Environment
```
python3.6 -m venv virtualenv

```
### Activating the Virtual Environment
```
source virtualenv/bin/activate

```

### Install dependencies
(run this command in the directory containing requirements.txt file)
```
pip install -r requirements.txt
```
### Database Setup 
(run this command in the directory containing manage.py file)
```
python manage.py migrate
```
### Running the Backend 
(run this command in the directory containing manage.py file)
```
python manage.py runserver
```


## Unit tests
(run this command in the directory containing manage.py file).
The tests are written using Django Tests
```
python3.6 manage.py test
