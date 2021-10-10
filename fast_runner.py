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
from lib.DB_CONN import DB_CONN
from lib.odbc import get_dict 
from lib.Authorization import *
from apps.User import *
from apps.home import *
from apps.okhati import *
from apps.cases import *
from apps.doctors_api import *
from apps.chat import *

from apps.shop import *



from apps.okhatiService.cases import *


from models.Invoice import Invoice
from models.Appointment import Appointment

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
#  administration section
# ------------------------------------------------------------------------------------------
@app.post("/signin", tags=["administration"])
async def _signIn(signInForm : SignInForm):
    return signin(signInForm)

@app.post("/doc_signin", tags=["administration"])
async def _doc_signin(signInForm : SignInForm):
    return doc_signin(signInForm)



@app.post("/signup", tags=["administration"])
async def _signUp(signUpForm:SignUpForm ):
    return signup(signUpForm)

@app.post("/forgot_password", tags=["administration"])
async def _forgot_password(form:ForgotPasswordForm ):
    return forgot_password(form)

@app.post("/reset_link", tags=["administration"])
async def _reset_link(user_id:str, token:str ):
    return reset_link(user_id, token)



@app.post("/okhati/signin", tags=["administration"])
async def _okhati_signIn(signInForm : SignInForm):
    # change to dedicated logijn
    return signin(signInForm)

@app.post("/doc/signin", tags=["administration"])
async def _doc_signIn(signInForm : SignInForm):
    # change to dedicated logijn
    return signin(signInForm)






# ------------------------------------------------------------------------------------------
#  monitoring section
# ------------------------------------------------------------------------------------------

@app.get("/health", tags=["monitoring"])
async def main():
    return {
        "msg":"good"
    }


# ------------------------------------------------------------------------------------------
#  personalization section
# ------------------------------------------------------------------------------------------
@app.get("/welcome_msg", tags=["personalization"])
async def _welcome_msg(request: Request ):
    return secure(welcome_msg, request)


@app.get("/notifications", tags=["personalization"])
async def get_notifications(request:Request):
    _data = []
    # _data = [{"id":"1","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"2","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"3","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"4","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"5","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"6","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"7","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"8","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"9","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"10","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"11","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"12","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"13","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"14","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"15","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"16","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"17","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"18","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"19","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":"20","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},]
    # _data = [{"id":"1","name":"Rabeen","rating":"5","tagline":"MSc CS PoU","image":"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"}]
    return _data

@app.get("/carts", tags=["personalization"])
async def get_carts(request:Request):
   
    return secure(carts, request)

@app.get("/about/me", tags=["personalization"])
async def _about_me(request: Request):
    # return about_me(1)
    return secure(about_me, request)

# @app.post("/about/me", tags=["personalization"])
# async def _about_me(request: Request, name:str):
#     return secure(update_my_name, request)



# ------------------------------------------------------------------------------------------
#  marketing section
# ------------------------------------------------------------------------------------------
@app.get("/banners", tags=["marketing"])
async def _banners(request : Request):
    return secure(banners, request)


# ------------------------------------------------------------------------------------------
#  appointment section
# ------------------------------------------------------------------------------------------
@app.get("/categories", tags=["appointments"])
async def _categories(request : Request):
    return secure(categories, request)


@app.get("/symptoms", tags=["appointments"])
async def _symptoms(request:Request):
    return secure(symptoms, request)

@app.get("/case/questionaire", tags=["appointments"])
async def questionaire():
    _data = [{"id":1,"question":"What is first question","type":"text"},{"id":2,"question":"What is the second question?","type":"number","min":0,"max":100},{"id":3,"question":"What is the third question?","type":"options","options":["option 1","option 2"]},{"id":4,"question":"What is the fourth question?","type":"radio","options":["radio 1","radio 2","radio 3"]}]
    return _data


@app.get("/doctors", tags=["appointments"])
async def _doctors(request : Request, category:str = "*", limit:int = 20, offset:int = 0):
    return secure( doctors,  request, category, limit, offset)


@app.get("/doctor", tags=["appointments"])
async def _doctor(doctor_id, request:Request):
    return secure(doctor, request, doctor_id)


# @app.get("/schedule")
# async def schedule_new():
#     return "schedule new task"




@app.get("/appointments", tags=["appointments"])
async def _appointments(request:Request, case:str="active"):
    return secure(appointments, request, case )

@app.post("/appointments", tags=["appointments"])
async def _post_appointments(request : Request, appointment : Appointment):
    return secure(post_appointment, request, appointment)


# ------------------------------------------------------------------------------------------
#  cases section
# ------------------------------------------------------------------------------------------
@app.get("/active_cases", tags=["cases"])
async def _active_cases( request : Request, limit: int = 10, offset: int = 0):
    return secure(active_cases, request, limit=limit, offset = offset)


# @app.get("/doc/active_cases", tags=["cases"])
# async def _doc_active_cases(request: Request):
#     return secure(doc_active_cases, request)


# ------------------------------------------------------------------------------------------
#  okhati section
# ------------------------------------------------------------------------------------------
@app.post("/okhati/request", tags=["okhati"])
async def _okhati_requests(
        request:Request,
        okhatiFile: UploadFile = File(...)
    ):
    return secure( okhati_request, request, okhatiFile)

@app.get("/okhati/requests", tags=["okhati"])
async def _okhati_my_requests(
        request:Request,
        limit:int = 20,
        offset:int = 0
    ):
    return secure( okhati_my_request,request, limit, offset)


