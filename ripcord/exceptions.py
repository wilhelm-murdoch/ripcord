# -*- coding: utf-8 -*-

from requests.status_codes import _codes
from string import capwords


class HTTPError(Exception):
    def __init__(self, code):
        super(HTTPError, self).__init__()
        self.code = code
        self.message = self.__wordify(_codes[code][0])

    def __str__(self):
        return "<{} {}>".format(self.code, self.message)

    def __wordify(self, message):
        return capwords(message, sep='_').replace('_', ' ')

class BadRequest(HTTPError):
    def __init__(self):
        super(BadRequest, self).__init__(400)

class Unauthorized(HTTPError):
    def __init__(self):
        super(Unauthorized, self).__init__(401)

class Forbidden(HTTPError):
    def __init__(self):
        super(Forbidden, self).__init__(403)

class NotFound(HTTPError):
    def __init__(self):
        super(NotFound, self).__init__(404)

class ServerError(HTTPError):
    def __init__(self):
        super(ServerError, self).__init__(500)