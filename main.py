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
        "paths_file",
        metavar="paths-file",
        type=str,
        help="A JSON file containing paths",
    )
    parser.add_argument("key", type=str, help="The key from the JSON file to use")
    parser.add_argument("--element", type=str, help="The HTML element to retrieve data from")
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
        "--verbose", type=bool, default=False, help="Shows details about the process"
    )
    return parser.parse_args()


def write_to_file(texts, filename, verbose=False):
    file_content = {}
    if exists(filename):
        file = open(filename)
        file_content = json.loads(file.read())
    for text in texts:
        if verbose:
            print(f"Adding {text['id']} to output")
        key = text["id"]
        file_content[key] = text["sentences"]
    with open(filename, "w", encoding="utf-8") as file:
        if verbose:
            print(
                f'Writing {len(file_content.keys())} objects to output file "{filename}"...'
            )
        json.dump(file_content, file, ensure_ascii=False)
        if verbose:
            print(f'Successfully wrote to file "{filename}"')


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
    for match in re.finditer(pattern, text["text"]):
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


def get_id(item):
    split_item = item.split("/")
    return split_item[len(split_item) - 1]


def read_paths(filename, key):
    paths = []
    if not filename:
        return paths
    file = open(filename, "r")
    content = json.loads(file.read())
    file.close()
    for item in content:
        item_id = get_id(item["item"])
        path = item[key]
        paths.append({"id": item_id, "path": path})
    return paths


def get_text(url, element, class_name):
    response = request(url=url, method="GET")
    soup = BeautifulSoup(response.text, features="html.parser")
    article = soup.find_all(element, {"class": class_name})
    article_text = ""
    for text in article:
        p_tags = text.findChildren("p", recursive=False)
        for p in p_tags:
            article_text += p.get_text() + " "
    return article_text


def get_all_texts(base_url, paths, element, class_name, verbose=False):
    texts = []
    for path in paths:
        url = base_url + path["path"]
        if verbose:
            if class_name:
                print(
                    f"Retrieving text from {url} with the class name \"{class_name}\" ({path['id']})..."
                )
            else:
                print(f"Retrieving text from {url} ({path['id']})...")
        texts.append(
            {
                "id": path["id"],
                "text": get_text(url, element, class_name),
            }
        )
        if verbose:
            print(f"Text retrieved from {url} ({path['id']})")
    return texts


def get_and_process_sentences(
    base_url, paths, element, class_name, limit, min_words, max_words, verbose=False
):
    sentences = []
    texts = get_all_texts(base_url, paths, element, class_name, verbose=verbose)
    for text in texts:
        if verbose:
            print(f"Finding sentences in {text['id']}...")
        found_sentences = get_sentences(text, limit, min_words, max_words)
        sentences.append({"id": text["id"], "sentences": found_sentences})
        if verbose:
            print(
                f"Found requested sentences in {text['id']}: {len(found_sentences['rest']) + 1} sentence(s) found"
            )
    return sentences


def main():
    args = init_args()
    base_url = args.base_url
    filename = args.output
    paths = read_paths(args.paths_file, args.key)
    element = args.element or "div"
    class_name = args.class_name
    verbose = args.verbose
    sentences = get_and_process_sentences(
        base_url,
        paths,
        element,
        class_name=class_name,
        limit=args.limit,
        min_words=args.min,
        max_words=args.max,
        verbose=verbose,
    )
    write_to_file(sentences, filename, verbose=verbose)


if __name__ == "__main__":
    main()
