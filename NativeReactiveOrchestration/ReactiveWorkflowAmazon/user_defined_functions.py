#
# User-defined functions to be deployed as Lambdas - Cloud Functions
#

import time
import boto3
import pickle
import redis
from framework import trigger_next
from util.config import REDIS_HOST, REDIS_PORT, REDIS_AUTH
from collections import Counter

def wait1(event, context):
    time.sleep(1)
    payload = {'id': event["id"], 'stage': event["stage"], 'input': event["input"]}
    trigger_next(payload, event["next"])
    return payload

def wait20(event, context):
    time.sleep(20)
    payload = {'id': event["id"], 'stage': event["stage"], 'input': event["input"]}
    trigger_next(payload, event["next"])
    return payload

def sum(event, context):
    result = int(event["input"]) + 1
    payload = {'id': event["id"], 'stage': event["stage"], 'input': result}
    trigger_next(payload, event["next"])
    return payload

def sumall(event, context):
    total = 0
    for elem in event["input"]:
        total += int(elem)
        print(elem)
    print(total)
    payload = {'stage': event['stage'], 'input': total}
    trigger_next(payload, event['next'])
    return payload


def wordcount_map(event, context):
    initt = time.time()
    id = event['input']
    bucket_name = 'amanda-lambdainfo'
    origin_bucket = 'daniel-lambdas'
    origin_data = 'user_dedup.json'

    s3_client = boto3.client('s3')
    metadata = s3_client.head_object(Bucket='daniel-lambdas', Key='user_dedup.json')
    file_size = metadata['ContentLength']
    bytes_per_lambda = file_size / 1000000
    init_b = int(bytes_per_lambda * (id - 1))
    end_b = int(bytes_per_lambda * id - 1)
    response = s3_client.get_object(Bucket=origin_bucket, Key=origin_data, Range='bytes={}-{}'.format(str(init_b), str(end_b)))

    punc = ',.:;!?-_\'\"+=/*&^%$#@[]()'
    mapped_words = Counter()
    dades = response['Body'].read().decode('utf-8').splitlines()
    for line in dades:
        mapped_words.update(val for val in [x.strip(punc).lower() for x in line.split()])

    with open('/tmp/tmp{}'.format(id), 'wb') as data:
        pickle.dump(mapped_words, data, pickle.HIGHEST_PROTOCOL)
        s3_client.upload_file('/tmp/tmp{}'.format(id), bucket_name, 'mapped{}'.format(id))

    payload = {'id': event["id"], 'stage': event['stage'], 'input': 'mapped{}'.format(id)}
    trigger_next(payload, event['next'])

    return payload


def wordcount_reduce(event, context):
    bucket = 'amanda-lambdainfo'
    data = Counter()
    s3 = boto3.client('s3')
    mapped_keys = event['input']
    i = 0

    for obj_key in mapped_keys:
        s3.download_file(bucket, obj_key, '/tmp/tmp-{}'.format(obj_key))
        with open('/tmp/tmp-{}'.format(obj_key), 'rb') as content:
            data.update(pickle.load(content))

    s3.put_object(Bucket=bucket, Key='reduced_res', Body=str(data))

    payload = {'stage': event['stage'], 'input': 'reduced_res'}
    trigger_next(payload, event['next'])
    return payload
