import os

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "")
LOG_FORMAT = os.getenv("LOG_FORMAT", '%(asctime)s,%(levelname)-5s %(filename)s:%(funcName)s:%(lineno)-5d %(message)s')
