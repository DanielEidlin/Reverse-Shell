import requests
from hashlib import sha256


class Client(object):
    def __init__(self):
        self.session = requests.Session()

    def register(self, username, password):
        password = sha256(password.encode()).hexdigest()
        r1 = self.session.get('http://localhost:8000/reverse_shell/register/')
        csrf = r1.cookies['csrftoken']
        r2 = self.session.post('http://localhost:8000/reverse_shell/register/',
                               data={
                                   'csrfmiddlewaretoken': csrf,
                                   'username': username,
                                   'password1': password,
                                   'password2': password,
                               })
        return r2

    def login(self, username, password):
        password = sha256(password.encode()).hexdigest()
        # Validate login first
        r1 = self.session.get('http://localhost:8000/reverse_shell/validate-login/')
        csrf = r1.cookies['csrftoken']
        r2 = self.session.post('http://localhost:8000/reverse_shell/validate-login/',
                               data={
                                   'csrfmiddlewaretoken': csrf,
                                   'username': username,
                                   'password': password,
                               })
        if r2.status_code == 200:
            # Do the real login
            r1 = self.session.get('http://localhost:8000/reverse_shell/login/')
            csrf = r1.cookies['csrftoken']
            r2 = self.session.post('http://localhost:8000/reverse_shell/login/',
                                   data={
                                       'csrfmiddlewaretoken': csrf,
                                       'username': username,
                                       'password': password,
                                   })
        return r2

    def logout(self):
        response = self.session.get('http://localhost:8000/reverse_shell/logout/')
        return response

    def create_victim(self, ip, port, computer_name, mac_address, username):
        response = self.session.get('http://localhost:8000/api/victims/')
        csrf = response.cookies['csrftoken']

        data = {
            'csrfmiddlewaretoken': csrf,
            'ip': ip,
            'port': port,
            'computer_name': computer_name,
            'mac_address': mac_address,
            'logged_in': True,
            'owner': username,
        }
        response = self.session.post('http://localhost:8000/api/victims/', data=data)
        return response

    def update_victim(self, mac_address, data):
        response = self.session.get('http://localhost:8000/api/victims/')
        csrf = response.cookies['csrftoken']
        data['csrfmiddlewaretoken'] = csrf

        response = self.session.patch(f'http://localhost:8000/api/victims/{mac_address}/',
                                      data=data)
        return response

    def get_attacker(self, mac_address):
        response = self.session.get(
            f'http://localhost:8000/api/attackers/get_attacker/?mac_address={mac_address}')
        return response
