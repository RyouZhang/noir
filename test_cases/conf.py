# -*- coding: utf-8 -*-
from . import reqs

__author__ = 'lvyi'

from fmco.http_tester import options

globals_host_dev = 'http://127.0.0.1:8080'
globals_host_test = 'http://127.0.0.1:8080'
globals_host_stage = 'http://127.0.0.1:8080'

globals_host = globals_host_dev


# email_host = "niu.la"
#
# user_login_name = "auto_mock_001@%s" % email_host
# user_login_1 = "auto_test_0021@%s" % email_host
# user_login_2 = "auto_test_0031@%s" % email_host
#

class ApiConf(options.Conf):

    def init(self):

        print("...api conf...")

        self.host = globals_host
        self.dir = "api"

        # self.req__signup_email = reqs.req__signup_email
        # self.req__login_email = reqs.req__login_email

