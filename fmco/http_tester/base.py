# -*- coding: utf-8 -*-

import json
import traceback
import time

import requests

from fmco.http_tester import constants, utils, options


class Session():
    req_dir = "api"
    req_env = "dev"

    def __init__(self, fz_uid=None, uid=None, utoken=None, conf=options.Conf, env=None,
                 is_login=False, headers_ext=None):
        self.uid = uid
        self.fz_uid = fz_uid
        self.utoken = utoken
        self.headers_ext = headers_ext

        self.conf = conf()

        req_dir = conf.dir
        if req_dir:
            self.req_dir = req_dir

        if env:
            # set temp env
            self.conf.host = env
            print("self.conf.host=%s" % self.conf.host)

        if is_login:
            self.login_user()

    def __str__(self):
        return '   session fz_uid,uid=%s,%s,%s' % (self.fz_uid, self.uid, self.req_dir)

    def send(self, req_fnc, req_dir=None, check_error_code=True):

        if req_dir:
            self.req_dir = req_dir

        res = send(req_fnc=req_fnc, session=self, check_error_code=check_error_code)

        return res

    def login_user(self, email=constants.user_login_name, password=constants.defaut_pws):
        try:
            conf = self.conf

            if options.user_email:
                email = options.user_email

            if options.user_password:
                password = options.user_password

            req_data = conf.req__login_email(email, password)
            res, code = send(req_fnc=req_data, session=self)
            # print "res=%s,%s" % (res, type(res))

            if 'Incorrect email or password' == res or "{\"message\": \"Internal Server Error\"}" == res:
                print("req__signup_email 1")
                req_data = conf.req__signup_email(email=email, password=password, is_random_email=False)
                res, code = send(req_fnc=req_data, session=self)

            # if 'Invalid email'==res:
            #    raise RuntimeError('Invalid email')
            # print res
            fz_uid = None
            utoken = None
            err_code = res.get('code', res.get('err_code', 0))
            if err_code >= 0:
                if err_code == 1009:
                    # 先修改密码
                    # res, code = send_one(reqs.req__reset_password(email=email_encode, password="h_%s"%password),
                    #                                   check_error_code=False)
                    # #self.assertEqual(res['err_code'], 1006, "email no found.")

                    # 再创建用户
                    req_data = conf.req__signup_email(email=email, password=password, is_random_email=False)
                    res, code = send(req_fnc=req_data, session=self)

                fz_uid = res['id']
                utoken = res['token']
                print(">>login ok:", fz_uid, utoken)
            else:
                raise

            time.sleep(1)

            self.fz_uid = fz_uid
            # self.uid = uid
            self.utoken = utoken

            return self;

        except Exception as e:
            utils.print_red(traceback.format_exc())
            raise e


class SessionBkend(Session):
    def __init__(self, uid=None, utoken=None, conf=options.Conf):
        self.uid = uid
        self.utoken = utoken
        self.req_dir = "bk"

        self.conf = conf()

        Session.__init__(self, uid=uid, utoken=utoken, req_dir=self.req_dir)

    def __str__(self):
        return '   session fz_uid=%s,uid=%s' % (self.fz_uid, self.uid)


def req_fnc_load(req_fnc):
    print("req_fnc", req_fnc)
    if isinstance(req_fnc, str):
        req = eval("reqs.req__%s()" % req_fnc)
    elif isinstance(req_fnc, dict):
        req = req_fnc
    else:
        req = req_fnc()
    return req


def get_env_url(req_def, session):
    req_dir = session.req_dir
    req_env = session.req_env
    uri = req_def['url']
    return uri, req_dir, req_env


def build_http_headers(req_dir, session):
    headers = {}
    if session and session.req_dir in [options.req_dir__api, options.req_dir__api_new]:
        headers = {"X-FIVEMILES-UID": session.uid,
                   'X-FIVEMILES-USER-ID': session.fz_uid,
                   'X-FIVEMILES-USER-TOKEN': session.utoken,
                   "X-FIVEMILES-APP-LOCATION": '1,1',
                   "X-FIVEMILES-DISABLE-VERIFY-SIGN": "T"
                   }

    elif session and req_dir == options.req_dir__bkend:
        headers = {'Authorization': session.conf.api_key}

    try:
        if session.conf.build_headers:
            headers = session.conf.build_headers(session)
    except Exception as ex:
        print("conf.build_headers not define:", ex)

    if session.headers_ext:
        headers.update(session.headers_ext)

    return headers


