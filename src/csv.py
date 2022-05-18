from datetime import datetime
import csv
import os
import glob
from .config import Config


class Csv():
    def create(self, tweets):
        dt_now = datetime.now().strftime('%Y%m%d%H%M%S')

        csv_path = '/tmp/files/result/' if Config.DEPLOY_TYPE == "server_less" else 'files/result/'
        os.makedirs(csv_path, exist_ok=True)
        filename = dt_now + '.csv'
        filepath = csv_path + filename
        with open(filepath, 'w') as f:
            writer = csv.writer(f)
            for tweet in tweets:
                writer.writerow([tweet['created_at'], tweet['screen_name'], tweet['name'], tweet['tweet_url']])

    def delete(self):
        csv_path = '/tmp/files/result/' if Config.DEPLOY_TYPE == "server_less" else 'files/result/'
        files = glob.glob(csv_path + "/*.csv")
        for file in files:
            os.remove(file)
