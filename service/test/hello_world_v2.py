import router

class HelloWorldV2(router.SericeHandler):
   async def process(self, args, context):
        return 'Hello world V2 from ApiHandler', None


router.register_api_handler('/api/hello/v2', HelloWorldV2())