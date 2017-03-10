import os
import codecs
import pandas as pd

# set output files and models paths
model_path = os.path.join('.','models')
data_files_path = os.path.join('.','files')
unigram_sentences_path = os.path.join(model_path,'unigram_sentences_wstop_all.txt')
bigram_model_path = os.path.join(model_path,'bigram_model_wstop')

# load data from preprocessing step
data = pd.read_excel('F5_concat_detail_cleaned.xlsx')
documents = data.clean_detail.tolist()

# replace text with '-' and '&nbsp'
replaced_documents = []
for doc in documents:
    tmp = doc.replace('-','_')
    tmp = tmp.replace('&nbsp','')
    replaced_documents.append(tmp)

import codecs
import spacy
# need to download spacy english corpus, takes about 10 mins
nlp = spacy.load('en')

def punct_stop_space(token):
    """
    helper function to eliminate tokens
    that are pure punctuation or whitespace
    """
    # don't remove stop words because word2vec model uses skip-gram
    # so no need
    return token.is_punct or token.is_space

def lemmatized_sentence_corpus(list_of_documents):
    """
    generator function to use spaCy to parse sentences,
    lemmatize them, and yield sentences(several sentences
    per document)
    """

    for parsed_review in nlp.pipe(list_of_documents,
                                  batch_size=10000, n_threads=4):
        for sentence in parsed_review.sents:
            yield u' '.join([token.lemma_ for token in sentence if not punct_stop_space(token)])

# build unigram sentence corpus(to train bigram model later)

if 1 == 0:
    with codecs.open(unigram_sentences_path,'w',encoding='utf-8') as f:
        for sentence in lemmatized_sentence_corpus(replaced_documents):
            f.write(sentence+'\n')

    from gensim.models import Phrases
    from gensim.models.word2vec import LineSentence

    # load unigram sentence corpus
    unigram_sentences = LineSentence(unigram_sentences_path)

    # training bigram_model
    bigram_model = Phrases(unigram_sentences)
    bigram_model.save(bigram_model_path)

def lemmatized_document(list_of_documents):
    """
    generator function to use spaCy to parse documents,
    lemmatize them, and yield, one per document
    """

    for parsed_review in nlp.pipe(list_of_documents,
                                  batch_size=10000, n_threads=4):
        yield [token.lemma_ for token in parsed_review if not punct_stop_space(token)]

if 1 == 0:
    unigram_documents = lemmatized_document(replaced_documents)
    unigram_documents_path = os.path.join(model_path,'unigram_documents_wstop.txt')
    with codecs.open(unigram_documents_path,'w',encoding='utf_8') as f:
        for unigram_document in unigram_documents:
            f.write(unigram_document + '\n')

bigram_model = Phrases.load(bigram_model_path)
bigram_documents_path = os.path.join(model_path,'bigram_documents_wstop.txt')

if 1 == 0:
    with codecs.open(bigram_documents_path, 'w', encoding='utf_8') as f:

        for unigram_document in unigram_documents:

            bigram_document = u' '.join(bigram_model[unigram_document])

            f.write(bigram_document + '\n')

bigram_documents = LineSentence(bigram_documents_path)
normalized_detail = []
for i in bigram_documents:
    normalized_detail.append(u' '.join(i))

data['normalized_detail'] = normalized_detail

data.to_excel(os.path.join(data_files_path,'F5_concat_detail_normalized_wstop.xlsx'),encoding='utf8')

# if prefer to use clean unigram text over clean bigram text, use this:
if 1 == 0:
    unigram_documents = lemmatized_document(replaced_documents)
    unigram_documents_path = os.path.join(model_path,'unigram_documents_wstop.txt')
    with codecs.open(unigram_documents_path,'w',encoding='utf_8') as f:
        for unigram_document in unigram_documents:
            tmp = ' '.join(unigram_document)
            f.write(tmp + '\n')
