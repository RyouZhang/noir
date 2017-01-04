# -*- coding: utf-8 -*-
from service.loader import load_service

__all__ =  load_service('service.comm.')

if __all__ is None:
    __all__ = (
        'health_check',
    )


from service.comm import *

