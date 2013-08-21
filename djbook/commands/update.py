import cStringIO
import logging
import os
import tarfile
import tempfile
import urllib2
import filecmp
import shutil

from cliff.command import Command as BaseCommand
from github import GithubException

from djbook.cliff_utils import GithubCommandMixin


class Command(GithubCommandMixin, BaseCommand):
    """
    Clone Django repo(https://github.com/django/django) to /tmp/
    """
    log = logging.getLogger(__name__)

    def get_parser(self, prog_name):
        parser = super(Command, self).get_parser(prog_name)
        parser.add_argument('tag', metavar='tag', type=str, help='Django git repo tag')
        return parser

    def take_action(self, parsed_args):
        repo = self.get_repo('django/django')
        tag = self.get_tag(repo, parsed_args.tag)

        archive = tarfile.open(mode="r:gz", fileobj=self.load_file(tag.tarball_url))
        self.sync_with_archive(archive, tag)
        self.app.run_subcommand(['makemessages'])

    def sync_with_archive(self, archive, tag):
        django_dir_name = archive.getmembers()[0].name.split('/')[0]
        doc_path = '%s/docs/' % (django_dir_name,)

        tmp_path = tempfile.mkdtemp()
        doc_tmp_path = os.path.join(tmp_path, doc_path)

        for obj in archive.getmembers():
            if obj.name.startswith(doc_path):
                archive.extract(obj, tmp_path)

        for root, dirs, files in os.walk(doc_tmp_path):
            for fname in files:
                tmp_fpath = os.path.join(root, fname)
                relative_fname = tmp_fpath[len(doc_tmp_path):]
                doc_fpath = os.path.join(self.app.doc_path, relative_fname)

                if not os.path.exists(doc_fpath):
                    self.app.stdout.write('%s [added/moved]\n' % (relative_fname))
                    self.copy_file(tmp_fpath, doc_fpath)
                elif not filecmp.cmp(doc_fpath, tmp_fpath):
                    self.app.stdout.write('%s [changed]\n' % (relative_fname))
                    self.copy_file(tmp_fpath, doc_fpath)

                    if relative_fname == 'conf.py':
                        self.fix_conf()

        for root, dirs, files in os.walk(self.app.doc_path):
            for fname in files:
                if not fname.endswith('.txt'):
                    continue

                doc_fpath = os.path.join(root, fname)
                relative_fname = doc_fpath[len(self.app.doc_path) + 1:]

                if relative_fname.startswith('_build/') or relative_fname.startswith('djbook/'):
                    continue

                tmp_fpath = os.path.join(doc_tmp_path, relative_fname)

                if not os.path.exists(tmp_fpath):
                    self.app.stdout.write('%s [removed/moved]\n' % (relative_fname))
                    os.remove(doc_fpath)

        shutil.rmtree(tmp_path)

    def fix_conf(self):
        conf_file = open(os.path.join(self.app.doc_path, 'conf.py'), 'a+')
        conf_file.write('sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "djbook")))\n')
        conf_file.write('from djbook_conf import *\n')

    def copy_file(self, src_path, dest_path):
        try:
            os.makedirs(os.path.dirname(dest_path))
        except OSError:
            pass
        shutil.copyfile(src_path, dest_path)

    def load_file(self, url):
        output = cStringIO.StringIO()
        url_obj = urllib2.urlopen(url)
        meta = url_obj.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        self.app.stdout.write("Downloading: {0} Bytes: {1}\n".format(url, file_size))

        file_size_dl = 0
        block_sz = 8192

        while True:
            buffer = url_obj.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            output.write(buffer)
            percent = float(file_size_dl) / file_size
            status = r"{0}  [{1:.2%}]".format(file_size_dl, percent)
            status = status + chr(8)*(len(status)+1)
            self.app.stdout.write(status)

        output.seek(0)
        return output
