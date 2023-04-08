import os
import re
import nltk
from nltk.corpus import stopwords
from pymorphy2 import MorphAnalyzer

# Скачиваем стопслова
nltk.download('stopwords')
stop_words = set(stopwords.words('russian'))

directory = os.fsencode(r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\1\texts')

patterns = "[^а-яА-ЯёЁ]+"

morph = MorphAnalyzer()

def lemmatize(doc):
    doc = re.sub(patterns, ' ', doc)
    tokens = []
    for token in doc.split():
        if token and token not in stop_words:
            token = token.strip()
            token = morph.normal_forms(token)[0]

            tokens.append(token)
    if len(tokens) > 2:
        return tokens
    return None


path = r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\2'
if not os.path.exists(fr'{path}\texts'):
    os.makedirs(fr'{path}\texts')

for file in os.listdir(directory):
    file_num = file.decode("utf-8").split('.')[0]

    with open(rf'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\1\texts\{file_num}.txt', 'r',
              encoding='utf-8') as file:
        data = file.read()
    print(file_num)

    # Лемматизируем слова
    result = ' '.join(lemmatize(data))

    with open(rf'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\2\texts\{file_num}.txt', 'w',
              encoding='utf-8') as file:
        file.write(result)

print('Success')