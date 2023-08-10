import os

RESOURCES_FOLDER = "resources"
TEST_RESOURCES_FOLDER = "test_resources"


def get_resources_folder() -> str:
    return f"{__get_main_script_dir_path()}/../{RESOURCES_FOLDER}"


def get_test_resources_folder() -> str:
    return f"{__get_main_script_dir_path()}/../{TEST_RESOURCES_FOLDER}"


def __get_main_script_dir_path() -> str:
    return os.path.abspath(os.path.dirname(__file__))