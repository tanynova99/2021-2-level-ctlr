"""
Tests for processing reference text
"""
import re
import shutil
from string import punctuation
import unittest

import pytest

from constants import ASSETS_PATH
from pipeline import CorpusManager, TextProcessingPipeline, validate_dataset
from config.test_params import TEST_FILES_FOLDER


MYSTEM_TAGS = ["A", "ADV", "S", "V", "PR", "ANUM"]
PYMORPHY_TAGS = ["ADJF", "PREP", "NOUN", "ADVB"]


class ReferenceTextPreprocessTestSimplified(unittest.TestCase):
    """
    Tests for simplified preprocessing of reference text
    """
    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        source = TEST_FILES_FOLDER / "0_raw.txt"
        destination = ASSETS_PATH / "0_raw.txt"
        shutil.copyfile(source, destination)
        corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        pipe = TextProcessingPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        path = TEST_FILES_FOLDER / 'reference_score_four_test.txt'
        with path.open('r', encoding='utf-8') as reference:
            self.reference = reference.read()
        path = ASSETS_PATH / "0_cleaned.txt"
        with path.open("r", encoding='utf-8') as processed:
            self.processed = processed.read()

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_reference_preprocessed_are_equal(self):
        """
        Ensure equal number of tags in processed and reference texts
        """
        # check number of tokens sequences
        self.assertEqual(len(self.reference.split()),
                         len(self.processed.split()),
                         msg=f"""Number of tokens sequences in reference
{self.reference} and processed {self.processed} texts is different""")

        # check tokenization
        self.assertEqual(self.reference.split(),
                         self.processed.split(),
                         msg="""Pipe does not tokenize admin text.
Check how you tokenize""")

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_overall_format(self):
        """
        Ensure that there is no punctuation of uppercase in clean text
        """
        self.assertTrue(self.processed.islower(),
                        'Cleaned text must be lowercase')
        self.assertFalse((set(self.processed) & set(punctuation)),
                         'Cleaned text must not have any punctuation')

    @classmethod
    def tearDownClass(cls) -> None:
        (ASSETS_PATH / "0_raw.txt").unlink()
        (ASSETS_PATH / "0_cleaned.txt").unlink()
        if (ASSETS_PATH / "0_single_tagged.txt").exists():
            (ASSETS_PATH / "0_single_tagged.txt").unlink()
            if (ASSETS_PATH / "0_multiple_tagged.txt").exists():
                (ASSETS_PATH / "0_multiple_tagged.txt").unlink()


