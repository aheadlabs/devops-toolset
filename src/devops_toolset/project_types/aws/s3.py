"""Provides tools for managing the AWS S3 service"""

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.aws.Literals import Literals as AwsLiterals

import boto3
import logging

app: App = App()
s3 = boto3.client("s3")
literals = LiteralsCore([AwsLiterals])

def get_objects_in_bucket(bucket_name: str, object_prefix: str = "") -> list:
    """Gets all objects that match the criteria from a S3 bucket.

    Args:
        bucket_name: S3 bucket name to get the objects from.
        object_prefix: Only the object keys that match this prefix will be
            retrieved.

    Returns:
        Returns the list of all the objects in the bucket.
    """

    object_list: list = []

    paginator = s3.get_paginator("list_objects_v2")
    pages = paginator.paginate(Bucket=bucket_name, Prefix=object_prefix)
    for page in pages:
        object_list.extend(page["Contents"])

    logging.info(literals.get("s3_got_x_objects_from_s3_bucket").format(
        number=len(object_list),
        bucket=bucket_name
    ))

    return object_list

if __name__ == "__main__":
    help(__name__)
