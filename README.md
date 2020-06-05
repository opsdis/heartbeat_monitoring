## Heartbeats from remote servers can provide rapid alerting particularly over VPN tunnels

### Requirements:
 - Redis on monitoring server
 - Python3 on monitoring server as well as remote server

### heartbeat_listener
- Listens to heartbeats and sends them to Nagios

### heartbeat_sender
- Sends heartbeats to Redis on the monitoring server