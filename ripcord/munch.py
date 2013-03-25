# -*- coding: utf-8 -*-

import bunch

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