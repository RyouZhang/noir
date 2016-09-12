import os

__all__ = (
    'hello_world',
    'hello_world_v2',
    'push_message',
    'http_proxy_v1',
)

services = os.getenv('SERVICES', None)
if services is not None:
    services = [s.strip() for s in services.split(',')]
    valid_services = [service.replace('service.test.', '') for service in services if service.startswith('service.test.')]
    if len(valid_services) > 0:
        __all__ = valid_services

from service.test import *