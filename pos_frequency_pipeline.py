"""
Implementation of POSFrequencyPipeline for score ten only.
"""
import json
import re

from constants import ASSETS_PATH
from core_utils.article import ArtifactType
from core_utils.visualizer import visualize
from pipeline import CorpusManager, validate_dataset


class EmptyFileError(Exception):
    """
    Custom error
    """


class IncorrectFormatError(Exception):
    """
    Custom error
    """


class POSFrequencyPipeline:
    def __init__(self, corpus_manager: CorpusManager):
        self.corpus_manager = corpus_manager

    def run(self):
        """
        Running the pipeline scenario
        """

        for article in self.corpus_manager.get_articles().values():
            
            # get the file to take the pos tags from
            with open(article.get_file_path(ArtifactType.single_tagged), encoding="utf-8") as st_file:
                morph_text = st_file.read()

            validate_input(morph_text)
            freqs = self._generate_freqs_pos(morph_text)

            # TASK
            freqs_cases = self._generate_freqs_n_cases(morph_text)

            # save calculated freqs to meta file
            with open(ASSETS_PATH / article.get_meta_file_path(), encoding="utf-8") as m_file:
                meta_info = json.load(m_file)

            meta_info.update({"pos_frequencies": freqs})

            with open(ASSETS_PATH / article.get_meta_file_path(), "w", encoding="utf-8") as m_file:
                json.dump(meta_info, m_file, indent=4, ensure_ascii=False, separators=(',', ':'))

            # visualise results
            visualize(statistics=freqs, path_to_save=ASSETS_PATH / f"{article.article_id}_image.png")
            visualize(statistics=freqs_cases, path_to_save=ASSETS_PATH / f"{article.article_id}_case_image.png")

    def _generate_freqs_pos(self, text):

        freqs_dict = {}

        pos_pattern = re.findall(r"<([A-Z]+)", text)

        for pos in pos_pattern:
            freqs_dict[pos] = freqs_dict.get(pos, 0) + 1

        return freqs_dict

    def _generate_freqs_n_cases(self, text):

        freqs_dict = {}

        nouns = re.findall(r"<S.*>", text)
        cases_search = re.compile(r"([а-я]+),(?=мн|ед)")
        cases_names = ["им", "род", "дат", "вин", "твор", "пр", "парт", "местн", "зват"]

        for noun in nouns:
            cases = re.findall(cases_search, noun)
            for case in cases:
                if case in cases_names:
                    freqs_dict[case] = freqs_dict.get(case, 0) + 1

        return freqs_dict


def validate_input(to_validate):

    if not to_validate:
        raise EmptyFileError("There is nothing in the file.")

    if not isinstance(to_validate, str):
        raise IncorrectFormatError("The file should be read into string.")


def main():
    validate_dataset(ASSETS_PATH)
    corpus_manager = CorpusManager(ASSETS_PATH)
    pipeline = POSFrequencyPipeline(corpus_manager=corpus_manager)
    pipeline.run()


if __name__ == "__main__":
    main()
