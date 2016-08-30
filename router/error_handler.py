import tornado.ioloop
import tornado.web
import tornado.httpserver


class ErrorHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_status(400)
        self.set_header('HTTP_X_FIVEMILES_CODE', 'INVALID_REQUEST')

    def post(self):
        self.set_status(400)
        self.set_header('HTTP_X_FIVEMILES_CODE', 'INVALID_REQUEST')