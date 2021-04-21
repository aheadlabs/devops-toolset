""" Unit core for the bootstrap repository script """

from unittest.mock import patch
import project_types.wordpress.bootstrap_repository as sut

# region main


@patch("os.chdir")
@patch("tools.git.git_init")
@patch("tools.git.git_commit")
@patch("project_types.wordpress.generate_wordpress.main")
def test_main_given_given_arguments_then_call_dependencies(generate_wordpress_mock, git_commit_mock,
                                                           git_init_mock, chdir_mock, wordpressdata):
    """ Given project path argument, then calls os.chdir to project_path """
    # Arrange
    project_path = wordpressdata.root_path
    db_user_password = db_admin_password = wp_admin_password = wordpressdata.default_pwd
    skip_git = False
    # Act
    sut.main(project_path, db_user_password, db_admin_password, wp_admin_password, wordpressdata.environment_name,
             [], [], False, False, skip_git)
    # Assert
    chdir_mock.assert_called_once_with(project_path)
    git_init_mock.assert_called_once_with(project_path, skip_git)
    generate_wordpress_mock.assert_called_once_with(project_path, db_user_password, db_admin_password,
                                                    wp_admin_password, wordpressdata.environment_name, [], [], False,
                                                    False)
    git_commit_mock.assert_called_once_with(skip_git)
# endregion main
