import re

file_name = "data.txt"


# загрузка данных и получение только предложений
def load_data(file__name: str) -> list:
    with open("data.txt", encoding="utf-8") as file:
        data_row = file.readlines()

    data_row = [row.split("	") for row in data_row]
    data = [row[1] for row in data_row] # добавляем только ответ
    return data


# получение чистых предложений
def get_clean_data(data: list) -> list:
    clean_data = []
    for sent in data:
        sent = sent.lower()
        # удаление знаков препинания
        sent = re.sub(r'[^A-Za-z0-9]+(?<!\')', ' ', sent)
        # удаление всего, что в скобках
        sent = re.sub(r'\([^\)]+\)', '', sent)
        # удаление цифр
        sent = re.sub(r"\d+", "", sent)

        clean_data.append(sent)
    return clean_data


data = load_data(file_name)
data_clean = get_clean_data(data)


