#!/usr/bin/env python3

import argparse
from lib.keyword_search import build_command, search_command

def main()-> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")
    
    subparsers.add_parser("build", help="Build the inverted index and save it to disk")
    
    args = parser.parse_args()
        
    match args.command:
        case "search":
            print(f"Searching for: {args.query}")
            results = search_command(args.query)
            for result in results:
                print(f"ID: {result['id']} Title:{result['title']}")
                
        case "build":
            print("Building inverted index")
            build_command()
            print("Inverted index build successfully.")
        case __:
            parser.print_help()
    
if __name__ == "__main__":
    main()
        