@app.get("/okhati/request", tags=["okhati"])
async def _okhati_my_requests_image(
        request:Request,
        request_id: str,
        limit:int = 20,
        offset:int = 0
    ):
    # return okhati_my_request_image(1, request_id, limit, offset)
    return secure( okhati_my_request_image, request, request_id, limit, offset)



@app.get("/okhati/request/sample", tags=["okhati"])
async def _okhati_request_sample(
        request:Request,
    ):
    return okhati_request_sample(1)
    # return secure( okhati_my_request_image, request, request_id, limit, offset)



# ------------------------------------------------------------------------------------------
#  payment section
# ------------------------------------------------------------------------------------------
@app.get("/paymentOptions", tags=["payment"])
async def _payment_options():
    return {
        "status":200,
        "msg":[
            {
                "id":1,
                "name":"esewa",
                "icon":"",
                "link":"https://uat.esewa.com.np/epay/main",
                "merchant_code":"epay_payment",
                "status":"good"
            },
            {
                "id":2,
                "name":"ConnectIPS",
                "link":"https://connectips.com"
            }
        ]
    }



@app.post("/invoice", tags=["payment"])
async def _invoice(invoice : Invoice):
    print(invoice)
    return {
        "status":200,
        "msg":{
            "activity_id":1,
            "bill":[
                {
                    "id":1,
                    "title":"Amount",
                    "value":500
                },
                {
                    "id":3,
                    "title":"Service Charge",
                    "value":100
                },
                                {
                    "id":5,
                    "title":"Discount",
                    "value":100,
                    "strike":"true"
                },
                {
                    "id":4,
                    "title":"Total",
                    "value":500
                },
                {
                    "id":2,
                    "title":"Tax",
                    "value":113
                },

                {
                    "id":6,
                    "title":"Grand Total",
                    "value":613
                }

            ]
        }
    }






# ------------------------------------------------------------------------------------------
#  chat section
# ------------------------------------------------------------------------------------------



@app.get("/chat_msgs", tags=["chat"])
async def _get_msgs(request: Request, case_id: int, last_msg_id:int = 0):
    return secure(get_msgs, request, case_id, last_msg_id)

@app.get("/chat_msgs_old", tags=["chat"])
async def _get_old_msgs(request: Request, case_id: int, offset:int = 0, limit:int=15):
    return secure(get_old_msgs, request, case_id, offset, limit)

@app.post("/chat_msgs", tags=["chat"])
async def _receive_msgs(request: Request, case_id: int, msg:str, ):
    return secure(receive_msgs, request, case_id, msg)

@app.get("/chat_app_view", tags=["chat"])
async def _chat_app_view(request: Request):
    return secure(chat_app_view, request,)


# ------------------------------------------------------------------------------------------
#  okhati section
# ------------------------------------------------------------------------------------------
@app.get("/okhatiService/all_cases", tags=["okhatiAdmin"])
async def _okhatiservice_all_cases(request:Request):
    return secure(okhati_all_cases, request)


@app.get("/okhatiService/my_cases", tags=["okhatiAdmin"])
async def _okhatiservice_my_cases(request:Request):
    return secure(okhati_my_cases, request)

@app.get("/okhatiService/request", tags=["okhatiAdmin"])
async def _okhati_my_requests_image(
        request:Request,
        request_id: str,
        limit:int = 20,
        offset:int = 0
    ):
    # return okhati_my_request_image(1, request_id, limit, offset)
    return secure( okhati_my_request_image, request, request_id, limit, offset)



# @app.get("/okhatiService/all_cases")
# async def _okhati_cases(request:Request, case:str="active", limit:int = 20, offset:int = 0):
#     return secure(okhati_all_cases, request, case , limit, offset)




# ------------------------------------------------------------------------------------------
#  shop section
# ------------------------------------------------------------------------------------------
@app.get("/shop/categories", tags=["shop"])
async def _shop_categories(request:Request):
    return secure( shop_categories, request)

@app.get("/shop/search", tags=["shop"])
async def _shop_search(request:Request, search_query:str, offset:int = 0, limit:int = 50):
    return secure( shop_search, request, search_query, limit, offset)

@app.get("/shop/category/{category_id}", tags=["shop"])
async def _shop_search_categories(request:Request, category_id:str, offset:int = 0, limit:int = 50):
    return secure( shop_search_categories, request, category_id, limit, offset)

@app.get("/shop/sales", tags=["shop"])
async def _shop_sales(request:Request, offset:int = 0, limit:int = 50):
    return secure( shop_sales, request, limit, offset)

@app.get("/shop/recommended", tags=["shop"])
async def _shop_recommended(request:Request, offset:int = 0, limit:int = 50):
    return secure( shop_recommended, request, limit, offset)

@app.get("/shop/add_to_cart", tags=["shop"])
async def _shop_add_to_cart(request:Request, product_id: int):
    return secure( shop_add_to_cart, request, product_id)

@app.get("/shop/popular", tags=["shop"])
async def _shop_popular(request:Request, offset:int = 0, limit:int = 50):
    return secure( shop_popular, request, limit, offset)








# ------------------------------------------------------------------------------------------
#  doc app section
# ------------------------------------------------------------------------------------------
@app.get("/docService/cases", tags=["docsService"])
async def _doc_active_cases(request: Request):
    return secure(doc_active_cases, request)



if __name__ == "__main__":
    uvicorn.run(
        "fast_runner:app", 
        host="0.0.0.0", 
        port=5000, 
        reload=True,
        # ssl_keyfile="certs/private.key",
        # ssl_certfile="certs/certificate.crt",
    )