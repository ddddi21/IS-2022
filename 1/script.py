import os
import re

import requests
from bs4 import BeautifulSoup


# Принимаем ссылки в фотмате: str1 str2 ...
sites = list(input().split())

links = []
# Добавляем ссылки в массив
for i in sites:
    if not links.__contains__(i):
        links.append(i)


path = r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\1'
if not os.path.exists(fr'{path}\texts'):
    os.makedirs(fr'{path}\texts')

# Счетчик подходящих страниц
count = 0

# Номер текущей ссылки
i = 0

while count < 100:
    # Проверка на валидность ссылки
    if links[i] == None:
        i += 1
        continue
    # Проверка наличия текущей ссылки в массиве ссылок чтобы не добавлять существующие
    if not links[i].__contains__('http'):
        i += 1
        continue

    current_site = links[i]
    i += 1

    try:
        html = requests.get(current_site)
    except:
        print(f'Ошибка при запросе на сайт: {current_site}')
        continue

    soup = BeautifulSoup(html.text, 'lxml')
    # Убираем html теги и оставляем текст
    text = soup.get_text()

    # Убираем лишние пробелы
    lines = (line.strip() for line in text.splitlines())
    chunks = [phrase.strip() for line in lines for phrase in line.split("  ")]

    # Разделяем слипшиеся слова по заглавным буквам
    chunks = [re.sub(r'([А-Я])', r' \1', phrase).split() for phrase in chunks]

    # Соединяем слова в текст
    text = " "
    for chunk in chunks:
        if len(chunk) < 1:
            continue
        text = text + " ".join(chunk)

    num_words = len(text.split())

    # Получаем ссылки со страницы
    all_a = soup.find_all('a')

    # Добавляем в массив ссылок ссылки с текущей страницы
    for a in all_a:
        # Добавляем в конец ссылки / если его нет
        href = a.get('href') if a.get('href')[-1] == "/" else a.get('href')+"/"
        if not links.__contains__(href):
            links.append(href)

    # Записываем в файл текст если колличество слов больше 1000, иначе пропускаем текущую страницу
    if num_words >= 1000:
        count += 1
        # Сохраняем файлы с текстом страниц
        with open(fr"{path}\texts\{count}.txt", "w", encoding="utf-8") as myfile:
            myfile.write(text)
            myfile.close()
        # Соответствие файлов и ссылок
        with open(fr"{path}\index2.txt", "a") as myfile:
            myfile.write(f"{count}.txt -> {current_site}\n")
    print(count)

print("Success")