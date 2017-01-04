import os

def import_service(service_name):
    services = os.getenv('SERVICES', None)

    if services is not None:
        services = [s.strip() for s in services.split(',')]
        valid_services = [service.replace(service_name, '').split('.')[0] for service in services if service.startswith(service_name)]
        if len(valid_services) > 0:
            return valid_services
        return None
    return None
