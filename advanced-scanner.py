import socket
import argparse
import textwrap
#20-80
def parse_range(value):
    """
    Parse the string obtained from the 'P' argument into a range
    :param value: (Str) obtained from the P argument on the CLI
    :return: Range
    """
    x = value.split('-')
    start, end = x
    try:
        #Typecasting to integer
        start = int(start)
        end = int(end)
        if start <= end:
            return range(start, end + 1)
    except ValueError:
        pass
    raise argparse.ArgumentTypeError('Invalid port range format')

def scan_range(host, ports):
    """
    Scan a range of ports
    :param ports: (range) range of ports to scan
    :param host: (str) host to scan
    :return: None
    """
    for port in ports:
        scan_port(host, port)

def scan_port(host, port):
    """
    Scan a single port
    :param port: (int) port to scan
    :param host: (str) host to scan
    :return: None
    """
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # setting the timeout to 0.3 seconds
        sock.settimeout(0.3)
        result = sock.connect_ex((host, port))
        if result == 0:
            print(f"The port {port} is open")
        else:
            pass
    except OSError as e:
        print(f"Connection Error: {e}")
    finally:
        # Closing the socket
        sock.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP port Scanning tool',
formatter_class=argparse.RawDescriptionHelpFormatter, epilog=textwrap.dedent('''Example: 
python3 adv_port_scanner.py -H 192.168.250.12 -P 20-90
python3 adv_port_scanner.py -H 192.168.250.12 -p 80
'''))
    parser.add_argument('-P', '--ports', type=parse_range, help="port range")
    parser.add_argument('-p', '--port', type=int, help="single port")
    parser.add_argument('-H', '--host', help="specified host")
    args = parser.parse_args()
    if args.ports:
        scan_range(args.host, args.ports)
    elif args.port:
        scan_port(args.host, args.port)