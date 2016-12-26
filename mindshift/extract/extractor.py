# script to read source data and provide a handle to it
import pandas
from mindshift.util import filehandler
import os
from mindshift.preprocess import data_filter


class Extractor:

    def __init__(self, source_dir, clean=False):
        self.dataset_dir = source_dir
        self.file_handler = filehandler.FileHandler()
        self.clean = clean
        self.data_filter = data_filter.DataFilter()

    # read data from source files
    def get_data_from_files(self):
        for file in self.file_handler.list_files(self.dataset_dir):
            full_filename = self.dataset_dir + os.path.sep + file
            yield file, self.file_handler.read_file(full_filename)

    # apply pre-processing/cleaning to data
    def _clean_data(self, data):
        return self.data_filter.rm_stopwords(data)

    # helper function to load data into dataframe
    def _load_data_into_dict(self):
        data_item = {}
        for data in self.get_data_from_files():
            if self.clean:
                data_item[data[0]] = self._clean_data(data[1])
            else:
                data_item[data[0]] = data[1]
        # print(data_item)
        return data_item

    # return the data as a pandas dataframe
    def as_dataframe(self):
        df = pandas.DataFrame.from_dict(self._load_data_into_dict(), orient='index')
        df.columns = ['content']
        return df
