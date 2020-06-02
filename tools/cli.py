"""Contains tools for working with the command line"""

import subprocess
import logging


def call_subprocess(command: str):
    """Calls a subprocess"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if out:
        logging.info(out)
    if err:
        logging.error(err)


class Commands(object):
    """Common command line commands :)"""

    # TODO(ivan.sainz) Do something like what is done in Literals and move this dict to /wordpress
    _wp_cli = {
        "wp_info": "wp --info"
    }


if __name__ == "__main__":
    help(__name__)
