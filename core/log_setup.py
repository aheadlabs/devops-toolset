"""Logging configuration"""

import logging as logger
import core.app

app: core.app.App = core.app.App()


def configure(filepath):
    """Configures the Python logging using a dictionary from a json file and adding a default
    fallback configuration with the basics

    Args:
        filepath: Path of the file which contains the configuration
        (See https://docs.python.org/2/library/logging.config.html#logging-config-api)
    """

    try:
        configure_by_file(filepath)
    except Exception as err:
        logger.error(f"Cannot configure logger: {format(err)}")
        configure_by_default(logger.INFO)


def configure_by_default(loglevel):
    """ Configures a root logger using a default configuration

    Args:
        logging.level used by default
    """
    log = logger.getLogger()
    log.setLevel(loglevel)
    log.addHandler(logger.StreamHandler())
    log.info("Default configuration loaded successfully.")


def configure_by_file(filepath):
    """Configures the Python logging using a dictionary from a json file

    Args:
        filepath: Path of the file which contains the configuration
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
    configure(app.settings.log_config_file_path)
