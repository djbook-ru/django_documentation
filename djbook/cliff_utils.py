import getpass
from github import Github


class GithubCommandMixin(object):
    PASS_CHACHE_FILE = '.github.auth'

    def get_github(self):
        if not hasattr(self, '_github'):
            github_username, github_password = None, None

            try:
                with open(GithubCommandMixin.PASS_CHACHE_FILE) as f:
                    data = f.read()
                    if data:
                        github_username, github_password = data.split('\n')
            except IOError:
                pass

            if not github_username or not github_password:
                print 'We need authenticate your in Github for Search API.'
                github_username = raw_input('Github username: ')
                github_password = getpass.getpass('Github password: ')

                with open(GithubCommandMixin.PASS_CHACHE_FILE, 'w') as f:
                    f.write(github_username)
                    f.write('\n')
                    f.write(github_password)
                    print 'WARNING! Your Github password is saved in %s' % GithubCommandMixin.PASS_CHACHE_FILE

            self._github = Github(github_username, github_password)

        return self._github

    def get_repo(self, repo_name):
        return self.get_github().get_repo(repo_name)

    def get_tag(self, repo, tag_name):
        for tag in repo.get_tags():
            if tag.name == tag_name:
                return tag
