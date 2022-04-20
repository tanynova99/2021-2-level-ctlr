"""
Test for CorpusManager abstraction realization
"""
import json
import shutil
import unittest

import pytest

from core_utils.article import Article
from constants import ASSETS_PATH
from pipeline import CorpusManager, validate_dataset
from config.test_params import TEST_FILES_FOLDER


class ArticleInstanceCreationBasicTest(unittest.TestCase):
    """
    Tests for basic aspects of CorpusManager realization
    """

    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copyfile(TEST_FILES_FOLDER / "0_raw.txt",
                        ASSETS_PATH / "0_raw.txt")

    def setUp(self) -> None:
        self.corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    def test_corpus_manager_instantiation(self):
        """
        Ensure that CorpusManager instances are instantiated correctly
        """
        self.assertTrue(hasattr(self.corpus_manager, '_storage'),
                        'CorpusManager instance must have _storage field')
        message = 'CorpusManager attribute _storage must be dict object'
        self.assertIsInstance(self.corpus_manager.get_articles(), dict,
                              message)
        message = 'CorpusManager attribute _storage must be ' \
                  'filled right away during initialisation'
        self.assertTrue(self.corpus_manager.get_articles(), message)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    def test_raw_files_are_found(self):
        """
        Ensure that CorpusManager finds all saved raw files
        """
        message = "Corpus Manager does not create " \
                  "article instances given raw files only"
        self.assertIn(0, self.corpus_manager.get_articles(), message)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    def test_article_instance_is_created(self):
        """
        Ensure CorpusManager creates Article instances
        """
        message = "CorpusManager _storage values must be Article instances"
        self.assertIsInstance(self.corpus_manager.get_articles()[0],
                              Article, message)

    @classmethod
    def tearDownClass(cls) -> None:
        (ASSETS_PATH / "0_raw.txt").unlink()


class ArticleInstanceCreationAdvancedTest(unittest.TestCase):
    """
    Tests for extended aspects of CorpusManager realization
    """

    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copyfile(TEST_FILES_FOLDER / "0_raw.txt",
                        ASSETS_PATH / "0_raw.txt")
        shutil.copyfile(TEST_FILES_FOLDER / "0_meta.json",
                        ASSETS_PATH / "0_meta.json")

    def setUp(self) -> None:
        self.corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        with (TEST_FILES_FOLDER / '0_meta.json').open(encoding='utf-8') as file:
            self.meta = json.load(file)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_2_corpus_manager_checks
    def test_meta_files_are_found(self):
        """
        Ensure CorpusManager finds all saved meta files
        """
        message = "Corpus Manager does not create article " \
                  "instances given both raw and meta files"
        self.assertIn(0, self.corpus_manager.get_articles(), message)

    @classmethod
    def tearDownClass(cls) -> None:
        (ASSETS_PATH / "0_raw.txt").unlink()
        (ASSETS_PATH / "0_meta.json").unlink()
