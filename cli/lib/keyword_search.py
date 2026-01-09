import json
import pickle
import os
import string
from collections import defaultdict
from nltk.stem import PorterStemmer

from .search_utils import(
    CACHE_DIR,
    DEFAULT_SEARCH_LIMIT,
    load_movies,
    load_stopwords
)

class InvertedIndex:
    def __init__(self):
        self.index = defaultdict(set)
        self.docmap : dict[int, dict] = {}
        self.index_path = os.path.join(CACHE_DIR, "index.pkl")
        self.docmap_path = os.path.join(CACHE_DIR, "docmap.pkl")
    
    def __add_document(self, doc_id, text):
        tokens = tokenize_text(text)
        for token in set(tokens):
            self.index[token].add(doc_id)
    
    def get_document(self, term):
        doc_ids = self.index[term]
        return sorted(list(doc_ids))

    def build(self):
        movies_data = load_movies()
        for movie in movies_data:
            text = f"{movie['title']} {movie['description']}"
            self.__add_document(movie["id"], text)
            self.docmap[movie["id"]] = movie
    
    def save(self):
        os.makedirs(CACHE_DIR, exist_ok=True)
        index_path = "cache/index.pkl"
        docmap_path = "cache/docmap.pkl"
        
        with open(index_path, 'wb') as file:
            pickle.dump(self.index, file)
            
        with open(docmap_path, 'wb') as file:
            pickle.dump(self.docmap, file)
    
    def load(self) -> None:
        index_path = "cache/index.pkl"
        docmap_path = "cache/docmap.pkl"
        if not os.path.isfile(index_path):
            raise Exception("Index file not exist")
        if not os.path.isfile(docmap_path):
            raise Exception("Docmap file not exist")
        
        with open(index_path, 'rb') as file:
            self.index = pickle.load(file)
        with open(docmap_path, 'rb') as file:
            self.docmap = pickle.load(file)
        
def build_command() -> None:
    inverted = InvertedIndex()
    inverted.build()
    inverted.save()

def search_command(query, limit=DEFAULT_SEARCH_LIMIT) -> list[dict]:
    inverted = InvertedIndex()
    inverted.load()
    results = []
    query_tokens = tokenize_text(query)
    for q_token in query_tokens:
        doc_ids = inverted.get_document(q_token)
        doc_ids = sorted(list(doc_ids))
        for doc_id in doc_ids:
            results.append(inverted.docmap[doc_id])
            if len(results) >= limit:
                break
    return results

def has_matching_token(query_tokens, title_tokens) -> bool:
    for q in query_tokens:
        for t in title_tokens:
            if q in t:
                return True
    return False

def preprocess_text(text:str) -> str:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    return text
    
def tokenize_text(text: str) -> list[str]:
    text = preprocess_text(text)
    tokens = text.split()
    valid_tokens = []
    for token in tokens:
        if token:
            valid_tokens.append(token)
    
    stop_words = load_stopwords()
    filterred_words = []
    for token in valid_tokens:
        if token not in stop_words:
            filterred_words.append(token)
    
    stemmer = PorterStemmer()
    stemmed_words = []
    for word in filterred_words:
        stemmed_words.append(stemmer.stem(word))
    
    return stemmed_words