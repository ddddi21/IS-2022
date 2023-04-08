import math
import os
import re
import json
import operator
from sklearn.metrics.pairwise import cosine_similarity
from pymorphy2 import MorphAnalyzer

with open(r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\4\index.json', 'r', encoding="utf-8") as file:
    data = dict(json.load(file))

texts_directory = os.fsencode(r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\2\texts')
doc_count = len(os.listdir(texts_directory))

morph = MorphAnalyzer()

def lemmatize(doc, stopwords = []):
    patterns = "[^а-яА-Я]+"
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stopwords:
            token = token.strip()
            token = morph.normal_forms(token)[0]

            tokens.append(token)
    if len(tokens) > 0:
        return tokens
    return None

# def get_url(index):
#     with open(r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\1\index.txt', 'r', encoding='utf-8') as file:
#         data = file.readlines()
#     result = None
#     for file in data:
#         num = file.split(" -> ")[0].split(".")[0]
#         url = file.split(" -> ")[1][:-1]
#         if str(num) == str(index):
#             result = url
#     return result

def query_tf_idf(token, query):
    try:
        doc_with_token_count = len(data.get(token))
    except:
        return 0

    q_tf = query.count(token) / len(query)
    q_idf = math.log(doc_count / doc_with_token_count)

    # кошачьи характеры кошачьи  tf(кошачьи): 2/3  idf: log(100/5) = 4. ...
    # кошачьи характеры  tf(кошачьи): 1/2   idf: log(100/5) = 4. ...

    return round(q_tf * q_idf, 6)

def search(query):
    query = lemmatize(query)

    query_vector = []

    # кошачьи характеры кошачьи
    for token in query:
        query_vector.append(query_tf_idf(token, query))

    # [5.4, 6.1, 7]

    vectors_distances = {}

    for file in os.listdir(texts_directory):
        index = file.decode("utf-8").split('.')[0]

        document_vector = []

        # 1: [tf-idf(кошачьи), tf-idf(характеры), tf-idf(кошачьи)] [0,0,0]
        # 2: [tf-idf(кошачьи), tf-idf(характеры), tf-idf(кошачьи)]
        # 3: [tf-idf(кошачьи), tf-idf(характеры), tf-idf(кошачьи)]
        # 4: [tf-idf(кошачьи), tf-idf(характеры), tf-idf(кошачьи)]
        # 5: [tf-idf(кошачьи), tf-idf(характеры), tf-idf(кошачьи)]
        # ...
        for token in query:
            try:
                tf_idf = data.get(token).get(index).get("TF-IDF")
                document_vector.append(tf_idf)
            except:
                document_vector.append(0.0)

        vectors_distances[index] = cosine_similarity([query_vector], [document_vector])[0][0]

        # print([query_vector], [document_vector])
        # print(vectors_distances[index])
        # print()


    searched_indices = sorted(vectors_distances.items(), key=operator.itemgetter(1), reverse=True)

    for index in searched_indices:
        doc_id, tf_idf = index

        print("Index: {}  Косинустное расстояние:{}".format(doc_id, tf_idf))

search(input())

# Косинусное растояние
# скалярное произведение(a,b) / (norm(a)* norm(b))

# [1, 0.5, 0.4]
# [0.5, 0.7, 0.8]
# Для нахождения косинусного расстояния между двумя векторами, можно воспользоваться формулой:
# cosine_distance = dot_product(a, b) / (norm(a) * norm(b))
# где a и b - это два вектора, dot_product(a, b) - скалярное произведение векторов a и b, а norm(a) и norm(b) - нормы векторов a и b соответственно.
# Применяя эту формулу к векторам [0.5, 0.3, 0] и [0.4, 0.3, 0], получим:
# dot_product = 0.5 * 0.4 + 0.3 * 0.3 + 0 * 0 = 0.22
# norm_a = sqrt(0.5^2 + 0.3^2 + 0^2) = 0.583
# norm_b = sqrt(0.4^2 + 0.3^2 + 0^2) = 0.5
# cosine_distance = 0.22 / (0.583 * 0.5) = 0.754
# Таким образом, косинусное расстояние между векторами [0.5, 0.3, 0] и [0.4, 0.3, 0] равно примерно 0.754.
