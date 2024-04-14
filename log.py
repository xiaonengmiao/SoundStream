import gzip
import logging
import logging.handlers
import os
import shutil
import sys
from typing import Optional

LOGGING_FMT = "%(asctime)s|%(name)s|%(levelname)s|%(message)s"
LOGGING_DATE_FMT = "%Y-%m-%dT%H:%H:%S"
LOG_FILENAME_PREFIX = "SoundStream"
LOG_ROTATION_INTERVAL = "D" # S/M/H/D

if not os.path.exists("./result/log"):
    os.makedirs("./result/log")


class ColoredFormatter(logging.Formatter):
    """
    Logging colored formatter.

    adapted from https://stackoverflow.com/a/56944256/3638629
    """

    grey = '\x1b[38;21m'
    blue = '\x1b[38;5;39m'
    yellow = '\x1b[38;5;226m'
    orange = '\x1b[38;5;166m'
    red = '\x1b[38;5;196m'
    bold_red = '\x1b[31;1m'
    reset = '\x1b[0m'

    def __init__(self, fmt: str, datefmt: Optional[str] = None) -> None:
        """Set color scheme."""
        super().__init__(fmt, datefmt)
        self.fmt = fmt
        self.FORMATS = {
            logging.DEBUG: self.grey + self.fmt + self.reset,
            logging.INFO: self.blue + self.fmt + self.reset,
            logging.WARNING: self.orange + self.fmt + self.reset,
            logging.ERROR: self.red + self.fmt + self.reset,
            logging.CRITICAL: self.bold_red + self.fmt + self.reset
        }

    def format(self, record: logging.LogRecord) -> str:
        """Format a log record."""
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt=self.datefmt)
        return formatter.format(record)


def rotator(source, dest):
    """Compress the source when rotating."""
    with open(source, 'rb') as f_in:
        with gzip.open(dest, 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)
    os.remove(source)


def init_log(log_name: str, log_level: int):
    """Instantiate logger."""
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    fh = logging.handlers.TimedRotatingFileHandler(
        f"result/log/{LOG_FILENAME_PREFIX}.log",
        when=LOG_ROTATION_INTERVAL, encoding="utf-8")
    fh.rotator = rotator  # compress the last log file on rotation
    fh.namer = lambda name: name + ".gz"
    fh.setLevel(log_level)
    fh.setFormatter(logging.Formatter(LOGGING_FMT, datefmt=LOGGING_DATE_FMT))

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(log_level)
    ch.setFormatter(ColoredFormatter(LOGGING_FMT, datefmt=LOGGING_DATE_FMT))

    root_logger.addHandler(fh)
    root_logger.addHandler(ch)
