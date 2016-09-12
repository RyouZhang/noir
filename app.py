import os
import asyncio

import tornado.ioloop
import tornado.web
import tornado.httpserver

tornado.ioloop.IOLoop.configure('tornado.platform.asyncio.AsyncIOLoop')
asyncio.get_event_loop = lambda : tornado.ioloop.IOLoop.current().asyncio_loop

import router

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
    process_num = int(os.getenv('SERVER_PROCESS_NUM', os.cpu_count()))

    server = tornado.httpserver.HTTPServer(FMApplication())
    server.bind(port)
    server.start(process_num)

    import service

    tornado.ioloop.IOLoop.current().start()