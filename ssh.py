import socket

def scan_port(host, port):
    """
    Scan a single port
    :param host: (str) host to scan
    :param port: (int) port to scan
    :return: None
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set the timeout to 1 second
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"Port {port} is open")
            if port == 22:  # If port 22 (SSH) is open, you can proceed with the brute-force attack here
                # Implement your brute-force attack code
                pass
        else:
            print(f"Port {port} is closed")
        sock.close()
    except socket.error:
        print("Error occurred while connecting to the host")

if __name__ == '__main__':
    host = input("Enter the host to scan: ")
    port = 22  # Specify the port you want to check (in this case, port 22 for SSH)
    scan_port(host, port)
