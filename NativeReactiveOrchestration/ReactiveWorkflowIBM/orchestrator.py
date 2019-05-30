# 
# Orchestrator deployed as a Cloud function: orchestration, joiner and choice.
# Input:
#    - stage: stage id 
#    - input: input data
#
# To invoke workflow: call this Cloud Function with { stage : 'stage0', input : 'YOUR_INPUT'}
#

import sys
import json
import redis
import http.client
from multiprocessing.pool import ThreadPool

def invoke(method, url, payload, headers):
    conn = http.client.HTTPSConnection("openwhisk.eu-gb.bluemix.net")
    conn.request(method, url, payload, headers=headers)
    return conn.getresponse()

def main(dict):

    # Composer for Redis connection
    redis_client = redis.Redis(host="HOST", port=PORT, password="PASSWORD", ssl=True, decode_responses=True)

    if (event["stage"] == "stage0"):
        redis_client.rpush("starting_times", startt)

    stage = dict["stage"][5:]
    new_stage = "stage" + str(int(stage) + 1)

   # Cloud Functions connection
    encoded_apikey = "ENCODED_API_KEY"
    url = "/api/v1/namespaces/NAMESPACE/actions/"
    headers = {
        'Accept': "application/json",
        'Content-type': "application/json",
        'Authorization': 'Basic %s' % encoded_apikey
    }
    conn = http.client.HTTPSConnection("openwhisk.eu-gb.bluemix.net")

    # Stage information 
    stage_doc = redis_client.hgetall(new_stage)

    # Invoke depending on the type of stage
    if (stage_doc["type"] == "if-else"):
        payload = {"id": "1",
                   "stage": new_stage,
                   "input": dict["input"],
                   "next": "orchestrator"
                   }
        if (str(dict[stage_doc["variable"]]) == stage_doc["expected"]):
            func_to_trigger = stage_doc["if_function"]
        else:
            func_to_trigger = stage_doc["else_function"]
        conn.request("POST", url + func_to_trigger, json.dumps(payload), headers=headers)
        res = conn.getresponse()

    if (stage_doc["type"] == "parallel"):
        calls = int(stage_doc["total_elements"])
        pool = ThreadPool(calls)
        post_results = []
        for i in range(0, calls):
            payload = {"id": i + 1, "stage": new_stage, "input": dict["input"][str(i + 1)], "next": "aggregator"}
            pr = pool.apply_async(invoke, ("POST", url + stage_doc["function"], json.dumps(payload), headers))
            post_results.append(pr)

        results = [c.get().read() for c in post_results]
        pool.close()
        pool.join()

    if (stage_doc["type"] == "reduce"):
        payload = {"id": 1,
                   "input": dict["input"],
                   "stage": new_stage,
                   "next": "orchestrator"
                   }
        conn.request("POST", url + stage_doc["function"], json.dumps(payload), headers=headers)
        res = conn.getresponse()

    if (stage_doc["type"] == "step"):
        payload = { "id": 1,
                    "input": dict["input"],
                    "stage": new_stage,
                    "next": "orchestrator"
                   }
        conn.request("POST", url + stage_doc["function"], json.dumps(payload), headers=headers)
        res = conn.getresponse()

    if (stage_doc["type"] == "finish"):
        endt = time.time()
        redis_client.rpush("ending_times", endt)
        return {"END": "Process finished"}

    return {"stage launched": new_stage }
