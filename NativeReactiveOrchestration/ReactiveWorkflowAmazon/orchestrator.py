# 
# Orchestrator deployed as a Cloud function: orchestration, joiner and choice.
# Input:
#    - stage: stage id 
#    - input: input data
#
# To invoke workflow: call this Cloud Function with { stage : 'stage0', input : 'YOUR_INPUT'}
#

import json
from multiprocessing.pool import ThreadPool

import redis
import boto3
import time
from util.config import REDIS_HOST, REDIS_PORT, REDIS_AUTH

def invoke(lambda_client, function_name, payload):
    return lambda_client.invoke(FunctionName=function_name, InvocationType='Event', Payload=payload)

def orchestrator(event, context):
    startt = time.time()

    # Redis connection
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_AUTH, decode_responses=True)

    if (event["stage"] == "stage0"):
        redis_client.rpush("starting_times", startt)

    stage = event["stage"][5:]
    new_stage = "stage" + str(int(stage) + 1)

    # Lambda client
    lambda_client = boto3.client('lambda')

    # Stage information 
    stage_doc = redis_client.hgetall(new_stage)

    # Invoke depending on the type of stage
    if (stage_doc["type"] == "if-else"):
        payload = {"id": "1",
            "stage": new_stage,
            "input": event["input"],
            "next": "orchestrator"
             }
        if (str(event[stage_doc["variable"]]) == stage_doc["expected"]):
            func_to_trigger = stage_doc["if_function"]
        else:
            func_to_trigger = stage_doc["else_function"]
        lambda_client.invoke(FunctionName=func_to_trigger, InvocationType='Event', Payload=json.dumps(payload))


    if (stage_doc["type"] == "parallel"):
        calls = int(stage_doc["total_elements"])
        pool = ThreadPool(calls)
        post_results = []
        for i in range(0, calls):
            payload = {"id": i + 1, "stage": new_stage, "input": event["input"][str(i + 1)], "next": "aggregator"}
            pr = pool.apply_async(invoke, (lambda_client, stage_doc["function"], json.dumps(payload)))
            post_results.append(pr)

        pool.close()
        pool.join()


    if (stage_doc["type"] == "reduce"):
        payload = {"id": 1,
                   "input": event["input"],
                   "stage": new_stage,
                   "next": "orchestrator"
                   }
        lambda_client.invoke(FunctionName=stage_doc["function"], InvocationType='Event', Payload=json.dumps(payload))


    if (stage_doc["type"] == "step"):
        payload = {"id": 1,
                   "input": event["input"],
                   "stage": new_stage,
                   "next": "orchestrator"
                       }
        lambda_client.invoke(FunctionName=stage_doc["function"], InvocationType='Event', Payload=json.dumps(payload))

    if (stage_doc["type"] == "finish"):
        endt = time.time()
        redis_client.rpush("ending_times", endt)
        #print("ended workflow at " + str(time.time()) + " (orchestrator init time: " + str(startt) + ")")
        return {"END": "Process finished"}

    return {"stage launched": new_stage}




