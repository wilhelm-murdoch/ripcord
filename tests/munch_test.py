# -*- coding: utf-8 -*-

from . import *
from ripcord import munch

class MunchTest(RipcordTest):
    def _snag_me_a_dict(self):
        return {
            'id': 12345,
            'handle': 'wilhelm',
            'first_name': 'Wilhelm',
            'last_name': 'Murdoch',
            'posts': {
                54321: {
                    'id': 54321,
                    'body': 'omg wtf bbq'
                },
                54234: {
                    'id': 54234,
                    'body': 'another test post, yo'
                },
                90354085: {
                    'id': 90354085,
                    'body': 'awww, shit son!'
                },
                562345: {
                    'id': 562345,
                    'body': 'sup, duder?'
                }
            }
        }

    def test_munchify_json(self):
        munched = munch.munchify(self._snag_me_a_dict())

        self.assertTrue(isinstance(munched, munch.Munch))
        self.assertEquals(munched.handle, 'wilhelm')
        self.assertEquals(munched.first_name, 'Wilhelm')
        self.assertEquals(munched.last_name, 'Murdoch')

    def test_munch_at(self):
        munched = munch.munchify(self._snag_me_a_dict())

        post = munched.posts.at(1)

        self.assertIsNotNone(post)
        self.assertEquals(post.id, 54234)
        self.assertEquals(post.body, 'another test post, yo')

    def test_munch_first(self):
        munched = munch.munchify(self._snag_me_a_dict())

        post = munched.posts.first()

        self.assertIsNotNone(post)
        self.assertEquals(post.id, 54321)
        self.assertEquals(post.body, 'omg wtf bbq')

    def test_munch_last(self):
        munched = munch.munchify(self._snag_me_a_dict())

        post = munched.posts.last()

        self.assertIsNotNone(post)
        self.assertEquals(post.id, 562345)
        self.assertEquals(post.body, 'sup, duder?')