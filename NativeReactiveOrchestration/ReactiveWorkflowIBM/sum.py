#
# Deployed user-defined function with the trigger_next framework function
#

import sys, json
import requests
import time
import http.client

# Invoke next Lambda in the orchestration
def trigger_next(payload, next_comput):
    encoded_apikey = "ENCODED_API_KEY"
    url = "/api/v1/namespaces/NAMESPACE/actions/"
    headers = {
        'Accept': "application/json",
        'Content-type': "application/json",
        'Authorization': 'Basic %s' % encoded_apikey
    }
    conn = http.client.HTTPSConnection("openwhisk.eu-gb.bluemix.net")
    conn.request("POST", url + next_comput, json.dumps(payload), headers=headers)
    res = conn.getresponse()
    
def main(dict):
    result = int(dict["input"]) + 1
    payload = {'id': dict["id"], 'stage': dict["stage"], 'input': result}
    trigger_next(payload, dict["next"])

    return payload
