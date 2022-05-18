# Twitter-Image-Keeper

いい感じにツイッターのキーワードに紐付いている画像を保存し通知します。
保存先や通知先などは `機能` を参照してください。


# 始め方

## TwitterAPI

1. https://developer.twitter.com/en/apps/ にて各種KEY・TOKENを取得し `.env` に入力。
1. 取得したいキーワードを `config.ini` の `BaseSearchQuery` に入力します。

## Slack

1. https://api.slack.com/apps/new にてWebhook URLを発行し `.env` の `SLACK_WEBHOOK_URL` に入力します。

## Google
### 自分の管理下のGoogleリソースを利用する場合

1. `OAuth 2.0 クライアント ID` を作成。jsonをダウンロードし、 `credentials.json` とリネームしrootに配置する。
1. `OAuth 同意画面` を作成。
1. ローカルで `python main.py` を実行し、token.jsonを作成


# 機能

未対応なのは今後優先的に実装予定。
対応してほしいのがあったらissue書いてね。

## 通知

|  通知先 |  対応  |
| ---- | ---- |
| Slack  | ○ |
| Discord  | ☓ |
| GCP Pub/Sub | ☓ |
| AWS SQS | ☓ |

## 保存

| 保存先 | 対応 |
| --- | --- |
| ローカル | ○ |
| GoogleDrive(自分の) | ○ |
| GoogleDrive(他人の) | ☓ |
| GCP GCS | ☓ |
| AWS S3 | ☓ |

## ロギング
| 保存先 | 対応 |
| --- | --- |
| Google spreadsheet | ○ |
| RDS | ☓ |
| GCP BigQuery| ☓ |
| CSV | ○ |
| JSON | ☓ |

# デプロイ

(ユーティリティがあるかという意味)

| ベンダー | 対応 |
| --- | --- |
| GCP Cloud Functions | ○ |
| AWS Lambda | ☓ |
