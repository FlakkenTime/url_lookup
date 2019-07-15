#!/usr/bin/python3

import json
import pytest
import random
import requests
from configparser import ConfigParser


class TestLookup(object):

    def setup(self):
        self.config = ConfigParser()
        self.config.read('resources/db.ini')
        self.url_request = 'http://localhost:8000/urlinfo/1/'
        self.url_post = 'http://localhost:8000/urlupdate/1/'
        self.headers = {'content-type': 'application/json'}

    def test_allowed(self):
        """
        Test for allowed URL
        """
        response = requests.get('%staco-shop.com' % self.url_request)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'True'

    def test_blocked(self):
        """
        Test for blocked URL
        """
        response = requests.get('%stest1' % self.url_request)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'False'

    def test_url_update_valid(self):
        """
        Test adding new blocked URL
        """
        # add a new url
        random_url = 'test_update_%d' % random.randint(1, 1000)
        payload = {'PASS': self.config['Database']['Update_Pass'],
                   'urls': random_url}
        response = requests.post(self.url_post,
                                 data=json.dumps(payload),
                                 headers=self.headers)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'True'

        # now test the new URL is blocked
        response = requests.get('%s%s' % (self.url_request, random_url))
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'False'

    def test_url_update_bad_pass(self):
        """
        Test update with bad password
        """
        payload = {'PASS': 'tater tots', 'urls': 'failed'}
        response = requests.post(self.url_post,
                                 data=json.dumps(payload),
                                 headers=self.headers)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'False'

    def test_no_json(self):
        response = requests.post(self.url_post)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'False no parameters provided'

    def test_no_pass(self):
        payload = {'urls': 'failed'}
        response = requests.post(self.url_post,
                                 data=json.dumps(payload),
                                 headers=self.headers)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'False no pass provided'

    def test_no_urls(self):
        payload = {'PASS': 'failed'}
        response = requests.post(self.url_post,
                                 data=json.dumps(payload),
                                 headers=self.headers)
        assert response.status_code == 200
        assert response.content.decode('utf-8') == 'False no urls provided'
