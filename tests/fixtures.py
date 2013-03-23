# -*- coding: utf-8 -*-

import ripcord

class Fixtures(ripcord.Client):
    def __init__(self, **kwargs):
        super(Fixtures, self).__init__(**kwargs)

        self.baseurl = 'http://httpbin.org/'

        self.add_extra_params({
            'token': 'a-random-token',
            'foo': 'oof',
            'bar': 'rab',
            'merp': 'prem',
            'flakes': 'sekalf'
        })

    def simulate_status_code(self, status_code):
        self.namespace = 'status'
        return self.get(str(status_code))