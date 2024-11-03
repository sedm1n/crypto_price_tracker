import logging


class InfoLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname == 'INFO'

class ErrorLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelno < logging.ERROR
    
class DebugWarningLogFilter(logging.Filter):
    def filter(self, record):
        return record.levelname in ('DEBUG', 'WARNING')