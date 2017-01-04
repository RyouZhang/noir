#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest

from fmco.http_tester import base
from test_cases import conf
from test_cases import reqs


class HealthCheckTest(unittest.TestCase):
    def setUp(self):
        # 初始化Session
        self.session = base.Session(conf=conf.ApiConf)

    def tearDown(self):
        pass

    def test_health_check(self):
        res, code = self.session.send(req_fnc=reqs.req__health_check)
        self.assertEqual(code, 200)
        # self.assertTrue(len(res)>0)

    def test_search_city(self):
        res, code = self.session.send(req_fnc=reqs.req__search_city)
        self.assertEqual(code, 200)

if __name__ == '__main__':
    unittest.main()
