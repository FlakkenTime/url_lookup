# url_lookup

## Info
This is a Proof of Concept for a URL Lookup service. It accepts a URL and checks
to see if it is black listed.

## Install
pip3 install mysqlclient

pip3 install flask

pip3 install gunicorn

pip3 install pytest

pip3 install configparser

## Config
1. Set your DB config info in `resources/db.ini`
2. If wanted can further customize gunicorn in `resources.config.py`

## Run it
Basic HTTP for testing: `gunicorn src.lookup:app`

HTTPS: `gunicorn --certfile=server.crt --keyfile=server.key src.lookup:app`

## Direct testing
1. simple query: `curl localhost:8000/urlinfo/1/your_URL_here`
2. db update:

```
curl -XPOST -H "Content-Typ-d '{"PASS":"FAKE","urls":"test1,test2"}' http://127.0.0.1:8000/urlupdate/1/
```
