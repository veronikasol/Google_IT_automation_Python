"""_________The first task of the course 2: "Working with python scripts" _______ """


# ------ health_checks.py -------

#!/usr/bin/env python3
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


"""_________The second  task of the course 2: "Handling files" _______ 
There's a csv file like 
Full Name, Username, Department
Audrey Miller, audrey, Development
Arden Garcia, ardeng, Sales
Bailey Thomas, baileyt, Human Resources ....
"""

# ----- generate_report.py ------

#!/usr/bin/env python3
import csv

def read_employees(csv_file_location):
    """Returns list of dictionaries with csv file header as keys and lines as data for these keys"""
      
      csv.register_dialect('empDialect', skipinitialspace=True, strict=True)
      employee_file = csv.DictReader(open(csv_file_location), dialect = 'empDialect')
      employee_list = []
      for data in employee_file:
          employee_list.append(data)
      return employee_list

employee_list = read_employees('/home/student-03-a77824e992dd/data/employees.csv')

def process_data(employee_list):
    """writes all departments tor list, 
    return dictionary from set of departments as keys and
     number of employee in each department, counted in list, as values"""
    department_list = []
    for employee_data in employee_list:
        department_list.append(employee_data['Department'])
    department_data = {}
    for department_name in set(department_list):
        department_data[department_name] = department_list.count(department_name)
    return department_data

dictionary = process_data(employee_list)

def write_report(dictionary, report_file):
    """Returns text file with departments and number of employee in it each on separate line"""
    with open(report_file, 'w+') as f:
        for k in sorted(dictionary):
            f.write(str(k) + ':' + str(dictionary[k]) + '\n')
        f.close()

write_report(dictionary,'/home/student-03-a77824e992dd/test_report.txt') 
