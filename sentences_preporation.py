import spacy
import re

nlp = spacy.load("en_core_web_sm")


class Decoding_sentences:
    def __init__(self, sentence: str):
        self.nlp = nlp
        self.doc_sent = []
        self.sent = sentence

    def make_clear(self):
        self.sent = self.sent.lower()
        #self.sent = re.sub(r"[^A-Za-z0-9]+", ' ', self.sent)
        self.doc_sent = nlp(self.sent)

    # grammatical features of every element in a list (.tag_)
    def get_tag(self) -> list:
        tags = [token.tag_ for token in self.doc_sent]
        return tags

    # syntactic tree of sentence (.dep_)
    def get_dep(self) -> list:
        dependencies = [token.dep_ for token in self.doc_sent]
        return dependencies

    # grammatical features of only the main sentence
    def get_main_sentences(self):
        dependencies_local = self.get_dep()
        tags_local = self.get_tag()
        if "nsubj" not in dependencies_local:
            return None

        subject, root = dependencies_local.index("nsubj"), dependencies_local.index("ROOT")

        return [tags_local[subject], tags_local[root]]

