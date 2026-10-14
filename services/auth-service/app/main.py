from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse


from app.core.exception import UserAlreadyExistsException, WrongLoginOrPassword


from app.api.auth import router



app = FastAPI()


app.include_router(router)

@app.exception_handler(UserAlreadyExistsException)
async def user_exists_handler(request: Request, 
                                     exc: UserAlreadyExistsException):
    
    return JSONResponse(status_code=409, content={"detail": str(exc)})

@app.exception_handler(WrongLoginOrPassword)
async def wrong_login_or_pass_handler(request: Request, 
                                     exc: WrongLoginOrPassword):
    
    return JSONResponse(status_code=401, content={"detail": str(exc)})