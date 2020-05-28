"""Downloads the last version of WordPress core files"""

from core.app import App
import requests
import logging
from devops.constants import Urls

app: App = App()


def main():
    logging.info("Getting WordPress core files")


if __name__ == "__main__":
    main()
