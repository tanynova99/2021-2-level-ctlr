"""
Pipeline for text processing implementation
"""

from pathlib import Path
import re

import pymorphy2
from pymystem3 import Mystem

from constants import ASSETS_PATH
from core_utils.article import Article, ArtifactType


class EmptyDirectoryError(Exception):
    """
    No data to process
    """


class InconsistentDatasetError(Exception):
    """
    Corrupt data:
        - numeration is expected to start from 1 and to be continuous
        - a number of text files must be equal to the number of meta files
        - text files must not be empty
    """


class MorphologicalToken:
    """
    Stores language params for each processed token
    """

    def __init__(self, original_word):
        self.original_form = original_word
        self.normalized_form = ''
        self.tags_mystem = ''
        self.tags_pymorphy = ''

    def get_cleaned(self):
        """
        Returns lowercased original form of a token
        """
        return self.original_form.lower()

    def get_single_tagged(self):
        """
        Returns normalized lemma with MyStem tags
        """
        pass

    def get_multiple_tagged(self):
        """
        Returns normalized lemma with PyMorphy tags
        """
        pass


class CorpusManager:
    """
    Works with articles and stores them
    """

    def __init__(self, path_to_raw_txt_data: str):
        self.path_to_raw_txt_data = path_to_raw_txt_data
        self._storage = {}
        self._scan_dataset()

    def _scan_dataset(self):
        """
        Register each dataset entry
        """

        files = list(self.path_to_raw_txt_data.glob('*_raw.txt'))

        for file in files:
            file_name = file.name
            match = re.search(r'\d+', file_name)
            article_id = int(match.group(0))
            self._storage[article_id] = Article(url=None, article_id=article_id)

    def get_articles(self):
        """
        Returns storage params
        """
        return self._storage


class TextProcessingPipeline:
    """
    Process articles from corpus manager
    """

    def __init__(self, corpus_manager: CorpusManager):
        self.corpus_manager = corpus_manager

    def run(self):
        """
        Runs pipeline process scenario
        """
        articles = CorpusManager.get_articles(self.corpus_manager).values()

        for article in articles:
            raw_text = Article.get_raw_text(article)
            tokens = self._process(raw_text)

            cleaned = []
            single_tagged = []
            multiple_tagged = []
            for token in tokens:
                cleaned.append(token.get_cleaned())
                single_tagged.append(token.get_single_tagged())
                multiple_tagged.append(token.get_multiple_tagged())

            article.save_as(' '.join(cleaned), ArtifactType.cleaned)
            article.save_as(' '.join(single_tagged), ArtifactType.single_tagged)
            article.save_as(' '.join(multiple_tagged), ArtifactType.multiple_tagged)

    def _process(self, raw_text: str):
        """
        Processes each token and creates MorphToken class instance
        """
        # txt from pdf comes with words like след-ующий
        # this replace deals with them
        text = raw_text.replace('-\n', '')

        result = Mystem().analyze(text)

        morph_tokens = []
        morph = pymorphy2.MorphAnalyzer()

        for token in result:

            # pre requisites for the token to be usable
            if "analysis" not in token:
                continue
            if not token["analysis"]:
                continue

            original_word = token["text"]
            if not re.match(r"[A-Za-zА-Яа-яЁё]", original_word):
                continue

            morph_token = MorphologicalToken(original_word=original_word)

            # next pre requisite
            if "lex" or "gr" not in token['analysis'][0]:
                continue

            # mystem tags
            morph_token.normalized_form = token['analysis'][0]['lex']
            morph_token.tags_mystem = token['analysis'][0]['gr']

            # pymorphy tags
            one_word = morph.parse(original_word)[0]
            morph_token.tags_pymorphy = one_word.tag

            morph_tokens.append(morph_token)


def validate_dataset(path_to_validate):
    """
    Validates folder with assets
    """

    if isinstance(path_to_validate, str):
        path_to_validate = Path(path_to_validate)

    if not path_to_validate.exists():
        raise FileNotFoundError

    if not path_to_validate.is_dir():
        raise NotADirectoryError

    if not any(path_to_validate.iterdir()):
        raise EmptyDirectoryError

    file_formats = [".json", ".txt", ".pdf"]
    checker = {}

    # creating a dictionary of file indexes
    # and checking the formats
    for file in Path(path_to_validate).iterdir():

        file_index = file.name.split("_")[0]
        if file_index not in checker.keys():
            checker[file_index] = 1
        else:
            checker[file_index] += 1

        if file.suffix not in file_formats:
            raise FileNotFoundError

    # checking that there are 3 files with said index
    if not all(value == 3 for value in checker.values()):
        raise InconsistentDatasetError

    # checking whether keys are consistent from 1 to N (max in files indices)
    current_i = list(int(x) for x in checker)
    ideal_i = range(1, max(current_i) + 1)
    if not set(current_i) & set(ideal_i) == set(ideal_i):
        raise InconsistentDatasetError

    return None


def main():
    # YOUR CODE HERE
    validate_dataset(ASSETS_PATH)
    corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
    pipeline = TextProcessingPipeline(corpus_manager=corpus_manager)
    pipeline.run()


if __name__ == "__main__":
    main()
