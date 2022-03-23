"""
Scrapper implementation
"""

import json
import pathlib
import random
import re
import shutil
import time

import requests
from bs4 import BeautifulSoup

from constants import ASSETS_PATH, CRAWLER_CONFIG_PATH, DOMAIN, HEADERS
from core_utils.article import Article, date_from_meta
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


class Crawler:
    """
    Crawler implementation
    """

    def __init__(self, seed_urls, max_articles: int):
        self.seed_urls = seed_urls
        self.max_articles = max_articles
        self.urls = []

    def _extract_url(self, article_bs):
        """
        get link to the article
        """
        for article_link in article_bs.find_all("a", class_="article__title"):
            self.urls.append(DOMAIN + article_link["href"])

    def find_articles(self):
        """
        Finds articles
        """

        for seed_url in self.seed_urls:
            response = requests.get(seed_url, headers=HEADERS)
            sleep_period = random.randrange(3, 7)
            time.sleep(sleep_period)

            if not response.ok:
                print("Request was unsuccessful.")
                continue

            seed_bs = BeautifulSoup(response.text, features="html.parser")
            self._extract_url(seed_bs)


def get_search_urls(self):
    """
    Returns seed_urls param
    """
    return self.seed_urls


def prepare_environment(base_path):
    """
    Creates ASSETS_PATH folder if not created and removes existing folder
    """

    path = pathlib.Path(base_path)

    if path.exists():
        shutil.rmtree(path)

    path.mkdir(parents=True)


def validate_config(crawler_path):
    """
    Validates config
    """

    with open(crawler_path) as file:
        config = json.load(file)

    urls = config["seed_urls"]
    articles = config["total_articles_to_find_and_parse"]
    http_regex = r"http[s]?://journals\.kantiana\.ru/."

    if not urls:
        raise IncorrectURLError

    if not isinstance(articles, int) or articles <= 0:
        raise IncorrectNumberOfArticlesError

    if articles > 100:
        raise NumberOfArticlesOutOfRangeError

    for url in urls:
        check = re.search(http_regex, url)
        if not check:
            raise IncorrectURLError

    prepare_environment(ASSETS_PATH)

    return urls, articles


class HTMLParser:

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
        response = requests.get(self.article_url, HEADERS)
        article_bs = BeautifulSoup(response.text, 'html.parser')

        self._fill_article_with_text(article_bs)
        self._fill_article_with_meta_information(article_bs)

        return self.article

    def _fill_article_with_text(self, article_bs):
        """
        Scrap the text from PDF link embedded in article url
        """
        possible_pdfs = article_bs.find("a", class_="article-panel__item button-icon").text

        for pdf in possible_pdfs:
            if ".pdf" in pdf:
                pdf_raw = PDFRawFile((DOMAIN + pdf), self.article_id)

                pdf_raw.download()
                pdf_text = pdf_raw.get_text()

                pdf_text = pdf_text.split("Список литературы")
                self.article.text = pdf_text[0]
                break

    def _fill_article_with_meta_information(self, article_bs):
        """
        Add meta information to Article class instance
        """
        self.article.title = article_bs.find(class_="article_title")

        authors = article_bs.find("a", class_="link link_const article__author")
        self.article.author = authors.text

        date_raw = re.search(r"\d{4} Выпуск №\d", article_bs.text)
        # Only year is available, the № of issues per year doesn't correspond with months
        # The year is divided into 4 parts then
        months = {"1": "01-01",
                  "2": "04-01",
                  "3": "08-01",
                  "4": "12-01"}
        self.article.date = date_from_meta(date_raw[:4] + "-" + months[date_raw[-1]])


if __name__ == '__main__':
    # checking the environment
    s_urls, all_articles = validate_config(CRAWLER_CONFIG_PATH)

    # initiating Crawler with PDF class instance and extract article links
    crawler = Crawler(s_urls, all_articles)
    crawler.find_articles()

    # extracting pdf, parsing pdf and saving text from every article link
    # stored in Crawler instance
    for i, link in enumerate(crawler.urls):
        parser = HTMLParser(link, i + 1)
        article = parser.parse()
        article.save_raw()
