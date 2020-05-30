"""Tools for managing the gettext API

If called with no arguments it compiles .po files to .mo format using Linux gettext

Args:
    --py: If present it will use Python pygettext.py and msgfmt.py instead of Linux's
    --generate-pot: If present it generates the .pot file
    --compile: If present it compiles .po files to .mo format
"""

from typing import List
import argparse
import os
import subprocess
import pathlib
import core.app
import logging

parser = argparse.ArgumentParser()
parser.add_argument("--py", action="store_true")
parser.add_argument("--generate-pot", action="store_true")
parser.add_argument("--compile", action="store_true")
parser.add_argument("--skip-i18n", action="store_true")
args, args_unknown = parser.parse_known_args()

app: core.app.App = core.app.App(args.skip_i18n)

if not pathlib.Path(app.settings.locales_path).is_dir():
    raise ValueError("locale_path parameter must be a directory. Check app settings.")


def get_files(starting_path: str, glob: str) -> List[pathlib.Path]:
    """Gets a list with the paths to the descendant files that match the glob pattern.

    Args:
        starting_path: Path to start the seek from.
        glob: glob pattern to match the files that should be found.

    Returns:
        List with the paths to the files that match.
    """

    return list(pathlib.Path(starting_path).rglob(glob))


def generate_pot_file():
    """Generates the .pot file from the strings found in the code"""

    pot_file = pathlib.Path.joinpath(app.settings.locales_path, "base.pot")

    if pathlib.Path(pot_file).exists():
        os.remove(str(pot_file))

    files = get_files(str(app.settings.root_path), "**/*.py")

    script = "pygettext.py" if args.py else "xgettext"
    command = f"{script} -d base -o {str(pot_file)} {' '.join(map(str, files))}"

    call_subprocess(command)


def compile_po_files():
    """Compiles .po files to .mo files"""

    paths = get_files(str(app.settings.locales_path), "**/*.po")

    for file in paths:
        po_file = pathlib.Path(file)
        mo_file = po_file.with_suffix(".mo")

        if pathlib.Path(mo_file).exists():
            os.remove(mo_file)

        py = ".py" if args.py else ""
        command = f"msgfmt{py} -o {mo_file} {file}"

        call_subprocess(command)


def merge_pot_file():
    """Merges a .pot file with existing .po files"""
    # TODO(ivansainz) Implement me! Hint: PoLib
    # msgmerge
    # https://www.gnu.org/software/gettext/manual/html_node/msgmerge-Invocation.html#msgmerge-Invocation
    pass


def call_subprocess(command: str):
    """Calls a subprocess"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    if out:
        logging.info(out)
    if err:
        logging.error(err)


if __name__ == "__main__":
    if args.generate_pot:
        generate_pot_file()
    if args.compile:
        compile_po_files()
