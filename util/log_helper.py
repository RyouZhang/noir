import os
import toml
import logging.config

logging_config_file = "logging.toml"

log_levels = None

log_level_str = os.getenv('LOG_LEVELS', None)
if log_level_str is not None:
    log_levels = log_level_str.upper().split(',')

class LogLevelAdapter(logging.LoggerAdapter):

    def process(self, msg, kwargs):
        return msg, kwargs 

    def isEnabledFor(self, lvl):
        if log_levels is None or len(log_levels) == 0:
            return lvl >= self.getEffectiveLevel()
        
        if any(lv == logging.getLevelName(lvl) for lv in log_levels):
            return True
        return False

with open(logging_config_file) as configfile:
    config = toml.loads(configfile.read())
    logging.config.dictConfig(config)

logger = LogLevelAdapter(logging.getLogger(), None)
