#!/usr/bin/env python3

import argparse
import json
import string
import pickle
from nltk.stem import PorterStemmer
from inverted_index import InvertedIndex

def main()-> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")
    
    build_parser = subparsers.add_parser("build", help="Build the inverted index and save it to disk")
    
    args = parser.parse_args()
    
    stemmer = PorterStemmer()
    
    match args.command:
        case "search":
            with open("data/movies.json", "r") as data:
                movies_data = json.load(data)
            with open("data/stopwords.txt", "r") as data:
                stopwords = data.read().splitlines()
            print(f"Searching for: {args.query}")
            results = []
            for movie in movies_data["movies"]:
                translation_table = str.maketrans("", "", string.punctuation)
                query_tokens = args.query.split(" ")
                query_tokens = [word for word in query_tokens if word not in stopwords]
                for query_token in query_tokens:            
                    if stemmer.stem(query_token.lower().translate(translation_table)) in movie["title"].lower().translate(translation_table):
                        results.append(movie["title"])
                        break
            for i in range(len(results)):
                print(f"{i+1}. {results[i]}")
        case "build":
            with open("data/movies.json", "r") as data:
                movies_data = json.load(data)
            inverted = InvertedIndex()
            inverted.build(movies_data)
            inverted.save()
            
            with open("cache/index.pkl", 'rb') as file:
                docs = pickle.load(file)
            print(f"First document for token 'merida' = {docs['merida']}")
        case __:
            parser.print_help()
    
if __name__ == "__main__":
    main()
        