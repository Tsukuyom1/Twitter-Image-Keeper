from slack_sdk.webhook import WebhookClient  # pylint: disable=reportPrivateImportUsage
from .config import Config


class Slack():
    def __init__(self, *args):
        super(Slack, self).__init__(*args)

    SLACK_WEBHOOK_URL = Config.SLACK_WEBHOOK_URL

    def send(self, tweet: dict):
        webhook = WebhookClient(self.SLACK_WEBHOOK_URL)

        text = '''
名前: {}
tweet URL: {}
profile URL: {}
profile imale URL: {}
テキスト:{}
以下画像URL
'''.format(tweet['name'], tweet['tweet_url'], tweet['profile_url'], tweet['profile_image_url'], tweet['text'])

        response = webhook.send(text=text)
        print(f"status: {response.status_code} body: {response.body}")

        for media_url in tweet['media_url']:
            self.send_to_image(media_url)

    def send_to_image(self, image_url: str):
        """
        If more than four URLs are included in one post due to Slack specifications,
        the images will not be expanded,
        so send them individually.
        """
        webhook = WebhookClient(self.SLACK_WEBHOOK_URL)
        response = webhook.send(text=image_url)
        print(f"status: {response.status_code} body: {response.body}")
