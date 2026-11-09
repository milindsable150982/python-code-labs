from fastapi import FastAPI
from Controller import authController, employeeController
from DataAccess.Database import engine, Base

app = FastAPI()
app.include_router(authController.router)
app.include_router(employeeController.router)

Base.metadata.create_all(bind=engine)