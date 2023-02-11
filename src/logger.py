from logging import getLogger, basicConfig
from config import LOG_LEVEL, LOG_FILE, LOG_FORMAT


class Logger:
    def __init__(self):
        self.logger = getLogger(__name__)
        basicConfig(filename=LOG_FILE, filemode='w', level=LOG_LEVEL, format=LOG_FORMAT)


logger = Logger().logger
