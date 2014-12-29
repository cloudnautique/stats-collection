import tweepy
import os
import sys
from collector import ElasticsearchDataCollector

import logging

FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT)

logger = logging.getLogger(__file__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())


class TwitterCollector(ElasticsearchDataCollector):
    '''
    Simple collector for getting a users followers/following counts.
    '''
    def __init__(self, consumer_key, consumer_secret, tracked_user):
        auth = self.__get_auth_obj(consumer_key, consumer_secret)
        self.api = tweepy.API(auth)
        self.user = tracked_user
        self.type = 'twitter_stat'

    def __get_auth_obj(self, consumer_key, consumer_secret):
        if consumer_key is not None and consumer_secret is not None:
            return tweepy.AppAuthHandler(consumer_key, consumer_secret)
        else:
            logger.error("Could not get Bearer token")
            logger.info("Can not get key or secret")
            sys.exit(1)

    def get_stats(self):
        try:
            user = self.api.get_user(self.user)
        except tweepy.error.TweepError:
            logger.error("User %s could not be retrieved", self.user)
            sys.exit(1)

        data = []
        data.append({
            'followers_count': user.followers_count,
            'following_count': user.friends_count,
        })

        return data


def main():
    tw_c = TwitterCollector(
        os.environ.get('TWITTER_CONSUMER_KEY', None),
        os.environ.get('TWITTER_SECRET_KEY', None),
        'rancher_labs')

    server = ':'.join([
        os.environ.get('ELASTICSEARCH_HOST', "elasticsearch"),
        os.environ.get('ELASTICSEARCH_PORT', '9200')
    ])

    index = os.environ.get('RANCHER_DATA_COLLECTOR_INDEX')

    tw_c.publish_stats(tw_c.get_stats(), hosts=[server], index=index)


if __name__ == '__main__':
    main()
