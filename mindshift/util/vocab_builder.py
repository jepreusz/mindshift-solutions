# create a custom vocabulary by reading a file with busniess terms

import fileinput


class VocabBuilder:

    def __init__(self, file):
        self.source_file = file
        self.vocab = set([])

    def build_vocab(self):
        for term in fileinput.input(self.source_file):
            self.vocab.add(term.replace("\n", "").strip())
        return self.vocab
