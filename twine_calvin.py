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
    if (employee_list[5] == ''):
        return 0
    else:
        return employee_list[5]

def get_salary_priority(job_list):
    if(job_list[6] == ''):
        return 0
    else:
        return job_list[6]

def get_score(employee_list, job_list):
    return get_salary_score(employee_list, job_list) * get_salary_risk(employee_list) * get_salary_priority(job_list)

@app.route('/')
def index():
    employee_csv_url = "https://s3.amazonaws.com/twine-labs-misc-data/recruiting/employees.csv"
    job_csv_url = "https://s3.amazonaws.com/twine-labs-misc-data/recruiting/jobs.csv"
    store_csv(job_csv_url, all_jobs)
    store_csv(employee_csv_url, all_employees)
    # print(all_employees)
    # print(all_jobs)
    print("execute get salary")
    print(get_salary_score(all_employees[1], all_jobs[1]))
    return 'Twine Employee Job Score'

@app.route('/employee/<employee_id>/limit/<limit_num>')
def print_employee(employee_id=None, limit_num=None):
    print(employee_id)
    print(limit_num)
    return "employee_id " + employee_id + " limit_num " + limit_num

@app.route('/job/<job_id>/limit/<limit_num>')
def print_job(job_id=None, limit_num=None):
    print(job_id)
    print(limit_num)
    return "job_id " + job_id + " limit_num " + limit_num
