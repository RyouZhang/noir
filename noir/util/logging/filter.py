import logging


class LogLevelFilter(logging.Filter):

    def __init__(self, min_level=None, max_level=None):
        self._min_level = min_level
        self._max_level = max_level
        logging.Filter.__init__(self)

    def filter(self, record):
        if self._min_level is not None and record.levelno < self._min_level:
            return False
        if self._max_level is not None and record.levelno > self._max_level:
            return False
        return True