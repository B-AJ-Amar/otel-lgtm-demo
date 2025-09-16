import loguru
from loguru import logger
import logging

import sys

logger.remove()

class InterceptHandler(logging.Handler):
    def emit(self, record):
        logging.getLogger(record.name).handle(record)

logger.add(sys.stdout, level="DEBUG", colorize=True)

logger.add(InterceptHandler(), level="DEBUG")
