import requests
import csv
from flask import Flask

app = Flask(__name__)

all_jobs = []
all_employees = []

def print_csv(csv_url):
    with requests.Session() as s:
        download = s.get(csv_url)
        decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    new_list = list(cr)
    for row in new_list:
        print(row)

def store_csv(csv_url, storage):
    with requests.Session() as s:
        download = s.get(csv_url)
        decoded_content = download.content.decode('utf-8')
    cr = csv.reader(decoded_content.splitlines(), delimiter=',')
    new_list = list(cr)
    for row in new_list:
        storage.append(row)

def get_salary_score(employee_list, job_list):
    salary = employee_list[3]
    job_salary_min = job_list[4]
    job_salary_max = job_list[5]

    if ( salary >= job_salary_max or salary <= job_salary_min ):
        return 0
    else:
        mid_salary = (job_salary_max - job_salary_min) / 2
        diff_mid = abs(mid_salary - salary)
        return diff_mid / (job_salary_max- job_salary_min)
    
def get_salary_risk(employee_list):
    return employee_list[5]

def get_salary_priority(job_list):
    return job_list[6]

def get_score(employee_list, job_list):
    return get_salary_score(employee_list, job_list) * get_salary_risk(employee_list) * get_salary_priority(job_list)

@app.route('/')
def index():
    employee_csv_url = "https://s3.amazonaws.com/twine-labs-misc-data/recruiting/employees.csv"
    job_csv_url = "https://s3.amazonaws.com/twine-labs-misc-data/recruiting/jobs.csv"
    store_csv(job_csv_url, all_jobs)
    store_csv(employee_csv_url, all_employees)
    print(all_employees)
    print(all_jobs)
    print(get_salary_score(all_employees[1], all_jobs[1]))
    return 'Hello, World'
