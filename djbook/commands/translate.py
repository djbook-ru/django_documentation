import logging
import os

from cliff.command import Command as BaseCommand
from polib import pofile
from textblob import TextBlob


class Command(BaseCommand):
    """
    Translate untranslated messages with Google Translator.

    Example:

        ./translator.py translate ref/models/options.po

    If something wrong, try to install extra packages for textblob:

        python -m textblob.download_corpora
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Command, self).get_parser(prog_name)
        parser.add_argument('file', metavar='file', type=str, help='Path to .po file')
        return parser

    def take_action(self, parsed_args):
        po_path = os.path.join(self.app.locale_path, parsed_args.file)
        po = pofile(po_path)

        for entry in po.untranslated_entries():
            if entry.obsolete:
                continue

            en_msg = TextBlob(entry.msgid)
            print
            print en_msg
            print
            entry.msgstr = unicode(en_msg.translate(from_lang="en", to='ru'))
            entry.flags.append(u'fuzzy')
            print entry.msgstr

        po.save()
