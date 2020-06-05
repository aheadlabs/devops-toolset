"""Logging Formatter to add colors to log records using Colorama """
import logging
from colorama import Fore, Back, Style


class ColorFormatter(logging.Formatter):
    """Logging Formatter to add colors to log records """

    def __init__(self, format_str):
        """ Initializes the color formatter with color data and takes the format string as parameter"""
        grey = Fore.WHITE
        yellow = Fore.YELLOW
        red = Fore.RED
        bold_red = Fore.LIGHTRED_EX
        reset = Style.RESET_ALL
        format_str = format_str

        self.FORMATS = {
            logging.DEBUG: grey + format_str + reset,
            logging.INFO: grey + format_str + reset,
            logging.WARNING: yellow + format_str + reset,
            logging.ERROR: red + format_str + reset,
            logging.CRITICAL: Fore.LIGHTWHITE_EX + Back.RED + format_str + reset
        }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)
