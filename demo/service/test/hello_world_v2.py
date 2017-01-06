import router

class HelloWorldV2(router.ServiceHandler):
   async def process(self, args, context):
        return 'Hello world V2 from ApiHandler', None


router.register_service_handler('/api/hello/v2', HelloWorldV2())