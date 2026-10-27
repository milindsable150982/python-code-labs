from fastapi import Body, FastAPI
from  Services.EmployeeServices import EmployeeService
from Models.employee import Employee

app = FastAPI()
employeeService = EmployeeService()

@app.get("/employees")
async def get_employees():
    return await employeeService.getEmployees();

@app.get("/employee/")
async def get_employee(name: str):
    return await employeeService.getEmployeeByName(name);

@app.get("/employee/{id}")
async def get_employee(id: int):
    return await employeeService.getEmployeeById(id);

@app.put("/employee/{id}")
async def update_employee(id: int, employee: Employee):
    await employeeService.updateEmployee(id, employee)
    return {"message": "Employee updated successfully"}



@app.post("/employees")
async def add_employee(employee: Employee):
    await employeeService.addEmployee(employee)
    return {"message": "Employee added successfully"}


@app.delete("/employees")
async def delete_employee(id: int):
   await employeeService.delete_emplyee(id)
   return {"message": "Employee deleted successfully"}