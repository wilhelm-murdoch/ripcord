# -*- coding: utf-8 -*-

__all__ = ['HTTPError', 'BadRequest', 'Unauthorized', 'Forbidden', \
    'NotFound', 'ServerError']

class HTTPError(Exception):
    def __init__(self, code=000, message=''):
        super(HTTPError, self).__init__()
        self.code = code
        self.message = message

    def __str__(self):
        return "<{} {}>".format(self.code, self.message)

class BadRequest(HTTPError):
    def __init__(self):
        self.code = 400
        self.message = 'Bad Request'

class Unauthorized(HTTPError):
    def __init__(self):
        self.code = 401
        self.message = 'Unauthorized'

class Forbidden(HTTPError):
    def __init__(self):
        self.code = 403
        self.message = 'Forbidden'

class NotFound(HTTPError):
    def __init__(self):
        self.code = 404
        self.message = 'Not Found'

class ServerError(HTTPError):
    def __init__(self):
        self.code = 500
        self.message = 'Internal Server Error'