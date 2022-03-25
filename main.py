from requests import request
import settings
import argparse
from bs4 import BeautifulSoup
import re
import json
from os.path import exists


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("base_url", metavar="base-url", type=str, help="The base URL")
    parser.add_argument(
        "output",
        type=str,
        help="The name of the output file that data is written to",
    )
    parser.add_argument(
        "--class-name", type=str, help="The class name to read text from"
    )
    parser.add_argument(
        "--min",
        type=int,
        default=settings.DEFAULT_MIN_WORDS,
        help="Minimum amount of required words in a sentence",
    )
    parser.add_argument(
        "--max",
        type=int,
        default=settings.DEFAULT_MAX_WORDS,
        help="Maximum amount of required words in a sentence",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=settings.DEFAULT_LIMIT,
        help="The number of sentences that are retrieved",
    )
    parser.add_argument(
        "--paths", type=str, help="List of space-separated paths to read from"
    )
    parser.add_argument(
        "--paths-file",
        # metavar="--paths-file",
        type=str,
        help="A file containing line-separated paths to read from",
    )
    return parser.parse_args()


def write_to_file(texts, filename):
    file_content = {}
    if exists(filename):
        file = open(filename)
        file_content = json.loads(file.read())
    for sentences in texts:
        key = f"Q{len(file_content.keys())}"
        file_content[key] = sentences
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(file_content, file, ensure_ascii=False)


def count_words(sentence):
    words = sentence.split()
    return len(words)


# Function to split sentences from a string. Returns sentences in a list.
def get_sentences(text, limit=None, min_words=None, max_words=None):
    if min_words is not None and max_words is not None and min_words > max_words:
        raise ValueError("Min value must be lower than, or equal to, max value.")
    pattern = r"([0-9]\. |[^.!?])*[.!?](\"|)"
    result = {"first": "", "rest": []}
    count = 0
    for match in re.finditer(pattern, text):
        if limit is not None and count >= limit:
            break
        sentence = match.group(0).strip()
        word_count = count_words(sentence)
        if min_words is not None and word_count < min_words:
            continue
        if max_words is not None and word_count > max_words:
            continue
        if count == 0:
            result["first"] = sentence
        else:
            result["rest"].append(sentence)
        count += 1
    return result


# def find_texts(url, paths, article_class):
#     count = 0
#     n_paths = len(paths)
#     while count < n_paths:
#         if paths:
#             response = request(url=f"{url}{paths[count]}", method="GET")
#         else:
#             response = request(url=url, method="GET")
#         soup = BeautifulSoup(response.text, features="html.parser")
#         article = soup.find_all("div", {"class": article_class})
#         article_text = ""
#         for text in article:
#             p_tags = text.findChildren("p", recursive=False)
#             for p in p_tags:
#                 article_text += p.get_text() + " "
#         count += 1
#     return article_text


def get_paths(paths):
    if paths:
        return paths.split()
    return []


def read_paths(filename):
    if filename:
        file = open(filename, "r")
        content = file.read()
        file.close()
        paths = content.strip().split("\n")
        return paths
    return []


def get_text(url, article_class):
    response = request(url=url, method="GET")
    soup = BeautifulSoup(response.text, features="html.parser")
    article = soup.find_all("div", {"class": article_class})
    article_text = ""
    for text in article:
        p_tags = text.findChildren("p", recursive=False)
        for p in p_tags:
            article_text += p.get_text() + " "
    return article_text


def get_all_texts(base_url, paths, article_class):
    texts = []
    for path in paths:
        texts.append(get_text(base_url + path, article_class))
    return texts


def get_and_process_sentences(
    base_url, paths, article_class, limit, min_words, max_words
):
    texts = []
    sentences = []
    if paths:
        texts = get_all_texts(base_url, paths, article_class)
    else:
        texts.append(get_text(base_url, article_class))
    for text in texts:
        sentences.append(get_sentences(text, limit, min_words, max_words))
    return sentences


def main():
    args = init_args()
    base_url = args.base_url
    filename = args.output
    paths = get_paths(args.paths)
    paths += read_paths(args.paths_file)
    class_name = args.class_name
    sentences = get_and_process_sentences(
        base_url,
        paths,
        class_name,
        limit=args.limit,
        min_words=args.min,
        max_words=args.max,
    )
    write_to_file(sentences, filename)


if __name__ == "__main__":
    main()
