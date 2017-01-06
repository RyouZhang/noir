import noir.router as router
import noir.rule as rule

class HelloWorldV2(router.ServiceHandler):
   async def process(self, args, context):
        return 'Hello world V2 from HelloWorldV2', None


router.register_service_handler('/api/hello/v2', HelloWorldV2())