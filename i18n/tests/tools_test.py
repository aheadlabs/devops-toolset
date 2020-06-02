"""Unit tests for the tools file"""
import unittest.mock as mock
import i18n.tools as sut
import argparse
import pathlib
import os
import subprocess
import logging


# region get_files()


@mock.patch.object(pathlib.Path, "rglob")
def test_get_files_given_starting_path_and_glob_should_return_list_pathlib_rglob(rglob_mock, filenames):
    """ Given a starting_path and a glob, should call pathlib.rglob with arguments and return a list"""
    # Arrange
    starting_path = filenames.path
    test_glob = "*.*"
    expected_result = filenames.paths
    rglob_mock.return_value = expected_result
    # Act
    result = sut.get_files(starting_path, test_glob)
    # Assert
    assert expected_result == result


# endregion get_files()

# region compile_po_files()


@mock.patch.object(sut, "call_subprocess")
def test_compile_po_files_given_path_then_calls_get_files(filenames):
    """Given a locale path, it should call get_file_paths_in_tree() to get the
    paths"""

    # Arrange
    with mock.patch.object(sut, "get_files") as file_paths:
        file_paths.return_value = filenames.paths

    # Act
        sut.compile_po_files()

    # Assert
    file_paths.assert_called()


@mock.patch.object(sut, "call_subprocess")
def test_compile_po_files_given_path_when_args_contain_py_then_calls_subprocess_with_dot_py(subprocess_mock):
    """ Given a locale path, when args contain the py arg, then compounds the command
        with msgfmt.py and files and calls it """

    # Arrange
    expected_files = ["foo1.po"]
    expected_command = "msgfmt.py -o foo1.mo foo1.po"

    with mock.patch.object(sut, "args") as sut_args_mock:
        sut_args_mock.return_value = argparse.Namespace(py=True)
        with mock.patch.object(sut, "get_files") as file_paths:
            file_paths.return_value = expected_files

            # Act
            sut.compile_po_files()

    # Assert
    subprocess_mock.assert_called_once_with(expected_command)


@mock.patch.object(sut, "call_subprocess")
def test_compile_po_files_given_path_when_args_not_contain_py_then_calls_subprocess_without_dot_py(subprocess_mock):
    """ Given a locale path, when args contain the py arg, then compounds the command
        with msgfmt and po/mo files and calls it """

    # Arrange
    expected_files = ["foo2.po"]
    expected_command = "msgfmt -o foo2.mo foo2.po"

    with mock.patch.object(sut, "get_files") as file_paths:
        file_paths.return_value = expected_files

        # Act
        sut.compile_po_files()

    # Assert
    subprocess_mock.assert_called_once_with(expected_command)


@mock.patch.object(os, "remove")
def test_compile_po_files_given_path_when_mo_file_exist_then_calls_os_remove(os_remove_mock):
    """ Given a locale path, when a mo file already exists, should remove it first """

    # Arrange
    expected_files = ["foo3.po"]
    expected_mo_deleted_file = "foo3.mo"

    with mock.patch.object(sut, "call_subprocess"):
        with mock.patch.object(sut, "get_files") as file_paths:
            file_paths.return_value = expected_files
            with mock.patch.object(pathlib.Path, "exists") as path_exists_mock:
                path_exists_mock.return_value = True

                # Act
                sut.compile_po_files()

                # Assert
                os_remove_mock.assert_called_once_with(pathlib.PurePath(expected_mo_deleted_file))

# endregion

# region generate_po_files()


@mock.patch.object(sut, "call_subprocess")
def test_generate_pot_file_given_path_then_calls_get_files(filenames):
    """Given a locale path, it should call get_file_paths_in_tree() to get the
    paths"""

    # Arrange
    with mock.patch.object(sut, "get_files") as file_paths:
        file_paths.return_value = filenames.paths

    # Act
        sut.generate_pot_file()

    # Assert
    file_paths.assert_called()


@mock.patch.object(sut, "call_subprocess")
def test_generate_pot_file_given_path_when_args_contain_py_then_calls_popen_with_pygettext(subprocess_mock, filenames):
    """ Given a pot file path, when args contain the py arg, then compounds the command
        with pygettext.py and all py files and calls it """
    # Arrange
    expected_pot_file = "foo1.pot"
    expected_path_list = [pathlib.PurePath(filenames.test_file), pathlib.PurePath(filenames.test_file)]
    expected_command = f"pygettext.py -d base -o {expected_pot_file} {' '.join(map(str, expected_path_list))}"

    with mock.patch.object(sut, "args") as sut_args_mock:
        sut_args_mock.return_value = argparse.Namespace(py=True)
        with mock.patch.object(sut, "get_files") as file_paths:
            file_paths.return_value = expected_path_list
            with mock.patch.object(pathlib.Path, "joinpath") as joinpath_mock:
                joinpath_mock.return_value = pathlib.PurePath(expected_pot_file)

                # Act
                sut.generate_pot_file()

    # Assert
    subprocess_mock.assert_called_once_with(expected_command)


