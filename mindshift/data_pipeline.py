# top level script to orchestrate data pre-processing & processing
from mindshift.extract import extractor
from mindshift.preprocess import data_filter, transformer
from mindshift.process import clustering
import argparse
import pandas


class DataPipeline:

    def __init__(self, source_dir, clean=False):
        self.dataset_directory = source_dir
        self.data_extractor = extractor.Extractor(self.dataset_directory, clean)
        self.datafilter = data_filter.DataFilter()
        self.data_transformer = transformer.Transformer()
        self.processor = clustering.Cluster()

    def load_data(self):
        return self.data_extractor.as_dataframe()

    def preprocess_data(self, data):
        return self.datafilter.rm_stopwords(str(data))

    def transform_data(self, data):
        return self.data_transformer.vectorize_text(data)

    def process_data(self, data, alg='kmeans'):
        if alg == 'kmeans':
            return self.processor.do_kmeans(data)
        elif alg == 'hierarchical':
            Z = self.data_transformer.get_cosine(data)
            return self.processor.do_ward(Z)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Enter source data location and action to perform on data',
                                     usage='data_pipeline source_data --task [show|preprocess|transform|process]')
    parser.add_argument('src_data', help='source data file or directory')
    parser.add_argument('--task', '-t', choices=['show', 'preprocess', 'transform', 'process'], default='show')
    parser.add_argument('--preprocess', '-pp', action='store_true', help='pre-process data? [True|False]')
    args = parser.parse_args()
    pipeline = DataPipeline(args.src_data, clean=False)
    if args.task == 'show':
        print(pipeline.load_data())
    elif args.task == 'transform':
        df = pipeline.load_data()
        # clean_data = pandas.DataFrame(df.apply(pipeline.preprocess_data, axis=1))
        # clean_data.columns = ['content']
        vectorized_data = pipeline.transform_data(df['content'])
        # print(vectorized_data.toarray())
        print(pipeline.data_transformer.get_features())
        labels = pipeline.process_data(vectorized_data, alg='kmeans')
        clustered_df = df.join(pandas.DataFrame(labels, index=df.index))
        print(clustered_df)
        clustered_df.columns = ['content', 'cluster_id']
        clustered_df.to_csv('./cluster_output.csv')
