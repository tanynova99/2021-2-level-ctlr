"""
Tests for MorphologicalToken functionality
"""
import unittest

import pytest

from pipeline import MorphologicalToken


class MorphologicalTokenTest(unittest.TestCase):
    """
    Tests for MorphologicalToken realization
    """

    def setUp(self) -> None:
        self.token = MorphologicalToken('Original_token')
        self.token.normalized_form = 'lemma'
        self.token.tags_mystem, self.token.tags_pymorphy = 'tags_mystem', 'tags_pymorphy'

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_morphological_token_checks
    def test_morphological_token_instantiation(self) -> None:
        """
        Ensure that MorphologicalToken instance is instantiated correctly
        """
        new_token = MorphologicalToken('оригинальное слово')
        attrs = ['original_word', 'normalized_form', 'tags_mystem', 'tags_pymorphy']
        self.assertTrue(all((
            hasattr(new_token, attrs[0]),
            hasattr(new_token, attrs[1]),
            hasattr(new_token, attrs[2]),
            hasattr(new_token, attrs[3]))),
            f"MorphologicalToken instance must possess the following arguments: {', '.join(attrs)}")

        self.assertFalse(any((
            new_token.normalized_form,
            new_token.tags_mystem,
            new_token.tags_pymorphy
        )),
        f"{', '.join(attrs[1:])} fields of MorphologicalToken instance must initially be empty")

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_morphological_token_checks
    def test_get_cleaned(self) -> None:
        """
        Ensure that clean representation of a token is appropriate
        """
        self.assertEqual(self.token.get_cleaned(), 'original_token')

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_morphological_token_checks
    def test_get_single_tagged(self):
        """
        Ensure that single-tagged representation of a token is appropriate
        """
        print(self.token.tags_mystem)
        self.assertEqual(self.token.get_single_tagged(), 'lemma<tags_mystem>')

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_3_3_morphological_token_checks
    def test_get_multiple_tagged(self):
        """
        Ensure that single-tagged representation of a token is appropriate
        """
        print(self.token.tags_mystem)
        self.assertEqual(self.token.get_single_tagged(), 'lemma<tags_mystem>')
