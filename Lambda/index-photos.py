import json
import os
import time
import logging
import boto3
from datetime import datetime
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

region = 'us-west-2'
service = 'es'
credentials = boto3.Session().get_credentials()

awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

rekognition = boto3.client('rekognition')

es = Elasticsearch(
    http_auth = awsauth,
    use_ssl = True,
    verify_certs = True,
    connection_class = RequestsHttpConnection
)



def handler(event, context):

    os.environ['TZ'] = 'America/New_York'
    time.tzset()

    logger.debug(credentials)
    records = event['Records']
    #print(records)

    for record in records:

        s3object = record['s3']
        bucket = s3object['bucket']['name']
        objectKey = s3object['object']['key']

        image = {
            'S3Object' : {
                'Bucket' : bucket,
                'Name' : objectKey
            }
        }

        response = rekognition.detect_labels(Image = image)
        labels = list(map(lambda x : x['Name'], response['Labels']))
        timestamp = datetime.now().strftime('%Y-%d-%mT%H:%M:%S')

        esObject = json.dumps({
            'objectKey' : objectKey,
            'bucket' : bucket,
            'createdTimesatamp' : timestamp,
            'labels' : labels
        })

        es.index(index = "photos", doc_type = "Photo", id = objectKey, body = esObject, refresh = True)


    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
