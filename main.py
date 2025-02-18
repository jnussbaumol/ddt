import argparse
import tiktoken
from pathlib import Path
from dataclasses import dataclass

GPT_4O = "gpt-4o"
GPT_4O_MINI = "gpt-4o-mini"
GPT_4_TURBO = "gpt-4-turbo"
GPT_4 = "gpt-4"


def main():
    print("Hello from tokenizer!")
    parser = setup_argparse()

    args = parser.parse_args()
    if len(args.directory) == 0:
        print("ERROR: No Directory Provided")
        exit(1)

    root = Path(args.directory)
    if not root.is_dir():
        print("ERROR: Path Provided Is Not A Directory")
        exit(1)

    files = list(root.glob("**/*.*"))
    file_categories: dict[str, list[tuple[str, int]]] = {}
    category_totals: dict[str, int] = {}
    running_total = 0

    for file in files:
        if "old" in file.__str__():
            continue
            # print("file marked as old, skipping for now")
            # print(file)
        text = file.read_text()
        filename = file.name
        filetype = file.suffix[1:]
        token_counts = num_tokens_from_string(text, GPT_4O)
        file_categories[filetype].append((filename, token_counts))
        category_totals[filetype] += token_counts
        running_total += token_counts

    # TODO: finish this - print all the totals and stuff


def setup_argparse() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="Tokenizer",
        description="Crawls a given directory, counts the number of tokens per filetype in the project and returns a per-type total and grand total",
        epilog="0x4D5352",
    )
    parser.add_argument("directory")
    # parser.add_argument("-v", "--verbose", action="store_true")
    return parser


def num_tokens_from_string(string: str, model_name: str) -> int:
    """Returns the number of tokens in a text string"""
    encoding = tiktoken.encoding_for_model(model_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


if __name__ == "__main__":
    main()
