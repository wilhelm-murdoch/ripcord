# -*- coding: utf-8 -*-

from urlparse import urlparse, urlunparse
from urllib import unquote
from string import lower
import re

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