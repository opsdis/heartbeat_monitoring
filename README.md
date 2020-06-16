## Heartbeats from remote servers can provide rapid alerting particularly over VPN tunnels

### Requirements:
 - Redis on monitoring server or on local server reachable by remote server
 - Python3 on monitoring server as well as remote server

## Components: 
#### heartbeat_listener:
- Listens to heartbeats and sends them to the monitoring server

#### heartbeat_sender:
- Sends heartbeats to Redis on the monitoring server

### Installation:
  - Install redis
  - Install python module dependencies: `pip install -r requirements.txt`
  - Customize heartbeat_listener.yaml and place on monitoring server
  - Customize heartbeat_sender.yaml and place on remote server
  - Run sender in the background on the remote server (supervisor?): `python3 heartbeat_sender.py`
  - Run listener in the background on the local server (supervisor?): `python3 heartbeat_listener.py`
  - Add a service with passive checks in Nagios and make sure to have that match your `heartbeat_listener.yaml` configuration `heartbeat_host` and `heartbeat_service`