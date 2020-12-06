import spacy

nlp = spacy.load("en_core_web_sm")


class Decoding_sentences:
    def __init__(self, sentence: str):
        self.nlp = nlp
        self.doc_sent = nlp(sentence)

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

