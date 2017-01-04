import os
import json
import router

import pika.adapters
import util.rabbitmq

class PushMessage(router.ApiHandler):
    def __init__(self):
        self._ampq_url = os.getenv('AMPQ_URL', None)
        super(PushMessage, self).__init__()

    async def process(self, args, context):
        if self._ampq_url is None:
            return None, 'Invalid_AMPQ_URL'

        publisher = await util.rabbitmq.rabbitMQPool.get_publisher(
                self._ampq_url)

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