#
# Cloud Function that sets up the stages information in Redis
#

import redis

if __name__ == "__main__":

  parallel = {
    "type": "parallel",
    "function": "wait20",
    "total_elements": 80,
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


  client = redis.Redis(host="HOST", port=PORT, password="PASSWORD", ssl=True, decode_responses=True)

  '''
  # Steps
  for i in range (0, 2):
    client.delete('stage'+str(i+1))
    client.hmset('stage'+str(i+1), step)

  client.delete('stage3')
  client.hmset('stage3', finish)
  '''

  # Complex steps
  client.delete('stage1')
  client.delete('stage2')
  client.delete('stage3')
  client.delete('stage4')
  client.hmset('stage1', parallel_sum)
  client.delete('stage1_results')
  client.hmset('stage2', reduce_sumall)
  client.hmset('stage3', choice)
  client.hmset('stage4', finish)
