import collections
import numpy as np

from data_preporation import get_sentences

sentences = get_sentences(["file.txt"])

class Model:
    def __init__(self):
        self.UNK = "<unk>"

        self.word_to_id = dict()
        self.mistakes_to_id = dict()
        self.speech_to_id = dict()
        self.tree_to_id = dict()

        self.singletons = []

    def build_vocabs(self, data_train: list, embedding_path=None):
        """
        creates dicts for words, mistakes and part_speech tokens to use it then for decoding
        :param data_train: data organised in conll format
        :param embedding_path: path to embeddings, isn't used for 07/01/20
        """

        data = data_train

        word_counter = collections.Counter()
        mistakes_counter = collections.Counter()
        parts_speech_counter = collections.Counter()
        parts_tree_counter = collections.Counter()

        for sent in data:
            for line in sent:
                word_counter.update([line[0]])  # add word
                mistakes_counter.update([line[1]])
                parts_speech_counter.update([line[2]])
                parts_tree_counter.update([line[3]])

        # words to ids
        self.word_to_id = collections.OrderedDict([(self.UNK, 1)])
        for word, count_w in word_counter.most_common():
            if word not in self.word_to_id:
                self.word_to_id[word] = len(self.word_to_id) + 1

        self.singletons = [word for word in word_counter if word_counter[word] == 1]  # единички

        # mistakes to ids
        self.mistakes_to_id = collections.OrderedDict()
        for mistake, count_m in mistakes_counter.most_common():
            if mistake not in self.mistakes_to_id:
                self.mistakes_to_id[mistake] = len(self.mistakes_to_id) + 1

        # parts of speech to ids
        self.speech_to_id = collections.OrderedDict()
        for speech, count_s in parts_speech_counter.most_common():
            if speech not in self.speech_to_id:
                self.speech_to_id[speech] = len(self.speech_to_id) + 1

        # parts of tree to ids
        self.tree_to_id = collections.OrderedDict()
        for tree, count_t in parts_tree_counter.most_common():
            if tree not in self.speech_to_id:
                self.tree_to_id[tree] = len(self.tree_to_id) + 1


    def decode_sentences(self, sentences: list, max_sent_length = 50):
        """
        :param sentences: raw data from get_sentences func
        :param max_sent_length: maximum length of sent, default value is 50
        :return: decoded_sents and labels
        """
        decoded_sents = []
        decoded_labels = []

        for sent in sentences:
            if len(sent) >= max_sent_length:
                continue

            #decoded_sent[0] - words, [1] - tokens, [2] - trees
            decoded_sent = np.zeros((3, max_sent_length))
            decoded_label = np.zeros(max_sent_length)
            for word_line_ind, word_line in enumerate(sent):
                decoded_sent[0][word_line_ind] = self.word_to_id[word_line[0]]
                decoded_sent[1][word_line_ind] = self.speech_to_id[word_line[2]]
                decoded_sent[2][word_line_ind] = self.tree_to_id[word_line[3]]

                decoded_label[word_line_ind] = self.mistakes_to_id[word_line[1]]

            decoded_sents.append(decoded_sent)
            decoded_labels.append(decoded_label)

        return decoded_sents, decoded_labels

    def get_batches_sentences(self, sentences: list, labels:list, batch_size:int):
        """
        :param sentences: data in numeric form - words, mistakes (labels), part_speech, tree
        sentences are in format:
        [[[tokens, part_speech, tree], [labels]], [[tokens, part_speech, tree], [labels]]]
        :param batch_size: the size of batch
        :return: yields batch
        """
        x, y = sentences, labels
        n_samples = len(x)

        batches = []

        # Shuffle at the start of epoch
        indices = np.arange(n_samples)
        np.random.shuffle(indices)

        for start in range(0, n_samples, batch_size):
            end = min(start + batch_size, n_samples)

            batch_idx = indices[start:end]
            yield np.array(x, "int_")[batch_idx], np.array(y, "int_")[batch_idx]


model = Model()
model.build_vocabs(sentences)
d_sents, d_labels = model.decode_sentences(sentences)

generator_batches = model.get_batches_sentences(d_sents, d_labels, 3)


sents_ex = [
    [
        ['good', ' None', 'JJ', 'amod'],
        ['luck', ' None', 'NN', 'ROOT'],
        ['on', ' None', 'IN', 'prep'],
        ['your', ' None', 'PRP$', 'poss'],
        ['new', ' None', 'JJ', 'amod'],
        ['start', ' None', 'NN', 'pobj'],
        ['!', ' None', '.', 'punct']
    ],
    [   ['my', ' None', 'PRP$', 'poss'],
        ['teacher', ' None', 'NN', 'nsubj'],
        ['is', ' None', 'VBZ', 'aux'],
        ['going', ' None', 'VBG', 'ROOT'],
        ['to', ' None', 'TO', 'aux'],
        ['move', ' None', 'VB', 'xcomp'],
        ['to', ' None', 'TO', 'aux'],
        ['change', ' None', 'VB', 'advcl'],
        ['his', ' None', 'PRP$', 'poss'],
        ['job', ' None', 'NN', 'dobj'],
        ['.', ' None', '.', 'punct']
        ]
    ]