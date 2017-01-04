from service.loader import impoer_service

__all__ =  impoer_service('service.')

if __all__ is None:
    __all__ = (
        'test'
    )

from service import *
