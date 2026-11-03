from fastapi import FastAPI, Depends, HTTPException, status
import employee
from Database import SessionLocal, engine

app = FastAPI()

employee.Base.metadata.create_all(bind=engine)

async def getDatabase():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
@app.get("/employees/")
async def GetEmployees(db: SessionLocal = Depends(getDatabase)):
    return db.query(employee.Employee).all()

@app.get("/employees/{id}")
async def GetEmployee(id: int, db: SessionLocal = Depends(getDatabase)):
     emp = db.query(employee.Employee).filter(employee.Employee.id == id).first()

     if( emp is None):
         raise HTTPException(status_code=404, detail="Employee not found")
    
     return emp


@app.post("/employees/", status_code=status.HTTP_201_CREATED)
async def CreateEmployee(employee_data: employee.EmployeeModel, db: SessionLocal = Depends(getDatabase)):
    employeeData = employee.Employee(**employee_data.dict())
    db.add(employeeData)
    db.commit()
    db.refresh(employeeData)


@app.put("/employees/{id}")
async def UpdateEmployee(id: int, employee_data: employee.EmployeeModel, db: SessionLocal = Depends(getDatabase)):
    emp = db.query(employee.Employee).filter(employee.Employee.id == id).first()

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


@app.delete("/employees/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def DeleteEmployee(id: int, db: SessionLocal = Depends(getDatabase)):
    emp = db.query(employee.Employee).filter(employee.Employee.id == id).first()
    if( emp is None):
        raise HTTPException(status_code=404, detail="Employee not found")
    db.delete(emp)
    db.commit()