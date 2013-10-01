#!/usr/bin/env python
from cliff.app import App
from djbook import commands
import imp
import logging
import os
import pkgutil
import sys


class CommandManager(object):

    def __init__(self, package):
        self.commands = {}
        self._load_commands(package)

    def _load_commands(self, package):
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            f, path, descr = imp.find_module(modname, package.__path__)
            module = imp.load_module(modname, f, path, descr)
            command_class = getattr(module, 'Command', None)
            if command_class:
                self.commands[modname] = self._add_load_to_command(command_class)

    def _add_load_to_command(self, command_class):
        def load(cls):
            return cls

        setattr(command_class, 'load', classmethod(load))

        return command_class

    def __iter__(self):
        return iter(self.commands.items())

    def add_command(self, name, command_class):
        self.commands[name] = self._add_load_to_command(command_class)

    def find_command(self, argv):
        """
        Given an argument list, find a command and
        return the processor and any remaining arguments.
        """
        search_args = argv[:]
        name = ''
        while search_args:
            if search_args[0].startswith('-'):
                raise ValueError('Invalid command %r' % search_args[0])
            next_val = search_args.pop(0)
            name = '%s %s' % (name, next_val) if name else next_val
            if name in self.commands:
                cmd_factory = self.commands[name]
                return (cmd_factory, name, search_args)
        else:
            raise ValueError('Unknown command %r' %
                             (argv,))


class TranslatorApp(App):

    log = logging.getLogger(__name__)

    def __init__(self):
        super(TranslatorApp, self).__init__(
            description='translator tools',
            version='0.1',
            command_manager=CommandManager(commands),
        )
        self.doc_path = os.path.dirname(os.path.abspath(__file__))
        self.locale_path = os.path.join(self.doc_path, 'locale', 'ru', 'LC_MESSAGES')
        self.templates_path = os.path.join(self.doc_path, 'djbook', 'templates')
        self.html_path = os.path.join(self.doc_path, '_build', 'html')

    def initialize_app(self, argv):
        pass

    def prepare_to_run_command(self, cmd):
        pass

    def clean_up(self, cmd, result, err):
        pass


def main(argv=sys.argv[1:]):
    translator_app = TranslatorApp()
    return translator_app.run(argv)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
