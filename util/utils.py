# -*- coding: utf-8 -*-

__author__ = 'lvyi'


def obj_to_str(obj):
    obj_string = []
    for key in obj.__dict__:
        obj_string.append("%s%s%s" % (key, ':', obj.__dict__[key]))
    return "%s __str__=%s" % (obj.__class__.__name__, obj_string)
