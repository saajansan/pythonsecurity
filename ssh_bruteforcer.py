from SSH_Bruteforcer_as_Class import SSHBruteforcer

bruteforcer = SSHBruteforcer("192.168.145.146", "passwords.txt", port=22)
bruteforcer.scan_port()
