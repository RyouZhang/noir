# -*- coding: utf-8 -*-

import os

__all__ = [
    'get_news_es_host',
    'get_item_es_host'
]


def get_news_es_host():
    host = os.getenv('ES_NEWS_HOST', None)
    if host is None:
        return None
    return host


def get_item_es_host():
    host = os.getenv('ES_ITEM_HOST', None)
    if host is None:
        return None
    return host
