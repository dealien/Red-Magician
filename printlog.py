import sys
from cogs.utils.settings import Settings
import logging

settings = Settings()


class PrintLog:
    def __init__(self, f):
        self.log = logging.getLogger(f)
        self.red_format = logging.Formatter(
            '%(asctime)s %(levelname)s %(module)s %(funcName)s %(lineno)d: '
            '%(message)s',
            datefmt="[%d/%m/%Y %H:%M]")
        self.stdout_handler = logging.StreamHandler(sys.stdout)
        self.stdout_handler.setFormatter(self.red_format)

        if settings.debug:
            self.log.setLevel(logging.DEBUG)
        else:
            self.log.setLevel(logging.INFO)
        self.fhandler = logging.handlers.RotatingFileHandler(
            filename='data/red/red.log', encoding='utf-8', mode='a',
            maxBytes=10 ** 7, backupCount=5)
        self.log.addHandler(self.fhandler)
        self.log.addHandler(self.stdout_handler)

    def info(self, msg):
        print(msg)
        self.log.info(msg)

    def debug(self, msg):
        print(msg)
        self.log.debug(msg)

    def error(self, msg):
        print(msg)
        self.log.error(msg)

    def critical(self, msg):
        print(msg)
        self.log.critical(msg)

    def exception(self, msg):
        print(msg)
        self.log.exception(msg)
