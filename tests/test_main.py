import os

import pytest

from this_cmd_be_boring_af import main, path_getter


@pytest.mark.parametrize(
    "path",
    [
        (path_getter.get_test_resources_folder() + "/file_sort/empty"),
        (path_getter.get_test_resources_folder() + "/file_sort/bad_filenames"),
    ],
)
def test_filesort__wrong_inputs(path: str):
    dir_files = os.listdir(path)
    try:
        dir_files.sort(key=main.file_sort)
    except ValueError:
        assert False


def test_filesort__correct_sort():
    dir_files = os.listdir(path_getter.get_test_resources_folder() + "/file_sort/correct")
    dir_files.sort(key=main.file_sort)
    assert dir_files == ["1.txt", "40.txt", "999999.txt"]


def test_extract_correct_text_files__filters_out_non_text_files():
    path = path_getter.get_test_resources_folder() + "/file_filter/non_txt_files"
    dir_files = main.extract_correct_text_files(path)
    assert "2.mp4" not in dir_files


def test_extract_correct_text_files__filters_out_non_number_names():
    path = path_getter.get_test_resources_folder() + "/file_sort/bad_filenames"
    dir_files = main.extract_correct_text_files(path)
    assert "3a.txt" not in dir_files and "a2.txt" not in dir_files
