import socket

class TcpScanner:
    def __init__(self, host):
        self.host = host

    def scan_port(self, port):
        """
        Scan a single port
        :param port: (int) port to scan
        :return: None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            # Setting the timeout to 0.5 seconds
            sock.settimeout(0.3)

            result = sock.connect_ex((self.host, port))

            if result == 0:
                print(f"The port {port} is open")
            else:
                pass
                # print(f"The port {port} is closed")

        except OSError as e:
            print(f"Connection Error: {e}")

        finally:
            # Closing the socket
            sock.close()

    def scan_range(self, start, end):
        """
        Scan a range of ports
        :param start: (int) starting port
        :param end: (int) ending port
        :return: None
        """
        for port in range(start, end):
            self.scan_port(port)
