import logging
import os
from logging.handlers import RotatingFileHandler

logger = logging.getLogger('chats')

logger_levels = {
    'debug': logging.DEBUG,
    'info': logging.INFO,
    'warn': logging.WARN,
    'error': logging.ERROR,
}
logger_level = logging.INFO

logger_level_key = os.getenv('LOGGER_LEVEL')
if logger_level_key is not None and logger_level_key in logger_levels:
    logger_level = logger_levels[logger_level_key]

logger.setLevel(logger_level)

console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler('chats.log', maxBytes=10000, backupCount=3)

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
console_handler.setFormatter(logging.Formatter(log_format))
file_handler.setFormatter(logging.Formatter(log_format))

logger.addHandler(console_handler)
logger.addHandler(file_handler)
