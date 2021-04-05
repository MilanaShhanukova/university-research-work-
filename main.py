# here is build the logic of work
import configparser
import json, os
from data_managers import DataManager, DataPreprosser
from model_pytroch import SimpleModel, Organizer
from create_config import change_variable, get_config
from logger import get_logger


def get_data():
    # how it works like
    row_data = preprocessed.load_data()

    num_sentences = row_data.count("")
    #here we preprocess data - should be commented if you've already prepared data
    slice_first = 0
    slice_second = 100000
    #
    for file_iter in range(num_sentences // 100000):
           output_name = "mistakes" + str(file_iter) + ".txt"
           data = row_data[slice_first: min(slice_second, len(row_data))]
           preprocessed.preprocess_data(data, output_name)
           slice_first = file_iter * 100000
           slice_second += 100000
    # #
    files_paths = os.listdir(r"C:\Users\Милана\PycharmProjects\курсовая работа\data resources\data_detection")
    files_paths = [file for file in files_paths if file.startswith("output")]
    os.chdir(r"C:\Users\Милана\PycharmProjects\курсовая работа\data resources\data_detection")

    sentences = preprocessed.get_sentences(files_paths)

    manager.build_vocabs(sentences)

    change_variable(path_config, "model_params", "vocab_size", str(len(manager.speech_to_id)))
    change_variable(path_config, "model_params", "target_size", str(len(manager.mistakes_to_id)))

    #add information to plot mistakes
    with open("info_to_plot_2014.json", "w") as file:
        json.dump(preprocessed.all_mistakes, file)

    x_train, y_train, x_val, y_val, x_test, y_test = manager.get_train_data(sentences)
    return x_train, y_train, x_val, y_val, x_test, y_test

def implement_model( x_train, y_train, x_val, y_val, x_test, y_test, config, kind_data=2,):
    x_train = [i[kind_data] for i in x_train]
    x_val = [i[kind_data] for i in x_val]
    x_test = [i[kind_data] for i in x_test]

    N_EPOCHS = config["epoch"]  # parameter to choose
    iterations = len(x_train) // config["batch_size"]  # how often we can learn the network for each epoch
    val_iterations = len(x_val) // config["batch_size"]

    model, optimizer, scheduler, criterion = model_organizer.create_model()

    batch_losses = model_organizer.train_model(model, optimizer, scheduler, criterion, x_train, y_train, x_val, y_val,
                                               N_EPOCHS, iterations, val_iterations)

    return batch_losses


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    path_config = "config.uni"
    path_data = r"C:\Users\Милана\PycharmProjects\курсовая работа\data resources\data_detection"
    config = get_config(path_config)

    logger = get_logger()

    manager = DataManager()
    preprocessed = DataPreprosser(path_data)

    get_data()
