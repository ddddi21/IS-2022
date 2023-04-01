import os

import requests
from bs4 import BeautifulSoup

# Принимаем ссылки в формате: str1 str2 ...
sites = list(input().split())

links = []
for i in sites:
    if not links.__contains__(i):
        links.append(i)

count = 0
i = 0

path = r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\1'
if not os.path.exists(fr'{path}\texts'):
    os.makedirs(fr'{path}\texts')

while count < 100:
    # if links[i] is None:
    #     pass
    # else:
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
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)

    num_words = len(text.split())

    # Получаем ссылки со страницы
    all_a = soup.find_all('a')

    for a in all_a:
        if not links.__contains__(a.get('href')):
            links.append(a.get('href'))
    if num_words >= 1000:
        count += 1
        # Сохраняем файлы с текстом страниц
        with open(fr"{path}\texts\{count}.txt", "w", encoding="utf-8") as myfile:
            myfile.write(text)
            myfile.close()
        # Соответствие файлов и ссылок
        with open(fr"{path}\index.txt", "a") as myfile:
            myfile.write(f"{count}.txt -> {current_site}\n")
            print(count)

print("Success")
