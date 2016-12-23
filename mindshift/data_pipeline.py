# top level script to orchestrate data pre-processing & processing
from mindshift.extract import extractor
from mindshift.preprocess import data_filter, transformer
import argparse
import pandas


class DataPipeline:

    def __init__(self, source_dir):
        self.dataset_directory = source_dir
        self.data_extractor = extractor.Extractor(self.dataset_directory)
        self.datafilter = data_filter.DataFilter()
        self.data_transformer = transformer.Transformer()

    def load_data(self):
        return self.data_extractor.as_dataframe()

    def preprocess_data(self, data):
        return self.datafilter.rm_blanklines(self.datafilter.rm_stopwords(str(data)))

    def transform_data(self, data):
        return self.data_transformer.vectorize_text(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter source data location and action to perform on data',
                                     usage='data_pipeline source_data --task [show|preprocess|transform|process]')
    parser.add_argument('src_data', help='source data file or directory')
    parser.add_argument('--task', '-t', choices=['show', 'preprocess', 'transform', 'process'], default='show')
    parser.add_argument('--preprocess', '-p', action='store_true', help='pre-process data? [True|False]')
    args = parser.parse_args()
    pipeline = DataPipeline(args.src_data)
    if args.task == 'show':
        print(pipeline.load_data())
    elif args.task == 'transform':
        df = pipeline.load_data()
        clean_data = pandas.DataFrame(df.apply(pipeline.preprocess_data, axis=1))
        clean_data.columns = ['content']
        print(clean_data)
