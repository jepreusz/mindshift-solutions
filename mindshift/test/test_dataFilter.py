from unittest import TestCase
from mindshift.preprocess import data_filter


class TestDataFilter(TestCase):
    def test_rm_stopwords(self):
        data_filt = data_filter.DataFilter()
        cleaned_text = data_filt.rm_stopwords('\n\n\n\n\nwhat the '
                                              'is this'
                                              ''
                                              ''
                                              ' non-sense')
        print(cleaned_text)

    def test_rm_blanklines(self):
        data_filt = data_filter.DataFilter()
        cleaned_text = data_filt.rm_blanklines('what the '
                                               '\n\n\nis this'
                                               ''
                                               ''
                                               ' non-sense')
        print(cleaned_text)
