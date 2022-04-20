"""
Checks raw dataset volume
"""

import unittest

import pytest

from constants import ASSETS_PATH


class VolumeBasicCheckTest(unittest.TestCase):
    """
    Checks folder volume is appropriate
    """

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_4_dataset_volume_check
    def test_folder_is_appropriate(self):
        """
        Ensure there are collected articles
        """
        self.assertTrue(any(ASSETS_PATH.iterdir()),
                        msg="ASSETS_PATH directory is empty")


class VolumeCheckTest(unittest.TestCase):
    """
    Checks folder volume is appropriate
    """

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_4_dataset_volume_check
    def test_folder_is_appropriate(self):
        """
        Ensure there are equal number of raw and meta files
        """
        metas, raws = 0, 0
        for file in ASSETS_PATH.iterdir():
            if file.name.endswith("_raw.txt"):
                raws += 1
            if file.name.endswith("_meta.json"):
                metas += 1
        message = "Collected dataset do not contain " \
                  "equal number of raw_articles and metas"
        self.assertEqual(metas, raws, msg=message)
