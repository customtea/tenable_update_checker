import subprocess
from pathlib import Path

__author__ = 'customtea (https://github.com/customtea)'
__version__ = '0.1.0'
__program__ = 'Show Windows Toast Notification'
def version():
    return f'{__program__} ver:{__version__} Created By {__author__}'

class ShowToastError(Exception):
    def __init__(self, arg=""):
        self.arg = arg
    
    def __str__(self) -> str:
        return f"Show Toast Error By {self.arg}"

class ShowToast():
    def __init__(self) -> None:
        self.ps_cmd = 'powershell -NoLogo -NoProfile -ExecutionPolicy RemoteSigned -File'
        self.ps_file = 'showToast.ps1'
        if not Path(self.ps_file).exists():
            raise ShowToastError("Not Found showToast.ps1. Plase Check That File")
    
    def notify(self, title: str, message:str=" ", detail:str=" "):
        # cmd = ps_cmd + " " + ps_file + " -title '" + title  +"' -message '" + message + "' -detail '" + detail + "'"
        cmd = f'{self.ps_cmd} {self.ps_file} -title "{title}" -message "{message}" -detail "{detail}"'
        # print(cmd)
        proc = subprocess.run(cmd)
        # print(proc)
        # if proc.returncode == 0:
        #     print("Sucess")
        return proc