def send(req_fnc=None, data=None, params=None, session=None, check_error_code=True, ignore_check=False):
    req_def = req_fnc_load(req_fnc)
    utils.print_blue("-----------------------------req start-----:%s" % req_def)

    host = session.conf.host
    # print "req_fnc type=%s" % type(req_fnc)
    # print "  %s" % req_name


    data = data or req_def['data']

    uri, req_dir, req_env = get_env_url(req_def, session)
    # print host, uri, req_dir, req_env

    headers = build_http_headers(req_dir, session)

    # utils.print_green("     headers=%s" % headers)

    method = req_def.get('method', 'get')
    if req_dir == session.conf.mock_type:
        # res = send_django_mock(uri, data, params=None, method='get', headers=None,
        #                        is_check_code=False, test_unit=None, check_error_code=False)
        pass
    else:
        if uri.find("be_api") > 0:
            if not params:
                params = {}
            params['ignore_check'] = True

        if data and ignore_check:
            data['ignore_check'] = True

        res = send_http(host, uri, data, params=params, method=method, headers=headers,
                        is_check_code=True, check_error_code=check_error_code)

    return res


def send_django_mock(req_name='req_name', req_fnc=None, data=None, headers=None,
                     is_check_code=False, test_unit=None, check_error_code=False):
    req = req_fnc_load(req_fnc, req_name)

    # from django.core.urlresolvers import reverse
    uri = req['url']

    # from django.test import Client
    #
    # client = Client()
    # response = client.post(uri, data, headers)
    # res_data = json.loads(response.content)

    # return res_data, response.status_code


def send_http(host, uri, data, params=None, method='get', headers=None,
              is_check_code=False, test_unit=None, check_error_code=False):
    url = None
    try:

        url = '%s%s' % (host, uri)
        # logging.info("%s,%s" % (url ,data))
        utils.print_blue(">>TST_REQ: %s: %s" % (method, url))
        utils.print_blue(">>TST_REQ_data: %s" % data)
        utils.print_blue(">>TST_REQ_headers: %s" % headers)

        if method == 'get':
            r = requests.get(url, params=data, headers=headers)
        elif method == 'post':
            r = requests.post(url, data=data, params=params, headers=headers)
        elif method == 'post_json':
            r = requests.post(url, json=data, params=params, headers=headers)
        else:
            r = requests.request(method, url, data=data, params=params, headers=headers)

        req_code = r.status_code

        utils.print_green("     req body: %s" % r.request.body)

        # print ">>TST_REQ_HEADERS:%s" % r.request.headers
        utils.print_blue(">>TST_RES_HEADERS:%s,%s" % (r.request, r.headers,))
        # print "  r.raw=%s" % r.raw
        # print ">>%s" % r.headers['content-type']
        # print "check_error_code=%s" % check_error_code

        res_text = r.text

        if req_code >= 500:
            err0 = ">>SVR_ERR:%s ,%s ,%s" % (req_code, url, ("%s" % res_text).encode("utf-8")[:200])
            err1 = ">>SVR_ERR:%s ,%s ,%s" % (req_code, url, res_text)
            utils.print_yellow("-----------------------------SVR_ERR-----:%s" % err0)
            utils.print_red(err1)
            if is_check_code and test_unit:
                test_unit.assertTrue(req_code, 200, err1)

            if "DOCTYPE html" in r.text:
                raise RuntimeError(err0)

            raise RuntimeError("ERR:%s,%s" % (req_code, url))

        elif req_code >= 400:
            err0 = ">>SVR_ERR:%s ,%s ,%s" % (req_code, url, ("%s" % res_text).encode("utf-8")[:200])
            utils.print_yellow("-----------------------------SVR_ERR-----:%s" % err0)
            # err1 = ">>SVR_ERR:%s ,%s ,%s" % (req_code, url, res_text)
            # utils.print_red(err1)
            if is_check_code and test_unit:
                test_unit.assertTrue(req_code, 200, err0)

            if "DOCTYPE html" in res_text:
                raise RuntimeError(err0)

            if "" == res_text:
                raise RuntimeError(err0)

            # print r.headers.get("Content-Type").find("json")
            # r.headers['content-type']
            if r.headers.get("Content-Type").find("json") > 0:
                res_json = r.json()
                # print res_json
                err_code = res_json.get("code", res_json.get('err_code', 0))
                if check_error_code and err_code > 0 and err_code != 1009:
                    raise RuntimeError(res_json)
            else:
                raise RuntimeError(err0)

            return res_json, req_code
        else:
            res_str = res_text
            print(res_str)
            if res_str != '' and res_str.find("{") >= 0:
                # print 'result json'
                res_json = r.json()
            else:
                res_json = res_str

            try:
                utils.print_blue(">>BIZ_RES: %s" % res_json)
                return res_json, req_code

            except Exception as e:
                err = ">>BIZ_ERR: %s,%s,%s" % (res_json, e, url)
                print(err)
                return res_json, req_code

    except Exception as e:
        err = ">>NWK_ERR: %s ,url=%s" % (e, url)
        utils.print_red(traceback.format_exc())
        utils.print_red(err)
        # if is_check_code and test_unit:
        # test_unit.assertEquals("!", "", err)

        raise e
