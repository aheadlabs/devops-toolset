"""Contains tools for logging"""

import logging
from enum import Enum
from typing import List


class LogLevel(Enum):
    """https://docs.python.org/3/library/logging.html#levels"""
    critical = 50,
    error = 40,
    warning = 30,
    info = 20,
    debug = 10


def log_list(logs_list: List[str], level: LogLevel):
    """Logs a list using the specified level"""
    if logs_list:
        for log in logs_list:
            logging.log(level.value[0], log)
