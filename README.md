Add variables into env

```make install```

Make sure that server sshd has GatewayPorts=clientspecified

Needs autossh, python3

On the remote server curl -d "role=doorbell&duration=3" http://localhost:REMOTE_PORT
