#
# Framework functions to be called by the user-defined functions
#

import boto3
import json

# Invoke next Lambda in the orchestration
def trigger_next(payload, next_comput):
    lambda_client = boto3.client('lambda')
    lambda_client.invoke(FunctionName=next_comput, InvocationType='Event', Payload=json.dumps(payload))
