# coding: utf-8
import logging
import os

from shutil import copyfile
from cliff.command import Command as BaseCommand


class Command(BaseCommand):
    """
    Spell-check translation. Words are lowered to reduce number of ignored words.
    Also `ё` replaced with `Ё`.
    """
    log = logging.getLogger(__name__)

    def take_action(self, parsed_args):
        self._check_enviroment()

        doctrees_path = os.path.join(self.app.doc_path, '_build/doctrees')
        spelling_path = os.path.join(self.app.doc_path, '_build/spelling')
        cmd = 'sphinx-build -b spelling -n -d %s -D language=ru_RU . %s'
        os.system(cmd % (doctrees_path, spelling_path))
        self.app.stdout.write('Check result in %s\n' % spelling_path)

    def _check_enviroment(self):
        import enchant
        enchant_path = os.path.dirname(enchant.__file__)

        # FIXME: dirty hack to fix tokenize fo ru_RU
        try:
            from enchant.tokenize.ru import tokenize
        except ImportError:
            copyfile(
                os.path.join(self.app.doc_path, 'djbook/spelling_tokenize_ru.py'),
                os.path.join(enchant_path, 'tokenize/ru.py')
            )

        from enchant.tokenize.ru import tokenize

        # Check if ru_RU dictionary exists
        if not os.path.exists(os.path.join(enchant_path, 'share/enchant/myspell/ru_RU.dic')):
            cmd = 'mkdir -p %s/share/enchant/myspell'
            os.system(cmd % enchant_path)

            cmd = 'tar -xzf %s/djbook/dict_ru.tar.gz -C %s/share/enchant/myspell'
            os.system(cmd % (self.app.doc_path, enchant_path))
