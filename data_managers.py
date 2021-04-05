import os
from sentences_preporation import Decoding_sentences as SentDecoder


class DataPreprosser:
    def __init__(self, path):
        self.path_data = path
        self.all_mistakes = {}

    def load_data(self):
        """
        :return: loads data from folder - return list object
        """
        data = []
        os.chdir(self.path_data)
        files = os.listdir(path=".")
        for file in files:
            with open(file, encoding="utf-8") as input_file:
                data.extend(input_file.read().split('\n'))
        return data

    def preprocess_data(self, data, output_file_name):
        """
        :param output_file_name: the name of file created
        :return: creates new file with clean and preprocessed sentences
        """
        errors = 0
        with open(output_file_name, "w", encoding="utf-8") as output_file:
            for line in data:
                line = line.strip()
                if line.startswith("S"):
                    sent = line[2:]
                    decoder = SentDecoder(sent)
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
                    if type_mistake.startswith("M") or type_mistake.startswith("U"):
                        continue

                    try:
                        mistakes[ind_mistake] = type_mistake
                        if type_mistake in self.all_mistakes:
                            self.all_mistakes[type_mistake] += 1
                        else:
                            self.all_mistakes[type_mistake] = 1
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

    def get_sentences(self, file_paths: list):
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
