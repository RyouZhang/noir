# -*- coding: utf-8 -*-
import traceback
from math import radians, sin, cos, asin, sqrt

import util

__author__ = 'lvyi'


def cal_distance(lat1,lon1,   lat2,lon2):
    """
    根据经纬度，计算2个点之间的距离
    """
    # convert decimal degrees to radians
    try:
        if lon1==0 or lat1==0 or lon2==0 or lat2==0:
            return -1

        lon1, lat1, lon2, lat2 = map(radians, [float(lon1), float(lat1), float(lon2), float(lat2)])
        # haversine formula
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        km = 6371 * c

        distance = int(km * 1000)
        util.logger.debug("lon1=%s, lat1=%s, lon2=%s, lat2=%s, distance=%s" % (lon1, lat1, lon2, lat2, distance))
        return distance
    except Exception as e:
        #logging.error(traceback.format_exc())
        util.logger.warn(traceback.format_exc())
        return -1