import pika
import sys

EXCHANGE = 'message'
EXCHANGE_TYPE = 'topic'
QUEUE = 'text_1'
ROUTING_KEY = 'example.text.%d'

connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='192.168.1.19'))
channel = connection.channel()

channel.exchange_declare(exchange=EXCHANGE,
                         type=EXCHANGE_TYPE)

message = ' '.join(sys.argv[2:]) or 'Hello World!'
for i in range(100):
    channel.basic_publish(exchange=EXCHANGE,
                        routing_key=ROUTING_KEY % (i%4),
                        body= '%s|%d' % (message, i))
print(" [x] Sent %r:%r" % (ROUTING_KEY, message))
connection.close()