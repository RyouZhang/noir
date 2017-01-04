# -*- coding: utf-8 -*-

import random
import sys
from hashids import Hashids
from fmco.http_tester import constants


def singleton(cls):
    instances = {}
    def _singleton(*args, **kw):
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]
    return _singleton

def random_phone(length):
    number = '0123456789'
    id = ''
    for i in range(0,length):
        id += random.choice(number)
    return id

def random_str(length):
    number = '0123456789'
    alpha = 'abcdefghijklmnopqrstuvwxyz'
    id = ''
    for i in range(0,length,2):
        id += random.choice(number)
        id += random.choice(alpha)
    return id

def random_word(length):

    words = '2001 toyota camry rubs great, one owner car leather interior sunroof, power windows. ' \
            'Factory car CD stereo/cassette player. Timing chain and oil water pump changed. Oil change ' \
            'and inspection ready. Interested should call 214-8094768 for test drive. OBO serious buyers only, ' \
            'negotiations is allowed.'
    arr = words.split(' ')
    arr_len = len(arr)
    res = []
    for i in range(length):
        item = arr[random.randint(0,arr_len-1)]
        res.append(item)
    return ' '.join(res)

def send_img(host , uri ,data ,file_name, headers=None, is_check_code=False, test_unit=None):
    url = '%s%s' % (host ,uri)
    print(url)
    file = {"image":open(file_name,'rb')}
    res = requests.post(url,data=data,files=file)

    req_code = res.status_code
    if 200 == req_code:
        res_json = res.json()
        res_code = res_json['code']
        return res_json ,res_code
    else:
        return res.json() ,req_code

def check_list(res, desc, unittest=None):
    meta = res.get('meta', None)
    total_count = meta['total_count']
    if unittest:
        unittest.assertTrue(total_count > 0, desc)
    return total_count

def check_list_exist(res, ckeck_id, check_exist=True, unittest=None):
    list = res['objects']
    exist = False
    for it in list:
        print("item_id = %s" % it['id'])
        if ckeck_id==it['id']:
            exist = True

    if check_exist:
        # 期望存在
        unittest.assertTrue(exist, "check_list_exist=%s" % check_exist)
    else:
        # 期望不存在
        unittest.assertFalse(exist, "check_list_exist=%s" % check_exist)

def get_random_login_name():
    password = '12345678'
    # 100 个用户之间，随机
    emails = []
    for i in range(100):
        emails.append("u_%s_rdm@%s" % (i, constants.email_host))

    email = random.sample(emails, 1)
    return email, password

def abc(*c):
    print(c)

def asd(**c):
    print(c)

def hhh(*c1,**c2):
    if len(c1): print(c1)
    if len(c2): print(c2)
    print("haha =%s,%s" % (c1,c2))

    print(sys._getframe().f_code.co_name)
    # print len(c1)
    # print len(c2)


def decrypt_item_id(fluzzy_item_id):

    ITEM_HASH_ID_MIN_LENGTH = 16
    ITEM_HASH_ID_SALT = 'fivemiles-1d27ca806afc'
    hashider4item = Hashids(min_length=ITEM_HASH_ID_MIN_LENGTH, salt=ITEM_HASH_ID_SALT)

    return hashider4item.decrypt(fluzzy_item_id)[0]

def decrypt_user_id(fluzzy_user_id):

    print("fluzzy_user_id=%s" % fluzzy_user_id)
    HASH_ID_MIN_LENGTH = 10
    HASH_ID_SALT = 'hello, soho0506'
    hashider = Hashids(min_length=HASH_ID_MIN_LENGTH, salt=HASH_ID_SALT)

    user_id = hashider.decrypt(fluzzy_user_id)
    print(user_id)
    return user_id[0]


import requests

def retry(attempt):
    def decorator(func):
        def wrapper(*args, **kw):
            att = 0
            while att < attempt:
                try:
                    return func(*args, **kw)
                except Exception as e:
                    att += 1
        return wrapper
    return decorator

# 重试次数
@retry(attempt=3)
def get_response(url):
    r = requests.get('http://www.oschina.net')
    return r.content


# todo req ansyc
# def req_ansyc():
#     from requests_futures.sessions import FuturesSession
#
#     #session = FuturesSession()
#     session = FuturesSession(executor=ThreadPoolExecutor(max_workers=10))
#
#     # first request is started in background
#     future_one = session.get('http://httpbin.org/get')
#     # second requests is started immediately
#     future_two = session.get('http://httpbin.org/get?foo=bar')
#     print "====>"
#     # wait for the first request to complete, if it hasn't already
#     response_one = future_one.result()
#     print('response one status: {0}'.format(response_one.status_code))
#     print(response_one.content)
#     # wait for the second request to complete, if it hasn't already
#     response_two = future_two.result()
#     print('response two status: {0}'.format(response_two.status_code))
#     print(response_two.content)



def _wrap_with(code):

    def inner(text, bold=False):
        c = code
        if bold:
            c = "1;%s" % c
        return "\033[%sm%s\033[0m" % (c, text)
    return inner

red = _wrap_with('31')
green = _wrap_with('32')
yellow = _wrap_with('33')
blue = _wrap_with('34')
magenta = _wrap_with('35')
cyan = _wrap_with('36')
white = _wrap_with('37')


def print_red(text, bold=False):
    print(red(text, bold))


def print_green(text, bold=False):
    print(green(text, bold))


def print_yellow(text, bold=False):
    print(yellow(text, bold))


def print_blue(text, bold=False):
    print(blue(text, bold))


def print_magenta(text, bold=False):
    print(magenta(text, bold))


def print_cyan(text, bold=False):
    print(cyan(text, bold))


def print_white(text, bold=False):
    print(white(text, bold))


def obj_to_str(obj):
    obj_string = []
    for key in obj.__dict__:
        obj_string.append("%s%s%s" % (key, ':', obj.__dict__[key]))
    return "%s __str__=%s" % (obj.__class__.__name__, obj_string)



if __name__ == '__main__':
    # for a in range(10):
    #     print random_word(5)

    # abc(1,2,3)
    # asd(a=1,b=2,c=3)
    # hhh(1,2)
    # hhh(b=2,c=3)
    # hhh(1,2,c=3)
    #
    # hhh()

    #print decrypt_user_id("E8oYKBK9Ra")

    #req_ansyc()

    print(blue(">>>>> %s " % 'haha', bold=True))