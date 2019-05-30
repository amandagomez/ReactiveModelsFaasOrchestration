#
# Sets up the stages information in Redis, it will be deployed as a Cloud Function
#

import redis
from util.config import REDIS_HOST, REDIS_PORT, REDIS_AUTH

def redis_setup(event, context):
    redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_AUTH, decode_responses=True)
    parallel = {
        "type": "parallel",
        "function": "wait20",
        "total_elements": 10,
        "done_elements": 0
    }

    parallel_sum = {
        "type": "parallel",
        "function": "sum",
        "total_elements": 5,
        "done_elements": 0
    }

    reduce_sumall = {
        "type": "reduce",
        "function": "sumall"
    }

    finish = {
        "type": "finish"
    }

    step = {
        "type": "step",
        "function": "wait1"
    }

    choice = {
        "type": "if-else",
        "variable": "input",
        "expected": 20,
        "if_function": "wait1",
        "else_function": "wait20"
    }

    wordcount_map = {
        "type": "parallel",
        "function": "wordcount_map",
        "total_elements": 100,
        "done_elements": 0
    }

    wordcount_reduce = {
        "type": "reduce",
        "function": "wordcount_reduce"
    }

    

    '''
    #redis_client.delete('starting_times')
    #redis_client.delete('ending_times')

    #Steps
    for i in range (0, 2):
      redis_client.delete('stage'+str(i+1))
      redis_client.hmset('stage'+str(i+1), step)

    redis_client.delete('stage3')
    redis_client.hmset('stage3', finish)

    #Parallel wait20
    redis_client.delete('stage1')
    redis_client.delete('stage2')
    redis_client.delete('stage1_results')
    redis_client.hmset('stage1', parallel)
    redis_client.hmset('stage2', finish)

    #Map+reduce
    redis_client.delete('stage1')
    redis_client.delete('stage2')
    redis_client.delete('stage3')
    redis_client.delete('stage4')
    redis_client.delete('stage1_results')
    redis_client.hmset('stage1', parallel_sum)
    redis_client.hmset('stage2', reduce_sumall)
    redis_client.hmset('stage3', choice)
    redis_client.hmset('stage4', finish)
    '''

    #WordCount
    redis_client.delete('stage1')
    redis_client.delete('stage2')
    redis_client.delete('stage3')
    redis_client.delete('stage1_results')
    redis_client.hmset('stage1', wordcount_map)
    redis_client.hmset('stage2', wordcount_reduce)
    redis_client.hmset('stage3', finish)


    return {"status": 'Redis docs set up'}
