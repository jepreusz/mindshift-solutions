# top level script to orchestrate data pre-processing & processing
from mindshift.extract import extractor
from mindshift.preprocess import data_filter, transformer
from mindshift.process import clustering
import argparse
import pandas
import pickle


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

    def transform_data(self, data, model="bag of words"):
        if model == "bag of words":
            return self.data_transformer.vectorize_text(data)
        elif model == "lda":
            return self.data_transformer.lda_vectorize_text(data)

    def process_data(self, data, alg='kmeans'):
        if alg == 'kmeans':
            return self.processor.do_kmeans(data)
        elif alg == 'hierarchical':
            Z = self.data_transformer.get_cosine(data)
            return self.processor.do_ward(Z)
        elif alg == 'lda':
            return self.processor.do_lda_sk(data)

    def export_results(self, filename, *dataframes, **fileparams):
        file_format = fileparams['format']
        if file_format == 'xlsx':
            writer = pandas.ExcelWriter(filename)
            for ind, dataframe in enumerate(dataframes):
                sheet_name = fileparams['sheet_names'][ind]
                keep_index = fileparams['indices'][ind]
                dataframe.to_excel(writer, sheet_name=sheet_name, engine='xlsxwriter', index=keep_index)
            writer.save()
            writer.close()
        elif file_format == 'csv':
            dataframes[0].to_csv(filename)


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
        vectorized_data = pipeline.transform_data(df['content'])
        with open("corpus_vocab", 'wb') as file:
            pickle.dump(pipeline.data_transformer.get_vocabulary(), file)
    elif args.task == 'process':
        df = pipeline.load_data()
        vectorized_data = pipeline.transform_data(df['content'])
        labels = pipeline.process_data(vectorized_data, alg='kmeans')
        clustered_df = df.join(pandas.DataFrame(labels, index=df.index))
        clustered_df.columns = ['Content', 'Cluster ID']
        clustered_df.index.name = 'Article ID'
        cluster_terms_df = pandas.DataFrame(pipeline.processor.get_top_cluster_terms(pipeline.data_transformer.
                                                                                     get_features()))
        cluster_terms_df.index.name = 'Cluster ID'
        cluster_terms_df.columns = ['Top Terms']
        lda_df = pandas.DataFrame()
        for ind in range(50):
            vectorized_data = pipeline.transform_data(clustered_df[clustered_df['Cluster ID'] == ind]['Content'])
            pipeline.process_data(vectorized_data, alg='lda')
            topics = pipeline.processor.get_top_cluster_terms(pipeline.data_transformer.get_features(), model='lda')
            temp_df = pandas.DataFrame([[ind, i, topic] for i, topic in enumerate(topics)])
            lda_df = lda_df.append(temp_df)
        lda_df.columns = ['Cluster ID', 'Topic ID', 'Top Topic Keywords']
        pipeline.export_results('Mindshift Clustering Spreadsheet v11 - unigrams - 50 clusters - 10,791 documents.xlsx', clustered_df,
                                cluster_terms_df, lda_df, format='xlsx',
                                sheet_names=['clusters', 'top cluster terms', 'top cluster topics'],
                                indices=[True, True, False])
