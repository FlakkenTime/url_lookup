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

pip3 install pytest

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

## Unit testing.
This currently takes some manual setup. I'd add a bash script that would do the setup
and teardown if I had more time.

1. Test db setup from commandline: `mysql -u user_name -p < tests/db_setup.sql`
2. In `resources/db.ini` set `Connect`, `User`, and `Password`.
3. In `resource/db.ini` set `Database_Name = url_lookup_testing`
4. In `resource/db.ini` set `Update_pass = testing_pass`
5. Start your service: `gunicorn src.url_lookup:app`
6. pytest
7. Cleanup: `mysql -u user_name -p < tests/db_cleanup.sql