class ReferenceTextPreprocessTest(unittest.TestCase):
    """
    Tests for preprocessing of reference texts
    """
    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copyfile(TEST_FILES_FOLDER / "0_meta.json",
                        ASSETS_PATH / "0_meta.json")
        shutil.copyfile(TEST_FILES_FOLDER / "0_raw.txt",
                        ASSETS_PATH / "0_raw.txt")
        corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        pipe = TextProcessingPipeline(corpus_manager)
        pipe.run()

    def setUp(self) -> None:
        path = TEST_FILES_FOLDER / 'reference_test.txt'
        with (path).open('r', encoding='utf-8') as ref:
            self.single_tagged_reference = ref.read()
        path = ASSETS_PATH / "0_single_tagged.txt"
        with (path).open("r", encoding='utf-8') as proc:
            self.single_tagged_processed = proc.read()
        self.mystem_tag_pattern = r"[а-яa-z]+<"

        if (ASSETS_PATH / "0_multiple_tagged.txt").exists():
            path = ASSETS_PATH / "0_multiple_tagged.txt"
            with path.open("r", encoding='utf-8') as processed:
                self.multiple_tagged_processed = processed.read()
            path = TEST_FILES_FOLDER / 'reference_score_eight_test.txt'
            with path.open('r', encoding='utf-8') as reference:
                self.multiple_tagged_reference = reference.read()
        self.pymorphy_tag_pattern = r"\w+<*>\(*\)"

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_single_tagged_reference_preprocessed_are_equal(self):
        """
        Ensure that there are equal number of tags
        in reference and processed texts
        after medium level processing
        """
        # check number of token word<tag> sequences
        message = f"Number of word<tag> sequences in reference " \
                  f"{self.single_tagged_reference} and processed " \
                  f"{self.single_tagged_processed} texts is different"
        self.assertEqual(len(re.findall(self.mystem_tag_pattern,
                                        self.single_tagged_reference)),
                         len(re.findall(self.mystem_tag_pattern,
                                        self.single_tagged_processed)),
                         msg=message)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_single_tagged_all_tokens_are_formatted(self):
        """
        Ensure correct formatting of single-tagged sequences
        """
        msg = 'In single-tagged files, all tokens must be accompanied ' \
              'by a single set of tags in angle brackets'
        self.assertEqual(len(re.findall(self.mystem_tag_pattern,
                                        self.single_tagged_processed)),
                         len(self.single_tagged_processed.split()), msg=msg)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_single_tagged_overall_format(self):
        """
        Ensure that overall formatting
        of single-tagged texts
        is appropriate
        """
        # check correctness of word<tag> sequences
        for word_tag in self.single_tagged_processed.split():
            message = f"{word_tag} --- There should be > " \
                      f"at the end of each word<tag> sequence"
            self.assertEqual(word_tag[-1], ">",
                             msg=message)
            message = f"{word_tag} --- < markup symbol " \
                      f"should be in processed text"
            self.assertTrue("<" in word_tag,
                            msg=message)
            message = f"{word_tag} --- In tagged sequence " \
                      f"there should be char symbol before < "
            self.assertTrue(word_tag[word_tag.index("<")-1].isalpha(),
                            msg=message)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_single_tagged_mystem_tag_format(self):
        """
        Ensure that mystem tags are correct
        """
        # check TAGS after each sequence:
        tags_pattern = r"<([A-Z]+)[,=]{1}"
        reference_tags = re.findall(tags_pattern, self.single_tagged_reference)
        processed_tags = re.findall(tags_pattern, self.single_tagged_processed)

        # check tag correctness.
        # Optional, but should be the same across each tagger,
        # as reference example is too simple
        for tag in processed_tags:
            message = f"Tag {tag} is an unknown Mystem " \
                      f"tag. Is it in required tags list?"
            self.assertTrue(tag in MYSTEM_TAGS, msg=message)
        message = f"Mystem tag sequence from reference text {reference_tags} " \
                  f"differs from processed text {processed_tags}"
        self.assertEqual(reference_tags, processed_tags, msg=message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_multiple_tagged_reference_preprocessed_are_equal(self):
        """
        Ensure that multi-tagged sequences are equal
        """
        # check number of token word<tag> sequences
        message = f"Number of word<tag>(tag) sequences in reference " \
                  f"{self.multiple_tagged_reference} and processed " \
                  f"{self.multiple_tagged_processed} texts is different"
        self.assertEqual(len(self.multiple_tagged_reference.split()),
                         len(self.multiple_tagged_processed.split()),
                         msg=message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_multiple_tagged_overall_format(self):
        """
        Ensure that multi-tagged sequences are formatted correctly
        """
        # check correctness of word<tag> sequences
        for word_tag in self.multiple_tagged_processed.split():
            try:
                self.assertEqual(word_tag[-1], ")")
            except AssertionError:
                message = f"{word_tag} --- There should be ) " \
                          f"at the end of each word<tag>(tag) sequence"
                self.assertTrue(word_tag[-1].isalpha(), msg=message)
            try:
                self.assertTrue("<" in word_tag)
            except AssertionError:
                message = f"{word_tag} --- < markup " \
                          f"symbol should be in processed text"
                self.assertTrue(word_tag[0].isalpha() and (word_tag[-1] == ")"),
                                msg=message)
            try:
                message = f"{word_tag} --- In tagged sequence " \
                          f"there should be char symbol before < "
                self.assertTrue(word_tag[word_tag.index("<")-1].isalpha(),
                                msg=message)
            except ValueError:
                message = f"{word_tag} --- In tagged sequence " \
                          f"there should be char symbol before < "
                self.assertTrue(word_tag[0].isalpha() and (word_tag[-1] == ")"),
                                msg=message)
            try:
                message = f"{word_tag} --- There should be " \
                          f"( after > in the word<tag>(tag) sequence"
                self.assertEqual(word_tag[word_tag.index(">")+1], "(",
                                 msg=message)
            except ValueError:
                message = f"{word_tag} --- There should be " \
                          f"( after > in the word<tag>(tag) sequence"
                self.assertTrue(word_tag[0].isalpha() and (word_tag[-1] == ")"),
                                msg=message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_multiple_tagged_tag_format(self):
        """
        Ensure that pymorphy tags are correct
        """
        # check TAGS after each sequences:
        tags_pattern = r">\([A-Z]+"
        reference_tags = re.findall(tags_pattern,
                                    self.multiple_tagged_reference)
        processed_tags = re.findall(tags_pattern,
                                    self.multiple_tagged_processed)

        # check tag correctness.
        # Optional, but should be the same across each tagger,
        # as reference example is too simple
        for tag in processed_tags:
            tag = tag[2:]
            message = f"Tag {tag} is an unknown pymorphy tag. " \
                      f"Is it in required tags list?"
            self.assertTrue(tag in PYMORPHY_TAGS,
                            msg=message)
        message = f"Tag sequence from reference text {reference_tags} " \
                  f"differs from processed text {processed_tags}"
        self.assertEqual(reference_tags, processed_tags, msg=message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_multiple_tagged_mystem_tag_format(self):
        """
        Ensure that mystem tags have appropriate format
        """
        # check TAGS after each sequence:
        tags_pattern = r"<([A-Z]+)[,=]{1}"
        reference_tags = re.findall(tags_pattern,
                                    self.multiple_tagged_reference)
        processed_tags = re.findall(tags_pattern,
                                    self.multiple_tagged_processed)
        for tag in processed_tags:
            message = f"Tag {tag} is an unknown Mystem tag. " \
                      f"Is it in required tags list?"
            self.assertTrue(tag in MYSTEM_TAGS, msg=message)
        message = f"Mystem tag sequence from reference text {reference_tags} " \
                  f"differs from processed text {processed_tags}"
        self.assertEqual(reference_tags, processed_tags, msg=message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_4_admin_data_processing
    def test_pymorphy_tag_format(self):
        """
        Ensure pymorphy tags match with reference
        """
        reference_tags = self.multiple_tagged_reference.split()
        processed_tags = self.multiple_tagged_processed.split()
        message = f"Tag sequence from reference text {reference_tags} " \
                  f"differs from processed text {processed_tags}"
        self.assertEqual(reference_tags, processed_tags, msg=message)

    @classmethod
    def tearDownClass(cls) -> None:
        (ASSETS_PATH / "0_meta.json").unlink()
        (ASSETS_PATH / "0_raw.txt").unlink()
        (ASSETS_PATH / "0_cleaned.txt").unlink()
        (ASSETS_PATH / "0_single_tagged.txt").unlink()
        if (ASSETS_PATH / "0_multiple_tagged.txt").is_file():
            (ASSETS_PATH / "0_multiple_tagged.txt").unlink()
