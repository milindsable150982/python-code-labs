from Models.employee import Employee

import csv

class EmployeeService:

    employees = []

    def __init__(self):
        with open('./Employee.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                self.employees.append(Employee(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8]))
                #next(reader)


    async def get_employees(self):
        return self.employees   

    async def get_employee(self, id: int):
        for employee in self.employees:
            if employee.get_id() == id:
                return employee
        return None