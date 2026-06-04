

async def check_params_rule(conf, args, context):
    for (key, v_type, v_range_func) in conf:
        value = args.get(key, None)
        if value is None or isinstance(value, v_type) is False:
            return False, 'Invalid_Params %s(%s)=%s' % (key, v_type, value)
        
        if v_range_func is not None and not v_range_func(value):
            return False, 'Invalid_Params %s(%s)=%s' % (key, v_type, value)
    return True, None


async def check_option_params_rule(conf, args, context):
    for (key, v_type, def_value) in conf:
        value = args.get(key, None)
        if value is not None and isinstance(value, v_type) is False:
            return False, 'Invalid_Params %s(%s)' % (key, v_type)
        if value is None and def_value is not None:
            args[key] = def_value
    return True, None 

# print(check_option_params_rule([('a', int, 0), ('b', str, None)], {"b":"ads"}, dict()))
