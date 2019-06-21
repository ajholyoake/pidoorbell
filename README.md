Add variables into env

```make install```

Make sure that server sshd has GatewayPorts=clientspecified

Needs autossh, python3, nginx


Time limited token is generated by
curl -s http://localhost:REMOTE_PORT/token | jq .token | tr -d '"'

On the remote server curl -d "role=doorbell&duration=3&token=$TOKEN" http://localhost:REMOTE_PORT/open

Need an env var called ENCRYPTION_KEY generated like this:
from cryptography.fernet import Fernet
key = Fernet.generate_key()
