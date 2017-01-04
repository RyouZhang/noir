from service.loader import load_service

__all__ =  load_service('service.news.')

if __all__ is None:
    __all__ = (
        'news_info_v1',
        'news_like_v1',
        'news_list_v1',
        'news_open_v1',
    )

from service.news import *