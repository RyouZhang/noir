import router
import rule
import functools

class HelloWorld(router.ServiceHandler):
    async def process(self, args, context):
        print('asdsadasdasdasd')
        return 'Hello world from ApiHandler', None

router.register_service_handler(
    '/api/hello/v1', 
    HelloWorld(), 
    rule_func=functools.partial(rule.check_params_rule, [('name', str, lambda name: name == 'hello')]))