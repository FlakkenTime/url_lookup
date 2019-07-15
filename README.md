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

## Run it
1. gunicorn src.lookup:app

## Direct testing
`curl localhost:8000/urlinfo/1/your_URL_here`

