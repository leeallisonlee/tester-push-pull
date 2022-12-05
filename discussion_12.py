import unittest
import sqlite3
import json
import os
import matplotlib.pyplot as plt
# starter code

#changes to the code

# Create Database
def setUpDatabase(db_name):
    path = os.path.dirname(os.path.abspath(__file__))
    conn = sqlite3.connect(path+'/'+db_name)
    cur = conn.cursor()
    return cur, conn


# TASK 1
# CREATE TABLE FOR EMPLOYEE INFORMATION IN DATABASE AND ADD INFORMATION
def create_employee_table(cur, conn):
    cur.execute("CREATE TABLE IF NOT EXISTS Employees(employee_id INTEGER PRIMARY KEY, first_name TEXT, last_name TEXT, hire_date TEXT, job_id INT, salary INT)")
    conn.commit()
    

# ADD EMPLOYEE'S INFORMTION TO THE TABLE

def add_employee(filename, cur, conn):
    #load .json file and read job data
    # WE GAVE YOU THIS TO READ IN DATA
    f = open(os.path.abspath(os.path.join(os.path.dirname(__file__), filename)))
    file_data = f.read()
    f.close()
    # THE REST IS UP TO YOU
    js_data = json.loads(file_data)
    for item in js_data:
        employee_id = int(item['employee_id'])
        first_name = item['first_name']
        last_name = item['last_name']
        hire_date = item['hire_date']
        job_id = int(item["job_id"])
        salary = int(item['salary'])
        cur.execute("INSERT OR IGNORE INTO Employees (employee_id, first_name, last_name, hire_date, job_id, salary) VALUES (?, ?, ?, ?, ?, ?)", (employee_id, first_name, last_name, hire_date, job_id, salary))
        conn.commit()
# TASK 2: GET JOB AND HIRE_DATE INFORMATION
def job_and_hire_date(cur, conn):
    cur.execute("SELECT Employees.hire_date, Jobs.job_title FROM Employees JOIN Jobs ON Employees.job_id = Jobs.job_id ORDER BY Employees.hire_date")
    job_date_list = cur.fetchone()[1]
    conn.commit()
   
    return job_date_list

# TASK 3: IDENTIFY PROBLEMATIC SALARY DATA
# Apply JOIN clause to match individual employees
def problematic_salary(cur, conn):
    cur.execute("SELECT Employees.first_name, Employees.last_name FROM Employees JOIN Jobs ON Employees.job_id = Jobs.job_id WHERE Employees.salary > Jobs.max_salary OR Employees.salary < Jobs.min_salary")
    conn.commit()
    return cur.fetchall()

# TASK 4: VISUALIZATION
def visualization_salary_data(cur, conn):
    cur.execute("SELECT Employees.salary, Jobs.job_title FROM Employees JOIN Jobs ON Employees.job_id = Jobs.job_id")
    salary_job_list = cur.fetchall()

    # x and y axis
    salary_list = []
    job_list = []

    for x in salary_job_list:
        job_list.append(x[1])
        salary_list.append(x[0])

    # plotting
    plt.figure()
    plt.scatter(x = job_list, y = salary_list)

    cur.execute("SELECT min_salary, max_salary, job_title FROM Jobs")
    salary_job_list = cur.fetchall()

    plt.xticks(rotation = 30)
    plt.tight_layout()
    plt.show()

class TestDiscussion12(unittest.TestCase):
    def setUp(self) -> None:
        self.cur, self.conn = setUpDatabase('HR.db')

    def test_create_employee_table(self):
        self.cur.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='Employees'")
        table_check = self.cur.fetchall()[0][0]
        self.assertEqual(table_check, 1, "Error: 'Employees' table was not found")
        self.cur.execute("SELECT * FROM employees")
        count = len(self.cur.fetchall())
        self.assertEqual(count, 13)

    def test_job_and_hire_date(self):
        self.assertEqual('President', job_and_hire_date(self.cur, self.conn))

    def test_problematic_salary(self):
        sal_list = problematic_salary(self.cur, self.conn)
        self.assertIsInstance(sal_list, list)
        self.assertEqual(sal_list[0], ('Valli', 'Pataballa'))
        self.assertEqual(len(sal_list), 4)


def main():
    # SETUP DATABASE AND TABLE
    cur, conn = setUpDatabase('HR.db')
    create_employee_table(cur, conn)

    add_employee("employee.json",cur, conn)

    job_and_hire_date(cur, conn)

    wrong_salary = (problematic_salary(cur, conn))
    print(wrong_salary)

    visualization_salary_data(cur, conn)

if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)

