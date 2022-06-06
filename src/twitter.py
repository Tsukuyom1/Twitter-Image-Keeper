import tweepy
from .config import Config
from datetime import datetime, timedelta, timezone


class Twitter():
    def __init__(self, *args):
        super(Twitter, self).__init__(*args)

    TW_API_KEY = Config.TW_API_KEY
    TW_API_SECRET = Config.TW_API_SECRET
    TW_ACCESS_TOKEN = Config.TW_ACCESS_TOKEN
    TW_ACCESS_TOKEN_SECRET = Config.TW_ACCESS_TOKEN_SECRET
    TW_BASE_SEARCH_QUERY = Config.TW_BASE_SEARCH_QUERY
    TW_DATE_INTERVAL = Config.TW_DATE_INTERVAL

    def get_args(self) -> dict[str, str]:
        return {
            'consumer_key': self.TW_API_KEY,
            'consumer_secret': self.TW_API_SECRET,
            'access_token': self.TW_ACCESS_TOKEN,
            'access_token_secret': self.TW_ACCESS_TOKEN_SECRET
        }

    def get_tweets(self, api: tweepy.API, count: int = 500) -> list[dict]:
        query = self.TW_BASE_SEARCH_QUERY + self.get_query_date(self.TW_DATE_INTERVAL)
        print(query)
        return api.search_tweets(q=query, count=count)

    def get_query_date(self, date_interval: str) -> str:
        """Get the date for the query.

        Args:
            date_interval (str): _description_

        Returns:
            str: _description_
        """
        t_delta = timedelta(hours=9)
        JST = timezone(t_delta, 'JST')

        if date_interval == 'hour':
            time = datetime.now(JST) - timedelta(hours=1)
        elif date_interval == 'day':
            time = datetime.now(JST) - timedelta(days=1)
        elif date_interval == 'week':
            time = datetime.now(JST) - timedelta(weeks=1)
        else:
            return ''

        return ' since:' + time.strftime('%Y-%m-%d_%H:%M:%S') + '_JST'

    def create_api(self, args: dict[str, str]) -> tweepy.API:
        auth = tweepy.OAuthHandler(
            args['consumer_key'], args['consumer_secret'])
        auth.set_access_token(args['access_token'], args['access_token_secret'])
        return tweepy.API(auth)

    def parse_tweet(self, tweet: tweepy.models.Status) -> dict:
        """Extract only the necessary information.

        Args:
            tweet (tweepy.models.Status): _description_

        Returns:
            dict: {
                name: String, user name
                tweet_url: https url
                profile_url: https url
                profile_url: https url
                text: String, tweet text
                media_url: list[String], media url
                                        Since multiple images will be submitted, we will use the LIST type.

            }
        """
        user_url = 'https://twitter.com/{}'.format(tweet.user.screen_name)
        tmp_media_urls = []
        try:
            for media in tweet.entities['media']:
                tmp_media_urls.append(media['media_url'])
        except KeyError:
            pass
        except Exception as e:
            print(e)
        print(tweet.created_at)
        print(type(tweet.created_at))
        return {
            'name': tweet.user.name,
            'id': tweet.id_str,
            'tweet_url': user_url + '/status/' + tweet.id_str,
            'profile_url': user_url,
            'screen_name': tweet.user.screen_name,
            'profile_image_url': tweet.user.profile_image_url_https,
            'text': tweet.text,
            'media_url': tmp_media_urls,
            'created_at': tweet.created_at.strftime('%Y/%m/%d %H:%M:%S')
        }
