# -*- coding: utf-8 -*-

from . import *
from ripcord import urls

class UrlsTest(RipcordTest):
    def test_normalize_url(self):
        tests = {
            '/foo/bar/.':                    '/foo/bar/',
            '/foo/bar/./':                   '/foo/bar/',
            '/foo/bar/..':                   '/foo/',
            '/foo/bar/../':                  '/foo/',
            '/foo/bar/../baz':               '/foo/baz',
            '/foo/bar/../..':                '/',
            '/foo/bar/../../':               '/',
            '/foo/bar/../../baz':            '/baz',
            '/foo/bar/../../../baz':         '/../baz',
            '/foo/bar/../../../../baz':      '/baz',
            '/./foo':                        '/foo',
            '/../foo':                       '/../foo',
            '/foo.':                         '/foo.',
            '/.foo':                         '/.foo',
            '/foo..':                        '/foo..',
            '/..foo':                        '/..foo',
            '/./../foo':                     '/../foo',
            '/./foo/.':                      '/foo/',
            '/foo/./bar':                    '/foo/bar',
            '/foo/../bar':                   '/bar',
            '/foo//':                        '/foo/',
            '/foo///bar//':                  '/foo/bar/',
            'http://www.foo.com:80/foo':     'http://www.foo.com/foo',
            'http://www.foo.com:8000/foo':   'http://www.foo.com:8000/foo',
            'http://www.foo.com./foo/bar.html': 'http://www.foo.com/foo/bar.html',
            'http://www.foo.com.:81/foo':    'http://www.foo.com:81/foo',
            'http://www.foo.com/%7ebar':     'http://www.foo.com/~bar',
            'http://www.foo.com/%7Ebar':     'http://www.foo.com/~bar',
            'ftp://user:pass@ftp.foo.net/foo/bar': 'ftp://user:pass@ftp.foo.net/foo/bar',
            'http://USER:pass@www.Example.COM/foo/bar': 'http://USER:pass@www.example.com/foo/bar',
            'http://www.example.com./':      'http://www.example.com/',
            '-':                             '-',
        }

        for bad, good in tests.items():
            self.assertEqual(urls.normalize(bad), good)
