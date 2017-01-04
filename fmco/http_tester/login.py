# -*- coding: utf-8 -*-
import time
import traceback

from fmco.http_tester.base import Session
from fmco.http_tester import utils, constants

__author__ = 'lvyi'


def random_login_user():
    try:
        email, password = utils.get_random_login_name()

        session = Session()
        conf = session.conf

        req_data = conf.req__login_email(email, password)
        res, code = session.send(req_fnc=req_data)
        print("res=%s,%s" % (res, type(res)))

        if 'Incorrect email or password' == res or "{\"message\": \"Internal Server Error\"}" == res:
            req_data = conf.req__signup_email(email=email, password=password, is_random_email=False)
            res, code = session.send(req_fnc=req_data)

        # if 'Invalid email'==res:
        # raise RuntimeError('Invalid email')

        elif res.get('err_code', res.get('code', 0)) == 1009:
            req_data = conf.req__signup_email(email=email, password=password, is_random_email=False)
            res, code = session.send(req_fnc=req_data)

        uid = res['id']
        utoken = res['token']

        time.sleep(1)

        return Session(uid, utoken)
    except Exception as e:
        utils.print_red(traceback.format_exc())
        raise e