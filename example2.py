import socket
import sys

# Taking the IP from the first argument on the CLI
ip = sys.argv[1]

# Looping over a range of port numbers (from 1 to 65535)
for port in range(20, 40):
    try:
        # Creating a TCP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Setting the timeout to 0.5 seconds
        sock.settimeout(0.5)

        result = sock.connect_ex((ip, port))

        if result == 0:
            print(f"The port {port} is open")
        else:
            print(f"The port {port} is closed")

        # Closing the socket
        sock.close()

    except OSError as e:
        print(f"Connection Error: {e}")
