from service.loader import load_service

__all__ =  load_service('service.stock.')

if __all__ is None:
    __all__ = (
        'stock_info_v1',
    )

from service.stock import *
