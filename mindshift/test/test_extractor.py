from unittest import TestCase
from mindshift.extract import extractor
import configparser


class TestExtractor(TestCase):
    def test_get_data_from_files(self):
        cfg = configparser.ConfigParser()
        cfg.read('../config/default.cfg')
        dataset_dir = cfg.get('source', 'files.directory')
        data_extractor = extractor.Extractor(dataset_dir)
        data_extractor.get_data_from_files()

    def test_as_dataframe(self):
        cfg = configparser.ConfigParser()
        cfg.read('../config/default.cfg')
        dataset_dir = cfg.get('source', 'files.directory')
        data_extractor = extractor.Extractor(dataset_dir)
        print(data_extractor.as_dataframe())
