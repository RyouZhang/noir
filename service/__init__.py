import os

__all__ = (
    'stock',
    'test',
)

services = os.getenv('SERVICES', None)
if services is not None:
    services = [s.strip() for s in services.split(',')]
    valid_services = [service.replace('service.', '').split('.')[0] for service in services if service.startswith('service.')]
    if len(valid_services) > 0:
        __all__ = valid_services

from service import *
