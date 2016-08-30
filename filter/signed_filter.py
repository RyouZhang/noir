import math

import util

def signed_access_filter(timestamp, sign, args, context):
    print(timestamp, util.get_timestamp())
    if timestamp is None or math.fabs(timestamp - util.get_timestamp()) > 300000:
        return False, 'Invalid_Timestamp'
    
    if sign is None:
        return False, 'Signed_Error'
    
    return True, None