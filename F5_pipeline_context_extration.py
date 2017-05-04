import pandas as pd
import os
import spacy
import re
import time
from collections import Counter

def get_np(parsed_doc):
    '''
    get a parsed document and return noun phrases
    with an index 1 word ahead of last word
    '''
    nps = []
    for np in parsed_doc.noun_chunks:
        nps.append((np.text,np.end)) # NOTE: np.end is 1 word ahead of actual word, use parsed_doc[np.end-1] to get last word in the phrase
    return nps

def wipe_useless_words(doc):
    '''
    doc:'   Impact:this is a test msg.   '
    new_doc:'this is a test msg.'
    '''
    new_doc = re.sub(' {2,}Impact {2,}',' ',doc)
    new_doc = re.sub(' {2,}','',new_doc)
    new_doc = re.sub('.Note:','. ',new_doc)
    return new_doc

def yield_parsed_document(list_of_documents):
    '''
    run parsing in multiple threads to speed up the process
    '''
    for parsed_document in nlp.pipe(list_of_documents,
                                  batch_size=10000, n_threads=4):
        yield parsed_document

def head_off(np):
    '''
    transform noun phrases into lower case, and remore punct words ahead of them
    '''
    np_list = map(lambda x:x.lower(),np[0].split(' '))
    punct_words = ['a','an','the','this','that','these','those','it']
    return ' '.join(np_list) if np_list[0] not in punct_words else ' '.join(np_list[1:]),np[1]

def in_title(title_words,np):
    ''''
    check if a noun phrase has at least one word in the title
    '''
    for word in np[0].split(' '):
        if word.lower() in title_words:
            return True
    return False

def filter_nps(title,nps):
    '''
    do head off and check if noun phrases have words in the title
    '''
    title_words = map(lambda x:x.lower(),title.split(' '))
    nps_head_off = map(head_off,nps)
    return filter(lambda p:in_title(title_words,p),nps_head_off)

def sort_nps(nps):
    '''
    count frequency of noun phrases and sort in decreasing order
    '''
    nps_lower = map(lambda x:x.lower(),nps)
    return Counter(nps_lower).most_common()

def find_nps_verb(parsed_doc,np_indexes):
    '''
    parsed_doc: document, in nlp parsed format
    np_index: index of noun phrase last word, from function find_np_index()
    finds connecting verb of a single noun phrase
    '''
    result = []
    for np_index in np_indexes:
        tmp = []
        token = parsed_doc[np_index-1].head # span.end is 1 ahead of actual ending word so np_index-1
        while token.head is not token and token.pos_ != 'VERB':
            if token.pos_ in ['NOUN'] and token.dep_ not in ['compound','conj']:
                tmp.append(token.text)
            token = token.head
        tmp.append(token.text)
        result.append(tmp)
    return result

def sort_verbs(nps_verb):
    '''
    count frequency of verbs/nouns and sort in decreasing order
    '''
    all_verbs = []
    for i in nps_verb:
        all_verbs.extend(i)
    return Counter(all_verbs).most_common()

def combine_np_and_verb(nps_text,nps_verb):
    '''
    nps_text: noun phrases of a single document
    nps_verb: all useful_nps related verbs/sentence head of a single document
    '''
    assert len(nps_text) == len(nps_verb)
    return zip(nps_text,nps_verb)

# load Spacy English model
nlp = spacy.load('en')

# set file path
files_path = './files'

file_path = os.path.join(files_path,'F5_context_extraction_final.xlsx')
if not os.path.isfile(file_path):
    # read file
    file_path = os.path.join(files_path,'F5_concat_detail_cleaned.xlsx')
    data = pd.read_excel(file_path)
    docs = data.clean_detail

    # get tight detail
    print 'Transform clean detail into tight detail'
    tight_detail = map(wipe_useless_words,docs)

    # get noun phrases
    all_nps = []

    start = time.time()
    print 'Get Noun phrases...'
    for parsed_doc in yield_parsed_document(tight_detail):
        nps = get_np(parsed_doc)
        all_nps.append(nps)
    print 'Done. Time used:',time.time()-start

    assert len(all_nps) == len(data)

    # filter noun phrases
    all_nps = [map(lambda x:x if x[-1] != ' ' else x[:-1],all_nps[i]) for i in range(len(all_nps))] # get rid of extra space in the end
    useful_nps = map(lambda title,nps:filter_nps(title,nps),data['Article/Title'],all_nps)

    nps_verb_indexes = map(lambda x:map(lambda np_index:np_index[1],x),useful_nps) # get list of index of nps in every parsed doc
    nps_text = map(lambda x:map(lambda np_index:np_index[0],x),useful_nps) # get list of nps text in every parsed doc
    useful_nps_collections = map(sort_nps,nps_text) # count freqs of nps for every parsed doc

    # get connecting verbs/nouns of filtered noun phrases
    ## if want to get other words connecting noun phrases, modify in find_nps_verb()
    print 'Get important verbs/head for useful nps...'
    start = time.time()
    nps_verb_list = []
    for i in range(len(tight_detail)):
        parsed_doc = nlp(tight_detail[i])
        nps_verb = find_nps_verb(parsed_doc,nps_verb_indexes[i])
        nps_verb_list.append(nps_verb)

    nps_verb_collection = map(sort_verbs,nps_verb_list)
    print 'Done. Time used:',time.time()-start

    all_nps_text = [map(lambda x:x[0].lower(),i) for i in all_nps]

    # add into columns
    data['tight_detail'] = tight_detail
    data['all_noun_phrases'] = all_nps_text
    data['useful_nps_verb_combination'] = map(lambda x,y:zip(x,y),nps_text,nps_verb_list)
    useful_nps_collections = map(sort_nps,nps_text)
    data['useful_nps_collections'] = useful_nps_collections
    data['nps_verb_collection'] = nps_verb_collection

    # write result file
    file_path = os.path.join(files_path,'F5_context_extraction_final.xlsx')
    if not os.path.isfile(file_path):
        print 'Writing {}'.format(file_path)
        data.to_excel(file_path,encoding='utf_8')
else:
    data = pd.read_excel(file_path)
    data.head(2)
