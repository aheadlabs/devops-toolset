"""Test configuration file for dotnet package.

This code is executed once per unit test session.
Add here whatever you want to pass as a fixture in your core.

    ie: (see FileNames example)
        - Add a class that contains what you want to pass as a fixture in your core.
        - Create a fixture with that same lowered name that returns an instance to that class."""


import pytest


class DotNetData(object):
    """Class used to create the dotnetdata fixture"""

    csproj_file_content = "<Project><PropertyGroup><Version>6.6.6</Version></PropertyGroup></Project>"


@pytest.fixture
def dotnetdata():
    """Sample data for testing .NET related functionality"""
    return DotNetData()
