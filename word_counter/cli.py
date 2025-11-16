import argparse
import os
import csv
from .logic import (
    tokenize, remove_stopwords, lemmatize_words,
    count_frequencies, filter_singletons, format_table
)

def run_cli(argv):
    parser = argparse.ArgumentParser(description="Word Counter")

    parser.add_argument("input", nargs=1, help="Text or filename")

    parser.add_argument(
        "-o", "--output",
        help="Save results as CSV (suppresses terminal display)"
    )

    parser.add_argument(
        "--hide-count-1", "-H",
        action="store_true",
        help="Hide words with count = 1"
    )

    args = parser.parse_args(argv)
    input_arg = args.input[0]

    # Determine if input is file or raw text
    if os.path.isfile(input_arg):
        with open(input_arg, "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = input_arg

    # Word processing pipeline
    words = tokenize(text)
    words = remove_stopwords(words)
    words = lemmatize_words(words)
    freqs = count_frequencies(words)

    # Apply singleton filtering if requested
    if args.hide_count_1:
        freqs = filter_singletons(freqs)

    # If no CSV output specified, print table
    if not args.output:
        print(format_table(freqs))

    # If CSV output specified, write file
    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["word", "count"])
            writer.writerows(freqs)
        print(f"Saved CSV → {args.output}")
