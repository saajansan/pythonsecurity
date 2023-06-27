from ssh_brutforcer_class import SSHBruteforcer

bruteforcer = SSHBruteforcer("192.168.145.146", "passwords.txt", port=22)
bruteforcer.scan_port()
