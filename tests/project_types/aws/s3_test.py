""" Unit tests for the project_types/aws/s3.py module"""

import devops_toolset.project_types.aws.s3 as sut
import json
from unittest.mock import patch


@patch("logging.info")
def test_get_objects_in_bucket_returns_list(log_info_mock, paginator, awsdata):
    """Given a bucket name, returns a list of objects"""

    # Arrange
    bucket_name: str = "my-bucket"
    expected_result = json.loads(awsdata.paginator_pages)[0]["Contents"]

    # Act
    with patch.object(sut, "s3") as s3_mock:
        with patch.object(s3_mock, "get_paginator") as get_paginator_mock:
            get_paginator_mock.return_value = paginator
            result = sut.get_objects_in_bucket(bucket_name)

    # Assert
    assert result == expected_result
