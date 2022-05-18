from pprint import pprint
from src.twitter import Twitter
from src.slack import Slack
from src.image import ImageDownload
from src.google_drive import GoogleDrive
from src.google_sheets import GoogleSheets
from src.csv import Csv
from src.config import Config
import os


def main(event, context):

    tweets = get_tweets()
    download_image(tweets)
    post_slack(tweets)
    upload_image()
    create_csv(tweets)
    update_sheet(tweets)
    delete_csv()


def get_tweets() -> list[dict]:
    tw = Twitter()
    args = tw.get_args()
    api = tw.create_api(args)
    tweets = tw.get_tweets(api)
    processed_tweets = [tw.parse_tweet(tweet) for tweet in tweets]
    pprint(processed_tweets)
    return processed_tweets


def download_image(tweets):
    img_path = '/tmp/images' if Config.DEPLOY_TYPE == "server_less" else 'files/images'
    os.makedirs(img_path, exist_ok=True)
    for tweet in tweets:
        for media_url in tweet['media_url']:
            ImageDownload(media_url, img_path + tweet['screen_name'] + '_' + media_url.split('/')[-1]).download()


def post_slack(tweets):
    if Config.SEND_POST_TO_SLACK:
        slack = Slack()
        for tweet in tweets:
            slack.send(tweet)


def upload_image():
    GoogleDrive().upload()


def create_csv(tweets):
    Csv().create(tweets)


def delete_csv():
    if Config.CSV_AFTER_DELETE:
        Csv().delete()


def update_sheet(tweets):
    GoogleSheets().update(tweets)


if __name__ == '__main__':
    main([], [])
