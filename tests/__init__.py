# -*- coding: utf-8 -*-

import ripcord
import unittest
from fixtures import Fixtures

class RipcordTest(unittest.TestCase):
    def setUp(self):
        self.fixtures = Fixtures()