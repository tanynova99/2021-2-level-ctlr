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
        self.original_word = original_word
        self.normalized_form = ''
        self.tags_mystem = ''
        self.tags_pymorphy = ''

    def get_cleaned(self):
        """
        Returns lowercased original form of a token
        """
        return self.original_word.lower()

    def get_single_tagged(self):
        """
        Returns normalized lemma with MyStem tags
        """
        return f'{self.normalized_form}<{self.tags_mystem}>'

    def get_multiple_tagged(self):
        """
        Returns normalized lemma with PyMorphy tags
        """
        return f'{self.normalized_form}<{self.tags_mystem}>({self.tags_pymorphy})'


class CorpusManager:
    """
    Works with articles and stores them
    """

    def __init__(self, path_to_raw_txt_data: str):
        self.path = Path(path_to_raw_txt_data)
        self._storage = {}
        self._scan_dataset()

    def _scan_dataset(self):
        """
        Register each dataset entry
        """

        files = self.path.glob('*_raw.txt')

        pattern = re.compile(r'(\d+)')

        for file in files:
            if re.match(pattern, file.name).group(0).isdigit():
                article_id = int(re.match(pattern, file.name).group(0))
                self._storage[article_id] = Article(url=None, article_id=article_id)
            else:
                print("Unsuccessful article id extraction")

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
        articles = self.corpus_manager.get_articles().values()
        for article in articles:
            raw_text = article.get_raw_text()
            processed_tokens = self._process(raw_text)

            cleaned_tokens = []
            single_tagged_tokens = []
            multiple_tagged_tokens = []


            for processed_token in processed_tokens:
                cleaned_tokens.append(processed_token.get_cleaned())
                single_tagged_tokens.append(processed_token.get_single_tagged())
                multiple_tagged_tokens.append(processed_token.get_multiple_tagged())

            article.save_as(' '.join(cleaned_tokens), ArtifactType.cleaned)
            article.save_as(' '.join(single_tagged_tokens), ArtifactType.single_tagged)
            article.save_as(' '.join(multiple_tagged_tokens), ArtifactType.multiple_tagged)

    def _process(self, raw_text: str):
        """
        Processes each token and creates MorphToken class instance
        """
        # txt from pdf comes with words like след-ующий
        # this replace deals with them
        text = raw_text.replace('-\n', '').replace('\n', ' ')
        result = Mystem().analyze(text)
        # launching morph_tokens list which then is appended with MorphologicalToken class instances
        morph_tokens = []

        # pymorphy analyzer which will be used for filling pymorphy tags
        morph = pymorphy2.MorphAnalyzer()
        for token in result:

            # pre requisites for the token to be usable
            if "analysis" not in token:
                continue
            if not token.get('analysis'):
                continue
            if not (token['analysis'][0].get("gr") or token['analysis'][0].get("lex")):
                continue

            original_word = token["text"]

            morph_token = MorphologicalToken(original_word=original_word)

            # mystem tags
            morph_token.normalized_form = token['analysis'][0]['lex']
            morph_token.tags_mystem = token['analysis'][0]['gr']

            # pymorphy tags

            one_word = morph.parse(original_word)[0]
            morph_token.tags_pymorphy = one_word.tag

            morph_tokens.append(morph_token)

        return morph_tokens


def validate_dataset(path_to_validate):
    """
    Validates folder with assets
    """

    path = Path(path_to_validate)

    if not path.exists():
        raise FileNotFoundError

    if not path.is_dir():
        raise NotADirectoryError

    if not any(path.iterdir()):
        raise EmptyDirectoryError

    file_formats = [".json", ".txt", ".pdf", ".png"]
    checker = {}

    # creating a dictionary of file indexes
    # and checking the formats

    pattern = re.compile(r'\d+')

    for file in path.iterdir():

        match_to = re.match(pattern, file.name)

        if not match_to:
            raise InconsistentDatasetError("There is a file with incorrect name pattern.")

        if file.stat().st_size == 0:
            raise InconsistentDatasetError("File is empty.")

        file_index = file.name.split("_")[0]

        if file_index not in checker.keys():
            checker[file_index] = 1
        else:
            checker[file_index] += 1

        if file.suffix not in file_formats:
            raise FileNotFoundError("File with incorrect format.")

    # checking that there are necessary files with said index

    if not all(value >= 2 for value in checker.values()):
        raise InconsistentDatasetError("There are files missing.")

    # checking whether keys are consistent from 1 to N (max in files indices)
    current_i = list(int(x) for x in checker)
    ideal_i = range(1, max(current_i) + 1)

    if not set(current_i) & set(ideal_i) == set(ideal_i):
        raise InconsistentDatasetError("The numbering is inconsistent.")


def main():
    validate_dataset(ASSETS_PATH)
    corpus_manager = CorpusManager(ASSETS_PATH)
    pipeline = TextProcessingPipeline(corpus_manager)
    pipeline.run()


if __name__ == "__main__":
    main()
