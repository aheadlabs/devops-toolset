"""Tools for managing the gettext API

If called with no arguments it compiles .po files to .mo format using Linux gettext

Args:
    --py: If present it will use Python pygettext.py and msgfmt.py instead of Linux's
    --generate-pot: If present it generates the .pot file
    --compile: If present it compiles .po files to .mo format
"""

import argparse
import os
import subprocess
import pathlib
import core.app
from filesystem.paths import get_file_paths_in_tree

parser = argparse.ArgumentParser()
parser.add_argument("--py", action="store_true")
parser.add_argument("--generate-pot", action="store_true")
parser.add_argument("--compile", action="store_true")
args, args_unknown = parser.parse_known_args()

app: core.app.App = core.app.App()

if not pathlib.Path(app.settings.locales_path).is_dir():
    raise ValueError("locale_path parameter must be a directory. Check app settings.")


# TODO(ivan.sainz) Tests pending
def compile_po_files():
    """Compiles .po files to .mo files"""

    paths = get_file_paths_in_tree(str(app.settings.locales_path), "**/*.po")

    for file in paths:
        po_file = pathlib.Path(file)
        mo_file = po_file.with_suffix(".mo")

        if pathlib.Path(mo_file).exists():
            os.remove(mo_file)

        py = ".py" if args.py else ""
        command = f"msgfmt{py} -o {mo_file} {file}"

        call_subprocess(command)


def generate_pot_file():
    """Generates the .pot file from the strings found in the code"""

    pot_file = pathlib.Path.joinpath(app.settings.locales_path, "base.pot")

    if pathlib.Path(pot_file).exists():
        os.remove(str(pot_file))

    files = get_file_paths_in_tree(str(app.settings.root_path), "**/*.py")

    script = "pygettext.py" if args.py else "xgettext"
    command = f"{script} -d base -o {str(pot_file)} {' '.join(map(str, files))}"

    call_subprocess(command)


def merge_pot_file():
    """Merges a .pot file with existing .po files"""

    # msgmerge
    # https://www.gnu.org/software/gettext/manual/html_node/msgmerge-Invocation.html#msgmerge-Invocation
    pass


def call_subprocess(command: str):
    """Calls a subprocess"""
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    for line in process.stdout.readlines():
        print(line.strip())
    for line in process.stderr.readlines():
        print(line.decode("utf-8").strip())


if __name__ == "__main__":
    if args.generate_pot:
        generate_pot_file()
    if args.compile:
        compile_po_files()
