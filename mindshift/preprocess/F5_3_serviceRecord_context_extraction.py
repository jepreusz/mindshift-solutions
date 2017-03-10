import pandas as pd

# data = pd.read_excel(os.path.join(data_files_path,'F5_concat_detail_normalized_wstop.xlsx'))

# build product_names, actions, effects from given taxonomy
products = pd.read_excel('F5 Symptom Taxonomy Map_IU Project.xlsx',sheetname = 'Product Map')
actions = pd.read_excel('F5 Symptom Taxonomy Map_IU Project.xlsx',sheetname = 'Frame - Action')
effects = pd.read_excel('F5 Symptom Taxonomy Map_IU Project.xlsx',sheetname = 'Frame - Effect')

products = products['Primary  Products'].values
actions = actions['ACTION'].values
effects = effects['Frame - Effects'].values

def no_space_dash(elements):
    result = map(lambda x:x.replace('-','_'),elements)
    result = map(lambda x:x.replace(' ','_'),result)
    return result

def lower(elements):
    return map(lambda x:x.lower(),elements)

products = lower(products)
products[4] = 'big_ip' # original: BIG-IP (4.x)
products2 = no_space_dash(products)
products2.extend(products)
product_set = set(products2)

actions = lower(actions)
actions = map(lambda x:x[:-2],actions)
actions2 = no_space_dash(actions)
actions2.extend(actions)
action_set = set(actions2)

effects = lower(effects)
effects = map(lambda x:x[:-2],effects)
effects2 = no_space_dash(effects)
effects2.extend(effects)
effect_set = set(effects2)


from gensim.models import Phrases
model_path = os.path.join('.','models')
bigram_model_path = os.path.join(model_path,'bigram_model_wstop')
bigram_model = Phrases.load(bigram_model_path)

def lemmatize_nonstop(record):
    return [token.lemma_ for token in nlp(record) if not (token.is_stop and token.orth_ != 'not')] # not is a stop word but we don't want to lose it

def bigram(record,model):
    return ' '.join(model[record.split(' ')])

def simplify_record(record,bigram_model):
    # normalize record: bigram,lemmatize, not_stop_words
    bigram_record = bigram(record,bigram_model)
    lemmatized_record = lemmatize_nonstop(bigram_record)
    # matching records with shrinked_documents
    return lemmatized_record

test_record = u'a flow in firepass client side is making big ip not responsive'
# match service record with all these sets
matched_product,matched_action,matched_effect = [],[],[]
for word in bigram_model[lower(test_record.split(' '))]:
    if word in product_set:
        matched_product.append(word)
    elif word in action_set:
        matched_action.append(word)
    elif word in effect_set:
        matched_effect.append(word)

def find_k_closest(k,search_range,original_record,word2vec_model,bigram_model):
    words = simplify_record(original_record,bigram_model)
    tags = [token.pos_ for i,token in enumerate(nlp(bigram(original_record,bigram_model))) if token.lemma_ in words]
    assert len(words)==len(tags)

    distances = []
    for i in xrange(len(words)):
        if words[i] in word2vec_model and tags[i]=='NOUN':
            anchor = words[i]
            for j in xrange(i+1,min(i+search_range,len(words))):
                if tags[j] != tags[i] and words[i] != words[j] and words[j] in word2vec_model:
                    distances.append((words[i],words[j],word2vec_model.similarity(words[i],words[j])))
            distances.sort(key=lambda x:-x[2])

    return distances[:k] if len(distances)>k else distances

from gensim.models import Word2Vec
word2vec_model = Word2Vec.load(os.path.join(model_path,'model_size100_wstop'))

print test_record
print find_k_closest(k=10,search_range=3,test_record,word2vec_model,bigram_model)
