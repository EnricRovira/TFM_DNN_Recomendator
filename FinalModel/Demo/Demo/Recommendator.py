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


path = os.path.join('../Data/')
path_models = os.path.join('../Models/')

data_processed = pd.read_csv(path + 'FinalItems/data_final.csv')
data_processed['text'] = data_processed['text'].astype(str)


items_unique = data_processed.item_id.unique()
items_map = {i:val for i,val in enumerate(items_unique)}
items_map_inv = {val:i for i,val in enumerate(items_unique)}
items_map_text = data_processed.set_index('item_id_int').text.to_dict()


# In[6]:


idx_customers_map = {i:val for i,val in enumerate(data_processed['customer_id_int'])}
idx_customers_df = pd.DataFrame({'idx': data_processed.index.values, 'customer_id_int': data_processed.customer_id_int})




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
model = load_model(path_models + 'candidate_generation')
global graph
graph = tf.get_default_graph()


def header(text, color='black', gen_text=None, size = 54):
    """Create an HTML header"""

    if gen_text:
        raw_html = f'<h1 style="margin-top:16px;color: {color};font-size:{size}px"><center>' + str(
            text) + '<span style="color: #00BFFF">' + str(gen_text) + '</center></h1>'
    else:
        raw_html = f'<h1 style="margin-top:12px;color: {color};font-size:{size}px"><center>' + str(
            text) + '</center></h1>'
    return raw_html

def box(text):
    """Create an HTML box of text"""
    raw_html = '<div style="border-bottom:1px inset black;border-top:1px inset black;padding:8px;font-size: 21px;">' + str(
            text) + '</div>'
    return raw_html


def recommend_1(model, customer  , N = 5):
    items_bought = ''
    items_rec = ''
    text = ''
    html = ''
    
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

        interacted_items = data_processed[['text', 'score_original']][data_processed['customer_id_int'] == customer].groupby('text')                            .sum().reset_index().sort_values(['score_original'], ascending = False)
        items_bought += '<br/>'.join([str(i+1) + str(' - ') + str(x) for i, x in enumerate(interacted_items['text'].values[0:20])])
        top = _pred.values.reshape(_pred.shape[1]).argsort()[-N:][::-1] #items positions
        items_rec += '<br/>'.join([str(i+1) + str(' - ') + str(items_map_text[x]) for i, x in enumerate(top)])

    except Exception as e:
        print(f'Exception: {e}')
        print(f'\nThe customer {customer} does not exist')

    html = header('', color = 'black', gen_text = f'Customer {customer} Recommendations')  
    html += header(text = f'Items bought by Customer {customer}:', size = 40)
    html += box(items_bought)
    html += header(text = f'Top {N} Items recommended to Customer {customer}:', size = 40)
    html += box(items_rec)
        
    return f'<div>{html}</div>'