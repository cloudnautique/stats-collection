import os
import argparse

from github3 import login
from collector import ElasticsearchDataCollector


class GithubReleaseCollector(ElasticsearchDataCollector):
    def __init__(self, user=None, api_key=None):
        self.github_client = login(user, api_key)
        self.type = "github_release_stats"

    def get_stats(self, user, repository):
        data = []

        repo = self.github_client.repository(user, repository)

        for release in repo.iter_releases():
            for asset in release.iter_assets():
                data.append({
                    'repo': repo.__str__(),
                    'release_name': release.tag_name,
                    'asset_name': asset.name,
                    'download_count': asset.download_count
                })

        return data


def setup_and_collect(repo):
    gh_c = GithubReleaseCollector(
        user=os.environ.get('GITHUB_USER_NAME', None),
        api_key=os.environ.get('GITHUB_API_KEY', None)
    )

    server = ':'.join([
        os.environ.get('ELASTICSEARCH_HOST', "elasticsearch"),
        os.environ.get('ELASTICSEARCH_PORT', '9200')
    ])

    index = os.environ.get('RANCHER_DATA_COLLECTOR_INDEX')

    user, repository = repo.split('/')
    gh_c.publish_stats(gh_c.get_stats(user, repository), hosts=[server], index=index)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("org_repository", type=str, nargs="+",
                        help='list of <user>/<repo> or <org>/<repo>')
    args = parser.parse_args()

    for repo in args.org_repository:
        setup_and_collect(repo)

if __name__ == '__main__':
    main()
