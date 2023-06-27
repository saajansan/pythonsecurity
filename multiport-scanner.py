import socket
import sys

# Taking the ip from the first argument on the CLI
ip = sys.argv[1]
"""
Taking the ports from the rest of the arguments on the CLI (List comprehension)
"""
ports = [int(x) for x in sys.argv[2:]]
# Looping over the ports and trying to connect
for port in ports:
    try:
        # Creating a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        PermissionError
        # setting the timeout to 0.5 seconds
        sock.settimeout(0.5)
        # print(port)
        result = sock.connect_ex((ip, port))
        # print(result)
        if result == 0:
            print(f"The port {port} is open")
        else:
            print(f"The port {port} is closed")
    except OSError as e:
        print(f"Connection Error: {e}")
        # Closing the socket
        sock.close()