import re
import urllib.request, urllib.error
from collections import Counter

from bs4 import BeautifulSoup
from tenacity import *


class HTMLParser:
    """ HTML parser returns word count for given URL """

    @retry(stop=stop_after_attempt(5), wait=wait_fixed(2), reraise=True)
    def __init__(self, url):
        html = urllib.request.urlopen(url).read()
        self.soup = BeautifulSoup(html, features="html.parser")

        # Remove style elements
        for script in self.soup(["script", "style"]):
            script.extract()

    @staticmethod
    def _count_words(word_list: list) -> dict:
        return dict(Counter(word_list))

    def _parse_text(self, text: str) -> dict:
        """
        Parse a string of text to find the number of unique words.

        :param text; string containing text to be formatted and counted
        :return count; dict containing unique words and number of occurrences
        """

        # Matching only words that use letters in the English alphabet
        # Contractions will have the apostrophe stripped and hyphenated words will be joined
        # In a real application this would be extended based on requirements/audience
        text_stripped = re.sub('[^A-Za-z ]', '', text)

        # Use common case and remove instances of empty string left from split
        all_words = [word for word in text_stripped.lower().split(' ') if word]

        count = self._count_words(all_words)

        return count

    def text(self) -> dict:
        """
        Count instances of words contained in all HTML tags.

        :return content; dict containing unique words and number of occurrences
        """
        text = self.soup.get_text(separator=' ')
        content = self._parse_text(text)

        return content

    def tag(self, tag: str) -> dict:
        """
        Count instances of words contained in specific HTML tags

        :return content; dict containing unique words and number of occurrences
        """

        text = ''
        for node in self.soup.find_all(tag):
            text += ' '.join(node.find_all(text=True)) + ' '

        content = self._parse_text(text)

        return content
