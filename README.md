# Flask-Vue Book Library

A book library application built with flask and vue.

## Main Features

- CRUD
- Authentication
- Pagination

## Setup

#### Backend

```bash
$ python -m venv venv
# or venv\Scripts\activate on windows
$ . venv/bin/activate 
$ pip install -r requirements.txt
# run tests
$ python -m py.test -x
# setup database
$ python manage.py db upgrade
# seed the database with some records
$ python manage.py seed
$ python manage.py runserver # http://localhost:5000
```

**Note**: You change the port number for the backend in case of a conflict by running `python manage.py runserver --port 5555`, but when you do, you will have to change the base URL in the file `ui/src/services/http.js`.

#### Frontend

```bash
$ cd ui
$ npm install
$ npm run serve # http://localhost:8080
```

#### Demo

You can check it out [here](https://flask-vue-book-library.herokuapp.com/).
