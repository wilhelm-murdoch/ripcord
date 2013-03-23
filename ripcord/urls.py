# -*- coding: utf-8 -*-

"""
urlnorm.py - URL normalisation routines

urlnorm normalises a URL by;
  * lowercasing the scheme and hostname
  * taking out default port if present (e.g., http://www.foo.com:80/)
  * collapsing the path (./, ../, etc)
  * removing the last character in the hostname if it is '.'
  * unquoting any %-escaped characters

Available functions:
  normalize - given a URL (string), returns a normalised URL
  norm      - given a URL tuple, returns a normalised tuple

CHANGES:
0.92 - unknown schemes now pass the port through silently
0.91 - general cleanup
     - changed dictionaries to lists where appropriate
     - more fine-grained authority parsing and normalisation
"""

from urlparse import urlparse, urlunparse
from urllib import unquote
from string import lower
import re

_collapse = re.compile('([^/]+/\.\./?|/\./|//|/\.$|/\.\.$)')
_server_authority = re.compile('^(?:([^\@]+)\@)?([^\:]+)(?:\:(.+))?$')
_default_port = {   'http': '80',
                    'https': '443',
                    'gopher': '70',
                    'news': '119',
                    'snews': '563',
                    'nntp': '119',
                    'snntp': '563',
                    'ftp': '21',
                    'telnet': '23',
                    'prospero': '191',
                }
_relative_schemes = [   'http',
                        'https',
                        'news',
                        'snews',
                        'nntp',
                        'snntp',
                        'ftp',
                        'file',
                        ''
                    ]
_server_authority_schemes = [   'http',
                                'https',
                                'news',
                                'snews',
                                'ftp',
                            ]


def normalize(urlstring):
    """given a string URL, return its normalised form"""
    return urlunparse(norm(urlparse(urlstring)))


def norm(urltuple):
    """given a six-tuple URL, return its normalised form"""
    (scheme, authority, path, parameters, query, fragment) = urltuple
    scheme = lower(scheme)
    if authority:
        userinfo, host, port = _server_authority.match(authority).groups()
        if host[-1] == '.':
            host = host[:-1]
        authority = lower(host)
        if userinfo:
            authority = "%s@%s" % (userinfo, authority)
        if port and port != _default_port.get(scheme, None):
            authority = "%s:%s" % (authority, port)
    if scheme in _relative_schemes:
        last_path = path
        while 1:
            path = _collapse.sub('/', path, 1)
            if last_path == path:
                break
            last_path = path
    path = unquote(path)
    return (scheme, authority, path, parameters, query, fragment)