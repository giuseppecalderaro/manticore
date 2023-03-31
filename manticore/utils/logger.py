from typing import Optional
import sys
import logging
from loguru import logger


class InterceptHandler(logging.Handler):
    loglevel_mapping = {
        50: 'CRITICAL',
        40: 'ERROR',
        30: 'WARNING',
        20: 'INFO',
        10: 'DEBUG',
        0: 'NOTSET',
    }

    def emit(self, record):
        try:
            level = logger.level(record.levelname).name
        except AttributeError:
            level = self.loglevel_mapping[record.levelno]

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        log = logger.bind()
        log.opt(depth=depth, exception=record.exc_info).log(level, record.getMessage())


class Logger:
    @staticmethod
    def make_logger(file_name: Optional[str], log_level: str):
        logger.remove()
        logger.add(
            file_name if file_name else sys.stdout,
            enqueue=True,
            backtrace=True,
            level=log_level.upper(),
            format="<level>{level: <8}</level> <green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> - <cyan>{name}</cyan>:<cyan>{function}</cyan> - <level>{message}</level>"
        )

        # Setup root logger
        logging.basicConfig(handlers=[InterceptHandler()], level=0)

        # Setup uvicorn and fastapi
        for _log in ['uvicorn', 'uvicorn.access', 'fastapi']:
            _logger = logging.getLogger(_log)
            _logger.handlers = [InterceptHandler()]

        return logger.bind(request_id=None, method=None)

    @staticmethod
    def critical(message: str) -> None:
        logging.critical(message)

    @staticmethod
    def error(message: str) -> None:
        logging.error(message)

    @staticmethod
    def warning(message: str) -> None:
        logging.warning(message)

    @staticmethod
    def info(message: str) -> None:
        logging.info(message)

    @staticmethod
    def debug(message: str) -> None:
        logging.debug(message)
