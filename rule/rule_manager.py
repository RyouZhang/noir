import asyncio

#common rule func def rule_func(config, params, context):

def register_api_rule(api, rule_funcs = None):
    if rule_funcs is None:
        return
    [ruleManager.register_api_rule(api, rule_func) for rule_func in rule_funcs]

class RuleManager:
    api_rule_dic = dict()

    def register_api_rule(self, api, rule_func):
        if rule_func is None:
            return
        rule_funcs = self.api_rule_dic.get(api, [])
        rule_funcs.append(rule_func)
        self.api_rule_dic[api] = rule_funcs
    
    async def check_api_rule(self, api, params, context):
        rule_funcs = self.api_rule_dic.get(api, [])
        for rule_func in rule_funcs:
            result, err = rule_func(params, context)
            if err is not None:
                return False, err
        return True, None

ruleManager = RuleManager()