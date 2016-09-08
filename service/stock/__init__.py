import os

__all__ = (
    'stock_info_v1',
)

services = os.getenv('SERVICES', None)
if services is not None:
    services = [s.strip() for s in services.split(',')]
    valid_services = [service.replace('service.stock.', '') for service in services if service.startswith('service.stock.')]
    if len(valid_services) > 0:
        __all__ = [service for service in valid_services]

from service.stock import *