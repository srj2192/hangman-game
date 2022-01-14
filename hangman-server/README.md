# hangman-server

Hangman REST API written in python using flask

## Getting started

Make sure you're using python 3.8

Setup virtual env

```
virtualenv --python=python3 venv
source venv/bin/activate
```

Build Project

```
make build
```

Install requirements

```
make setup
```

Run the tests

```
make test
```

Start server

```
python server.py
```

Hit the API

```
POST http://localhost:5000/api/hangman
GET http://localhost:5000/api/hangman/{game_id}
```
