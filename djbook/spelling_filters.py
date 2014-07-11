# coding: utf-8
import re
from enchant.tokenize import Filter


class IgnoreEnglishFilter(Filter):
    """Given a set of words, ignore them all.
    """

    def __init__(self, *args, **kwargs):
        super(IgnoreEnglishFilter, self).__init__(*args, **kwargs)
        self.pattern = re.compile(ur'[а-яА-Я]+')

    def _skip(self, word):
        return not self.pattern.search(word)
