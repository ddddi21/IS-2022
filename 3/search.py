import ast
import sys

a = input()

arr = a.split(' ')

if len(arr) != 5:
    sys.exit('Некорректное выражение')


with open(r'C:\Users\Dilyara\Desktop\2023_ITIS_IS_11-907_AskhadullinaDM\3\index.json', 'r', encoding='utf-8') as file:
    index = ast.literal_eval(file.read())


all = set(range(1,101))
all_doc_count = set([str(i) for i in all])

new_arr = []


# Проходимся по словам и сопоставляем им документы содержащие данные слова
for i in range(len(arr)):
    if i % 2 == 0:
        if arr[i].startswith('!'):
            if index.get(arr[i][1:]) == None:
                sys.exit('Слова из выражения не существуют')
            new_arr.append(all_doc_count - set(index.get(arr[i][1:])))
            arr[i] = arr[i][1:]
        else:
            if index.get(arr[i]) == None:
                sys.exit('Слова из выражения не существуют')
            new_arr.append(set(index.get(arr[i])))


# Получаем множество документов соответсвующих условию
if arr[1] == '|' or arr[1] == 'ИЛИ':
    if arr[3] == '|' or arr[3] == 'ИЛИ':
        result = new_arr[0] | new_arr[1] | new_arr[2]
    elif arr[3] == '&' or arr[3] == 'И':
        result = new_arr[0] | new_arr[1] & new_arr[2]
elif arr[1] == '&' or arr[1] == 'И':
    if arr[3] == '|' or arr[3] == 'ИЛИ':
        result = new_arr[0] & new_arr[1] | new_arr[2]
    elif arr[3] == '&' or arr[3] == 'И':
        result = new_arr[0] & new_arr[1] & new_arr[2]

if len(result) == 0:
    print("не найдено")
else:
    result = set([int(i) for i in result])
    print(sorted(result))


# мобилизация астрология лапка

# мобилизация & астрология | лапка		мобилизация & !астрология | !лапка
# мобилизация | астрология | лапка		мобилизация | !астрология | !лапка
