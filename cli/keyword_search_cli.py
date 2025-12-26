#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer

def preprocess_text(text: str) -> list[str]:
    text = text.lower()
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = text.split()
    return text

def any_token_matches(query_tokens: list[str], title_tokens: list[str]) -> bool:
    return any(
        query_token in title_token
        for query_token in query_tokens
        for title_token in title_tokens
    )

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    with open("data/movies.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open("data/stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = f.read()

    stopwords = stopwords.splitlines()

    stemmer = PorterStemmer()

    limit = 5


    match args.command:
        # uv run cli/keyword_search_cli.py search "alien"
        case "search":
            results = []
            print(f"Searching for: {args.query}")
            for movie in data["movies"]:
                query_tokens = preprocess_text(args.query)
                title_tokens = preprocess_text(movie["title"])

                for query_token in query_tokens:
                    if query_token in stopwords:
                        query_tokens.remove(query_token)
                
                for title_token in title_tokens:
                    if title_token in stopwords:
                        title_tokens.remove(title_token)

                query_tokens = [stemmer.stem(token) for token in query_tokens]
                title_tokens = [stemmer.stem(token) for token in title_tokens]

                if any_token_matches(query_tokens, title_tokens):
                    results.append(movie)
                    if len(results) >= limit:
                        break

            for i in range(0, len(results)):
                print(f"{i}. {results[i]['title']}")

        # uv run cli/keyword_search_cli.py
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
