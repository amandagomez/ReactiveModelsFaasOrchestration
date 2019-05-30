# 
# Aggregator Cloud function: aggregation of parallel stages
# Input:
#    - stage: stage id
#    - input: result from parallel function
#    - id: id of the parallel function
#

import json
import redis
import boto3
from util.config import REDIS_HOST, REDIS_PORT, REDIS_AUTH
import time

# Update stage status in Redis
def update_status(info, redis_client):
    stw_id = info["id"]
    working_stage = info["stage"]
    stw_res = info["input"]

    ended = redis_client.hincrby(working_stage, 'done_elements', 1)
    redis_client.rpush(working_stage + '_results', stw_res)

    stage_doc = redis_client.hgetall(working_stage)
    done = (ended == int(stage_doc['total_elements']))
    if done:
        return True
    return False


# If stage is done retrieve results from Redis
def get_aggregated_data(stage, redis_client):
    aggregated_data = redis_client.lrange(stage + '_results', 0, -1)
    return aggregated_data


def aggregator(event, context):

    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_AUTH, decode_responses=True)
    done = update_status(event, redis_client)

    if done:
        data = get_aggregated_data(event["stage"], redis_client)
        payload = {"stage": event["stage"],
                   "input": data
                   }
        '''Aggregator always triggers orchestrator'''
        lambda_client = boto3.client('lambda')
        lambda_client.invoke(FunctionName="orchestrator", InvocationType='Event', Payload=json.dumps(payload))

        return {'message': 'stage finished'}
    else:
        return {'message': 'stage not finished'}
