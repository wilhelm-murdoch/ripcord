# -*- coding: utf-8 -*-

from . import *
from ripcord.exceptions import *

class ExceptionTest(RipcordTest):
    def test_raises_badrequest(self):
        try:
            self.fixtures.simulate_status_code(400)
        except Exception, e:
            self.assertEquals(e.code, 400)
            self.assertEquals(e.message, 'Bad Request')
            self.assertTrue(isinstance(e, BadRequest))

    def test_raises_unauthorized(self):
        try:
            self.fixtures.simulate_status_code(401)
        except Exception, e:
            self.assertEquals(e.code, 401)
            self.assertEquals(e.message, 'Unauthorized')
            self.assertTrue(isinstance(e, Unauthorized))

    def test_raises_forbidden(self):
        try:
            self.fixtures.simulate_status_code(403)
        except Exception, e:
            self.assertEquals(e.code, 403)
            self.assertEquals(e.message, 'Forbidden')
            self.assertTrue(isinstance(e, Forbidden))

    def test_raises_not_found(self):
        try:
            self.fixtures.simulate_status_code(404)
        except Exception, e:
            self.assertEquals(e.code, 404)
            self.assertEquals(e.message, 'Not Found')
            self.assertTrue(isinstance(e, NotFound))

    def test_raises_server_error(self):
        try:
            self.fixtures.simulate_status_code(500)
        except Exception, e:
            self.assertEquals(e.code, 500)
            self.assertEquals(e.message, 'Internal Server Error')
            self.assertTrue(isinstance(e, ServerError))

    def test_raises_like_whatever_man(self):
        try:
            self.fixtures.simulate_status_code(405)
        except Exception, e:
            self.assertEquals(e.code, 405)
            self.assertTrue(isinstance(e, HTTPError))

    def test_raises_invalid_json_error(self):
        try:
            self.fixtures.get('html')
        except Exception, e:
            self.assertTrue(isinstance(e, InvalidJSONResponse))