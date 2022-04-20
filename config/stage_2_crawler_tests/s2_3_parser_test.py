# pylint: disable=no-member, no-name-in-module
"""
Parser realization validation
"""
import json
import random
import unittest

import pytest

from core_utils.article import Article
from scrapper import validate_config, Crawler, HTMLParser
from constants import CRAWLER_CONFIG_PATH, ASSETS_PATH


class HTMLParserTest(unittest.TestCase):
    """
    A class for testing Parser abstraction
    """

    def setUp(self) -> None:
        validate_config(CRAWLER_CONFIG_PATH)
        with CRAWLER_CONFIG_PATH.open(encoding='utf-8') as file:
            data = json.load(file)

        if not ASSETS_PATH.exists():
            ASSETS_PATH.mkdir(parents=True)

        self.crawler = Crawler(data['seed_urls'],
                               data['total_articles_to_find_and_parse'])
        self.crawler.find_articles()
        self.parser = HTMLParser(random.choice(self.crawler.urls), 1)
        self.return_value = self.parser.parse()

    def tearDown(self) -> None:
        for pdf_file in ASSETS_PATH.glob('*.pdf'):
            print(f'Removing {pdf_file}')
            pdf_file.unlink()

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_3_HTML_parser_check
    def test_html_parser_instantiation(self):
        """
        Ensure Parser is instantiated correctly
        """
        parser = HTMLParser(random.choice(self.crawler.urls), 1)
        self.assertTrue(hasattr(parser, 'article'),
                        "Parser instance must possess 'article' attribute")
        message = "Attribute 'article' of Parser " \
                  "instance must be an instance of Article"
        self.assertIsInstance(parser.article,
                              Article,
                              message)

    @pytest.mark.mark4
    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_3_HTML_parser_check
    def test_html_parser_parse_return_value_basic(self):
        """
        Ensure Parser.parser() returns Article with filled text field
        """
        self.assertIsInstance(self.return_value, Article,
                              "parse() method must return Article instance")
        self.assertTrue(self.return_value.article_id,
                        "parse() method must return Article with filled id")
        message = "parse() method must return an " \
                  "Article instance with filled text"
        self.assertTrue(self.return_value.text,
                        message)

    @pytest.mark.mark6
    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_3_HTML_parser_check
    def test_html_parser_parse_return_value_medium(self):
        """
        Ensure Parser.parser() returns Article with filled title and author
        """
        self.assertTrue(self.return_value.title,
                        "parse() method must return Article with filled title")
        message = "parse() method must return " \
                  "an Article instance with filled author"
        self.assertTrue(self.return_value.author,
                        message)

    @pytest.mark.mark8
    @pytest.mark.mark10
    @pytest.mark.stage_2_3_HTML_parser_check
    def test_html_parser_parse_method_advanced(self):
        """
        Ensure Parser.parser() returns Article with filled date field
        """
        message = "parse() method must return an " \
                  "Article instance with filled date"
        self.assertTrue(self.return_value.date,
                        message)
