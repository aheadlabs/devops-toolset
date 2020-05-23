import sys
import os
import subprocess
import pathlib
from filesystem.paths import get_filepaths_in_tree

python_path = pathlib.Path(sys.executable).parent
i18n_path = pathlib.Path.joinpath(python_path, "Tools/i18n")
pygettext = pathlib.Path.joinpath(i18n_path, "pygettext.py")
msgfmt = pathlib.Path.joinpath(i18n_path, "msgfmt.py")

def compile_po_files(locale_path: str = "locales"):
    """Compiles .po files to .mo files"""
    # TODO Tests pending
    
    paths = get_filepaths_in_tree(os.path.dirname(os.path.realpath(__file__)), "**/*.po")

    for file in paths:
        po_file = pathlib.Path(file)
        mo_file = po_file.with_suffix(".mo")
        
        if pathlib.Path(mo_file).exists():
            os.remove(mo_file)

        output = mo_file

        process = subprocess.Popen(f"{msgfmt} -o {output} {file}", shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        for line in process.stdout.readlines():
            print(line.strip())
        for line in process.stderr.readlines():
            print(line.decode("utf-8").strip())


def create_pot_file(locale_path: str = "locales"):
    """# pygettext.py -d base -o D:\Source\_aheadlabs\devops-toolset\locales\base.pot D:\Source\_aheadlabs\devops-toolset\tools\git.py"""
    pass


if __name__ == "__main__":
    compile_po_files()

# TODO Add arguments to condition execution
