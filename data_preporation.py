import csv
import os
from sentences_preporation import Decoding_sentences as sent_decoder

# load data and preprocess it in conll-u-format


def load_data(path_data: str):
    data = []
    os.chdir(path_data)
    files = os.listdir(path=".")
    for file in files:
        with open(file, encoding="utf-8") as input_file:
            data.extend(input_file.read().split('\n'))
    return data



def preprocess_data(data: list, output_file_name: str):
    errors = 0
    with open(output_file_name, "w", encoding="utf-8") as output_file:
        for line in data:
            line = line.strip()
            if line.startswith("S"):
                sent = line[2:]
                decoder = sent_decoder(sent)
                decoder.make_clear()

                words = [token.text for token in decoder.doc_sent]
                mistakes = [None for _ in range(len(words) + 1)]
                tags = decoder.get_tag()
                dep = decoder.get_dep()

            elif line.startswith("A"):
                line = line[2:]
                info = line.split("|||")
                ind_mistake = int(info[0].split()[0])
                type_mistake = info[1]
                try:
                    mistakes[ind_mistake] = type_mistake
                except IndexError:
                    errors += 1
                except UnboundLocalError:
                    errors += 1

            elif not line:
                try:
                    for ind_w in range(len(words)):
                        info_word = f"{words[ind_w]}    {mistakes[ind_w]}   {tags[ind_w]}   {dep[ind_w]} \n"
                        output_file.write(info_word)

                except UnboundLocalError:
                    errors += 1

                output_file.write("\n")
    print(f"{output_file_name} errors {errors}")


def get_sentences(file_paths: list):
    """
    :param self:
    :param file_paths:
    :return: list of sentences parts
    """
    sentences = []
    for file_name in file_paths:
        with open(file_name) as f:
            sentence = []
            for line in f:
                line_parts = line.strip().split("   ")
                if len(line_parts) != 1:
                    sentence.append(line_parts)
                elif len(line_parts) == 1:
                    sentences.append(sentence)
                    sentence = []
    return [sent for sent in sentences if len(sent) > 0]

files = ["file.txt"]
#print(os.chdir(r"C:\Users\Милана\PycharmProjects\курсовая работа\data"))
sentences = get_sentences(files)
# d = load_data(r"C:\Users\Милана\PycharmProjects\курсовая работа\data")
#
# sentences = d.count("")
# slice_first = 0
# slice_second = 10000
#
# for file_iter in range(sentences // 10000):
#      output_name = "output_file" + str(file_iter)
#      data = d[slice_first: min(slice_second, len(d))]
#      preprocess_data(data, output_name)
#      slice_first = file_iter * 10000
#      slice_second += 10000






