import router
import rule
import functools

class HelloWorld(router.ApiHandler):
    async def process(self, args, context):
        return 'Hello world from ApiHandler', None


rule.register_api_rule(
    '/api/hello/v1', 
    [functools.partial(rule.api_signed_rule, None)])
        
router.register_api_handler('/api/hello/v1', HelloWorld())