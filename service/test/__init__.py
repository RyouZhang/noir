from service.loader import import_service

__all__ =  import_service('service.test')

if __all__ is None:
    __all__ = (
        'hello_world',
        'hello_world_v2',
        'push_message',
    )

from service.test import *