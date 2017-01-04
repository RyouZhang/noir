# -*- coding: utf-8 -*-
# from util import utils

__author__ = 'lvyi'


class BaseParams(dict):
    def __init__(self, **args):
        for k in args:
            self[k] = args[k]

    def __str__(self):
        obj_string = []
        for key, value in super(BaseParams, self).items():
            obj_string.append("%s%s%s" % (key, ':', value))
        return "%s __str__=%s" % (self.__class__.__name__, obj_string)

    def __getattr__(self, name):
        return super(BaseParams, self).__getitem__(name)

    def __setattr__(self, name, value):
        super(BaseParams, self).__setitem__(name, value)

class BaseParamsAA(BaseParams):
    pass


if __name__ == "__main__":
    req = BaseParamsAA(a=99)
    req['aaa'] = '1111'
    req.bbb = "222"

    print(req.items())

    print(len(req))
    print(req)
    print(req.aaa)
    print(req.bbb)
    print(req.get('bbb'))

    print(req['a'])

    # print(req['lon'])
