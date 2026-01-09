import json
import pickle
import os

class InvertedIndex:
    def __init__(self):
        self.index = {}
        self.docmap = {}
    
    def __add_document(self, doc_id, text):
        tokens = text.split()
        
        for token in tokens:
            token = token.lower()
            if token not in self.index.keys():
                self.index[token] = set()
            self.index[token].add(doc_id)
    
    def get_document(self, term):
        documents = self.index[term.lower()]
        return list(documents).sort()

    def build(self, movies_data):
        for movie in movies_data["movies"]:
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(movie["id"], text)
            self.docmap[movie["id"]] = movie
    
    def save(self):
        os.makedirs("cache", exist_ok=True)
        index_path = "cache/index.pkl"
        docmap_path = "cache/docmap.pkl"
        
        with open(index_path, 'wb') as file:
            pickle.dump(self.index, file)
            
        with open(docmap_path, 'wb') as file:
            pickle.dump(self.docmap, file)