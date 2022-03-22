from requests import request
import argparse, sys
from bs4 import BeautifulSoup
import re

# def init_args():
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--file')
#    return vars(parser.parse_args())

# Regex to identify a sentence.
regular_expression = '([A-z][^.!?]*[.!?]*"?)'


# Function to split sentences from a string. Returns sentences in a list.
def get_sentences(text, regex):
    sentences = []
    for sentence in re.findall(regex, text):
        sentences.append(sentence)
    return sentences


def main():
    if len(sys.argv) < 2:
        raise TypeError('Missing argument')
    url = sys.argv[1]
    response = request(url=url, method='GET')
    soup = BeautifulSoup(response.text, features='html.parser')
    article = soup.find_all('div', {'class': 'article-text'})
    article_text = ''
    for text in article:
        p_tags = text.findChildren('p', recursive=False)
        for p in p_tags:
            article_text += p.get_text() + ' '
    print(article_text)


if __name__ == '__main__':
    main()
