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



"""_________The third task of the course 2: "Working with regular expressions" _______ """


# ------ script.py -------

#!/usr/bin/env python3

#Import libraries
import csv
import re

def contains_domain(address, domain):
    domain = r'[\w\.-]+@'+domain+'$'
    if re.match(domain,address):
        return True
    return False

def replace_domain(address, old_domain, new_domain):
    old_domain_pattern = r'' + old_domain + '$'
    address = re.sub(old_domain_pattern, new_domain, address)
    return address

def main():
    """Processes the list of emails, replacing any instances of the
    old domain with the new domain."""
    old_domain,new_domain = 'abc.edu','xyz.edu'
    csv_file_location = '/home/student-01-ceadb84c5ea3/data/user_emails.csv'
    report_file = '/home/student-01-ceadb84c5ea3/data/updated_user_emails.csv'
    user_email_list = []
    old_domain_email_list = []
    new_domain_email_list = []
    with open(csv_file_location, 'r') as f:
        user_data_list = list(csv.reader(f))
        user_email_list = [data[1].strip() for data in user_data_list[1:]]

        for email_address in user_email_list:
            if contains_domain(email_address, old_domain):
                old_domain_email_list.append(email_address)
                replaced_email = replace_domain(email_address, old_domain, new_domain)
                new_domain_email_list.append(replaced_email)
        email_key = ' ' + 'Email Address'
        email_index = user_data_list[0].index(email_key)

        for user in user_data_list[1:]:
            for old_domain, new_domain in zip(old_domain_email_list, new_domain_email_list):
                if user[email_index] == ' ' + old_domain:
                    user[email_index] = ' ' + new_domain

    with open(report_file, 'w+') as output_file:
        writer = csv.writer(output_file)
        writer.writerows(user_data_list)


main()


"""_________The fourth task of the course 2: "Working with log files" _______ 
We'll search for the CRON error that failed to start. 
To do this, we'll use a python script to search log files for a particular type of ERROR log. 
In this case, we'll search for a CRON error within the fishy.log file that failed to start by 
narrowing our search to "CRON ERROR Failed to start"."""

# ------ find_error.py -------

#!/usr/bin/env python3
import sys
import os
import re


def error_search(log_file):
    error = input("What is the error? ")
    returned_errors = []
    with open(log_file, mode='r',encoding='UTF-8') as file:
        for log in  file.readlines():
            error_patterns = ["error"]
            for i in range(len(error.split(' '))):
                error_patterns.append(r"{}".format(error.split(' ')[i].lower()))
            if all(re.search(error_pattern, log.lower()) for error_pattern in error_patterns):
                returned_errors.append(log)
        file.close()
    return returned_errors

  
def file_output(returned_errors):
    with open(os.path.expanduser('~') + '/data/errors_found.log', 'w') as file:
        for error in returned_errors:
            file.write(error)
    file.close()


if __name__ == "__main__":
    
    log_file = sys.argv[1]
    returned_errors = error_search(log_file)
    file_output(returned_errors)
    sys.exit(0)


# CRON ERROR Failed to start


"""_________The fifth task of the course 2: "Implementing unit testing " _______ 

    Write a simple test to check for basic functionality
    Write a test to check for edge cases
    Correct code with a try/except statement
    There's user_emails.csv in data directory, we have emails.py to test and
     we will create ~/scripts/emails_test.py

"""
# ------ emails.py -------

#!/usr/bin/env python3
import sys
import csv

def populate_dictionary(filename): 
    """Populate a dictionary with name/email pairs for easy lookup."""
    email_dict = {}
    with open(filename) as csvfile:
        lines = csv.reader(csvfile, delimiter = ',')
        for row in lines:
            name = str(row[0].lower())
            email_dict[name] = row[1]
    return email_dict

def find_email(argv):
    """ Return an email address based on the username given."""
    # Create the username based on the command line input.
    try:
        fullname = str(argv[1] + " " + argv[2])
        # Preprocess the data
        email_dict = populate_dictionary('/home/student-03-aa83a0edc859/data/user_emails.csv')
        # Find and print the email
         # If email exists, print it
        if email_dict.get(fullname.lower()):
            return email_dict.get(fullname.lower())
        else:
            return "No email address found"
    except IndexError:
        return "Missing parameters"


