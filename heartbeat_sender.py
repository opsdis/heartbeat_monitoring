#!/usr/bin/python3
import redis
import time
import json
import yaml

try:
 with open(r'heartbeat_sender.yaml') as file:
    configuration = yaml.load(file, Loader=yaml.BaseLoader)

 redis_server=configuration['redis_server']
 host=configuration['host']
 channel=configuration['channel']
 heartbeat_interval=int(configuration['heartbeat_interval'])
except:
 print('loading of configuration failed')
 exit(3)

print('heartbeat sender')

redis_server_connection = redis.Redis(redis_server, db=0)

print('connecting to redis')

while True:
 try:
  print('sending heartbeat')
  payload = {}
  payload['event'] = 'host still alive'
  payload['host'] = host
  payload['timestamp'] = time.time()
  json_values = json.dumps(payload, separators=(',', ':'))
  redis_server_connection.publish(channel, json_values)
  print('sleeping for '+str(heartbeat_interval)+' seconds')
  time.sleep(heartbeat_interval)
 except Exception as e:
  print(e)
  print('exception occured, will retry connection soon')
  time.sleep(10)
