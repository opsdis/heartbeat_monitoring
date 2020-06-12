#!/usr/bin/python3
import redis
import time
import json
import yaml
import traceback

try:
 with open(r'heartbeat_listener.yaml') as file:
    configuration = yaml.load(file, Loader=yaml.BaseLoader)
 continuous_passive_checks = int(configuration['continuous_passive_checks'])
 nagios_rw_file = configuration['nagios_rw_file']
 redis_server = configuration['redis_server']
 heartbeat_host = configuration['heartbeat_host']
 heartbeat_service = configuration['heartbeat_service']
 channel = configuration['channel']
 heartbeat_key = configuration['heartbeat_key']
 time_to_live = int(configuration['time_to_live'])
 exception_sleep_time =  int(configuration['exception_sleep_time'])
except:
 print('loading of configuration failed')
 traceback.print_exc()
 exit(3)

print('heartbeat listener')
print('connecting to redis')
redis_server_connection = redis.Redis(redis_server, db=0)
pubsub_engine=redis_server_connection.pubsub()
pubsub_engine.subscribe(channel)

# Initial state
last_state = 'n/a'
alert = 0

while True:
 try:
  pubsub_engine=redis_server_connection.pubsub()
  pubsub_engine.subscribe(channel)
  for payload in pubsub_engine.listen():
   if payload['type'] == 'subscribe':
    if payload['data'] == 1:
     print('subscribed to: %s' % (payload['channel']))
   elif payload['type'] == 'message':
     print('data received:')
     if (redis_server_connection.get(heartbeat_key)) == None:
      print('no local heartbeat key found')
      current_state = 1
     else: 
      current_state = 0
     print(json.loads(payload['data']))
     received_data=json.loads(payload['data'])
     if continuous_passive_checks == 1 or current_state == 1 or (last_state != current_state):
      if current_state == 1:
       last_state = 1
      if current_state == 0:
       last_state = 0
      command = '['+str(int(time.time()))+'] PROCESS_SERVICE_CHECK_RESULT;'+heartbeat_host+';'+heartbeat_service+';'+str(current_state)+';Last heartbeat received -'+str(received_data['timestamp'])
      with open(nagios_rw_file, "w") as nagios_command_file:
       print('sending passive check:')
       msg = command + '\n'
       nagios_command_file.write(msg)
       print(msg)
       redis_server_connection.set(heartbeat_key,1,ex=time_to_live+5)
   else:
    print(payload)
 except KeyboardInterrupt:
    print('request to quit received, quitting')
    exit(3)
 except:
  traceback.print_exc()
  print(f"exception, sleeping for {exception_sleep_time}  seconds")
  time.sleep(exception_sleep_time)
