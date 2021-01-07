import csv
import re

csv_filename = "data_2.csv"


# get clean data without punctuation
def get_clean_data(file: str):
    with open(file, encoding="utf-8") as row_file:
        data_to_clean = row_file.read().lower().split("\n")

        clean_sentences = [re.sub(r"[^A-Za-z0-9]+", ' ', sent) for sent in data_to_clean]

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
        writer = csv.DictWriter(data_file,
                                delimiter=",",
                                fieldnames=["Sentence", "target"])
        writer.writeheader()

        writer.writerows({"Sentence": right_txt[n], "target": 1} for n in range(len(right_txt)))
        writer.writerows({"Sentence": wrong_txt[n], "target": 0} for n in range(len(wrong_txt)))


if __name__ == '__main__':
    get_clean_data("data/no_mistake.ref0")
    get_clean_data("data/with_mistakes.src")
    create_csv(csv_filename)
