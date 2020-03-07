import socket


class Server(object):

    def __init__(self):
        self.alive = True

    def start_connection(self):
        bind_ip = '0.0.0.0'
        bind_port = 4444
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((bind_ip, bind_port))
        self.server.listen(5)
        print(f'Listening on {bind_ip}:{bind_port}')

    def send_commands(self, client_socket):
        while True:
            command = input('Enter the commands below: ')
            if command == 'quit':
                client_socket.send(str.encode(command))
                self.server.close()
                self.alive = False
                break
            elif len(str.encode(command)) > 0:
                client_socket.send(str.encode(command))
                client_response = str(client_socket.recv(1024), "utf-8")
                print(client_response)

    def main(self):
        while self.alive:
            try:
                self.start_connection()
                new_socket, address = self.server.accept()
                print(f'Accepted connection from {address[0]} and port {address[1]}')
                self.send_commands(new_socket)
            except:
                self.server.close()


if __name__ == '__main__':
    server = Server()
    server.main()
