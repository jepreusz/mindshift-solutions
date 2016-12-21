from unittest import TestCase
from mindshift.preprocess import data_filter


class TestDataFilter(TestCase):
    def test_rm_stopwords(self):
        data_filt = data_filter.DataFilter()
        cleaned_text = data_filt.rm_stopwords('what the '
                                              'fuck is this'
                                              ''
                                              ''
                                              ' non-sense')
        print(cleaned_text)
