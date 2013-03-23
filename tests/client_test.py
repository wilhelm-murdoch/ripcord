# -*- coding: utf-8 -*-

from . import *
from ripcord import Client
from ripcord import munch
from ripcord.exceptions import *
from mock import Mock

class ClientTest(RipcordTest):
    def test_baseurl(self):
        self.fixtures.baseurl = 'http://test.com/'

        self.assertEquals(self.fixtures.baseurl, 'http://test.com/')

    def test_namespace(self):
        self.fixtures.namespace = 'v3'

        self.assertEquals(self.fixtures.namespace, 'v3')

    def test_endpoint(self):
        self.fixtures.endpoint = 'resource_name'

        self.assertEquals(self.fixtures.endpoint, 'resource_name')

    def test_construct_url(self):
        self.fixtures.baseurl = 'http://test.com/'
        self.fixtures.namespace = 'v3'
        self.fixtures.endpoint = 'resource_name'

        self.assertEquals(self.fixtures.construct_url('resource_id'), \
            'http://test.com/v3/resource_name/resource_id')

    def test_keep_trailing_slash(self):
        self.fixtures.keep_trailing_slash = True

        self.fixtures.baseurl = 'http://test.com/'
        self.fixtures.namespace = 'v3'
        self.fixtures.endpoint = 'resource_name'

        self.assertEquals(self.fixtures.construct_url('resource_id/'), \
            'http://test.com/v3/resource_name/resource_id/')

    def test_keep_trailing_slash_type_check(self):
        try:
            self.fixtures.keep_trailing_slash = 'merp'
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_add_extra_params_key_value(self):
        self.fixtures.add_extra_params('foo', 'bar')

        self.assertIsNotNone(self.fixtures.extra_params['foo'])
        self.assertEquals(self.fixtures.extra_params['foo'], 'bar')

    def test_add_extra_params_dict(self):
        self.fixtures.add_extra_params({'foo': 'bar', 'merp': 'flakes'})

        self.assertIsNotNone(self.fixtures.extra_params['foo'])
        self.assertIsNotNone(self.fixtures.extra_params['merp'])
        self.assertEquals(self.fixtures.extra_params['foo'], 'bar')
        self.assertEquals(self.fixtures.extra_params['merp'], 'flakes')

    def test_add_extra_params_type_check(self):
        try:
            self.fixtures.add_extra_params(True)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_add_extra_data_key_value(self):
        self.fixtures.add_extra_data('foo', 'bar')

        self.assertIsNotNone(self.fixtures.extra_data['foo'])
        self.assertEquals(self.fixtures.extra_data['foo'], 'bar')

    def test_add_extra_data_dict(self):
        self.fixtures.add_extra_data({'foo': 'bar', 'merp': 'flakes'})

        self.assertIsNotNone(self.fixtures.extra_data['foo'])
        self.assertIsNotNone(self.fixtures.extra_data['merp'])
        self.assertEquals(self.fixtures.extra_data['foo'], 'bar')
        self.assertEquals(self.fixtures.extra_data['merp'], 'flakes')

    def test_add_extra_data_type_check(self):
        try:
            self.fixtures.add_extra_data(True)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_add_path_to_parse_response_key(self):
        self.fixtures.add_path_to_parse_response('foo')

        self.assertEqual(len(self.fixtures.path_to_parse_response), 1)
        self.assertEquals(self.fixtures.path_to_parse_response.pop(0), 'foo')

    def test_add_path_to_parse_response_list(self):
        self.fixtures.add_path_to_parse_response(['foo', 'bar', 'baz'])

        self.assertEqual(len(self.fixtures.path_to_parse_response), 3)
        self.assertEquals(self.fixtures.path_to_parse_response[0], 'foo')
        self.assertEquals(self.fixtures.path_to_parse_response[1], 'bar')
        self.assertEquals(self.fixtures.path_to_parse_response[2], 'baz')

    def test_add_path_to_parse_response_type_check(self):
        try:
            self.fixtures.add_path_to_parse_response(True)
        except Exception, e:
            self.assertTrue(isinstance(e, ValueError))

    def test_check_error_response(self):
        code_to_response_map = {
            200: Mock,
            201: Mock,
            400: BadRequest,
            401: Unauthorized,
            403: Forbidden,
            404: NotFound,
            500: ServerError,
            418: HTTPError
        }

        for code, response in code_to_response_map.items():
            mock_response = Mock(status_code=200)
            mock_response.status_code = code

            try:
                response = self.fixtures.check_error_response(mock_response)
                self.assertEquals(mock_response.status_code, \
                    response.status_code)
            except Exception, e:
                self.assertEquals(e.code, code)
                self.assertTrue(isinstance(e, response))

    def test_send(self):
        methods = ['GET', 'POST', 'PUT', 'DELETE']

        for method in methods:
            response = self.fixtures.send(method, method.lower())

            self.assertEquals(len(response.args.keys()), 5)
            self.assertTrue(isinstance(response, munch.Munch))

    def test_http_methods(self):
        methods = ['GET', 'POST', 'PUT', 'DELETE']

        for method in methods:
            response = getattr(self.fixtures, method.lower())(method.lower())

            self.assertEquals(len(response.args.keys()), 5)
            self.assertEquals(response.args['token'], 'a-random-token')
            self.assertEquals(response.args['foo'], 'oof')
            self.assertEquals(response.args['bar'], 'rab')
            self.assertEquals(response.args['merp'], 'prem')
            self.assertEquals(response.args['flakes'], 'sekalf')
            self.assertTrue(isinstance(response, munch.Munch))