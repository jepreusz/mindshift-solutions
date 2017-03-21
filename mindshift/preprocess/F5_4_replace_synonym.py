import pandas as pd
import spacy
nlp = spacy.load('en')

synonym = pd.read_excel('F5 Symptom Taxonomy Map_IU Project.xlsx',sheetname = 'Synonym Map')

for col in range(synonym.shape[1]):
    synonym.ix[:,col] = map(lambda x:' '.join([token.lemma_ for token in nlp(unicode(x))]),synonym.ix[:,col].values)
    synonym.ix[:,col] = map(lambda x:re.sub(' {2,}','',x),synonym.ix[:,col].values) # drop more than 1 spalces in the end of words
    synonym.ix[:,col] = map(lambda x:re.sub(' [/|-] | {1}|-','_',x),synonym.ix[:,col].values) # replace " / "," " and "-" with "_"

synonym_dict = dict(zip(synonym['Synonym / Customer Language Terms'],synonym['Primary Term']))
synonym_dict_copy = synonym_dict.copy()
for key in synonym_dict_copy:
    if key[::-1].startswith('sserdda'):
        del synonym_dict[key]

data = pd.read_excel('./files/F5_concat_detail_normalized_wstop.xlsx'))

def replace_synonym(document,synonym_dict):
    tokens = document.split(' ')
    for i in range(len(tokens)):
        word = tokens[i]
        if word in synonym_dict:
            tokens[i] = synonym_dict[word]
    return ' '.join(tokens)

data['synonym_detail'] = map(lambda x:replace_synonym(x,synonym_dict),data.normalized_detail)
del data['clean_detail']

if not os.path.exists('./files/F5_concat_detail_synonym.xlsx'):
    data.to_excel('./files/F5_concat_detail_synonym.xlsx')
