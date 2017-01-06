import os
import logging.config

log_levels = None

class LogLevelAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        return msg, kwargs 

    def isEnabledFor(self, lvl):
        if log_levels is None or len(log_levels) == 0:
            return lvl >= self.getEffectiveLevel()
        
        if any(lv == logging.getLevelName(lvl) for lv in log_levels):
            return True
        return False


logger = LogLevelAdapter(logging.getLogger(), None)


def setLoggerConfig(config):
    logging.config.dictConfig(config)


def setLoggerEffectLevels(levels):
    if type(levels) is list:
        log_levels = levels
    elif type(levels) is str:
        log_levels = levels.upper().split(',')


def getLogger():
    return logger