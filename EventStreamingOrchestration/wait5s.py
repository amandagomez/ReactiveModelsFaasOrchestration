#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
import sys
import time
from kafka import KafkaProducer

def notify_end(fn_id, result):
    producer = KafkaProducer(bootstrap_servers=['SERVER_IP:9092'], key_serializer=str.encode, value_serializer=str.encode)
    future = producer.send('event_input_topic', key=fn_id, value=result)

    # Block for 'synchronous' sends
    try:
        record_metadata = future.get(timeout=10)
    except KafkaError:
        # Decide what to do if produce request failed...
        log.exception()
        print("Could not publish to Kafka")
        pass

def main(dict):
    
    time.sleep(5)
    notify_end(dict['id'], dict['input'])
    return { 'result': dict['input'] }
