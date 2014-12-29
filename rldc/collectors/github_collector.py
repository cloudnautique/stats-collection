import os

from github import Github
from collector import ElasticsearchDataCollector


class GithubCollector(ElasticsearchDataCollector):
    def __init__(self, api_key=None, user=None):
        self.github_client = Github(user, api_key)
        self.type = "github_repo_stats"

    def get_stats(self):
        try:
            repos = [repo for org in self.github_client.get_user().get_orgs() for repo in org.get_repos()]
        except:
            pass

        data = []
        for repo in repos:
            data.append({
                'repo_name': repo.name,
                'stargazers_count': repo.stargazers_count,
                'subscribers_count': repo.raw_data['subscribers_count'],
                'open_issues_count': repo.open_issues_count,
                'forks_count': repo.forks_count
            })

        return data


def get_gh_object():
    gh_c = GithubCollector(
        api_key=os.environ.get('GITHUB_API_KEY', None),
        user=os.environ.get('GITHUB_USER_NAME', None)
    )
    return gh_c


def get_server_config():
    server = ':'.join([
        os.environ.get('ELASTICSEARCH_HOST', "elasticsearch"),
        os.environ.get('ELASTICSEARCH_PORT', '9200')
    ])

    return server


def get_index():
    return os.environ.get('RANCHER_DATA_COLLECTOR_INDEX')


def main():
    gh_c = get_gh_object()
    server = get_server_config()
    index = get_index()

    gh_c.publish_stats(gh_c.get_stats(), hosts=server, index=index)


if __name__ == '__main__':
    main()