def main():
    print(find_email(sys.argv))

if __name__ == "__main__":
    main()


# ------ emails_test.py -------

#!/usr/bin/env python3
import unittest
from emails import find_email

class TestFile(unittest.TestCase):

    def test_basic(self):
        testcase = [None, "Bree", "Campbell"]
        expected = "breee@abc.edu"
        self.assertEqual(find_email(testcase), expected)

    def test_one_name(self):
        testcase = [None, "John"]
        expected = "Missing parameters"
        self.assertEqual(find_email(testcase), expected)

    def test_two_name(self):
        testcase = [None, "Roy","Cooper"]
        expected = "No email address found"
        self.assertEqual(find_email(testcase), expected)



if __name__ == '__main__':
    unittest.main()





"""_________The task #6 of the course 2: "Editing files using substrings" _______

To comply with the company policy the tsk is to change  username "jane" to "jdoe".
We have a list of files. Will work in shell 
grep ' jane ' ../data/list.txt
grep " jane " ../data/list.txt | cut -d ' ' -f 1  ### delimiter = d: ' ' field -f=1

# Cheching the existance of the file with test
if test -e ~/data/jane_profile_07272018.doc; then echo "File exists"; else echo "File doesn't exist"; fi

# iteration
for i in 1 2 3; do echo $i; done

Next we'll write script: 
This script should catch all "jane" lines and store them in another text file called oldFiles.txt. 

"""

#-----findJane.sh -----
"""Create new text file, 
grep files that belong to jane from list.txt
and put their names into new tex file.
""" 

!/bin/bash
>oldFiles.txt

files="$(grep " jane " ../data/list.txt | cut -d ' ' -f 3)"
for i in $files; do
        if test -e /home/student-03-06b4b6d6baa2"$i"; then
        echo "$i" >> oldFiles.txt; fi
done


#----- changeJane.py ----
"""Takes filename as an argument, 
renames files listed in this file using subprocess.run and list with mv command as an argument"""

#!/usr/bin/env python3
import sys
import subprocess
f_name = sys.argv[1]
with open(f_name, 'r') as f:
    for line in f.readlines():
        old_name = line.strip()
        new_name = old_name.replace("jane","jdoe")
        subprocess.run(['mv','/home/student-03-06b4b6d6baa2'+ old_name,
            '/home/student-03-06b4b6d6baa2'+ new_name])










"""_________The task #7 of the course 2: "Log analysis using regular expression" _______ 

working in shell:
>>> import re
>>> line = "May 27 11:45:40 ubuntu.local ticky: INFO: Created ticket [#1234] (username)"
>>> re.search(r"ticky: INFO: ([\w ]*) ", line)
<_sre.SRE_Match object; span=(29, 57), match='ticky: INFO: Created ticket '>
>>> line = "May 27 11:45:40 ubuntu.local ticky: ERROR: Error creating ticket [#1234] (username)"
>>> re.search(r"ticky: ERROR: ([\w ]*) ", line)
<_sre.SRE_Match object; span=(29, 65), match='ticky: ERROR: Error creating ticket '>
>>> fruit = {"oranges":3, "aples": 5, "bananas": 7, "pears": 2}
>>> sorted(fruit.items())
[('aples', 5), ('bananas', 7), ('oranges', 3), ('pears', 2)]
>>> import operator
>>> sorted(fruit.items(), key=operator.itemgetter(0))
[('aples', 5), ('bananas', 7), ('oranges', 3), ('pears', 2)]
>>> sorted(fruit.items(), key=operator.itemgetter(1))
[('pears', 2), ('oranges', 3), ('aples', 5), ('bananas', 7)]
>>> sorted(fruit.items(), key=operator.itemgetter(1), reverse=True)
[('bananas', 7), ('aples', 5), ('oranges', 3), ('pears', 2)]"""


#!/usr/bin/env python3
import re
import operator

error_messages = {}
user_entries = {}
with open ('syslog.log', 'r') as f:
        for log in f.readlines():
                username = re.search(r"\((\w*)\)", line).groups()[0]
                user_entries[username] = 
                if re.search(r"ticky: INFO: ([\w ]*) ", log):
                                             
                elif re.search(r"ticky: ERROR: ([\w ]*) ", log):
                        pass


