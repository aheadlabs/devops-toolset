import pytest

class FileNames(object):
    """Test file names"""
    test_file = "test.py"
    path = "/pathto"
    deep_path = "/deep/pathto"
    paths = ["/pathto/file1", "/pathto/file2"]
    no_paths = []
    file = ".gitignore"

@pytest.fixture
def filenames():
    """Sample file names for testing file system related functionality"""
    return FileNames()
