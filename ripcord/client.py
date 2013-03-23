# -*- coding: utf-8 -*-

import requests
import urls
from exceptions import *
from munch import *

class Client(object):
    def __init__(self, **kwargs):
        self._baseurl = kwargs.get('baseurl', '')
        self._namespace = kwargs.get('namespace', '')
        self._endpoint = kwargs.get('endpoint', '')
        self._extra_params = kwargs.get('extra_params', {})
        self._extra_data = kwargs.get('extra_data', {})
        self._path_to_parse_response = kwargs.get('path_to_parse_response', [])
        self._path_to_parse_error = kwargs.get('path_to_parse_error', [])
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
    def endpoint(self):
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        self._endpoint = value

    @property
    def keep_trailing_slash(self):
        return self._keep_trailing_slash

    @keep_trailing_slash.setter
    def keep_trailing_slash(self, value):
        if not isinstance(value, bool):
            raise ValueError, 'argument `value` must be of type `bool`'
        self._keep_trailing_slash = value

    @property
    def extra_params(self):
        return self._extra_params

    def add_extra_params(self, key, value=None):
        if isinstance(key, dict):
            self._extra_params = key
        else:
            if not isinstance(key, str):
                raise ValueError, 'argument `key` must be of type `str`'
            self._extra_params[key] = value

    @property
    def extra_data(self):
        return self._extra_data

    def add_extra_data(self, key, value=None):
        if isinstance(key, dict):
            self._extra_data = key
        else:
            if not isinstance(key, str):
                raise ValueError, 'argument `key` must be of type `str`'
            self._extra_data[key] = value

    @property
    def path_to_parse_response(self):
        return self._path_to_parse_response

    def add_path_to_parse_response(self, key):
        if isinstance(key, list):
            self._path_to_parse_response = key
        else:
            if not isinstance(key, str):
                raise ValueError, 'argument `key` must be of type `str`'
            self._path_to_parse_response.append(key)

    @property
    def path_to_parse_error(self):
        return self._path_to_parse_error

    def add_path_to_parse_error(self, key):
        if isinstance(key, list):
            self._path_to_parse_error = key
        else:
            if not isinstance(key, str):
                raise ValueError, 'argument `key` must be of type `str`'
            self._path_to_parse_error.append(key)

    def construct_url(self, url):
        components = []
        if self.baseurl:
            components.append(self.baseurl)

        if self.namespace:
            components.append(self.namespace)

        if self.endpoint:
            components.append(self.endpoint)

        components.append(url)

        normalized_url = urls.normalize('/'.join(components))

        if not self.keep_trailing_slash:
            return normalized_url.rstrip('/')

        return normalized_url

    def check_error_response(self, response):
        if response.status_code in [200, 201]:
            return response

        if response.status_code == 400:
            raise BadRequest
        elif response.status_code == 401:
            raise Unauthorized
        elif response.status_code == 403:
            raise Forbidden
        elif response.status_code == 404:
            raise NotFound
        elif response.status_code == 500:
            raise ServerError
        else:
            raise HTTPError(response.status_code)

    def send(self, method, url, **kwargs):
        if self.extra_params:
            kwargs.update(params=dict(kwargs.get('params', {}).items() + \
                self.extra_params.items()))

        if self.extra_data:
            kwargs.update(data=dict(kwargs.get('data', {}).items() + \
                self.extra_data.items()))

        path_to_parse_response = kwargs.get('path_to_parse_response', None) \
            or self.path_to_parse_response
        kwargs.pop('path_to_parse_response', None)

        request = requests.Request(method=method, \
            url=self.construct_url(url), **kwargs)
        session = requests.Session()
        response = session.send(request.prepare())

        response = self.check_error_response(response)

        json = response.json()
        if path_to_parse_response:
            json = self._find_path_to_parse(json, path_to_parse_response)

        return munchify(json)

    def _find_path_to_parse(self, json, path_to_parse):
        if not isinstance(json, dict):
            raise ValueError, 'argument `json` must be of type `dict`'

        matched_node = json
        for node in path_to_parse:
            if node in matched_node:
                matched_node = matched_node[node]
        return matched_node

    def get(self, url, **kwargs):
        """ A wrapper method for `requests.get`. Takes the same parameters
            as the `requests` package.

            :Parameters
              - `url` (str) - URL target for the GET request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            :Returns
              ripcord.munch.Munch

            :Example
            >>> client = MyRipcordClient()
            >>> client.get('http://test.com/merp', param={'foo': 'bar'})
            <ripcord.munch.Munch>
        """
        return self.send('GET', url, **kwargs)

    def post(self, url, **kwargs):
        """ A wrapper method for `requests.posts`. Takes the same parameters
            as the `requests` package.

            :Parameters
              - `url` (str) - URL target for the POST request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            :Returns
              ripcord.munch.Munch

            :Example
            >>> client = MyRipcordClient()
            >>> client.post('http://test.com/merp', data={'foo': 'bar'})
            <ripcord.munch.Munch>
        """
        return self.send('POST', url, **kwargs)

    def put(self, url, **kwargs):
        """ A wrapper method for `requests.put`. Takes the same parameters
            as the `requests` package.

            :Parameters
              - `url` (str) - URL target for the PUT request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            :Returns
              ripcord.munch.Munch

            :Example
            >>> client = MyRipcordClient()
            >>> client.put('http://test.com/merp', data={'foo': 'bar'})
            <ripcord.munch.Munch>
        """
        return self.send('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        """ A wrapper method for `requests.delete`. Takes the same parameters
            as the `requests` package.

            :Parameters
              - `url` (str) - URL target for the DELETE request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            :Returns
              ripcord.munch.Munch

            :Example
            >>> client = MyRipcordClient()
            >>> client.delete('http://test.com/merp', params={'foo': 'bar'})
            <ripcord.munch.Munch>
        """
        return self.send('DELETE', url, **kwargs)

    def head(self, url, **kwargs):
        """ A wrapper method for `requests.head`. Takes the same parameters
            as the `requests` package.

            :Parameters
              - `url` (str) - URL target for the HEAD request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            :Returns
              ripcord.munch.Munch

            :Example
            >>> client = MyRipcordClient()
            >>> client.head('http://test.com/merp')
            <ripcord.munch.Munch>
        """
        return self.send('HEAD', url, **kwargs)

    def patch(self, url, **kwargs):
        """ A wrapper method for `requests.patch`. Takes the same parameters
            as the `requests` package.

            :Parameters
              - `url` (str) - URL target for the PATCH request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            :Returns
              ripcord.munch.Munch

            :Example
            >>> client = MyRipcordClient()
            >>> client.patch('http://test.com/merp', data={'foo': 'bar'})
            <ripcord.munch.Munch>
        """
        return self.send('PATCH', url, **kwargs)