from fastapi import Body, FastAPI, Path, Query, HTTPException
from  Services.EmployeeServices import EmployeeService
from Models.employee import Employee
from starlette import status

app = FastAPI()
employeeService = EmployeeService()

@app.get("/employees")
async def get_employees():
    return await employeeService.getEmployees();

@app.get("/employee/")
async def get_employee(name: str):
    employee = await employeeService.getEmployeeByName(name)
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee

@app.get("/employee/{id}", status_code=status.HTTP_200_OK) #Path
async def get_employee(id: int = Path(gt=0, description="The ID of the employee should be greater than 0.")):
    employee = await employeeService.getEmployeeById(id)
    if employee is None:
       raise HTTPException(status_code=404, detail="Employee not found")
    return await employee;

@app.put("/employee/{id}")
async def update_employee(employee: Employee, id: int = Path(gt=0, description="The ID of the employee should be greater than 0.")):
    await employeeService.updateEmployee(id, employee)
    return {"message": "Employee updated successfully"}



@app.post("/employees")
async def add_employee(employee: Employee):
    await employeeService.addEmployee(employee)
    return {"message": "Employee added successfully"}


@app.delete("/employees") #query
async def delete_employee(id: int = Query(gt=0, description="The ID of the employee should be greather than 0.")):
   await employeeService.delete_emplyee(id)
   return {"message": "Employee deleted successfully"}