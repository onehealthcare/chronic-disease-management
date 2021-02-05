import logging
import os

from config import LOG_PATH


def syslogger_handler(path, loglevel=logging.INFO):
    formatter = logging.Formatter('{} %(levelname)s %(message)s'.format(path))
    if not os.path.exists(os.path.join(LOG_PATH, path)):
        os.makedirs(os.path.join(LOG_PATH, path))
    handler = logging.FileHandler(filename=os.path.join(LOG_PATH, path, 'log'))
    handler.setFormatter(formatter)
    handler.setLevel(loglevel)
    return handler


def logger(logname, loglevel=logging.INFO, path=None):
    logger = logging.getLogger(logname)

    for handler in logger.handlers:
        if isinstance(handler, logging.FileHandler):
            return logger

    if not path:
        path = logname.strip(' /').replace('.', '/')

    handler = syslogger_handler(path, loglevel)
    logger.addHandler(handler)

    logger.setLevel(loglevel)
    logger.propagate = False

    return logger
