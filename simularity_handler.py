from nltk.corpus import stopwords
# import spacy
from pymystem3 import Mystem
from string import punctuation
import difflib

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

# lmr = spacy.load("ru_core_news_md")
mystem = Mystem()
sw = stopwords.words("russian")

def prepare_text(text: str):
    whitelist = set('АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ абвгдеёжзийклмнопрстуфхцчшщъыьэюя0123456789')
    text = ''.join(filter(whitelist.__contains__, text))
    # print(text)
    tokens = mystem.lemmatize(text.lower())
    # print(tokens)
    tokens = [token for token in tokens if token not in sw\
              and ' ' not in token \
              and token != '' \
              and token not in punctuation \
              and token != '\n'] 
    
    text = tokens

    # text = text.translate(str.maketrans('', '', punctuation)).lower()

    # text = text.split(' ')
    # # print(text)
    # for word in text:
    #     if word in sw or word == " " or word == '':
    #         text.remove(word)
    #         continue
    #     doc = lmr(word)
    #     lemmas = [token.lemma_.lower() for token in doc]
    #     word = lemmas[0]
    return text

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
    similarity = cosine_similarity([counts1], [counts2])[0][0]
    return similarity

# def compare_texts(text1, text2):
#     sm = difflib.SequenceMatcher(text1, text2)
#     return sm.ratio()

def compare_post_to_posts(base, posts, cutoff):
    res = []
    for post in posts:
        sim = calculate_similarity(base.lem_text.split(' '), post.lem_text.split(' '))
        # if sim > 0.1:
        #     print(post.id)
        #     print(sim)
        if sim > cutoff:
            res.append(post)
    return res

# text1 = prepare_text("От обстрелов в Шебекинском округе погибли две женщины Губернатор Белгородской области сообщил, что «с самого утра под обстрелом ВСУ находятся населенные пункты Шебекинского городского округа». Он рассказал о погибших и раненных: «В Новой Таволжанке в результате обстрела погибла пожилая женщина. От полученных травм она скончалась на месте. Еще одна женщина пострадала — у нее осколочные ранения левого плеча», — сообщил Гладков. Еще два человека попали под обстрелы в Безлюдовке: «Погибла женщина, у нее множественные осколочные ранения, не совместимые с жизнью. Еще один человек пострадал — мужчина с осколочными ранениями грудной клетки, верхних и нижних конечностей», — написал губернатор.")
# # text2 = prepare_text("При обстрелах Белгородской области погибли две женщины Во время сегодняшних обстрелов Шебекинского городского округа Белгородской области погибли две местные жительницы, сообщает губернатор Вячеслав Гладков. «В Новой Таволжанке в результате обстрела погибла пожилая женщина. От полученных травм она скончалась на месте. Еще одна женщина пострадала — у нее осколочные ранения левого плеча», — пишет Гладков. Вторая жительница погибла от осколочных ранений во время обстрела села Безлюдовка, утверждает Гладков. Также был ранен мужчина.")
# text2 = prepare_text("Московского следователя обвинили в получении взятки биткоинами стоимостью 1,6 миллиарда рублей. Коды к кошельку он хранил в папке «Пенсия» По версии следствия, московский следователь Марат Тамбиев получил криптовалюту от членов хакерской группировки Infraud Organization Марка и Константина Бергманов, а также Кирилла Самокутяевского в апреле 2022 года. Все трое в тот момент находились под следствием по делу о торговле данными банковских карт. Согласно «Коммерсанту», они дали взятку Тамбиеву, чтобы следователь не накладывали арест на активы хакеров. Позднее во время обыска у Тамбиева изъяли макбук, в котором нашли папку «Пенсия» с кодами доступа к криптокошелькам, в которых хранились 1032,1 биткоина, пишет газета. Сам бывший следователь свою вину отрицает. По данным «Коммерсанта», взятка в размере 1,6 миллиарда рублей является рекордной для сотрудников российских силовых ведомств.")
# print(calculate_similarity(text1, text2))