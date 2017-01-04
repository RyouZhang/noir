import router
import util



class HealthCheck(router.ApiHandler):
    async def process(self, args, context):
        util.logger.info("haha")

        return 'Health Check from HealthCheck!', None

router.register_api_handler('/api/health_check', HealthCheck())
