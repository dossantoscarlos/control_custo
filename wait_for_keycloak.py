import socket
import time
import subprocess
import sys

host = "keycloak"
port = 8080
cmd = sys.argv[1:]

while True:
    try:
        with socket.create_connection((host, port), timeout=1):
            break
    except OSError:
        print("Keycloak is unavailable - sleeping", file=sys.stderr)
        time.sleep(1)

print("Keycloak is up - executing command", file=sys.stderr)
subprocess.run(cmd)