@mock.patch.object(sut, "call_subprocess")
def test_generate_pot_file_given_path_when_args_not_py_then_calls_popen_with_xgettext(subprocess_mock, filenames):
    """ Given a locale path, when args not contain the py arg, then iterates on files and compounds the command
        with xgettext and all py files and calls it """

    # Arrange
    expected_pot_file = "foo1.pot"
    expected_path_list = [pathlib.PurePath(filenames.test_file), pathlib.PurePath(filenames.test_file2)]
    expected_command = f"xgettext -d base -o {expected_pot_file} {' '.join(map(str, expected_path_list))}"

    with mock.patch.object(sut, "get_files") as file_paths:
        file_paths.return_value = expected_path_list
        with mock.patch.object(pathlib.Path, "joinpath") as joinpath_mock:
            joinpath_mock.return_value = pathlib.PurePath(expected_pot_file)

            # Act
            sut.generate_pot_file()

    # Assert
    subprocess_mock.assert_called_once_with(expected_command)


@mock.patch.object(os, "remove")
def test_generate_pot_files_given_path_when_mo_file_exist_then_calls_os_remove(os_remove_mock, filenames):
    """ Given a locale path, when a pot file already exists, should remove it first """

    # Arrange
    expected_pot_deleted_file = "foo.pot"
    expected_path_list = [pathlib.PurePath(filenames.test_file), pathlib.PurePath(filenames.test_file2)]

    with mock.patch.object(sut, "call_subprocess"):
        with mock.patch.object(pathlib.Path, "joinpath") as joinpath_mock:
            joinpath_mock.return_value = pathlib.PurePath(expected_pot_deleted_file)
            with mock.patch.object(sut, "get_files") as file_paths:
                file_paths.return_value = expected_path_list
                with mock.patch.object(pathlib.Path, "exists") as path_exists_mock:
                    path_exists_mock.return_value = True

                    # Act
                    sut.generate_pot_file()

    # Assert
    os_remove_mock.assert_called_once_with(expected_pot_deleted_file)


# endregion

# region call_subprocess(str)

@mock.patch.object(subprocess, "Popen")
def test_call_subprocess_given_command_srt_then_calls_popens_with_command(subprocess_mock):
    """ Given an str command, then calls subprocess. Popen with that command"""

    # Arrange
    foo_command = "test-command"
    expected_out = "Some out"
    shell = True
    stdout = subprocess.PIPE
    stderr = subprocess.PIPE
    subprocess_mock.return_value.return_code = 0
    subprocess_mock.return_value.communicate.return_value = (expected_out, expected_out)

    # Act
    sut.call_subprocess(foo_command)

    # Assert
    subprocess_mock.assert_called_once_with(foo_command, shell=shell, stdout=stdout, stderr=stderr)


@mock.patch.object(subprocess, "Popen")
def test_call_subprocess_given_command_srt_when_stdout_has_lines_then_log_info(subprocess_mock):
    """ Given an str command, then calls subprocess.Popen and must log stdout as info"""

    # Arrange
    foo_command = "test-command"
    expected_log_message = "Info message on stdout"
    subprocess_mock.return_value.return_code = 0
    subprocess_mock.return_value.communicate.return_value = (expected_log_message, "")

    # Act
    with mock.patch.object(logging, "info") as logging_mock:
        sut.call_subprocess(foo_command)
        # Assert
        logging_mock.assert_called_once_with(expected_log_message)


@mock.patch.object(subprocess, "Popen")
def test_call_subprocess_given_command_srt_when_stderr_has_lines_then_log_error(subprocess_mock):
    """ Given an str command, then calls subprocess.Popen and must log stderr as error"""

    # Arrange
    foo_command = "test-command"
    expected_log_message = "Error message on stderr"
    subprocess_mock.return_value.return_code = 0
    subprocess_mock.return_value.communicate.return_value = ("", expected_log_message)

    # Act
    with mock.patch.object(logging, "error") as logging_mock:
        sut.call_subprocess(foo_command)

        # Assert
        logging_mock.assert_called_once_with(expected_log_message)

# endregion call_subprocess(str)
