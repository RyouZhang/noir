from service.loader import load_service

__all__ =  load_service('service.')

if __all__ is None:
    __all__ = (
        'comm',
        'stock',
        'news',
        'search',
    )

from service import *
