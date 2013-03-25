# -*- coding: utf-8 -*-

import requests
import urls
from exceptions import *
from munch import *

class Client(object):
    def __init__(self, **kwargs):
        """Construct and return an instance of class `Client`.

        Parameters::
            - `baseurl` (str) - The root path of the API to send requests to.
            - `namespace` (str) - A path segment relative to `baseurl`
            - `endpoint` (str) - A path segment relative to `namespace`
            - `extra_params` (dict) - Default dict of extra query parameters to pass on through each request
            - `extra_data` (dict) - Default dict of extra data parameters to pass on through each request
            - `path_to_parse_response` (list) - A list of values that define a path to an API response body
            - `keep_trailing_slash` (bool) - Used to determine whether to strip the ending slash of a compiled full URL

        Returns::
            ripcord.Client instance

        Example::
            >>> client = ripcord.Client(
                    baseurl='https://api.twitter.com/',
                    namespace='1/',
                    endpoint='statuses/user_timeline',
                    extra_data={ 'foo': 'bar' },
                    extra_params={ 'merp': 'flakes'},
                    path_to_parse_response=['path', 'to', 'response'],
                    keep_trailing_slash=False
                )
            >>> client.get('wilhelm')
            ripcord.munch.Munch
        """
        self._baseurl = kwargs.get('baseurl', '')
        self._namespace = kwargs.get('namespace', '')
        self._endpoint = kwargs.get('endpoint', '')
        self._extra_params = kwargs.get('extra_params', {})
        self._extra_data = kwargs.get('extra_data', {})
        self._path_to_parse_response = kwargs.get('path_to_parse_response', [])
        self._keep_trailing_slash = kwargs.get('keep_trailing_slash', False)

    @property
    def baseurl(self):
        """Returns the value assigned to the `_baseurl` property.

        Returns::
            str

        Example::
            >>> client = ripcord.Client()
            >>> client.baseurl
            'http://www.example.com'
        """
        return self._baseurl

    @baseurl.setter
    def baseurl(self, value):
        """Assigns a value to the `_baseurl` property.

        Parameters::
            - `value` (str) - Contains the hostname portion of the API URL.

        Example::
            >>> client = ripcord.Client(baseurl='http://www.example.com')
            or
            >>> client = ripcord.Client()
            >>> client.baseurl = 'http://www.example.com'
            or
            >>> class API(ripcord.Client):
            >>>   def __init__(self, **kwargs):
            >>>     super(API, self).__init__(**kwargs)
            >>>     self.baseurl = 'http://www.example.com'
        """
        self._baseurl = value

    @property
    def namespace(self):
        """Returns the value assigned to the `_namespace` property.

        Returns::
            str

        Example::
            >>> client = ripcord.Client()
            >>> client.namespace
            'v1/'
        """
        return self._namespace

    @namespace.setter
    def namespace(self, value):
        """Assigns a value to the `_namespace` property.

        Parameters::
            - `value` (str) - Contains optional the namespace portion of the API URL.

        Example::
            >>> client = ripcord.Client(namespace='http://www.example.com')
            or
            >>> client = ripcord.Client()
            >>> client.namespace = 'v1/'
            or
            >>> class API(ripcord.Client):
            >>>   def __init__(self, **kwargs):
            >>>     super(API, self).__init__(**kwargs)
            >>>     self.namespace = 'v1/'
        """
        self._namespace = value

    @property
    def endpoint(self):
        """Returns the value assigned to the `_endpoint` property.

        Returns::
            str

        Example::
            >>> client = ripcord.Client()
            >>> client.endpoint
            'user_timeline/'
        """
        return self._endpoint

    @endpoint.setter
    def endpoint(self, value):
        """Assigns a value to the `_endpoint` property.

        Parameters::
            - `value` (str) - Contains optional the endpoint portion of the API URL.

        Example::
            >>> client = ripcord.Client(endpoint='user_timeline/')
            or
            >>> client = ripcord.Client()
            >>> client.endpoint = 'user_timeline/'
            or
            >>> class API(ripcord.Client):
            >>>   def __init__(self, **kwargs):
            >>>     super(API, self).__init__(**kwargs)
            >>>     self.endpoint = 'user_timeline/'
        """
        self._endpoint = value

    @property
    def keep_trailing_slash(self):
        """Returns the value assigned to the `_keep_trailing_slash` property.

        Returns::
            bool

        Example::
            >>> client = ripcord.Client()
            >>> client.keep_trailing_slash
            False
        """
        return self._keep_trailing_slash

    @keep_trailing_slash.setter
    def keep_trailing_slash(self, value):
        """Assigns a value to the `_keep_trailing_slash` property.

        Parameters::
            - `value` (bool) - Used to determine whether to strip the ending slash of a compiled full URL

        Example::
            >>> client = ripcord.Client(keep_trailing_slash=False)
            or
            >>> client = ripcord.Client()
            >>> client.keep_trailing_slash = False
            or
            >>> class API(ripcord.Client):
            >>>   def __init__(self, **kwargs):
            >>>     super(API, self).__init__(**kwargs)
            >>>     self.keep_trailing_slash = False

        Throws::
            ValueError
        """
        if not isinstance(value, bool):
            raise ValueError, 'argument `value` must be of type `bool`'
        self._keep_trailing_slash = value

    @property
    def extra_params(self):
        """Returns the value assigned to the `_extra_params` property.

        Returns::
            dict

        Example::
            >>> client = ripcord.Client()
            >>> client.extra_params
            {
                'foo': 'bar',
                'merp': 'flakes'
            }
        """
        return self._extra_params

    def add_extra_params(self, key, value=None):
        """Assigns a value to the `_extra_params` property. Use this method to
        add extra GET or DELETE query parameters that you want to include with
        every request. This method can also be used to assign default field
        values.

        Parameters::
            - `key` (str, dict) - Field name, or dict of field/value pairs
            - `value` (str, None) - Field value or None if `key` is a dict

        Example::
            >>> client = ripcord.Client(extra_params={ 'foo': 'bar' })
            or
            >>> client = ripcord.Client()
            >>> client.add_extra_params('foo', 'bar')
            >>> client.add_extra_params({ 'foo': 'bar' })
            or
            >>> class API(ripcord.Client):
            >>>   def __init__(self, **kwargs):
            >>>     super(API, self).__init__(**kwargs)
            >>>     self.add_extra_params('foo', 'bar')
            >>>     self.add_extra_params({ 'foo': 'bar' })

        Throws::
            ValueError
        """
        if isinstance(key, dict):
            self._extra_params = key
        else:
            if not isinstance(key, str):
                raise ValueError, 'argument `key` must be of type `str`'
            self._extra_params[key] = value

    @property
    def extra_data(self):
        """Returns the value assigned to the `_extra_data` property.

        Returns::
            dict

        Example::
            >>> client = ripcord.Client()
            >>> client.extra_data
            {
                'foo': 'bar',
                'merp': 'flakes'
            }
        """
        return self._extra_data

    def add_extra_data(self, key, value=None):
        """Assigns a value to the `_extra_data` property. Use this method to
        add extra POST, PUT or PATCH parameters that you want to include with
        every request. This method can also be used to assign default field
        values.

        Parameters::
            - `key` (str, dict) - Field name, or dict of field/value pairs
            - `value` (str, None) - Field value or None if `key` is a dict

        Example::
            >>> client = ripcord.Client(extra_data={ 'foo': 'bar' })
            or
            >>> client = ripcord.Client()
            >>> client.add_extra_data('foo', 'bar')
            >>> client.add_extra_data({ 'foo': 'bar' })
            or
            >>> class API(ripcord.Client):
            >>>   def __init__(self, **kwargs):
            >>>     super(API, self).__init__(**kwargs)
            >>>     self.add_extra_data('foo', 'bar')
            >>>     self.add_extra_data({ 'foo': 'bar' })

        Throws::
            ValueError
        """
        if isinstance(key, dict):
            self._extra_data = key
        else:
            if not isinstance(key, str):
                raise ValueError, 'argument `key` must be of type `str`'
            self._extra_data[key] = value

    @property
    def path_to_parse_response(self):
        """Returns the value assigned to the `_path_to_parse_response` property.

        Returns::
            list

        Example::
            >>> client = ripcord.Client()
            >>> client.path_to_parse_response
            ['path', 'to', 'response']
        """
        return self._path_to_parse_response

    def add_path_to_parse_response(self, key):
        """Assigns a value to the `_path_to_parse_response` property. This
        method can be used if you only wish to return a specific portion of the
        API response body. For instance, given the following JSON response:

            {
                'meta': {
                    // ... some data ...
                },
                'response': {
                    'users': [
                        // ... user entries ...
                    ],
                    'posts': [
                        // ... post entries ...
                    ]
                }
            }

        You only want to return the list of users, so here's what you do:

        >>> client = ripcord.Client(path_to_parse_response=['response', 'users'])
        >>> client.get('http://api.example.com/test')
        [
            // ... user entries ...
        ]

        Parameters::
            - `key` (str, dict) - Field name, or dict of field/value pairs
            - `value` (str, None) - Field value or None if `key` is a dict

        Example::
            >>> client = ripcord.Client(extra_data={ 'foo': 'bar' })
            or
            >>> client = ripcord.Client()
            >>> client.add_extra_data('foo', 'bar')
            >>> client.add_extra_data({ 'foo': 'bar' })
            or
            >>> class API(ripcord.Client):
            >>>   def __init__(self, **kwargs):
            >>>     super(API, self).__init__(**kwargs)
            >>>     self.add_extra_data('foo', 'bar')
            >>>     self.add_extra_data({ 'foo': 'bar' })

        Throws::
            ValueError
        """
        if isinstance(key, list):
            self._path_to_parse_response = key
        else:
            if not isinstance(key, str):
                raise ValueError, 'argument `key` must be of type `str`'
            self._path_to_parse_response.append(key)

    def construct_url(self, url):
        """Using the specified URL components, this method attempts to combine
        `_baseurl`, `_namespace`, `_endpoint` and the specified `url` into a
        single, normalized, path.

        Parameters::
            - `url` (str) - The full URL, or URL segment, to send to specified request to

        Returns::
            str

        Example::
            >>> client = ripcord.Client(
                    baseurl='https://api.twitter.com',
                    namespace='1/',
                    endpoint='statuses/user_timeline/'
                )
            >>> client.construct_url('wilhelm.json')
            'https://api.twitter.com/1/statuses/user_timeline/wilhelm.json'
        """
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
        """As the name suggests, this method checks the requests response body
        for any errors and will raise the appropriate exception. This method can
        be overloaded with your own version if you like. Though, it is
        recommended that you first call the parent version of this method. This
        method is invoked upon every successful request.

        Parameters::
            - `response` () - `requests.Response` instance containing the response of the latest request.

        Returns::
            requests.Response

        Example::
            >>> def API(ripcord.Client):
            >>>   def check_error_response(self, response):
            >>>     super(API, self).check_error_response(response)
            >>>     # ... my own error checking is done here ...

        Raises::
            ripcord.exceptions.BadRequest
            ripcord.exceptions.Unauthorized
            ripcord.exceptions.Forbidden
            ripcord.exceptions.NotFound
            ripcord.exceptions.ServerError
            ripcord.exceptions.HTTPError
        """
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
        """Builds and dispatches a request. Expects a JSON-based response and
        raise an appropriate exception if the response body cannot be parsed.
        Applies all specified `extra_data` and `extra_params`, checks for error
        responses, parses JSON data and returns it according to any existing
        paths specified in `path_to_parse_response`.Will return a Munch'ed JSON
        response body, for dot-notation access.

        Parameters::
            - `method` (str) - The HTTP method to apply to the given URL, eg: POST, PUT, GET, DELETE, PATCH, HEAD
            - `url` (str) - The URL, or URL segment, to invoke.

        Returns::
            ripcord.munch.Munch

        Example::
            >>> client = ripcord.Client()
            >>> client.send('GET', 'https://api.twitter.com/1/statuses/user_timeline/wilhelm.json')
            ripcord.munch.Munch

        Raises::
            ripcord.exceptions.InvalidJSONResponse
        """
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

        try:
            json = response.json()
        except Exception:
            raise InvalidJSONResponse(response.text)

        if path_to_parse_response:
            json = self._find_path_to_parse(json, path_to_parse_response)

        return munchify(json)

    def _find_path_to_parse(self, json, path_to_parse):
        """ Will attempt to return the dict at the end of a specified path to
        parse. Given a list of named fields, this method will recursively
        iterate through the JSON dict's keys and return the dict associated
        with the last matched key name. Note, that if no keys from the list are
        matched, this method will return the original JSON dict.

        Parameters::
          - `json` (dict) - The JSON response to parse
          - `path_to_parse` (list) - The list of key names to iterate through

        Returns::
          JSON dict

        Example::
        >>> nested_dict = { 'foo': { 'bar': { 'baz': [1, 2, 3] } } }
        >>> client = MyRipcordClient()
        >>> client._find_path_to_parse(nested_dict, ['foo', 'bar', 'baz'])
        [1, 2, 3]
        """
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

            Parameters::
              - `url` (str) - URL target for the GET request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            Returns::
              ripcord.munch.Munch

            Example::
            >>> client = MyRipcordClient()
            >>> client.get('http://test.com/merp', param={'foo': 'bar'})
            ripcord.munch.Munch
        """
        return self.send('GET', url, **kwargs)

    def post(self, url, **kwargs):
        """ A wrapper method for `requests.post`. Takes the same parameters
            as the `requests` package.

            Parameters::
              - `url` (str) - URL target for the POST request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            Returns::
              ripcord.munch.Munch

            Example::
            >>> client = MyRipcordClient()
            >>> client.post('http://test.com/merp', data={'foo': 'bar'})
            ripcord.munch.Munch
        """
        return self.send('POST', url, **kwargs)

    def put(self, url, **kwargs):
        """ A wrapper method for `requests.put`. Takes the same parameters
            as the `requests` package.

            Parameters::
              - `url` (str) - URL target for the PUT request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            Returns::
              ripcord.munch.Munch

            Example::
            >>> client = MyRipcordClient()
            >>> client.put('http://test.com/merp', data={'foo': 'bar'})
            ripcord.munch.Munch
        """
        return self.send('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        """ A wrapper method for `requests.delete`. Takes the same parameters
            as the `requests` package.

            Parameters::
              - `url` (str) - URL target for the DELETE request
              - `**kwargs` (dict) - Optional keyword arguments as outlined in
                `requests.Request` documentation.

            Returns::
              ripcord.munch.Munch

            Example::
            >>> client = MyRipcordClient()
            >>> client.delete('http://test.com/merp', params={'foo': 'bar'})
            ripcord.munch.Munch
        """
        return self.send('DELETE', url, **kwargs)

    def head(self, url, **kwargs):
        """ A wrapper method for `requests.head`. Takes the same parameters
        as the `requests` package.

        Parameters::
          - `url` (str) - URL target for the HEAD request
          - `**kwargs` (dict) - Optional keyword arguments as outlined in
            `requests.Request` documentation.

        Returns::
          ripcord.munch.Munch

        Example::
            >>> client = MyRipcordClient()
            >>> client.head('http://test.com/merp')
            ripcord.munch.Munch
        """
        return self.send('HEAD', url, **kwargs)

    def patch(self, url, **kwargs):
        """ A wrapper method for `requests.patch`. Takes the same parameters
        as the `requests` package.

        Parameters::
          - `url` (str) - URL target for the PATCH request
          - `**kwargs` (dict) - Optional keyword arguments as outlined in
            `requests.Request` documentation.

        Returns::
          ripcord.munch.Munch

        Example::
            >>> client = MyRipcordClient()
            >>> client.patch('http://test.com/merp', data={'foo': 'bar'})
            ripcord.munch.Munch
        """
        return self.send('PATCH', url, **kwargs)