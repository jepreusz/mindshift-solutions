# Parts of speech tagging on Call records, to extract context information
from nltk.tag import pos_tag
from nltk import NgramTagger
from nltk.corpus import brown, treebank
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
import pandas
import configparser
import os


class ContextExtractor:

    def __init__(self):
        self.pos_tagger = None
        self.config_handler = configparser.ConfigParser()
        self.script_dir = os.path.dirname(__file__)
        self._load_config()

    def _load_config(self):
        self.config_handler.read(os.path.abspath(os.path.join(self.script_dir, "..", "config", "default.cfg")))

    def get_context_params(self, call_record):
        return pos_tag([word for word in word_tokenize(call_record) if word.lower() not in stopwords.words()])

    def tag_pos(self, data):
        pass

    def train_hmm(self, trainingCorpus):
        pass

    def load_training_data(self):
        training_filename = self.config_handler.get('context-extraction', 'training_data.file')
        training_data_col_name = self.config_handler.get('context-extraction', 'training_data.header.name')
        with open(training_filename, 'rb') as training_file:
            training_dataframe = pandas.read_excel(training_file, header=0)
        return training_dataframe[training_data_col_name]






ce = ContextExtractor()
ce.load_training_data()


