# -*- coding: utf-8 -*-
"""Task1.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Ebyd9h_Ca4jOEupiFR6eBVZDyW_xGnTH

Step 1: Setup and Read Data
"""

import spacy
import re
import nltk
from collections import Counter
import os
import glob

from google.colab import drive
drive.mount('/content/drive')

# Load English tokenizer, POS tagger, parser, NER and word vectors
nlp = spacy.load("en_core_web_sm")

# Read stop words from file
with open('/content/drive/MyDrive/Natural Language Processing/Assignment5 data/stopwords_en.txt', 'r') as f:
    stopwords = set(f.read().splitlines())

# Function to extract job categries
def extract_job_categories(data_folder):
    job_categories = []
    for category in os.listdir(data_folder):
        category_path = os.path.join(data_folder, category)
        if os.path.isdir(category_path):
            job_categories.append(category)
    return job_categories

job_categories = extract_job_categories('/content/drive/MyDrive/Natural Language Processing/Assignment5 data/data')
print(job_categories)

def load_job_descriptions(data_folder):
    job_descriptions = []

    for category in os.listdir(data_folder):
        category_path = os.path.join(data_folder, category)

        if os.path.isdir(category_path):
            for job_file in glob.glob(os.path.join(category_path, "Job_*.txt")):
                with open(job_file, 'r', encoding='utf-8') as f:
                    content = f.read()

                    # Extracting the relevant parts of the job description
                    title = extract_value(content, 'Title:')
                    webindex = extract_value(content, 'Webindex:')
                    company = extract_value(content, 'Company:')
                    description = extract_value(content, 'Description:')

                    # Creating the job dictionary
                    job_data = {
                        'Category': category,
                        'Title': title,
                        'Webindex': webindex,
                        'Company': company,
                        'Description': description
                    }

                    job_descriptions.append(job_data)

    return job_descriptions

def extract_value(content, key):
    try:
        # Find the starting point of the key
        start_idx = content.index(key) + len(key)
        # Find the end of the line or the next key
        end_idx = content.find('\n', start_idx)
        if end_idx == -1:  # If there's no newline character, take until the end of content
            end_idx = len(content)
        value = content[start_idx:end_idx].strip()
        return value
    except ValueError:
        return None

job_descriptions = load_job_descriptions('/content/drive/MyDrive/Natural Language Processing/Assignment5 data/data')

job_descriptions[0:5]

"""Step 2: Tokenize each job description"""

# Function To Tokenize each job description
def tokenize_descriptions(descriptions):
  for job in descriptions:
    # Tokenize the description in each job dictionary
    description = job.get('Description', '')
    tokens = re.findall(r"[a-zA-Z]+(?:[-'][a-zA-Z]+)?", description)
    job['Description'] = tokens
  return descriptions

tokenized_descriptions = tokenize_descriptions(job_descriptions)
# for tokens in tokenized_descriptions:
#     print(tokens)
len(tokenized_descriptions)

tokenized_descriptions[0:5]

"""Step 3: Convert all words to lowercase"""

for desc_list in tokenized_descriptions:
  description=[]
  for token in desc_list['Description']:
  # desc_list['Description'] = [token.lower() for token in desc_list['Description']]
    description.append(token.lower())
  desc_list['Description']=description

tokenized_descriptions[0:5]

def has_uppercase(token_list,size):
    for token in token_list:
        for char in token:
            if char.isupper():
                size+=1
                print(token)

size=0
for token_list in tokenized_descriptions:
    has_uppercase(token_list['Description'],size)
print(f"Count of words who have uppercase characters: {size}")

"""Step 4: Remove words with length less than 2"""

size=0
for token_list in tokenized_descriptions:
  for token in token_list['Description']:
    if len(token) < 2:
        size+=1
        print(token)
print(f"Count of words whose length is less than 2 characters: {size}")

for token_list in tokenized_descriptions:
  for token in token_list['Description']:
    if len(token) < 2:
        token_list['Description'].remove(token)

size=0
for token_list in tokenized_descriptions:
  for token in token_list['Description']:
    if len(token) < 2:
        size+=1
        print(token)
print(f"Count of words whose length is less than 2 characters: {size}")

tokenized_descriptions[0:5]

"""Step 5: Remove Stopwords"""

def check_stopwords(tokens, stopwords_file):
    stopwords = set()
    with open(stopwords_file, 'r') as file:
        stopwords = set(file.read().splitlines())
    size=0
    for token_list in tokens:
      for token in token_list['Description']:
        if token in stopwords:
            size+=1
            print("Stopword found:", token)
    print(f"Count of stopwords: {size}")

stopwords_file = "/content/drive/MyDrive/Natural Language Processing/Assignment5 data/stopwords_en.txt"
check_stopwords(tokenized_descriptions, stopwords_file)

def remove_stopwords(tokens_list, stopwords_file):
    stopwords = set()
    with open(stopwords_file, 'r') as file:
        stopwords = set(file.read().splitlines())

    filtered_tokens_list = []
    for tokens in tokens_list:
      # Create a copy to avoid modifying original dictionary
      filtered_tokens = dict(tokens)
      if 'Description' in filtered_tokens:
        # Lowercase and filter description tokens
        filtered_tokens['Description'] = [
          token for token in [t.lower() for t in filtered_tokens['Description']] if token not in stopwords
      ]
      filtered_tokens_list.append(filtered_tokens)
    return filtered_tokens_list

