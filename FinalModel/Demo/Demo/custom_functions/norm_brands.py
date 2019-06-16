
import os
import re, unicodedata


def to_lowercase(words):
    """Convert all characters to lowercase from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = word.lower()
        new_words.append(new_word)
    return new_words

def remove_punctuation(words):
    """Remove punctuation from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = re.sub(r'[^\w\s]', '', word)
        if new_word != '':
            new_words.append(new_word)
    return new_words

def normalize_brands(words):
    words = str(words)
    words  = words.strip().split()
    words = to_lowercase(words)
    words = remove_punctuation(words)    
    words = list(dict.fromkeys(words)) #Remove duplicates
    words = " ".join(words)
    return words

def launch_normalizer(df):
    df['brand'] = df['brand'].apply(normalize_brands)
    brands = list(dict.fromkeys(df['brand'].values))

    more_brands = ['tarocco', 'tucci', 'fjord', 'tommy', 'hilfiger', 'easy', 'wear', 'josma', 'jaipur', 'ralph', 'nemeziz']
    try:
        brands.remove('marvel')
    except Exception:
        print('Marvel not in list')
        pass

    for brand in more_brands:
        brands.append(brand)
        
    return brands