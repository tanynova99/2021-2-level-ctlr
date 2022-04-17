"""
Tests for POS frequency pipeline
"""
import json
import shutil
import unittest

import pytest

from constants import ASSETS_PATH, PROJECT_ROOT
from pipeline import CorpusManager, TextProcessingPipeline, validate_dataset
from pos_frequency_pipeline import POSFrequencyPipeline, EmptyFileError
from config.test_params import TEST_FILES_FOLDER


MYSTEM_TAGS = ['A', 'ADV', 'ADVPRO', 'ANUM', 'APRO', 'COM', 'CONJ',
               'INTJ', 'NUM', 'PART', 'PR', 'S', 'SPRO', 'V']
TEST_TMP = PROJECT_ROOT / 'tmp_tests'


class PosFrequencyPipelineTests(unittest.TestCase):
    """
    Class for testin POSFrequencyPipeline realization
    """

    @classmethod
    def setUpClass(cls) -> None:
        validate_dataset(ASSETS_PATH)
        shutil.copytree(ASSETS_PATH, TEST_TMP)  # cash ASSETS_PATH state before
                                                # modifying it for testing
        shutil.copyfile(TEST_FILES_FOLDER / "0_raw.txt",
                        ASSETS_PATH / "0_raw.txt")
        shutil.copyfile(TEST_FILES_FOLDER / "0_meta.json",
                        ASSETS_PATH / "0_meta.json")

        cls.corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        path = cls.corpus_manager.get_articles()[0].get_meta_file_path()
        with open(path, 'r', encoding='utf-8') as meta_file:
            meta = json.load(meta_file)
        cls.frequencies = meta.pop('pos_frequencies')
        with open(path, 'w', encoding='utf-8') as meta_file:
            json.dump(meta,
                      meta_file,
                      sort_keys=False,
                      indent=4,
                      ensure_ascii=False,
                      separators=(',', ': '))

        pipe = TextProcessingPipeline(cls.corpus_manager)
        pipe.run()
        pos_pipe = POSFrequencyPipeline(cls.corpus_manager)
        pos_pipe.run()

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    def test_meta_files_readable(self):
        """
        Ensure meta files are not corrupt
        """
        failed = False
        try:
            article = self.corpus_manager.get_articles()[0]
            path = article.get_meta_file_path()
            with open(path, 'r', encoding='utf-8') as meta_file:
                json.load(meta_file)
        except json.decoder.JSONDecodeError:
            failed = True
        finally:
            message = 'Generated meta files are corrupt: ' \
                      'check how you update .json files'
            self.assertFalse(failed, message)

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    def test_frequencies_are_correct(self):
        """
        Ensure frequencies are counted correctly
        """
        article = self.corpus_manager.get_articles()[0]
        path = article.get_meta_file_path()
        with open(path, 'r', encoding='utf-8') as meta_file:
            frequencies = json.load(meta_file)['pos_frequencies']
        self.assertEqual(self.frequencies, frequencies,
                         'POS frequencies are calculated incorrectly')

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    def test_tags_are_mystem(self):
        """
        Ensure that mystem tags are used
        """
        article = self.corpus_manager.get_articles()[0]
        path = article.get_meta_file_path()
        with open(path, 'r', encoding='utf-8') as meta_file:
            pos_tags = json.load(meta_file)['pos_frequencies'].keys()
        for tag in pos_tags:
            self.assertTrue(tag in MYSTEM_TAGS,
                            msg=f"Tag {tag} not in list of known mystem tags")

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    def test_images_are_generated(self):
        """
        Ensure images are generated
        """
        msg = 'POSFrequencyPipeline does not create image ' \
              'file for at least one of articles available'
        extract_id = lambda filename: int(str(filename.name).split('_')[0])
        ids_available = set(list(map(extract_id, ASSETS_PATH.iterdir())))
        for identifier in ids_available:
            path = ASSETS_PATH / f'{identifier}_image.png'
            self.assertTrue(path.is_file(), msg)

    @pytest.mark.mark10
    @pytest.mark.stage_4_pos_frequency_pipeline_checks
    def test_empty_file_exception_thrown(self):
        """
        Ensure that in case empty file is encountered right exception is thrown
        """
        msg1 = 'POSFrequencyPipeline does not ' \
               'throw exception when fed empty file'
        msg2 = 'POSFrequencyPipeline throws ' \
               'inappropriate exception when fed empty file'

        # create empty files with the unlikeliest to be reserved names
        chunks = ['_raw.txt', '_single_tagged.txt', '_multiple_tagged.txt']
        for chunk in chunks:
            path = ASSETS_PATH / ('1000' + chunk)
            with open(path, 'w', encoding='utf-8') as file:
                file.write('')

        corpus_manager = CorpusManager(path_to_raw_txt_data=ASSETS_PATH)
        exception_is_thrown = False
        exception_is_correct = True

        try:
            POSFrequencyPipeline(corpus_manager=corpus_manager).run()
        except EmptyFileError:
            exception_is_thrown = True
        except Exception: # pylint: disable=broad-except
            exception_is_thrown = True
            exception_is_correct = False

        for chunk in chunks:
            path = ASSETS_PATH / ('1000' + chunk)
            path.unlink()

        self.assertTrue(exception_is_thrown, msg1)
        self.assertTrue(exception_is_correct, msg2)

    @classmethod
    def tearDownClass(cls) -> None:
        shutil.rmtree(ASSETS_PATH)  # cleaning and restoring original state
        shutil.copytree(TEST_TMP, ASSETS_PATH)
        shutil.rmtree(TEST_TMP)
