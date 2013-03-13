# -*- coding: utf-8 -*-

import requests
from bunch import *
from utils import normalize_url

# create own bunchify with helper methods similar to those in jetpack. Also,
# gracefully check for key errors and return None or automatically define them.

class Ripcord(object):
    def __init__(self, **kwargs):
        self._baseurl = kwargs.get('baseurl', '')
        self._namespace = kwargs.get('namespace', '')
        self._extra_query = kwargs.get('extra_query', {})
        self._extra_body = kwargs.get('extra_body', {})
        self._path_to_parse = kwargs.get('path_to_parse', [])
        self._keep_trailing_slash = kwargs.get('keep_trailing_slash', False)

    @property
    def baseurl(self):
        return self._baseurl

    @baseurl.setter
    def baseurl(self, value):
        self._baseurl = value

    @property
    def namespace(self):
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        self._namespace = value

    @property
    def keep_trailing_slash(self):
        return self._keep_trailing_slash

    @keep_trailing_slash.setter
    def keep_trailing_slash(self, value):
        assert isinstance(value, bool), 'wtf, seriously guys.'
        self._keep_trailing_slash = value

    @property
    def extra_body(self):
        return self._extra_body

    @property
    def extra_query(self):
        return self._extra_query

    def add_extra_body(self, key, value=None):
        if isinstance(key, dict):
            self._extra_body = key
        else:
            assert isinstance(key, str), 'wtf, dude?'
            self._extra_body[key] = value

    def add_extra_query(self, key, value=None):
        if isinstance(key, dict):
            self._extra_query = key
        else:
            assert isinstance(key, str), 'wtf, dude?'
            self._extra_query[key] = value

    def construct_url(self, url):
        return normalize_url("{}/{}/{}".format(self._baseurl, self._namespace, \
            url))

    def check_error_response(self, response):
        return response

    def send(self, method, url, **kwargs):
        params = self.extra_query
        request = requests.Request(method=method, url=self.construct_url(url), params=params, **kwargs)
        session = requests.Session()
        response = session.send(request.prepare())

        return bunchify(response.json())

    def get(self, url, **kwargs):
        return self.send('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self.send('POST', url, **kwargs)

    def put(self, url, **kwargs):
        return self.send('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self.send('DELETE', url, **kwargs)

    def head(self, url, **kwargs):
        return self.send('HEAD', url, **kwargs)

    def patch(self, url, **kwargs):
        return self.send('PATCH', url, **kwargs)