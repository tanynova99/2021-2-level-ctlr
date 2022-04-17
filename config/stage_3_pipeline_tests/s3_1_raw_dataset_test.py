"""
Tests for validation dataset of raw texts
"""
import json
import pathlib
import shutil

import pytest

from pipeline import (
                        EmptyDirectoryError,
                        InconsistentDatasetError,
                        validate_dataset
                     )
from config.stage_2_crawler_tests.s2_1_crawler_config_test import (
                                                        ExtendedTestCase
                                                                    )

print("Stage 2A: Validating Assets Path")
print("Starting tests with received assets folder")


def generate_test_directory(directory, raw_n=5, meta_n=5, raw_empty=False):
    """
    An auxiliary function for creating different kind of
    directories to test dataset validator implementation
    """
    if directory.exists():
        shutil.rmtree(directory)
    directory.mkdir()

    # create n raw files
    for index in range(raw_n):
        filename = f"{index + 1}_raw.txt"
        with open(directory / filename, 'w', encoding="utf-8") as file:
            text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit, " \
                   "sed do eiusmod tempor incididunt ut labore et dolore " \
                   "magna aliqua. Ut enim ad minim veniam, quis nostrud " \
                   "exercitation ullamco laboris nisi ut aliquip ex ea " \
                   "commodo consequat."
            if not raw_empty:
                file.write(text)

    # create m meta files
    for index in range(meta_n):
        meta_dummy = {'id': 0,
                      'url': 'https://vja.ruslang.ru/ru/archive/2021-3/7-25',
                      'author': 'С.В. Князев'}
        filename = f"{index + 1}_meta.json"
        with (directory / filename).open("w", encoding='utf-8') as file:
            json.dump(meta_dummy, file, sort_keys=False,
                      indent=4, ensure_ascii=False, separators=(',', ': '))
    return directory


class PipelinePathCheck(ExtendedTestCase):
    """
    Tests for pipeline behavior relating different path input
    """

    empty = pathlib.Path('empty')
    broken_id = pathlib.Path('broken_id')
    imbalanced = pathlib.Path('imbalanced')
    empty_raw = pathlib.Path('empty_raw')
    normal = pathlib.Path('normal')
    filepath = pathlib.Path('filepath.txt')

    @classmethod
    def setUpClass(cls) -> None:
        generate_test_directory(cls.empty, raw_n=0, meta_n=0)
        generate_test_directory(cls.broken_id)
        (cls.broken_id / '1_raw.txt').unlink()
        generate_test_directory(cls.imbalanced, raw_n=3, meta_n=2)
        generate_test_directory(cls.empty_raw, raw_empty=True)
        generate_test_directory(cls.normal)
        cls.filepath.open('w').close()

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_1_dataset_sanity_checks
    def test_pipe_fails_given_non_existent_path(self):
        """
        Ensure that pipeline raises an error when given invalid path
        """
        non_existent_path = pathlib.Path("non_existent_path")
        error_message = "Checking that scrapper can handle " \
                        "not existing assets paths failed."
        self.assertRaisesWithMessage(error_message,
                                     FileNotFoundError,
                                     validate_dataset,
                                     non_existent_path)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_1_dataset_sanity_checks
    def test_pipe_processes_plain_path(self):
        """
        Ensure that pipeline raises an error when given invalid path
        """
        plain_string_path = str(self.normal)
        success = True
        try:
            validate_dataset(plain_string_path)
        except AttributeError:
            success = False
        error_message = "Checking that scrapper can handle " \
                        "path in a form of plain string, not Path object."
        self.assertTrue(success, error_message)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_1_dataset_sanity_checks
    def test_pipeline_fails_given_filepath(self):
        """
        Ensure that pipeline raises an error when given non-existing directory
        """
        error_message = "Checking that pipeline fails " \
                        "if given not a directory path."
        self.assertRaisesWithMessage(error_message,
                                     NotADirectoryError,
                                     validate_dataset,
                                     self.filepath)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_1_dataset_sanity_checks
    def test_pipe_fails_given_empty_directory(self):
        """
        Ensure that pipeline raises an error when given empty directory
        """
        error_message = "Checking that empty directories " \
                        "cannot be processed."
        self.assertRaisesWithMessage(error_message,
                                     EmptyDirectoryError,
                                     validate_dataset,
                                     self.empty)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_1_dataset_sanity_checks
    def test_pipe_fails_given_inconsistent_dataset(self):
        error_message = "Checking that pipeline does not accept " \
                        "dataset with inconsistent numeration"
        self.assertRaisesWithMessage(error_message,
                                     InconsistentDatasetError,
                                     validate_dataset,
                                     self.broken_id)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_1_dataset_sanity_checks
    def test_pipe_fails_given_imbalanced_dataset(self):
        error_message = "Checking that pipeline does not accept " \
                        "dataset with uneven numbers of meta and text files"
        self.assertRaisesWithMessage(error_message,
                                     InconsistentDatasetError,
                                     validate_dataset,
                                     self.imbalanced)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_1_dataset_sanity_checks
    def test_pipe_fails_given_dataset_with_empty_texts(self):
        error_message = "Checking that pipeline does not accept " \
                        "dataset with empty text files"
        self.assertRaisesWithMessage(error_message,
                                     InconsistentDatasetError,
                                     validate_dataset,
                                     self.empty_raw)

    @classmethod
    def tearDownClass(cls) -> None:
        for path in [cls.empty, cls.broken_id, cls.imbalanced,
                     cls.empty_raw, cls.normal]:
            shutil.rmtree(path)
        cls.filepath.unlink()
