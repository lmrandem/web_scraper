#!/usr/bin/env python3
import unittest
from unittest.mock import patch

from main import get_and_process_sentences, init_args, read_paths, get_id, count_words


class TestWebScrape(unittest.TestCase):
    # def setUp(self):
    # self.parser = init_args()

    def test_getAndProcessTwoSentences(self):
        with patch("sys.argv", ["", "https://snl.no/", "out.json", "query1.json", "snl"]):
            args = init_args()
            paths = read_paths(args.paths_file, args.key)
            self.test = get_and_process_sentences(args.base_url,
                                                  paths,
                                                  args.element,
                                                  class_name="article-text",
                                                  limit=args.limit,
                                                  min_words=args.min,
                                                  max_words=args.max)
            self.assertEqual(self.test[0]['sentences']["first"],
                             "George Washington var en nordamerikansk offiser, politiker og plantasjeeier fra Virginia.")
            self.assertEqual(self.test[1]['sentences']["first"],
                             "Adams skrev også flere andre bøker og manus til en rekke dataspill.")

    def test_getID(self):
        value = "https://www.wikidata.org/entity/Q23232111111"
        self.test = get_id(value)
        self.assertEqual(self.test, "Q23232111111")

    def test_countWords(self):
        words = "Google is best Computer Science Tool"
        self.test = count_words(words)
        self.assertEqual(self.test, 6)


if __name__ == '__main__':
    unittest.main()
