import asyncio

#common rule func def rule_func(config, params, context):

def and_rule(config, params, context):
    rule_func_array = config.get('rules', None)
    if rule_func_array is None or len(rule_func_array) == 0:
        return True, None
    for rule_func in rule_func_array:
        result, err = rule_func(params, context)
        if err is not None:
            return False, err
    return True, None

def or_rule(config, params, context):
    rule_func_array = config.get('rules', None)
    if rule_func_array is None or len(rule_func_array) == 0:
        return True, None
    
    err = None
    for rule_func in rule_func_array:
        result, err = rule_func(params, context)
        if err is None:
            return True, None
    return False, err