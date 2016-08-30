import math

import util

def signed_filter(params, context):
    timestamp = params.get('timestamp', None)
    sign = params.get('sign', None)
    args = params.get('args', dict())

    if timestamp is None or math.fabs(timestamp - util.get_timestamp()) > 300000:
        return False, 'Invalid_Timestamp'
    
    if sign is None:
        return False, 'Signed_Error'
    
    return True, None
