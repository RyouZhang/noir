import signal

import tornado
import tornado.httpserver
from tornado.web import Application, RequestHandler

import tornaduv
tornado.ioloop.IOLoop.configure('tornaduv.UVLoop')

# import asyncio
# tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')

def handle_signal(sig, frame):
    loop = tornado.ioloop.IOLoop.current()
    loop.add_callback(loop.stop)

class MainHandler(RequestHandler):
    def get(self):
        self.write("Hello, world")

application = Application([
    (r"/", MainHandler),
])


if __name__ == "__main__":
    signal.signal(signal.SIGINT, handle_signal)
    signal.signal(signal.SIGTERM, handle_signal)

    server = tornado.httpserver.HTTPServer(application)
    server.bind(8080)
    server.start(4)

    tornado.ioloop.IOLoop.current().start()