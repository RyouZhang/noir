import logging


class LogLevelFilter(logging.Filter):

    def __init__(self, min_level=None, max_level=None):
        self.min_level = min_level
        self.max_level = max_level
        logging.Filter.__init__(self)


    def filter(self, record):
        if self.min_level is not None and record.levelno < self.min_level:
            return False
        if self.max_level is not None and record.levelno > self.max_level:
            return False
        return True
