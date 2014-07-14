# coding: utf-8
import logging
import os

from cliff.command import Command as BaseCommand


class Command(BaseCommand):
    """
    Spell-check translation. Words are lowered to reduce number of ignored words.
    Also `ё` replaced with `Ё`.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self.app.run_subcommand(['compilemessages'])

        doctrees_path = os.path.join(self.app.doc_path, '_build/doctrees')
        spelling_path = os.path.join(self.app.doc_path, '_build/spelling')
        cmd = 'sphinx-build -b spelling -n -d %s -D language=ru_RU . %s'
        os.system(cmd % (doctrees_path, spelling_path))
        self.app.stdout.write('Check result in %s\n' % spelling_path)
