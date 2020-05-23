"""Logging configuration"""

import logging as logger
from os import path as os_path

def configure(filepath):
    """Configures the Python logging using a dictionary from a json file and adding a default
    fallback configuration with the basics

    Args:
        filename: Path of the file which contains the configuration
        (See https://docs.python.org/2/library/logging.config.html#logging-config-api)
    """

    import json
    from logging.config import dictConfig
    try:
        configure_by_file(filepath)
    except Exception as err:
        logger.error(f"Couldn't configure logger: {format(err)}")
        configure_by_default(logger.INFO)

def configure_by_default(loglevel):
    """ Configures a root logger using a default configuration

    Args:
        logging.level used by default
    """
    log = logger.getLogger()
    log.setLevel(loglevel)
    log.addHandler(logger.StreamHandler())
    log.info("Default configuration loaded succesfully.")

def configure_by_file(filepath):
    """Configures the Python logging using a dictionary from a json file

    Args:
        filename: Path of the file which contains the configuration
        (See https://docs.python.org/2/library/logging.config.html#logging-config-api)

    Raises:
        FileNotFoundError: If filepath doesn't exist.
        OSError: If filepath cannot be opened.
        AttributeError: If json config file content is not well-formed
    """
    import json
    from logging.config import dictConfig

    with open(filepath, "r") as configFile:
        config = json.load(configFile)
        dictConfig(config["logging"])


if __name__ == "__main__":
    import core.log_setup
    configure("./core/logging-config.json")
