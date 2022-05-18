#!/bin/sh

# exsample:
# ./util/CloudFunctions.sh "my-project-name" "my-service-account" "schedule"
# ./util/CloudFunctions.sh hoge fuga@hoge.iam.gserviceaccount.com "0 * * * *"



ProjectName=$1
ServiceAccount=$2
Schedule=$3
TopicName="Twitter-Image-Keeper-topic"
SubscriptionsName="Twitter-Image-Keeper-subscription"

# create a topic
gcloud pubsub topics list --filter="name.scope(topic):'${TopicName}'"|grep ${TopicName}
if [ $? = 0 ]; then
  echo "Topic already exists"
else
  gcloud pubsub topics create ${TopicName} \
    --project ${ProjectName}
fi

# create a subscription
gcloud pubsub subscriptions list --filter="name.scope(topic):'${SubscriptionsName}'"|grep ${SubscriptionsName}
if [ $? = 0 ]; then
  echo "Subscription already exists"
else
  gcloud pubsub subscriptions create ${SubscriptionsName} \
    --topic=${TopicName} \
    --project ${ProjectName}
fi

# create a scheduler
gcloud scheduler jobs list --location asia-northeast1 --filter="name.scope(id):'twitter-image-keeper'"|grep twitter-image-keeper
if [ $? = 0 ]; then
  echo "Scheduler already exists"
else
  gcloud beta scheduler jobs create pubsub twitter-image-keeper \
    --location=asia-northeast1 \
    --schedule="${Schedule}" \
    --time-zone="Asia/Tokyo" \
    --topic=${TopicName} \
    --message-body="Hello" \
    --project ${ProjectName}
fi

# deploy the function
gcloud beta functions deploy Twitter-Image-Keeper \
  --entry-point main \
  --timeout 300 \
  --trigger-topic ${TopicName} \
  --runtime python39 \
  --service-account ${ServiceAccount} \
  --project ${ProjectName} \
  --region asia-northeast1
