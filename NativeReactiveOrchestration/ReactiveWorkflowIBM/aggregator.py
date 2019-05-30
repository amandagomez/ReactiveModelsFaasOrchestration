# 
# Aggregator Cloud function: aggregation of parallel stages
# Input:
#    - stage: stage id
#    - input: result from parallel function
#    - id: id of the parallel function
#

import requests, json
import redis
import http.client

# Update stage status in Redis
def update_status(info):
    stw_id = info["id"]
    working_stage = info["stage"]
    stw_res = info["input"]

    redis_client = redis.Redis(
        host="HOST", port=PORT,
        password="PASSWORD", ssl=True, decode_responses=True)

    ended = redis_client.hincrby(working_stage, 'done_elements', 1)
    redis_client.rpush(working_stage + '_results', stw_res)

    stage_doc = redis_client.hgetall(working_stage)
    done = (ended == int(stage_doc['total_elements']))
    if done:
        return True
    return False


# If stage is done retrieve results from Redis
def get_aggregated_data(stage):
    redis_client = redis.Redis(
        host="HOST", port=PORT,
        password="PASSWORD", ssl=True, decode_responses=True)
    aggregated_data = redis_client.lrange(stage + '_results', 0, -1)
    return aggregated_data


def main(dict):
    done = update_status(dict)
    if done:
        data = get_aggregated_data(dict["stage"])
        payload = {"stage": dict["stage"],
                   "input": data
                   }
        '''Aggregator always triggers orchestrator'''
        encoded_apikey = "ENCODED_API_KEY"
        url = "/api/v1/namespaces/NAMESPACE/actions/"
        headers = {
            'Accept': "application/json",
            'Content-type': "application/json",
            'Authorization': 'Basic %s' % encoded_apikey
        }
        conn = http.client.HTTPSConnection("openwhisk.eu-gb.bluemix.net")
        conn.request("POST", url + "orchestrator", json.dumps(payload), headers=headers)
        res = conn.getresponse()
        
        return {'message': 'stage finished'}
    else:
        return {'message': 'stage not finished'}
