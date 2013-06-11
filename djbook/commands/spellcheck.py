from cliff.command import Command as BaseCommand
import logging
import os
import re
import subprocess


class Command(BaseCommand):
    """
    Spell check .po files.
    """

    ignore_patterns = (
        re.compile(r'^@\(#\) Yandex Speller 1\.0$'),
    )
    missed_pattern = re.compile('^# (?P<word>.+) \d+$')
    error_pattern = re.compile('^& (?P<word>.+) \d+ \d+: (?P<correct_word>.+)$')
    log = logging.getLogger(__name__)

    def __init__(self, *args, **kwargs):
        super(Command, self).__init__(*args, **kwargs)

        if getattr(self.app, 'doc_path', None):
            ignore_file_path = os.path.join(self.app.doc_path, 'djbook', 'spellcheck_ignore.txt')

            with open(ignore_file_path) as f:
                self.ignore_words = [unicode(s, 'utf-8').lower() for s in f.read().split('\n')]

    def get_parser(self, prog_name):
        parser = super(Command, self).get_parser(prog_name)
        parser.add_argument("--all", action="store_true", help="Show all errors", dest="show_all", default=True)
        parser.add_argument("--no-ignore", action="store_true", help="Do not ignore words from djbook/spellcheck_ignore.txt",
            dest="no_ignore", default=False)
        parser.add_argument("--missed", action="store_true", help="Show missed in dictionary words", dest="show_missed")
        parser.add_argument("--errors", action="store_true", help="Show errors in words", dest="show_errors")
        parser.add_argument("--pause", action="store_true", help="Make pause when errors are fount", dest="pause")
        return parser

    def take_action(self, parsed_args):
        yspell = os.path.join(self.app.doc_path, 'djbook/yspell.pl')
        cmd = 'perl %s --encoding=utf8 --lang=ru < %s | egrep -v "^\*?$"'

        for path, dirs, files in os.walk(self.app.locale_path):
            for f in files:
                if f.endswith('.po'):
                    po_path = os.path.join(path, f)
                    self.app.stdout.write('Check: %s\n' % po_path)
                    output = subprocess.check_output(cmd % (yspell, po_path), shell=True)
                    lines = self.show_output(output, parsed_args)

                    if lines and parsed_args.pause:
                        raw_input()

    def show_output(self, output, parsed_args):
        """
        Output format description http://aspell.net/man-html/Through-A-Pipe.html
        """
        lines = 0

        for line in output.split('\n'):
            if not line or self.filter_output(line, parsed_args):
                continue

            lines += 1
            self.app.stdout.write(line)
            self.app.stdout.write('\n')

        return lines

    def filter_output(self, line, parsed_args):
        for ptr in self.ignore_patterns:
            if ptr.match(line):
                return True

            missed_match = self.missed_pattern.match(line)

            if parsed_args.show_errors and missed_match:
                return True

            if missed_match and unicode(missed_match.group('word'), encoding='utf-8').lower() in self.ignore_words and not parsed_args.no_ignore:
                return True

            error_match = self.error_pattern.match(line)

            if parsed_args.show_missed and error_match:
                return True

            if error_match and unicode(error_match.group('word'), encoding='utf-8').lower() in self.ignore_words and not parsed_args.no_ignore:
                return True
