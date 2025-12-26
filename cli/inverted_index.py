from collections.abc import Callable
import os
import pickle
from typing import Iterable

class InvertedIndex:
    def __init__(self, tokenize: Callable[[str], Iterable[str]] | None = None):
        self.index = {}
        self.docmap = {}
        self._tokenize = tokenize or (lambda text: text.split())

    def __add_document(self, doc_id, text):
        tokens = self._tokenize(text)
        for token in tokens:
            if token not in self.index:
                self.index[token] = set()
            self.index[token].add(doc_id)

    def get_documents(self, term):
        normalized_term = term.lower()
        return sorted(self.index.get(normalized_term, set()))

    def build(self, movies):
        for movie in movies:
            doc_id = movie["id"]
            self.docmap[doc_id] = movie
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(doc_id, text)

    def save(self):
        os.makedirs("cache", exist_ok=True)
        with open("cache/index.pkl", "wb") as f:
            pickle.dump(self.index, f)
        with open("cache/docmap.pkl", "wb") as f:
            pickle.dump(self.docmap, f)
