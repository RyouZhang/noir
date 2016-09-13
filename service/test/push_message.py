import json
import router

import pika.adapters
import util.rabbitmq

class PushMessage(router.ApiHandler):
    async def process(self, args, context):
        publisher = await util.rabbitmq.rabbitMQPool.get_publisher(
                'amqp://192.168.1.19:5672/')

        msg = dict(
            api = '/api/stock/info/v1',
            args = json.dumps(dict(symbol='MSFT'))
        )
        publisher.publish_message(
            body = json.dumps(msg),
            exchange = 'message',
            routing_key = 'example.text.3')
        return 'Hello world from PushMessage', None
        
router.register_api_handler('/api/push/message/v1', PushMessage())