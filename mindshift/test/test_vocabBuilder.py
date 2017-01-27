from unittest import TestCase
from mindshift.util import vocab_builder


class TestVocabBuilder(TestCase):
    def test_build_vocab(self):
        vb = vocab_builder.VocabBuilder("C:\\Users\\ramji\\PycharmProjects\\mindshift-solutions\\mindshift\\dataFiles\\busniess_terms.txt")
        vocab = vb.build_vocab()
        print(vocab)
