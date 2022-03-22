"""
Scrapper implementation
"""

import json
import os
import random
import re
import shutil
import time
import urllib.parse

import requests
from bs4 import BeautifulSoup

from constants import ASSETS_PATH, CRAWLER_CONFIG_PATH, DOMAIN, HEADERS
from core_utils.article import Article
from core_utils.pdf_utils import PDFRawFile


class IncorrectURLError(Exception):
    """
    Seed URL does not match standard pattern
    """


class NumberOfArticlesOutOfRangeError(Exception):
    """
    Total number of articles to parse is too big
    """


class IncorrectNumberOfArticlesError(Exception):
    """
    Total number of articles to parse in not integer
    """


class PDFCrawler:
    """
    Crawler implementation
    """

    def __init__(self, seed_urls, max_articles: int):
        self.seed_urls = seed_urls
        self.max_articles = max_articles
        self.urls = []

    def _extract_url(article_bs):

        urls = []
        for article_link in article_bs.find_all("a", class_="article_title"):
            urls.append(''.join([DOMAIN, article_link.get("href")]))

        return urls

    def find_articles(self):
        """
        Finds articles
        """

        for seed_url in self.seed_urls:
            response = requests.get(seed_url, headers=HEADERS)
            if not response.ok:
                print("Request was unsuccessful.")
                continue

            article_text = BeautifulSoup(response.text, features="html.parser")
            self._extract_url(article_text)

            sleep_period = random.randrange(3, 7)
            time.sleep(sleep_period)

    def get_search_urls(self):
        """
        Returns seed_urls param
        """
        return self._seed_urls


def prepare_environment(base_path):
    """
    Creates ASSETS_PATH folder if not created and removes existing folder
    """
    if base_path.exists():
        shutil.rmtree(base_path)
    os.mkdir(base_path)


def validate_config(crawler_path):
    """
    Validates given config
    """

    with open(crawler_path) as file:
        config = json.load(file)

    urls = config["seed_urls"]
    articles = config["total_articles_to_find_and_parse"]
    http_regex = r"http[s]?://journals\.kantiana\.ru/."

    if not urls:
        raise IncorrectURLError

    if not isinstance(articles, int):
        raise IncorrectNumberOfArticlesError

    if articles > 1000 or articles < 0:
        raise NumberOfArticlesOutOfRangeError

    for url in urls:
        check = re.search(http_regex, url)
        if not check:
            raise IncorrectURLError

    return urls, articles


class HTMLWithPDFParser:

    def __init__(self, article_url, article_id):
        """
        Init
        """
        self.article_url = article_url
        self.article_id = article_id
        self.article = Article(url=article_url, article_id=article_id)

    def parse(self):
        """
        filling the class Article instance
        """
        response = requests.get(self.article_url)
        article_bs = BeautifulSoup(response.text, 'html.parser')

        self._fill_article_with_text(article_bs)
        self._fill_article_with_meta_information(article_bs)

        return self.article

    def _fill_article_with_text(self, article_bs):
        """
        Scrap the text from PDF link embedded in article url
        """
        possible_pdfs = article_bs.find_all('a', class_="article-panel__item button-icon")

        for pdf in possible_pdfs:
            if "upload" in pdf["href"]:
                pdf_raw = PDFRawFile(prf['href'], self.article_id)

                pdf_raw.download()
                pdf_text = pdf_raw.get_text()

                text_only = pdf_text.split('Список литературы')
                self.article.text = ''.join(text_only[:-1])
                break

    def _fill_article_with_meta_information(self, article_bs):
        """
        Add meta information to Article class instance
        """
        title = article_bs.find("h3", class_="article__title")
        self.article.title = title.text

        authors = article_bs.find_all("a", class_="link link_const article__author")
        self.article.author = authors.text

        date_raw = re.search("\d{4} Выпуск №\d", self.article.text)

        # Only year is available, the № of issues per year doesn't correspond with months
        if date_raw:
            self.article.date = datetime.datetime.strptime(date_raw.group(0)[:4], '%Y')


if __name__ == '__main__':
    # checking the environment
    seed_urls, max_articles = validate_config(CRAWLER_CONFIG_PATH)

    # initiating Crawler with PDF class instance and extract article links
    crawler = PDFCrawler(seed_urls, max_articles)
    crawler.find_articles()

    # extracting pdf, parsing pdf and saving text from every article link
    # stored in PDFCrawler instance
    for i, url in enumerate(crawler.urls):
        parser = HTMLWithPDFParser(url, i + 1)
        article = parser.parse()
        article.save_raw()
