import spacy
from senteces_process import data_clean


nlp = spacy.load("en_core_web_sm")


# получение тегов .tag
def get_tag(sentence: str) -> list:
    doc = nlp(sentence)
    tags = [token.tag_ for token in doc]
    return tags


# получение массива по предложению тегов предложения
def get_data_tagged(data: list) -> dict:
    tagged = {}
    for sentence in data:
        tagged[sentence] = get_tag(sentence)

    return tagged


for key, value in get_data_tagged(data_clean).items():
    print(key, value)


