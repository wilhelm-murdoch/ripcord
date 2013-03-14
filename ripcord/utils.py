# -*- coding: utf-8 -*-

from urlparse import urlparse, urlunparse
from urllib import unquote
from string import lower
import re
import bunch


_collapse = re.compile('([^/]+/\.\./?|/\./|//|/\.$|/\.\.$)')
_parse_netloc = re.compile('^(?:([^\@]+)\@)?([^\:]+)(?:\:(.+))?$')

def normalize_url(url):
    (scheme, netloc, path, parameters, query, fragment) = urlparse(url)

    if netloc:
        userinfo, host, port = _parse_netloc.match(netloc).groups()
        if host[-1] == '.':
            host = host[:-1]
        netloc = lower(host)
        if userinfo:
            netloc = "{}@{}".format(userinfo, netloc)
        if port:
            netloc = "{}:{}".format(netloc, port)

    if scheme:
        last_path = path
        while 1:
            path = _collapse.sub('/', path, 1)
            if last_path == path:
                break
            last_path = path

    return urlunparse((scheme, netloc, unquote(path), parameters, \
        query, fragment))


class Munch(bunch.Bunch):
    def at(self, index=0):
        return self.get(self.keys()[index], None)

    def first(self):
        return self.get(self.keys()[0], None)

    def last(self):
        return self.get(self.keys().pop(), None)


def munchify(x):
    if isinstance(x, dict):
        return Munch( (k, munchify(v)) for k,v in x.iteritems() )
    elif isinstance(x, (list, tuple)):
        return type(x)( munchify(v) for v in x )
    else:
        return x