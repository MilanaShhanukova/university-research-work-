import csv
from sentences_preporation import Decoding_sentences as sent_decoder


class Data_decoder:
    def __init__(self):
        self.file_main_sent = "main_sent_feature.csv"
        self.clean_data = "data_2.csv"
        self.decoder_of_sent = sent_decoder

    def get_text_data(self):
        sentences, targets = [], []
        with open(self.clean_data) as file:
            reader = csv.DictReader(file, delimiter=',')
            for line in reader:
                decoded_sent = self.decoder_of_sent(line["Sentence"]).get_main_sentences()
                sentences.append(decoded_sent)
                targets.append(line["target"])

        return sentences, targets

    def get_main_sent_features(self):
        with open(self.file_main_sent, "w") as file:
            file_writer = csv.writer(file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(["main_sent", "target"])
            main_sent, targets = self.get_text_data()
            for i in range(len(main_sent)):
                file_writer.writerow([main_sent[i], targets[i]])


encoder = Data_decoder()
encoder.get_main_sent_features()