remove_stopwords_description = remove_stopwords(tokenized_descriptions, stopwords_file)

check_stopwords(remove_stopwords_description, stopwords_file)

remove_stopwords_description[0:5]

size=0
for i in remove_stopwords_description:
  size+=len(i['Description'])
print(size)

len(remove_stopwords_description)

"""Step 6: Remove the word that appears only once"""

from collections import Counter

def find_single_occurrence_words(tokens):
    word_counts = Counter()
    # Count the frequency of each word
    for token_list in tokens:
      word_counts.update(token_list['Description'])

    # Identify words that appear only once
    single_occurrence_words = [word for word, count in word_counts.items() if count == 1]

    return single_occurrence_words

single_occurrence_words = find_single_occurrence_words(remove_stopwords_description)
print("Words that appear only once:", single_occurrence_words)
print("Count of Words that appear only once:", len(single_occurrence_words))

def remove_single_occurrence_words(tokens_list):
    filtered_tokens_list = []
    for tokens in tokens_list:
        filtered_tokens = dict(tokens)
        if 'Description' in filtered_tokens:
          # Lowercase and filter description tokens
          filtered_tokens['Description'] = [
            token for token in [t for t in filtered_tokens['Description']] if token not in single_occurrence_words
          ]
        # Append the filtered token list to the result
        filtered_tokens_list.append(filtered_tokens)
    return filtered_tokens_list

remove_single_occurrence_words_description = remove_single_occurrence_words(remove_stopwords_description)

single_occurrence_word_present = find_single_occurrence_words(remove_single_occurrence_words_description)
print("Words that appear only once:", single_occurrence_word_present)
print("Count of Words that appear only once:", len(single_occurrence_word_present))

size=0
for i in remove_single_occurrence_words_description:
  size+=len(i['Description'])
print(size)

len(remove_single_occurrence_words_description)

"""Step 7:Remove the top 50 most frequent words"""

from collections import Counter

def find_top_frequent_words(tokens, n):
    word_counts = Counter()
    # Count the frequency of each word
    for token_list in tokens:
      word_counts.update(token_list['Description'])

    # Identify words that appear only once
    top_n_occurrence_words = [word for word, count in word_counts.most_common(n)]

    return top_n_occurrence_words

top_50_occurrence_words = find_top_frequent_words(remove_single_occurrence_words_description,50)
print("Top 50 most occurrance Words:", top_50_occurrence_words)
print("Count of top 50 most occurrance Words:", len(top_50_occurrence_words))

def remove_top_frequent_words(tokens_list, n):
    filtered_tokens_list = []
    for tokens in tokens_list:
      filtered_tokens = dict(tokens)
      if 'Description' in filtered_tokens:
        # Lowercase and filter description tokens
        filtered_tokens['Description'] = [
          token for token in [t for t in filtered_tokens['Description']] if token not in top_50_occurrence_words
        ]
        # # Append the filtered token list to the result
        filtered_tokens_list.append(filtered_tokens)

    return filtered_tokens_list

remove_top_50_frequent_words_description = remove_top_frequent_words(remove_single_occurrence_words_description, 50)

size=0
for i in remove_top_50_frequent_words_description:
  size+=len(i['Description'])
print(f"Count of words after removing top 50 frequent words: {size}")

remove_top_50_frequent_words_description[0:3]

len(remove_top_50_frequent_words_description)

"""Step 8: Save all job advertisement text"""

import json

def convert_descriptions_to_sentence(data):
  processed_data = []
  for item in data:
    if 'Description' in item:
      # Join description tokens into a sentence
      description_sentence = ' '.join(item['Description'])
      item['Description'] = description_sentence
    processed_data.append(item)

  # Write processed data to JSON file (replace 'output.json' with your desired filename)
  with open('/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/preprocessed_ads.json', 'w') as outfile:
    json.dump(processed_data, outfile)

convert_descriptions_to_sentence(remove_top_50_frequent_words_description)

json_file = '/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/preprocessed_ads.json'
with open(json_file, 'r') as file:
    preprocessed_ads = json.load(file)  # Load JSON data from the file

preprocessed_ads[500]

def save_job_categories(job_categories, file_path):
    with open(file_path, 'w') as file:
        file.write('\n'.join(job_categories))

save_job_categories(job_categories,'/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/job_categories.txt')

"""Step 9: Build vocabulary of the cleaned job advertisement descriptions"""

def build_vocabulary(tokens_list):
    vocabulary = []
    for job in tokens_list:
      # Tokenize the description in each job dictionary
      description = job.get('Description', '')
      tokens = re.findall(r"[a-zA-Z]+(?:[-'][a-zA-Z]+)?", description)
      for token in tokens:
        if token not in vocabulary:
          vocabulary.append(token)
    vocabulary=sorted(set(vocabulary))
    return vocabulary

def save_vocabulary(vocabulary, file_path):
    with open(file_path, 'w') as file:
        for index, word in enumerate(vocabulary):
            file.write(f"{word}:{index}\n")

# Build vocabulary
vocabulary = build_vocabulary(remove_top_50_frequent_words_description)
print(vocabulary[0:10])
print(len(vocabulary))

save_vocabulary(vocabulary, '/content/drive/MyDrive/Natural Language Processing/Assignment5_Solution/vocab.txt')

