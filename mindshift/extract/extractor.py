# script to read source data and provide a handle to it
import pandas
from mindshift.util import filehandler
import os


class Extractor:

    def __init__(self, source_dir):
        self.dataset_dir = source_dir
        self.file_handler = filehandler.FileHandler()

    # read data from source files
    def get_data_from_files(self):
        for file in self.file_handler.list_files(self.dataset_dir):
            full_filename = self.dataset_dir + os.path.sep + file
            yield file, self.file_handler.read_file(full_filename)

    # helper function to load data into dataframe
    def _load_data_into_dict(self):
        data_item = {}
        for data in self.get_data_from_files():
            data_item[data[0]] = data[1]
        # print(data_item)
        return data_item

    # return the data as a pandas dataframe
    def as_dataframe(self):
        df = pandas.DataFrame.from_dict(self._load_data_into_dict(), orient='index')
        df.columns = ['content']
        return df
