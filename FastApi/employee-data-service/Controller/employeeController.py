from fastapi import APIRouter, Depends, HTTPException, status
from DataAccess.employee import Employee
from DataAccess.employee import EmployeeModel
from DataAccess.Database import SessionLocal, getDatabase
from Controller.authController import FetchToken
from typing import Annotated

router = APIRouter()

        
@router.get("/employees/")
async def GetEmployees(authenticate: Annotated[None, Depends(FetchToken)], db: SessionLocal = Depends(getDatabase)):
    return db.query(Employee).all()

@router.get("/employees/{id}")
async def GetEmployee(id: int, authenticate: Annotated[None, Depends(FetchToken)], db: SessionLocal = Depends(getDatabase)):
     emp = db.query(Employee).filter(Employee.id == id).first()

     if( emp is None):
         raise HTTPException(status_code=404, detail="Employee not found")
    
     return emp


@router.post("/employees/", status_code=status.HTTP_201_CREATED)
async def CreateEmployee(employee_data: EmployeeModel, authenticate: Annotated[None, Depends(FetchToken)], db: SessionLocal = Depends(getDatabase)):
    employeeData = Employee(**employee_data.dict())
    db.add(employeeData)
    db.commit()
    db.refresh(employeeData)


@router.put("/employees/{id}")
async def UpdateEmployee(id: int, employee_data: EmployeeModel, authenticate: Annotated[None, Depends(FetchToken)], db: SessionLocal = Depends(getDatabase)):
    emp = db.query(Employee).filter(Employee.id == id).first()

    if( emp is None):
        raise HTTPException(status_code=404, detail="Employee not found")

    emp.FirstName = employee_data.FirstName
    emp.LastName = employee_data.LastName
    emp.Address1 = employee_data.Address1
    emp.Address2 = employee_data.Address2
    emp.City = employee_data.City
    emp.State = employee_data.State
    emp.Zip = employee_data.Zip
    emp.country = employee_data.Country
    emp.IsContract = employee_data.IsContract
    emp.Position = employee_data.Position
    emp.Salary = employee_data.Salary
    emp.DateOfJoining = employee_data.DateOfJoining

    db.commit()
    db.refresh(emp)
    return emp


@router.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def DeleteEmployee(id: int, authenticate: Annotated[None, Depends(FetchToken)], db: SessionLocal = Depends(getDatabase)):
    emp = db.query(Employee).filter(Employee.id == id).first()
    if( emp is None):
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()