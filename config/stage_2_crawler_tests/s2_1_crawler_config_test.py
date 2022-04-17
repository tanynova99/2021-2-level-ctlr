"""
Crawler configuration validation
"""

import json
import unittest

import pytest

from constants import CRAWLER_CONFIG_PATH
from config.test_params import TEST_CRAWLER_CONFIG_PATH
from config.stage_2_crawler_tests.config_generator import generate_config
import scrapper
from scrapper import (IncorrectURLError,
                      IncorrectNumberOfArticlesError,
                      NumberOfArticlesOutOfRangeError)


print("Stage 1A: Validating Crawler Config")
print("Starting tests with received config")


class ExceptionIsNotRaised(Exception):
    """
    No exception was raised
    """


class ExtendedTestCase(unittest.TestCase):
    """
    Enable messaging when assertRaises is triggered
    """
    # pylint: disable=invalid-name
    def assertRaisesWithMessage(self, msg, exception, func, *args, **kwargs):
        """
        assertRaises method counterpart with enabled messaging
        """
        try:
            func(*args, **kwargs)
            print(msg)
            raise ExceptionIsNotRaised
        except ExceptionIsNotRaised:
            raise AssertionError(msg) from ExceptionIsNotRaised
        except Exception as inst: # pylint: disable=broad-except
            self.assertEqual(type(inst), exception, msg)


class CrawlerConfigCheck(ExtendedTestCase):
    """
    A class for Crawler configuration validation
    """
    def setUp(self) -> None:
        with CRAWLER_CONFIG_PATH.open() as file:
            self.reference = json.load(file)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    def test_incorrect_base_urls_config_param(self):
        """
        Checks that scrapper returns error message and exit code 1 with incorrect config params
        """
        generate_config(seed_urls='https://sample.com/',
                        num_articles=self.reference['total_articles_to_find_and_parse'])
        error_message = """Checking that scrapper can handle incorrect seed_urls inputs.
Seed URLs must be a list of strings, not a single string"""
        self.assertRaisesWithMessage(error_message,
                                     IncorrectURLError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)

        generate_config(seed_urls=[],
                        num_articles=self.reference['total_articles_to_find_and_parse'])

        error_message = "Checking that scrapper can handle incorrect seed_urls inputs. " \
                        "A list of seed URLs must not be empty"
        self.assertRaisesWithMessage(error_message,
                                     IncorrectURLError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)

        generate_config(seed_urls=['plain text', 1],
                        num_articles=self.reference['total_articles_to_find_and_parse'])

        error_message = "Checking that scrapper can handle incorrect seed_urls inputs. " \
                        "Real URLs always follow https:// pattern or similar"
        self.assertRaisesWithMessage(error_message,
                                     IncorrectURLError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    def test_incorrect_num_articles_config_param(self):
        """
        Checks that scrapper returns error message and exit code 1 with incorrect config params
        """
        generate_config(seed_urls=self.reference['seed_urls'],
                        num_articles=1000000)

        error_message = """Checking that num_articles parameter is not big for connection block.
                            This parameter must not be too big so as not to break connection"""
        self.assertRaisesWithMessage(error_message,
                                     NumberOfArticlesOutOfRangeError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    def test_incorrect_num_articles_config_param_type(self):
        """
        Checks that scrapper returns error message and exit code 1 with incorrect config params
        """
        generate_config(seed_urls=self.reference['seed_urls'],
                        num_articles='plain text')

        error_message = "Checking that scrapper can handle incorrect " \
                        "total_articles_to_find_and_parse inputs. Number " \
                        "of articles parameter must be an integer for scrapper to work"
        # self.assertRaises(IncorrectNumberOfArticlesError, scrapper.validate_config,
        #                   TEST_CRAWLER_CONFIG_PATH, msg=error_message)
        self.assertRaisesWithMessage(error_message,
                                     IncorrectNumberOfArticlesError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)

        generate_config(seed_urls=self.reference['seed_urls'],
                        num_articles=0)

        error_message = "Checking that scrapper can handle " \
                        "incorrect total_articles_to_find_and_parse inputs. " \
                        "Number of articles parameter must be a positive " \
                        "integer value for scrapper to work"
        self.assertRaisesWithMessage(error_message,
                                     IncorrectNumberOfArticlesError,
                                     scrapper.validate_config,
                                     TEST_CRAWLER_CONFIG_PATH)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_1_crawler_config_check
    def test_return_value_is_correct(self):
        """
        Checks that validation of correct config returns correct values
        """
        generate_config(seed_urls=self.reference['seed_urls'],
                        num_articles=self.reference['total_articles_to_find_and_parse'])

        error_message = "Checking that validate config returns " \
                        "exclusively the values from config file"

        self.assertTrue(scrapper.validate_config(TEST_CRAWLER_CONFIG_PATH) in
                        [(self.reference['seed_urls'],
                          self.reference['total_articles_to_find_and_parse']),
                         (self.reference['total_articles_to_find_and_parse'],
                          self.reference['seed_urls'])],
                        error_message)


if __name__ == "__main__":
    unittest.main()
