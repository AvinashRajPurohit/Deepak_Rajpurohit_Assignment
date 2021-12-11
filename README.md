# Sales-Stats 

### [See Application live](https://myapp963635.herokuapp.com/)

## Requirements
  * Python-version -: Python 3.9.9
  * Django-version -: 4.0.0

### After installing requirements cross check it using:
```sh
$ python3 -V
$ django-admin --version
```
## Setup

The first thing to do is to clone the repository:
```sh
$  git clone https://github.com/AvinashRajPurohit/Deepak_Rajpurohit_Assignment.git
$ git checkout v2
$ cd dir_name
```

Create a virtual environment to install dependencies in and activate it:

```sh
$ sudo apt install python3-venv
$ python3 -m venv env
$ source env/bin/activate
```
Then install the dependencies:

```sh
(env)$ pip install -r requirements.txt
```
Once `pip` has finished downloading the dependencies:

# Add the SECRET_KEY in Env variables:
```
export SECRET_KEY = 'django-insecure-_p#p@b9^&nj0c$ogl2hx3gbw4^d#c!&4g66l%q&1e%k@xw7e#n'
```

## DataBase configrations
After DB configurations

```sh
(env)$ python manage.py migrate
(env)$ python manage.py runserver
```
And navigate to `http://127.0.0.1:8000/docs`


 

