

#!/usr/bin/env python3

# ------ health_checks.py -------
import shutil
import psutil
from network import *

def check_disk_usage(disk):
    """Verifies that there's enough free space on disk"""
    du = shutil.disk_usage(disk)
    free = du.free / du.total * 100
    return free > 20
def check_cpu_usage():
    """Verifies that there's enough unused CPU"""
    usage = psutil.cpu_percent(1)
    return usage < 75
# If there's not enough disk, or not enough CPU, print an error
if not check_disk_usage('/') or not check_cpu_usage():
    print("ERROR!")
elif check_localhost() and check_connectivity():
    print("Everything ok")

else:
    print("Network checks failed")



# ----- second python module in the same directory network.py -----

#!/usr/bin/env python3
import requests
import socket

def check_localhost():
    localhost = socket.gethostbyname('localhost')
    return localhost == '127.0.0.1'

def check_connectivity():
    request = requests.get("http://www.google.com")
    return request.status_code == 200


# before that: sudo apt install python3-requests
# change file permission to executable: sudo chmod +x health_checks.py
# to run the script:  ./health_checks.py
