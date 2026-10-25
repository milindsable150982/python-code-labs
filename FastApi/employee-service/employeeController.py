from fastapi import Body, FastAPI
from  Services.EmployeeServices import EmployeeService

app = FastAPI()
employee_service = EmployeeService()

@app.get("/employees")
async def get_employees():
    return await employee_service.get_employees();

@app.get("/employees/{id}")
async def get_employee(id: str):
    return await employee_service.get_employee(id);

