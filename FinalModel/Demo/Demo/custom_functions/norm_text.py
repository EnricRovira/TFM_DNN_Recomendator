#!/usr/bin/env python
# coding: utf-8


import os
import re, unicodedata
import wget
from nltk.corpus import stopwords
import nltk



def gen_stopwords(path):

    nltk.download('stopwords')

    STOPWORDS_ESP = list(set(stopwords.words('spanish')))
    STOPWORDS_CAT = open(path + '\stopwords_catalan.txt', 'r', encoding= 'UTF-8').read().split()
    STOPWORDS_ENG = list(set(stopwords.words('english')))
    CUSTOM  = ['uf', '100st', '100t', '100u', 'pal', 'zzb21601xu', 'x2']

    STOPWORDS_ALL = STOPWORDS_ESP + STOPWORDS_CAT + STOPWORDS_ENG + CUSTOM

    return STOPWORDS_ALL

def get_lemmatizer(path):
    lemmatizer = {}
    with open(path + '\lemmatization-es.txt', encoding= 'UTF-8') as f:
        for line in f:
            try:
                (key, val) = line.split()
            except:
                pass
            lemmatizer[str(key)] = val

    lemmatizer_inv = {v: k for k, v in lemmatizer.items()}

    return lemmatizer_inv

def remove_non_ascii(words):
    """Remove non-ASCII characters from list of tokenized words"""
    new_words = []
    for word in words:
        new_word = unicodedata.normalize('NFKD', word).encode('ascii', 'ignore').decode('utf-8', 'ignore')
        #new_word = unicodedata.normalize('NFD', word).encode('ascii', 'ignore')
        new_words.append(new_word)
    return new_words

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

def replace_numbers(words):
    """Remove all interger occurrences in list"""
    new_words = []
    for word in words:
        if not word.isdigit():
            new_words.append(word)
    return new_words

def remove_stopwords(words, STOPWORDS_ALL):
    """Remove stop words from list of tokenized words"""
    new_words = []
    for word in words:
        if word not in STOPWORDS_ALL and len(word) > 1:
            new_words.append(word)
    return new_words

def stem_words(words):
    """Stem words in list of tokenized words"""
    stemmer = SnowballStemmer('spanish')
    stems = []
    for word in words:
        stem = stemmer.stem(word)
        stems.append(stem)
    return stems

def remove_brands(words, brands):
    """Remove brands from the text"""
    clean_words = []
    for word in words:
        if word not in brands:
            clean_words.append(word)
    return clean_words

def lemmatize(words, lemmatizer_inv):
    """Lemmatize verbs in list of tokenized words"""
    lemmas = []
    for word in words:
        if word in lemmatizer_inv:
            lemmas.append(lemmatizer_inv[word])
        else: lemmas.append(word)
    return lemmas

def replace_ngrams(words, ngrams):
    for gram in ngrams:
        if (gram in words):
            g = "_".join(gram.split())
            words = words.replace(gram, g)
    return words

def normalize(words, p_brands, STOPWORDS_ALL, lemmatizer_inv):


    ngrams = ['corte ingles', 'bob esponja', 'color azul', 'cristiano ronaldo', 'fc barcelona', 'lionel messi', 'real madrid',
         'azul oscuro', '1a temporada', '2a temporada', '3a temporada', '4a temporada', '5a temporada', '6a temporada',
         '7a temporada', '8a temporada', 'mrs increible', 'mr increible', 'fc barcelona', 'harry potter']

    #words  = words.strip().split()
    words = to_lowercase(words)
    words = remove_punctuation(words)
    words = remove_brands(words, brands = p_brands)
    words = remove_stopwords(words, STOPWORDS_ALL)
    words = lemmatize(words, lemmatizer_inv)
    words = replace_numbers(words)
    words = remove_non_ascii(words)
    words = list(dict.fromkeys(words)) #Remove duplicates
    words = " ".join(words)
    words = replace_ngrams(words, ngrams)
    return words

