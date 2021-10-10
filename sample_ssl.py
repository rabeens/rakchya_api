from fastapi import FastAPI, Request, File, UploadFile, Depends, Cookie
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware



from typing import Optional
# from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
import json
import uvicorn

from lib.logger import Logger
from lib.odbc import get_dict 
from lib.Authorization import *
from apps.chat import *



logger = Logger.get_logger()
logger.info("Starting app...")



app = FastAPI(
    title="RAKCHYA",
    description="This is the API reference for rakchya's API"
)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBasic()



# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     start_time = time.time()
#     response = await call_next(request)
#     process_time = time.time() - start_time
#     print(request.headers)
#     print(dir(response))
#     # response.headers["X-Process-Time"] = str(process_time)
#     # msg = {

#     # }
#     return response



def secure(f, request, *args, **kwargs):
    user = False
    if "Cookie"  in request.headers:
        user = get_user_by_session(request.headers["Cookie"])
    elif "Authorization"  in request.headers:
        user  = get_user_by_token(request.headers["Authorization"])
    else:
        # pass
        # return f(14, *args, **kwargs)
        return f(1, *args, **kwargs)
        
    print("-------------------------------------------")
    # print(request.headers)
    print(user)
    print("-------------------------------------------")
    if user == False:
        return {
            "status":401,
            "msg":"Unauthorized access"
        }
    return f(user, *args, **kwargs)



# ------------------------------------------------------------------------------------------
#  chat section
# ------------------------------------------------------------------------------------------


@app.get("/chat_app_view", tags=["chat"])
async def _chat_app_view(request: Request):
    return secure(chat_app_view, request,)




if __name__ == "__main__":
    uvicorn.run(
        "fast_runner:app", 
        host="0.0.0.0", 
        port=5001, 
        reload=True,
        ssl_keyfile="certs/ssl.key",
        ssl_certfile="certs/ssl.crt",
    )