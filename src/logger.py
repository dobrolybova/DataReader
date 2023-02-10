from logging import INFO, CRITICAL, getLogger, basicConfig


class Logger:
    def __init__(self):
        self.logger = getLogger(__name__)
        basicConfig(level=INFO)


logger = Logger().logger
