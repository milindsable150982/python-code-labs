from fastapi import FastAPI, status
from  DataAccess.config.database import Base, engine
import Controllers.memberController
import Controllers.bookController
import Controllers.authorController
import Controllers.borrowingController
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder({"detail": exc.errors(), "body": exc.body}),
    )

app.include_router(Controllers.memberController.router)
app.include_router(Controllers.bookController.router)
app.include_router(Controllers.authorController.router)
app.include_router(Controllers.borrowingController.router)

Base.metadata.create_all(bind=engine)