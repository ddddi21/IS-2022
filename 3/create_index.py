import os
import sys
import json as j

json = dict()

directory = os.fsencode(r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\2\texts')
count = 0
for file in os.listdir(directory):
    # Номер текущкго файла
    file_num = file.decode("utf-8").split('.')[0]

    # Считываем данные файла
    with open(rf'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\2\texts\{file_num}.txt', 'r', encoding='utf-8') as file:
        data = file.read()

    # Заполняем словарь для получения инвертированного индекса
    for word in data.split(' '):
        if word in json:
            if not json.get(word).__contains__(file_num):
                json.get(word).append(file_num)
        else:
            json[word] = [file_num]


with open(rf'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\3\index.json', 'w', encoding='utf-8') as file:
    j.dump(json, file, ensure_ascii=False)

print('Success')