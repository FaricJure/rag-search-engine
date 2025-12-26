#!/usr/bin/env python3

import argparse
import json
import string
from nltk.stem import PorterStemmer
from inverted_index import InvertedIndex

class TextTokenizer:
    def __init__(self, stopwords: set[str]) -> None:
        self._stopwords = stopwords
        self._stemmer = PorterStemmer()

    def tokenize_text(self, text: str) -> list[str]:
        text = text.lower()
        text = text.translate(str.maketrans("", "", string.punctuation))
        tokens = text.split()
        return [self._stemmer.stem(token) for token in tokens if token not in self._stopwords]

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

    subparsers.add_parser("build", help="Build inverted index")

    args = parser.parse_args()

    with open("data/movies.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    with open("data/stopwords.txt", "r", encoding="utf-8") as f:
        stopwords = f.read()

    stopwords = set(stopwords.splitlines())

    tokenizer = TextTokenizer(stopwords)

    limit = 5


    match args.command:
        # uv run cli/keyword_search_cli.py search "alien"
        case "search":
            results = []
            print(f"Searching for: {args.query}")
            for movie in data["movies"]:
                query_tokens = tokenizer.tokenize_text(args.query)
                title_tokens = tokenizer.tokenize_text(movie["title"])

                if any_token_matches(query_tokens, title_tokens):
                    results.append(movie)
                    if len(results) >= limit:
                        break

            for i in range(0, len(results)):
                print(f"{i}. {results[i]['title']}")

        # uv run cli/keyword_search_cli.py build
        case "build":
            index = InvertedIndex(tokenize=tokenizer.tokenize_text)
            index.build(data["movies"])
            index.save()
            merida_docs = index.get_documents("merida")
            first_merida_id = merida_docs[0] if merida_docs else None
            print(f"First document ID for token 'merida': {first_merida_id}")

        # uv run cli/keyword_search_cli.py
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()
