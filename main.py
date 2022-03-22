from requests import request
import argparse, sys
from bs4 import BeautifulSoup

#def init_args():
#    parser = argparse.ArgumentParser()
#    parser.add_argument('--file')
#    return vars(parser.parse_args())

def main():
    if len(sys.argv) < 2:
        raise TypeError('Missing argument')
    url = sys.argv[1]
    response = request(url=url, method='GET')
    soup = BeautifulSoup(response.text, features='html.parser')
    article = soup.find_all('div', {'class': 'article-text' })
    article_text = ''
    for text in article:
        p_tags = text.findChildren('p', recursive=False)
        for p in p_tags:
            article_text += p.get_text() + ' '
    print(article_text)

if __name__ == '__main__':
    main()