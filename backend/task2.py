# -*- coding: utf-8 -*-
"""Task2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1krt7GrMcgWg6OqILX9rXpWXIjEzQvaoS
"""

import spacy
import gensim
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import numpy as np

from google.colab import drive
drive.mount('/content/drive')

"""Step 1: Generate Count Vectors"""

nlp = spacy.load('en_core_web_sm')

# Load the vocabulary from vocab.txt
def load_vocab(vocab_file):
    vocab = {}
    with open(vocab_file, 'r') as file:
        for line in file:
          word, index = line.strip().split(':')
          vocab[word] = int(index)
    return vocab

vocab_file = '/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/vocab.txt'
vocabulary = load_vocab(vocab_file)

def generate_count_vector(description, vocab):
    doc = nlp(description.lower())
    word_freq = defaultdict(int)
    for token in doc:
        if token.text in vocab:
            word_freq[vocab[token.text]] += 1
    return word_freq

descriptions = pd.read_json('/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/preprocessed_ads.json')
descriptions.head()

count_vectors = []
for _, row in descriptions.iterrows():
    webindex = row['Webindex']
    description = row['Description']
    word_freq = generate_count_vector(description, vocabulary)
    count_vector = f"#{webindex}, " + ", ".join([f"{idx}:{freq}" for idx, freq in sorted(word_freq.items())])
    count_vectors.append(count_vector)
count_vectors[0]

with open('/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/count_vectors.txt', 'w') as file:
    for count_vector in count_vectors:
        file.write(count_vector + "\n")

"""Step 2: Generate Weighted and Unweighted Word Embeddings using Word2Vec model"""

import gensim.downloader as api
word2vec_model = api.load('word2vec-google-news-300')

def preprocess(text):
    doc = nlp(text.lower())
    return [token.text for token in doc if token.is_alpha]

sentences = [preprocess(desc) for desc in descriptions['Description']]
word2vec_model = gensim.models.Word2Vec(sentences, vector_size=100, window=5, min_count=1, workers=4)

# Fit TF-IDF Vectorizer
tfidf = TfidfVectorizer(vocabulary=vocabulary)
tfidf.fit(descriptions['Description'])

def get_word2vec_vector(description, model, vocab, tfidf=None):
    doc = preprocess(description)
    word_vecs = []
    for word in doc:
        if word in vocab:
            vec = model.wv[word]
            if tfidf:
                tfidf_weight = tfidf[word]
                vec = vec * tfidf_weight
            word_vecs.append(vec)
    if word_vecs:
        return np.mean(word_vecs, axis=0)
    else:
        return np.zeros(model.vector_size)

unweighted_vectors = []
weighted_vectors = []

for index, row in descriptions.iterrows():
    webindex = row['Webindex']
    description = row['Description']
    tfidf_weights = dict(zip(tfidf.get_feature_names_out(), tfidf.transform([description]).toarray()[0]))

    unweighted_vector = get_word2vec_vector(description, word2vec_model, vocabulary)
    weighted_vector = get_word2vec_vector(description, word2vec_model, vocabulary, tfidf_weights)

    unweighted_vectors.append((webindex, unweighted_vector))
    weighted_vectors.append((webindex, weighted_vector))

weighted_vectors[0]

unweighted_vectors[0]

def save_vectors(vectors, filename):
    with open(filename, 'w') as file:
        for webindex, vector in vectors:
            sparse_representation = ", ".join([f"{i}:{v}" for i, v in enumerate(vector) if v != 0])
            file.write(f"#{webindex}, {sparse_representation}\n")

# Save unweighted vectors to a file
save_vectors(unweighted_vectors, '/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/unweighted_vectors.txt')
# Save weighted vectors to a file
save_vectors(weighted_vectors, '/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/weighted_vectors.txt')