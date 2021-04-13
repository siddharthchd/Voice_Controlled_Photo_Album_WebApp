import json
import math
import dateutil.parser
import datetime
import time
import os
import logging
import boto3
from botocore.vendored import requests

## demo!!
    
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

headers = { "Content-Type": "application/json" }
host = 'https://search-photos-4xttynqx2xfjhzz4cvf4tlz2ma.us-west-2.es.amazonaws.com/'
region = 'us-west-2'
lex = boto3.client('lex-runtime', region_name=region)

def lambda_handler(event, context):

    print ('event : ', event)

    q1 = event['q']
    
    # if(q1 == "searchAudio" ):
    #     q1 = convert_speechtotext()
        
    print("q1:", q1 )
    labels = get_labels(q1)
    print("labels", labels)
    return
    if len(labels) == 0:
        return
    else:
        img_paths = get_photo_path(labels)

    return {
        'statusCode':200,
        'body': {
            'imagePaths':img_paths,
            'userQuery':q1,
            'labels': labels,
        },
        'headers':{
            'Access-Control-Allow-Origin': '*'
        }
    }
    
def get_labels(query):
    response = lex.post_text(
        botName='SearchBot',                 
        botAlias='$LATEST',
        userId="string",           
        inputText=query
    )
    print("lex-response", response)
    
    labels = []
    if 'slots' not in response:
        print("No photo collection for query {}".format(query))
    else:
        print ("slot: ",response['slots'])
        slot_val = response['slots']
        for key,value in slot_val.items():
            if value!=None:
                labels.append(value)
    return labels

def get_photo_path(labels):
    img_paths = []
    unique_labels = [] 
    for x in labels: 
        if x not in unique_labels: 
            unique_labels.append(x)
    labels = unique_labels
    print("inside get photo path", labels)
    for i in labels:
        path = host + '/_search?q=labels:'+i
        print(path)
        response = requests.get(path, headers=headers)
        print("response from ES", response)
        dict1 =  json.loads(response.text)
        hits_count = dict1['hits']['total']['value']
        print ("DICT : ", dict1)
        for k in range(0, hits_count):
            img_obj = dict1["hits"]["hits"]
            img_bucket = dict1["hits"]["hits"][k]["_source"]["bucket"]
            print("img_bucket", img_bucket)
            img_name = dict1["hits"]["hits"][k]["_source"]["objectKey"]
            print("img_name", img_name)
            img_link = 'https://s3.amazonaws.com/' + str(img_bucket) + '/' + str(img_name)
            print (img_link)
            img_paths.append(img_link)
    print (img_paths)
    return img_paths