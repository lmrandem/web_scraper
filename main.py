from requests import request
import argparse, sys
from bs4 import BeautifulSoup
import re
import json
from os.path import exists


# def init_args():
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--file')
#    return vars(parser.parse_args())


def write_to_file(sentences, filename):
    file_content = {}
    if exists(filename):
        file = open(filename)
        file_content = json.loads(file.read())
    key = f'Q{len(file_content.keys()) + 1}'
    file_content[key] = sentences
    with open(filename, 'w', encoding='utf-8') as file:
        json.dump(file_content, file, ensure_ascii=False)


def count_words(sentence):
    words = sentence.split()
    return len(words)


# Function to split sentences from a string. Returns sentences in a list.
def get_sentences(text, limit=None, min_words=None, max_words=None):
    pattern = r"([0-9]\. |[^.!?])*[.!?](\"|)"
    result = {'first': '', 'rest': []}
    count = 0
    for match in re.finditer(pattern, text):
        if limit is not None and count >= limit:
            break
        sentence = match.group(0).strip()
        word_count = count_words(sentence)
        if min_words is not None and max_words is not None:
            if min_words <= max_words:
                if word_count < min_words:
                    continue
                if word_count > max_words:
                    continue
        if count == 0:
            result['first'] = sentence
        else:
            result['rest'].append(sentence)
        count += 1
    return result


def find_text(url, article_class):
    response = request(url=url, method='GET')
    soup = BeautifulSoup(response.text, features='html.parser')
    article = soup.find_all('div', {'class': article_class})
    article_text = ''
    for text in article:
        p_tags = text.findChildren('p', recursive=False)
        for p in p_tags:
            article_text += p.get_text() + ' '
    return article_text


def main():
    if len(sys.argv) < 2:
        raise TypeError('Missing argument')
    url = sys.argv[1]
    text = find_text(url, 'article-text')
    result = get_sentences(text, 20, 5, 30)
    filename = sys.argv[2]
    write_to_file(result, filename)
    print(result)


if __name__ == '__main__':
    main()
