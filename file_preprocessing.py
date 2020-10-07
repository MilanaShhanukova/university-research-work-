import csv
import re

csv_filename = "data.csv"


# get clean data without punctuation
def get_clean_data(file: str):
    with open(file, encoding="utf-8") as row_file:
        data_to_clean = row_file.read().lower().split("\n")

        clean_sentences = [re.sub(r"[^A-Za-z0-9]+", ' ', sent) for sent in data_to_clean]
        print(clean_sentences)
    with open("clean_" + file, "w") as clean_file:
        clean_file.write("\n".join(clean_sentences))


def create_csv(file_csv: str):
    # get right sentences
    with open("clean_no_mistake.ref0") as file_no_mistake:
        right_txt = file_no_mistake.read().split("\n")

    # get wrong sentences
    with open("clean_with_mistakes.src") as file_with_mistakes:
        wrong_txt = file_with_mistakes.read().split("\n")

    # create .csv file with combination of right and wrong sentences
    with open(file_csv, 'w') as data_file:
        file_writer = csv.writer(data_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        file_writer.writerow(["Sentence", "target"])

        for right_sent in right_txt:
            file_writer.writerow([right_sent, 1])

        for wrong_txt in wrong_txt:
            file_writer.writerow([wrong_txt, 0])


if __name__ == '__main__':
    get_clean_data("no_mistake.ref0")
    get_clean_data("with_mistakes.src")
    create_csv(csv_filename)
