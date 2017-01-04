# Parts of speech tagging on Call records, to extract context information
from nltk.tag import pos_tag
from nltk import NgramTagger
from nltk.corpus import brown
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


class ContextExtractor:

    def __init__(self):
        self.pos_tagger = None
        # self.pos_tagger = NgramTagger(2, brown)

    def get_context_params(self, call_record):
        return pos_tag([word for word in word_tokenize(call_record) if word.lower() not in stopwords.words()])

ce = ContextExtractor()
print(ce.get_context_params("Cannot access web Gui"))
