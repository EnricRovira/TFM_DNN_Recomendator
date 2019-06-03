#!/usr/bin/env python
# coding: utf-8

# # Let´s recommend!!

# We will load the model that generate candidates and create a function that receives a customer as input and returns a top of N products to be recommended. We will evaluate the results afterwords.

# In[1]:


import pandas as pd
import os, sys
import numpy as np
import seaborn as sns
import gc
import warnings
import matplotlib.pyplot as plt
import tensorflow as tf

from tensorflow.keras.models import Model, Sequential, load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.layers import Embedding
from gensim.models import Word2Vec


# In[4]:


path = os.path.join('../../Data/')
data = pd.read_csv(path + 'data_filtered_20190422.csv', sep = ';')
data_processed = pd.read_csv(path + 'data_final_20190525.csv')
data_processed['text'] = data_processed['text'].astype(str)


# In[5]:


items_unique = data_processed.item_id.unique()
items_map = {i:val for i,val in enumerate(items_unique)}
items_map_inv = {val:i for i,val in enumerate(items_unique)}
items_map_text = data_processed.set_index('item_id_int').text.to_dict()


# In[6]:


idx_customers_map = {i:val for i,val in enumerate(data_processed['customer_id_int'])}
idx_customers_df = pd.DataFrame({'idx': data_processed.index.values, 'customer_id_int': data_processed.customer_id_int})


# In[7]:


data.head(3)


# In[8]:


data_processed.head(3)


# In[9]:


MAX_NB_WORDS = 30_000 #decided by cumsum wordcount plot (Script 01)
MAX_SEQUENCE_LENGTH = 24 #decided by max words in a product (Script 00)
EMBEDDING_DIM = 100 #Same dim as our W2V embedding

all_text = data_processed['text']
all_text = all_text.drop_duplicates (keep = False)

tokenizer = Tokenizer(num_words=MAX_NB_WORDS, )
tokenizer.fit_on_texts(all_text)

data_sequences = tokenizer.texts_to_sequences(data_processed['text'])
data_vec = pad_sequences(data_sequences, maxlen=MAX_SEQUENCE_LENGTH)

word_index = tokenizer.word_index
print('Found %s unique tokens.' % len(word_index))


global rec_model
model = load_model('../04_Modelado_y_Evaluacion/candidate_generation_20190525')
global graph
graph = tf.get_default_graph()


def diversify(arr, diversity, plot = False):
    div = np.log(arr) / diversity
    exp_preds = np.exp(div)
    preds = exp_preds / np.sum(exp_preds)
    if plot:
        plt.figure(figsize = (10, 8));
        plt.subplot(2, 1, 1);
        sns.distplot(arr); plt.title('Original Distribution');
        plt.subplot(2, 1, 2);
        sns.distplot(preds); plt.title(f'Distribution with {diversity} diversity')
    probas = np.random.multinomial(1, preds, 1)
    return probas


def recommend(model, customer  , N = 5):
    print (data_processed.head())
    print(data_vec[:1])
    try:
        _data = data_processed[data_processed['customer_id_int'] == customer]
        _data_vec = data_vec[_data.index]
        _pred = model.predict([_data['customer_id_int'], _data['item_id_int'], 
                             _data['brand_id'], _data['PRICE'],
                             _data_vec, _data['item_age'], _data['score'],
                             _data['power_price'], _data['power_score'], _data['power_item_age'],
                             _data['sqrt_price'], _data['sqrt_score'], _data['sqrt_item_age']],
                             batch_size = 1, verbose = 0)
        _pred = pd.DataFrame(_pred)
        _pred['customer_id_int'] = customer
        _pred = _pred.groupby(['customer_id_int']).max()
        del _pred.index.name
        
    #########################################################
        #_pred = diversify(_pred.values.reshape(_pred.shape[1]), diversity = 0.7, plot = False)
        #print(_pred)
        print('\n' + '=='*30 + '\n')
        print(f'==> Top {N} Recommended items to Customer {customer}: ')
        print(f'\nThe customer {customer} has bought this items: ')
        print('\n' + '=='*30 + '\n')
        interacted_items = data_processed[['text', 'score_original']][data_processed['customer_id_int'] == customer].groupby('text')                            .sum().reset_index().sort_values(['score_original'], ascending = False)
        print('\n'.join([str(i+1) + str(' - ') + str(x) for i, x in enumerate(interacted_items['text'].values[0:20])]))
        top = _pred.values.reshape(_pred.shape[1]).argsort()[-N:][::-1] #items positions
        print('\n====================== IDs DE PRODUCTOS RECOMENDADOS ==============')
        print([items_map[item] for item in top])
        print ("\n===================== PRODUCTOS RECOMENDADOS =====================")
        print('\n'.join([str(i+1) + str(' - ') + str(items_map_text[x]) for i, x in enumerate(top)]))
        print ("==================================================================")
    except Exception as e:
        print(f'Exception: {e}')
        print(f'\nThe customer {customer} does not exist')


def recommend_1(model, customer  , N = 5):
    text = ''
    try:
        _data = data_processed[data_processed['customer_id_int'] == customer]
        _data_vec = data_vec[_data.index]
        _pred = model.predict([_data['customer_id_int'], _data['item_id_int'], 
                             _data['brand_id'], _data['PRICE'],
                             _data_vec, _data['item_age'], _data['score'],
                             _data['power_price'], _data['power_score'], _data['power_item_age'],
                             _data['sqrt_price'], _data['sqrt_score'], _data['sqrt_item_age']],
                             batch_size = 1, verbose = 0)
        _pred = pd.DataFrame(_pred)
        _pred['customer_id_int'] = customer
        _pred = _pred.groupby(['customer_id_int']).max()
        del _pred.index.name
        
    #########################################################
        #_pred = diversify(_pred.values.reshape(_pred.shape[1]), diversity = 0.7, plot = False)
        #print(_pred)
        text += '\n' + '=='*30 + '\n'
        text += '==> Top ' + str(N) + 'Recommended items to Customer ' + str(customer) + ': '
        text += '\nThe customer ' + str(customer) + 'has bought this items: '
        text += '\n' + '=='*30 + '\n'
        interacted_items = data_processed[['text', 'score_original']][data_processed['customer_id_int'] == customer].groupby('text')                            .sum().reset_index().sort_values(['score_original'], ascending = False)
        text += '\n'.join([str(i+1) + str(' - ') + str(x) for i, x in enumerate(interacted_items['text'].values[0:20])])
        top = _pred.values.reshape(_pred.shape[1]).argsort()[-N:][::-1] #items positions
        text += '\n====================== IDs DE PRODUCTOS RECOMENDADOS =============='
        text += ''.join([str(items_map[item]) for item in top])
        text += "\n===================== PRODUCTOS RECOMENDADOS ====================="
        text += '\n'.join([str(i+1) + str(' - ') + str(items_map_text[x]) for i, x in enumerate(top)])
        text += "=================================================================="
    except Exception as e:
        print(f'Exception: {e}')
        print(f'\nThe customer {customer} does not exist')

    return text