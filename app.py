import os
import asyncio

import tornado.ioloop
import tornado.web
import tornado.httpserver

import router

tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
asyncio.get_event_loop = lambda : tornado.ioloop.IOLoop.current().asyncio_loop

class FMApplication(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/api/.+", router.BaseHandler),
        ]

        settings = dict(
            default_handler_class = router.ErrorHandler,
            compress_response = True
        )

        super(FMApplication, self).__init__(handlers, **settings)

if __name__ == "__main__":
    port = int(os.getenv('SERVER_PORT', 8888))

    server = tornado.httpserver.HTTPServer(FMApplication())
    server.bind(port)
    server.start(1)

    import api
    tornado.ioloop.IOLoop.current().start()