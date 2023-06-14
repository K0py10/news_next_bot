from nltk.corpus import stopwords
# import spacy
from pymystem3 import Mystem
from string import punctuation

import numpy as np
from numpy.linalg import norm
# from sklearn.metrics.pairwise import cosine_similarity

# lmr = spacy.load("ru_core_news_md")
mystem = Mystem()
sw = stopwords.words("russian")

def prepare_text(text: str):
    whitelist = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ')
    text = ''.join(filter(whitelist.__contains__, text))
    # print(text)
    tokens = mystem.lemmatize(text.lower())
    # print(tokens)
    tokens = [token for token in tokens if token not in sw\
              and ' ' not in token \
              and token != '' \
              and token not in punctuation \
              and token != '\n'] 

    return tokens

def calculate_similarity(words1, words2):
    # Create a set of all unique words
    all_words = set(words1 + words2)
    # print(all_words)
    # Create a dictionary that maps each word to its index in the set
    word_to_index = {word: i for i, word in enumerate(all_words)}
    # print(word_to_index)
    # Create a matrix of word counts for each list of words
    counts1 = np.zeros(len(all_words))
    counts2 = np.zeros(len(all_words))
    for word in words1:
        counts1[word_to_index[word]] += 1
    for word in words2:
        counts2[word_to_index[word]] += 1
    # Calculate the cosine similarity between the two word count vectors
    similarity = np.dot(counts1, counts2)/(norm(counts1)*norm(counts2))
    return similarity

# def compare_texts(text1, text2):
#     sm = difflib.SequenceMatcher(text1, text2)
#     return sm.ratio()

def find_similar_posts(base, posts, cutoff):
    res = []
    for post in posts:
        sim = calculate_similarity(base, post.lem_text.split(' '))
        # if sim > 0.1:
        #     print(post.id)
        #     print(sim)
        if sim > cutoff:
            res.append(post)
    return res

# text1 = prepare_text("Мама мыла раму.")
# text2 = prepare_text("Мама мыла окно.")
# print(calculate_similarity(text1, text2))