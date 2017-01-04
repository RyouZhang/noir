from service.loader import impoer_service

__all__ =  impoer_service('service.test')

if __all__ is None:
    __all__ = (
        'hello_world',
        'hello_world_v2',
        'push_message',
    )

from service.test import *