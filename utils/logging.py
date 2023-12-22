import logging
import os
from logging.handlers import SysLogHandler

from config import LOG_PATH


def file_logger_handler(path, loglevel=logging.INFO):
    formatter = logging.Formatter(f'%(asctime)s {path} %(levelname)s %(message)s')
    if not os.path.exists(os.path.join(LOG_PATH, path)):
        os.makedirs(os.path.join(LOG_PATH, path))
    handler = logging.FileHandler(filename=os.path.join(LOG_PATH, path, 'log'))
    handler.setFormatter(formatter)
    handler.setLevel(loglevel)
    return handler


def syslogger_handler(path, loglevel=logging.INFO):
    formatter = logging.Formatter(f'{path} %(levelname)s %(message)s')
    if os.path.exists('/dev/log'):
        handler = SysLogHandler(address='/dev/log', facility=SysLogHandler.LOG_LOCAL0)
    else:
        handler = SysLogHandler(facility=SysLogHandler.LOG_LOCAL0)
    handler.setFormatter(formatter)
    handler.setLevel(loglevel)
    return handler


def file_logger(log_name, loglevel=logging.INFO, path=None):
    logger = logging.getLogger(log_name)

    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return logger

    if not path:
        path = log_name.strip(' /').replace('.', '/')

    handler = file_logger_handler(path, loglevel)
    logger.addHandler(handler)

    logger.setLevel(loglevel)
    logger.propagate = False

    return logger


def syslogger(log_name, loglevel=logging.INFO, path=None):
    logger = logging.getLogger(log_name)

    for handler in logger.handlers:
        if isinstance(handler, SysLogHandler):
            return logger

    if not path:
        path = log_name.strip(' /').replace('.', '/')

    handler = syslogger_handler(path, loglevel)
    logger.addHandler(handler)

    logger.setLevel(loglevel)
    logger.propagate = False

    return logger
