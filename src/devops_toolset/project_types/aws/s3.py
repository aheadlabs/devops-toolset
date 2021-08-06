"""Provides tools for managing the AWS S3 service"""

import boto3
import devops_toolset.filesystem.paths as paths
import logging
import pathlib

from devops_toolset.core.app import App
from devops_toolset.core.LiteralsCore import LiteralsCore
from devops_toolset.project_types.aws.Literals import Literals as AwsLiterals


app: App = App()
s3 = boto3.client("s3")
literals = LiteralsCore([AwsLiterals])


def get_objects_from_bucket(bucket_name: str, keys: list[str], destination_path: str):
    """Downloads objects that match the specified keys from the bucket.

    Args:
        bucket_name: S3 bucket name to get the objects from.
        keys: Keys of the objects to be downloaded.
        destination_path: Path where the objects will be downloaded to.
    """

    if not paths.is_valid_path(destination_path, True):
        raise ValueError

    if len(keys) == 0:
        raise ValueError

    destination_path_obj = pathlib.Path(destination_path)

    logging.info(literals.get("s3_downloading_objects_from_s3_bucket").format(
        number=len(keys),
        bucket=bucket_name,
        destination=str(destination_path_obj)
    ))

    for key in keys:
        object_destination_path_obj = pathlib.Path.joinpath(destination_path_obj, key)
        with open(object_destination_path_obj, "wb") as file:
            s3.download_fileobj(bucket_name, key, file)
            logging.info(literals.get("s3_downloaded_object_from_s3_bucket").format(
                name=key,
                bucket=bucket_name,
                destination=str(object_destination_path_obj)
            ))


def get_filtered_objects_from_bucket(bucket_name: str, object_prefix: str, destination_path: str):
    """Downloads filtered objects that match the specified keys and prefix from
    the bucket.

    Args:
        bucket_name: S3 bucket name to get the objects from.Hello world!
        object_prefix: Only the object keys that match this prefix will be
            retrieved.
        destination_path: Path where the objects will be downloaded to.
    """

    if not paths.is_valid_path(destination_path, True):
        raise ValueError()

    if object_prefix is None or object_prefix == "":
        raise ValueError()

    object_list = list_objects_in_bucket(bucket_name, object_prefix)
    key_list = list(map(lambda x: x["Key"], object_list))
    get_objects_from_bucket(bucket_name, key_list, destination_path)


def list_objects_in_bucket(bucket_name: str, object_prefix: str = "") -> list:
    """Gets all objects that match the criteria from a S3 bucket.

    Args:
        bucket_name: S3 bucket name to get the object list from.
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


def put_object_to_bucket(bucket_name: str, local_path: str, destination_path: str):
    """Uploads an object to the S3 bucket."""
    pass

if __name__ == "__main__":
    help(__name__)
