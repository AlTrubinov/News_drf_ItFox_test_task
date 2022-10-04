Installation
-------------

1. Clone repo
2. Input next commands in console:
``` bash
$ python3 -m venv venv
$ . ./venv/bin/activate
$ pip install -r requirements.txt
$ ./manage.py migrate
$ ./manage.py runserver
``` 

Endpoints
-------------

`POST /auth/token/login` -- create token for authorized user

`GET /api/v1/` -- list of news with pagination

`POST /api/v1/` -- create news

`PUT /api/v1/{pk}/` -- edit news

`DELETE /api/v1/{pk}/` -- delete news

`GET /api/v1/{pk}/comment/` -- list of comments for news with pagination

`POST /api/v1/{new_pk}/comment/` -- create comment

`PUT /api/v1/{new_pk}/comment/{pk}/` -- edit comment

`DELETE /api/v1/{new_pk}/comment/{pk}/` -- delete comment
