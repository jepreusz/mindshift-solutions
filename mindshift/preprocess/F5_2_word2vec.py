# pip install --upgrade gensim
import os
# word2vec

from gensim.models import Word2Vec
# let's try small size,no parallel to set baseline

if 1 == 0:
    sentences = data.normalized_detail.tolist()

    model = Word2Vec(sentences,min_count=5,size=50) # bigger size require larger amount of data, but is more accurate.
    model.save(os.path.join(model_path,'model_size50_wstop'))

    model = Word2Vec(sentences,min_count=5,size=100)
    model.save(os.path.join(model_path,'model_size100_wstop'))

    model = Word2Vec(sentences,min_count=5,size=200)
    model.save(os.path.join(model_path,'model_size200_wstop'))

model_path = os.path.join('.','models')
loaded_model = Word2Vec.load(os.path.join(model_path,'model_size100_wstop'))

print loaded_model.most_similar(positive=['big_ip_ltm','failure'])

print loaded_model['big_ip']
