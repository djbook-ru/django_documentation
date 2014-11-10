# coding: utf-8
import logging
import os

from cliff.command import Command as BaseCommand


class Command(BaseCommand):
    """
    [for development purpose]
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        spelling_path = os.path.join(self.app.doc_path, '_build/spelling/output.txt')
        stats = {}
        with open(spelling_path) as f:
            for row in f:
                word = row[:-1]

                if word in stats:
                    stats[word] += 1
                else:
                    stats[word] = 1

        stats = stats.items()
        stats = sorted(stats, key=lambda item: item[1], reverse=True)

        for word, count in stats:
            if count > 1:
                self.app.stdout.write('%s - %s\n' % (word, count))
