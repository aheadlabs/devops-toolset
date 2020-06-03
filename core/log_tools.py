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
    """Logs a list using the specified level.

    Args:
        logs_list: List of strings to be logged.
        level: Logging level.
    """
    if logs_list:
        for log in logs_list:
            logging.log(level.value[0], log)


def log_stdouterr(output: bytes, level: LogLevel):
    """Logs stdout or stderr outputs.

    It splits lines using the universal line ending and decodes content to
    UTF-8.

    Args:
        output: stdout or stderr output to be logged.
        level: Logging level.
    """

    for line in output.splitlines():
        logging.log(level.value[0], line.decode("utf-8"))
