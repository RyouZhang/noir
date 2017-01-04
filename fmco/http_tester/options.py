# -*- coding: utf-8 -*-

from fmco.http_tester import utils

__author__ = 'lvyi'

req_dir__api = "api"
req_dir__api_new = "api_new"
req_dir__bkend = "bk"
req_dir__msvc = "msvc"
req_dir__web = "web"

user_email = ""
user_password = ""

class Conf():
    """
        mock_type = 'http'  # dj_mock/ td_mock
    """
    host = 'http://127.0.0.1:8500'
    # mock_type = 'http'  # dj_mock/ td_mock
    mock_type = None
    dir = req_dir__api

    def __init__(self):
        # print "...Conf init..."
        # self.host = 'http://127.0.0.1:8500'
        self.dir = req_dir__api
        self.api_key = ''

        self.init()


    def init(self):
        raise NotImplementedError()

    def __str__(self):
        return utils.obj_to_str(self)


# __HTTP_TEST_CONF = None
#
#
# def get_conf():
#
#     global __HTTP_TEST_CONF
#     if not __HTTP_TEST_CONF:
#         __HTTP_TEST_CONF = Conf()
#
#         # 查找当前目录的conf.py
#         print auto_import()
#     else:
#         print __HTTP_TEST_CONF
#
#     return __HTTP_TEST_CONF

# def auto_import():
#     import importlib
#
#
#     conf_py_path = 'samples.http_test.conf'
#     conf = importlib.import_module(conf_py_path)
#
#     print conf
#
#     return conf