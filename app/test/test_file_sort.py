import os

import pytest

from src.main import file_sort
from src.path_getter import get_test_resources_folder


@pytest.mark.parametrize(
    "path",
    [
        (get_test_resources_folder() + "/file_sort/empty"),
        (get_test_resources_folder() + "/file_sort/bad_filenames"),
    ],
)
def test_filesort__wrong_inputs(path: str):
    dir_files = os.listdir(path)
    try:
        dir_files.sort(key=file_sort)
    except ValueError:
        assert False


def test_filesort__correct_sort():
    dir_files = os.listdir(get_test_resources_folder() + "/file_sort/correct")
    dir_files.sort(key=file_sort)
    assert dir_files == ["1.txt", "40.txt", "999999.txt"]
