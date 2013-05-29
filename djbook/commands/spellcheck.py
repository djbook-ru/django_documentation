from cliff.command import Command as BaseCommand
import logging
import os


class Command(BaseCommand):
    """
    Spell check .po files.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        'perl yspell.pl --encoding=utf8 --lang=ru < locale/ru/LC_MESSAGES/intro/tutorial02.po | grep -v "*" | grep -v -e "^$"'
        pass
