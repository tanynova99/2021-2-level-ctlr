"""
Tests for student text preprocessing
"""
import re
import unittest

import pytest

from constants import ASSETS_PATH


MYSTEM_TAGS = ['A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ',
               'INTJ', 'NUM', 'PART', 'PR', 'S', 'SPRO', 'V']
PYMORPHY_TAGS = ['NOUN', 'ADJF', 'ADJS', 'COMP', 'VERB',
                 'INFN', 'PRTF', 'PRTS', 'GRND',
                 'NUMR', 'ADVB', 'NPRO', 'PRED', 'PREP',
                 'CONJ', 'PRCL', 'INTJ', 'UNKN']

PUNCTUATION_MARKS = [',', '.', '-', ';', ':', '!', '?', '<']


class StudentTextBasicPreprocessTest(unittest.TestCase):
    """
    Class for checking basic text preprocessing
    """
    def setUp(self) -> None:
        self.articles = dict()
        for article in ASSETS_PATH.iterdir():
            if article.name.endswith("_cleaned.txt"):
                with article.open("r", encoding="utf-8") as txt:
                    self.articles[int(article.name[:-12])] = txt.read()

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    def test_clean_tokens(self):
        """
        Ensure there is no punctuation of uppercase in cleaned text
        """
        for article_id, article_text in self.articles.items():
            for token in article_text.split():
                message = f"There are some punctuation " \
                          f"marks found in article {article_id}"
                self.assertTrue(token not in PUNCTUATION_MARKS, message)
                message = f"Token {token} in article " \
                          f"{article_id} is not lowercase"
                self.assertTrue(token.islower(), msg=message)


class StudentTextAdvancedPreprocessTest(unittest.TestCase):
    """
    Class for checking advanced text preprocessing
    """
    def setUp(self) -> None:
        self.articles = dict()
        for article in ASSETS_PATH.iterdir():
            if article.name.endswith("_multiple_tagged.txt"):
                with article.open("r", encoding="utf-8") as txt:
                    self.articles[int(article.name[:-20])] = txt.read()

    @staticmethod
    def custom_split(string) -> list:
        """
        Split a string into tagged sequences
        """
        return [element+')' for element in string.split(') ')]

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    def test_multiple_tagged_tokens_format(self):
        """
        Ensure multi-tagged sequences are formatted correctly
        """
        for _, article_text in self.articles.items():
            word_tag_sequences = self.custom_split(article_text)
            for sequence in word_tag_sequences:
                message = f"{sequence} --- ( markup " \
                          f"symbol should be in processed text"
                self.assertTrue("(" in sequence, msg=message)
                message = f"{sequence} --- In tagged sequence " \
                          f"there should be > symbol before ( "
                self.assertEqual(sequence[sequence.rindex("(") - 1], ">",
                                 msg=message)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    def test_mystem_tags_correctness_multiple_tagged(self):
        """
        Ensure there are no unknown mystem tags in multi-tagged sequences
        """
        for _, article_text in self.articles.items():
            tags = re.findall(r"<([A-Z]+)[,=]?", article_text)
            for tag in tags:
                message = f"Tag {tag} not in list of known mystem tags"
                self.assertTrue(tag in MYSTEM_TAGS, msg=message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    def test_pymorphy_tags_correctness_multiple_tagged(self):
        """
        Ensure there are no unknown pymorphy tags in multi-tagged sequences
        """
        for _, article_text in self.articles.items():
            tags = re.findall(r"\([A-Z]+", article_text)
            for tag in tags:
                tag = tag[1:]
                message = f"Tag {tag} not in list of known pymorphy tags"
                self.assertTrue(tag in PYMORPHY_TAGS, msg=message)


class StudentTextMediumPreprocessTest(unittest.TestCase):
    """
    Class for checking extended text preprocessing
    """
    def setUp(self) -> None:
        self.articles = dict()
        for article in ASSETS_PATH.iterdir():
            if article.name.endswith("_single_tagged.txt"):
                with article.open("r", encoding="utf-8") as txt:
                    self.articles[int(article.name[0])] = txt.read()

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    def test_single_tagged_tokens_format(self):
        """
        Ensure msingle-tagged sequences are formatted correctly
        """
        for _, article_text in self.articles.items():
            word_tag_sequences = article_text.split()
            for sequence in word_tag_sequences:
                message = f"{sequence} --- There should be > at " \
                          f"the end of each word<tag> sequence"
                self.assertTrue(sequence.endswith(">"), msg=message)
                message = f"{sequence} --- < markup symbol should " \
                          f"be in processed text"
                self.assertIn("<", sequence, msg=message)
                message = f"{sequence} --- In tagged sequence " \
                          f"there should be char symbol before < "
                self.assertTrue(sequence[sequence.index("<") - 1].isalpha(),
                                msg=message)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_5_student_dataset_validation
    def test_mystem_tags_correctness_single_tagged(self):
        """
        Ensure there are no unknown mystem tags in multi-tagged sequences
        """
        for _, article_text in self.articles.items():
            tags = re.findall(r"<([A-Z]+)[,=]?", article_text)
            for tag in tags:
                message = f"Tag {tag} not in list of known mystem tags"
                self.assertTrue(tag in MYSTEM_TAGS, msg=message)
