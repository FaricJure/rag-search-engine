#!/usr/bin/env python3

import argparse
import json


def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    search_parser = subparsers.add_parser("search", help="Search movies using BM25")
    search_parser.add_argument("query", type=str, help="Search query")

    args = parser.parse_args()

    with open("data/movies.json", "r", encoding="utf-8") as f:
        data = json.load(f)
        #print(data["movies"][0])    


    match args.command:
        # uv run cli/keyword_search_cli.py search "alien"
        case "search":
            results = []
            print(f"Searching for: {args.query}")
            for movie in data["movies"]:
                if args.query.lower() in movie["title"].lower():
                    results.append(movie)

            for i in range(0, len(results)):
                print(f"{i}. {results[i]['title']}")

            results = results[:5]  # keep only first 5 results

        # uv run cli/keyword_search_cli.py
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()