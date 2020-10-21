"""Utils for managing the gettext API

If called with no arguments it compiles .po files to .mo format using Linux gettext

Args:
    --py: If present it will use Python pygettext.py and msgfmt.py instead of Linux's
    --generate-pot: If present it generates the .pot file
    --compile: If present it compiles .po files to .mo format
    --merge: If present it merges the .pot file with the existing po files.
"""

# from core.LiteralsCore import LiteralsCore
# from i18n.Literals import Literals as I18nLiterals
from typing import List
import argparse
import core.app
import core.log_tools
# import logging
import os
import pathlib
import tools.cli as tools_cli

parser = argparse.ArgumentParser()
parser.add_argument("--py", action="store_true")
parser.add_argument("--generate-pot", action="store_true")
parser.add_argument("--compile", action="store_true")
parser.add_argument("--skip-i18n", action="store_true")
parser.add_argument("--merge", action="store_true")
args, args_unknown = parser.parse_known_args()

app: core.app.App = core.app.App(args.skip_i18n)
# literals = LiteralsCore([I18nLiterals])


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
    # logging.info(literals.get("i18n_pot_file_path").format(path=pot_file))

    if pathlib.Path(pot_file).exists():
        os.remove(str(pot_file))
        # logging.info(literals.get("i18n_pot_file_removed").format(path=pot_file))

    files = get_files(str(app.settings.root_path), "**/*.py")
    # core.log_tools.log_indented_list(literals.get("i18n_pot_file_list"), files, core.log_tools.LogLevel.info)

    script = "pygettext.py" if args.py else "xgettext"
    # logging.info(literals.get("i18n_pot_script").format(script=script))

    command = f"{script} -d base -o {str(pot_file)} {' '.join(map(str, files))}"
    # logging.info(literals.get("i18n_pot_command").format(command=command))

    tools_cli.call_subprocess(command)


def compile_po_files():
    """Compiles .po files to .mo files"""

    paths = get_files(str(app.settings.locales_path), "**/*.po")
    # core.log_tools.log_indented_list(literals.get("i18n_po_file_list"), paths, core.log_tools.LogLevel.info)

    for file in paths:
        po_file = pathlib.Path(file)
        mo_file = po_file.with_suffix(".mo")

        if pathlib.Path(mo_file).exists():
            os.remove(mo_file)
            # logging.info(literals.get("i18n_mo_file_removed").format(path=mo_file))

        py = ".py" if args.py else ""
        command = f"msgfmt{py} -o {mo_file} {file}"
        # logging.info(literals.get("i18n_po_command").format(command=command))

        tools_cli.call_subprocess(command)


def merge_pot_file():
    """Merges a .pot file with existing .po files
    # https://www.gnu.org/software/gettext/manual/html_node/msgmerge-Invocation.html#msgmerge-Invocation """

    paths = get_files(str(app.settings.locales_path), "**/*.po")
    pot_file = pathlib.Path.joinpath(app.settings.locales_path, "base.pot")

    if not pathlib.Path(pot_file).exists():
        generate_pot_file()

    for file in paths:
        po_file = pathlib.Path(file)
        command = f"msgmerge -U {po_file} {pot_file}"
        tools_cli.call_subprocess(command)


if __name__ == "__main__":
    if not pathlib.Path(app.settings.locales_path).is_dir():
        raise ValueError("locale_path parameter must be a directory. Check app settings.")
    if args.generate_pot:
        generate_pot_file()
    if args.compile:
        compile_po_files()
    if args.merge:
        merge_pot_file()
