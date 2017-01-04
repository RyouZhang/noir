import router
import rule
import functools

class HelloWorld(router.SericeHandler):
    async def process(self, args, context):
        return 'Hello world from ApiHandler', None

router.register_api_handler(
    '/api/hello/v1', 
    HelloWorld(), 
    rule_func = functools.partial(rule.api_signed_rule, None))