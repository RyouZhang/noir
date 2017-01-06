from service.loader import import_service

__all__ =  import_service(__name__)

if __all__ is None:
    __all__ = [
        'hello_world',
        'hello_world_v2',
    ]

from service.test import *