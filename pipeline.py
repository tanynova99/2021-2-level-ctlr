"""
Pipeline for text processing implementation
"""

from pathlib import Path

from constants import ASSETS_PATH


class EmptyDirectoryError(Exception):
    """
    No data to process
    """


class NotDirectoryError(Exception):
    """
    Not a directory
    """


class InconsistentDatasetError(Exception):
    """
    Corrupt data: numeration is expected to start from 1 and to be continuous
    """


class FileNotFoundError(Exception):
    """
    """


class MorphologicalToken:
    """
    Stores language params for each processed token
    """

    def __init__(self, original_word):
        pass

    def get_cleaned(self):
        """
        Returns lowercased original form of a token
        """
        pass

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
        pass

    def _scan_dataset(self):
        """
        Register each dataset entry
        """
        pass

    def get_articles(self):
        """
        Returns storage params
        """
        pass


class TextProcessingPipeline:
    """
    Process articles from corpus manager
    """

    def __init__(self, corpus_manager: CorpusManager):
        pass

    def run(self):
        """
        Runs pipeline process scenario
        """
        pass

    def _process(self, raw_text: str):
        """
        Processes each token and creates MorphToken class instance
        """
        pass


def validate_dataset(path_to_validate):
    """
    Validates folder with assets
    """

    if not path_to_validate.is_dir():
        raise NotADirectoryError

    if not any(Path(path_to_validate).iterdir()):
        raise EmptyDirectoryError

    file_formats = [".json", ".txt", ".pdf"]
    files = path_to_validate.iterdir()
    for i, file in enumerate(files, 1):
        if str(i) != str(file.name)[0]:
            raise InconsistentDatasetError
        if file.suffix not in file_formats:
            raise FileNotFoundError

    return None


def main():
    # YOUR CODE HERE
    validate_dataset(ASSETS_PATH)


if __name__ == "__main__":
    main()
