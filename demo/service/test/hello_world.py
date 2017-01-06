import nori.router as router
import nori.rule as rule
import functools

class HelloWorld(router.ServiceHandler):
    async def process(self, args, context):
        return 'Hello world from HelloWorld', None

router.register_service_handler(
    '/api/hello/v1', 
    HelloWorld(), 
    rule_func=functools.partial(rule.check_params_rule, [('name', str, lambda name: name == 'hello')]))