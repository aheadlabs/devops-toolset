"""Unit core for the apache file"""

import project_types.aws.get_aws_resources as sut
from unittest.mock import patch, mock_open


# region main()


@patch("tools.cli.call_subprocess_with_result")
@patch("json.loads")
@patch("json.dump")
def test_main_given_json_path_should_dump_resources(json_dump_mock, json_loads_mock,
                                                    call_subprocess_with_result_mock, tmp_path):
    """Given json_dump, should generate a dict by calling subprocess and dumping into path"""

    # Arrange
    resource: dict = {"SomeResource": "SomeValue"}
    json_path = "path/to/json"
    hosted_zone = "/hostedzone/ABCDEFGHIJKL123456789"
    json_loads_mock.return_value = resource
    m = mock_open()

    # Act
    with patch("builtins.open", m, create=True):
        sut.main(json_path, hosted_zone)
        # Assert
        json_dump_mock.assert_called_once()


# endregion
