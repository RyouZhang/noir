# -*- coding: utf-8 -*-
from fmco.http_tester import utils
from fmco.http_tester import constants

__author__ = 'lvyi'


def req__health_check():
    return {
        "url":"/api/health_check",
        "method":"get",
        #"post_format":"kv/json",
        "data":{}
    }


def req__msvc_servers():
    return {
        "url":"/msvc/v2/servers/",
        "method":"get",
        "data":{}
    }

#
# def req__msvc_init():
#     return {
#         "url":"/msvc/v2/init/",
#         "method":"get",
#         "data":{}
#     }


# def req__signup_email(email='testuser@wespoke.com', password=constants.defaut_pws, nickname='haha',is_random_email=True):
#     if is_random_email:
#         random_str = utils.random_str(8)
#         email = 'a%s@wespoke.com' % random_str
#         nickname = random_str
#     return {
#         "url":"/api/v2/signup_email/",
#         "method":"post",
#         "data":{'email':email,'password':password,'nickname':nickname},
#     }
#
#
# def req__login_email(email='testuser@wespoke.com' ,password=constants.defaut_pws):
#     return {
#         "url":"/api/v2/login_email/",
#         "method":"post",
#         "data":{'email':email,'password':password},
#     }

def req__search_city():
    return {
        "url":"/api/search/city/item/v1",
        "method":"get",
        #"post_format":"kv/json",
        "data":{}
    }
