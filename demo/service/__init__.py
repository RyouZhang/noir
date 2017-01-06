from demo.service.loader import import_service

__all__ =  import_service(__name__)

if __all__ is None:
    __all__ = [
        'test'
    ]

from service import *