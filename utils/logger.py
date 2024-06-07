import logging
import logging.handlers
import multiprocessing
import os
import sys
import threading
from datetime import datetime

from dotenv import load_dotenv

load_dotenv()

log_level = {
    "DEBUG": logging.DEBUG,
    "INFO": logging.INFO,
    "WARNING": logging.WARNING,
    "ERROR": logging.ERROR,
    "CRITICAL": logging.CRITICAL,
    "FATAL": logging.FATAL,
    "NOTSET": logging.NOTSET
}


class Logger:
    __default_log_level = "DEBUG"
    __default_log_format = "%(levelname)s [%(asctime)s] %(process)d/%(thread)d %(folder_name)s %(filename)s %(funcName)s : %(message)s"
    __default_log_date_format = "%m/%d/%Y %I:%M:%S %p"

    __log_level = __default_log_level
    __format = __default_log_format
    __date_format = __default_log_date_format

    __filename = None
    __config = None
    __log_to_console = False

    __home_path = os.getenv("HOME_PATH", ".")

    def __init__(self, filename=None, config=None, log_to_console=False):
        self.__filename = filename
        self.__config = config
        self.__log_to_console = log_to_console

        if self.__config is not None:
            self.__log_level = self.__config.get("log_level", self.__default_log_level)
            self.__format = self.__config.get("format", self.__default_log_format)
            self.__date_format = self.__config.get("date_format", self.__default_log_date_format)

    def get_logger(self, is_multiprocess=False, folder_name=None):
        current_date = datetime.now().strftime("%Y-%m-%d")
        now = datetime.now()
        month_name = now.strftime("%B")
        log_path = os.path.join(self.__home_path, "logs", str(now.year), month_name, str(now.day))
        # log_path = os.path.join(self.__home_path, "logs", current_date)
        logging.basicConfig(level=log_level.get(self.__log_level))

        if self.__log_to_console:
            if is_multiprocess:
                logger = logging.getLogger(__name__)
                log_handler = logging.StreamHandler(stream=sys.stdout)
                log_handler.setFormatter(logging.Formatter(fmt=self.__format, datefmt=self.__date_format))
                logger.propagate = 0
                logger.addHandler(log_handler)
            else:
                logger = logging.getLogger(__name__)
                stream_handlers_list = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
                if not len(stream_handlers_list):
                    log_handler = logging.StreamHandler(stream=sys.stdout)
                    log_handler.setFormatter(logging.Formatter(fmt=self.__format, datefmt=self.__date_format))
                    logger.propagate = 0
                    logger.addHandler(log_handler)
        else:
            logger = logging.getLogger(self.__filename)
            stream_handler_list = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
            if not len(stream_handler_list):
                if not os.path.exists(log_path):
                    os.makedirs(log_path)
                if is_multiprocess:
                    log_handler = MultiProcessingLogHandler(filename=os.path.join(log_path, f"{self.__filename}.log"), when="midnight")
                else:
                    log_handler = logging.handlers.TimedRotatingFileHandler(filename=os.path.join(log_path, f'{self.__filename}.log'),
                                                                            when="midnight")
                log_handler.setFormatter(logging.Formatter(self.__format, datefmt=self.__date_format))
                logger.propagate = 0
                logger.addHandler(log_handler)
        logger = logging.LoggerAdapter(logger, extra={"folder_name": folder_name})
        return logger


class MultiProcessingLogHandler(logging.Handler):
    def __init__(self, filename, when="midnight"):
        logging.Handler.__init__(self)
        self._handler = logging.handlers.TimedRotatingFileHandler(filename=filename, when=when)
        self.queue = multiprocessing.Queue(-1)
        threading.Thread(target=self.receive)

    def setFormatter(self, fmt):
        logging.Handler.setFormatter(self, fmt)
        self._handler.setFormatter(fmt)

    def receive(self):
        """this function checks the queue and sends logging output to stream(file like object in this case)
        """
        while True:
            try:
                record = self.queue.get()
                self._handler.emit(record)
            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception:
                break

    def send(self, s):
        self.queue.put_nowait(s)

    def _format_record(self, record):
        """format message before writing in file."""
        if record.args:
            record.msg = record.msg % record.args
            record.args = None
        if record.exc_info:
            self.format(record)
            record.exc_info = None
        return record

    def emit(self, record):
        try:
            s = self._format_record(record)
            self.send(s)
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)

    def close(self):
        self._handler.close()
        logging.Handler.close(self)