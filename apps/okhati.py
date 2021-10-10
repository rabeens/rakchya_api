import json
import time
from lib.logger import Logger
from lib.DB_CONN import DB_CONN
from fastapi.responses import FileResponse


logger = Logger.get_logger()


def okhati_request(user_id, okhatiFile):
    res = {}
    epoch =  int(time.time())
    data = okhatiFile.file.read()
    okhati_dump_file = "dumps/{}_{}_{}".format( user_id, epoch, okhatiFile.filename) 
    with open(okhati_dump_file, "wb") as _f:
        _f.write(data)

    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        user_data = (okhati_dump_file, user_id)
        cursor.execute("Insert into okhati_requests (invoice_asset_path, client_id, is_active) values(%s, %s, True)", user_data)
        res = {
            "msg" : "Invoice added",
            "status":200
        }
        conn.commit()
    except Exception as e:
        logger.error(e)
        print(e)
        res = {
            "msg" : "Cannot process your request! Please try again",
            "status":400
        }
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    return res



def okhati_my_request(user_id , limit = 20, offset = 0):
    res = {}
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        cursor.execute('''select 
            concat_ws("_", "O", request_id, unix_timestamp(date(requested_date)), unix_timestamp(now())) as submissionId,
            request_id as ID, 
            date(requested_date) as date, 
            progress as Progress,
            is_confirmed as Confirmed,
            is_paid as Paid,
            amt as Amount,
            service_charge as ServiceCharge,
            delivery_charge as DeliveryCharge,
            tax as VAT,
            amt + service_charge + delivery_charge + tax as Total,
            currency_symbol as Currency
            from okhati_requests where client_id = %s and is_active = true and is_closed = false order by requested_date desc limit %s, %s''', (user_id, offset, limit ))
        res = {
            "msg" : DB_CONN.get_dict(cursor),
            "status":200
        }
    except Exception as e:
        logger.error(e)
        res = {
            "msg" : "Cannot process your request! Please try again",
            "status":400
        }
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    return res


def okhati_my_request_image(user_id, request_id, limit = 20, offset = 0):
    res = {}
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        cursor.execute('''select 
            invoice_asset_path
            from okhati_requests where request_id = %s and  client_id = %s and is_active = true  order by requested_date desc limit %s, %s''', (request_id, user_id, offset, limit ))
        asset = DB_CONN.get_dict(cursor)
        logger.info(asset)
        if len(asset) != 1:
            res = {
                "msg" :"Cannot process your request!" ,
                "status":400
            }
        else:
            res = {
                "msg" : asset[0],
                "status":200
            }
    except Exception as e:
        logger.error(e)
        res = {
            "msg" : "Cannot process your request! Please try again",
            "status":400
        }
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    if res["status"] == 400:
        return res
    else: 
        return FileResponse(res["msg"]["invoice_asset_path"])


def okhati_request_sample(limit = 20, offset = 0):
        return FileResponse("static/images/okhati_sample.jpg")

