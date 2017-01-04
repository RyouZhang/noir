from service.loader import load_service

__all__ =  load_service('service.search.')

if __all__ is None:
    __all__ = (
        'search_api_handler',
        'search_city_item_v1',
        'search_category_item_v1',
        'search_category_job_v1',
    )

from service.search import *