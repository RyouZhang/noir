import router

import util.rabbitmq

class PushMessage(router.ApiHandler):
    async def process(self, args, context):
        rabbitmq = await util.rabbitmq.rabbitMQPool.get_pool(
                'amqp://192.168.1.19:5672/', 
                exchange_name = 'message',
                exchange_type = 'topic')
        rabbitmq.publish_message('Hello world from PushMessage', routing_key = 'example.text.3')
        return 'Hello world from PushMessage', None
        
router.register_api_handler('/api/push/message/v1', PushMessage())