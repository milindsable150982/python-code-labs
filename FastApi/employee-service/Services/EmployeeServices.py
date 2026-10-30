from Models.employee import Employee

import csv

class EmployeeService:

    employees = []

    def __init__(self):
        with open('./Employee.csv', mode='r', encoding='utf-8') as file:
            reader = csv.reader(file)
            for row in reader:
                self.employees.append(Employee(
                    id=row[0],
                    firstname=row[1],
                    lastname=row[2],
                    address=row[3],
                    state=row[4],
                    zip=row[5],
                    country=row[6],
                    position=row[7],
                    salary=row[8],
                    joiningDate=row[9]
                ))


    async def getEmployees(self):
        return self.employees   

    async def getEmployeeById(self, id: int):
        for employee in self.employees:
            if employee.id == id:
                return employee
        return None


    async def getEmployeeByName(self, name: str):
       returnEmployee = []
       for employee in self.employees:
         if employee.firstname.lower() == name.lower() :
             returnEmployee.append(employee)
       return returnEmployee



    async def addEmployee(self, employee: Employee):
        employee.id = len(self.employees) + 1
        self.employees.append(employee)
        with open('./Employee.csv', mode='a', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            
            writer.writerow([
                employee.id,
                employee.firstname,
                employee.lastname,
                employee.address,
                employee.state,
                employee.zip,
                employee.country,
                employee.position,
                employee.salary,
                employee.joiningDate
            ])


    async def updateEmployee(self, updated_employee: Employee, id: int):
            for i, employee in enumerate(self.employees):
                if employee.id == id:
                    self.employees[i] = updated_employee
                    self.employees[i].id = id  # Ensure the ID remains the same
                    break

    async def delete_emplyee(self, id:int):
           for i, employee in enumerate(self.employees):
             if employee.id == id:
                 self.employees.pop(i)
                 break;