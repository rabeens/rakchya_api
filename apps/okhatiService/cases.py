import time
from lib.logger import Logger
from lib.DB_CONN import DB_CONN



logger = Logger.get_logger()


def okhati_all_cases(user_id , case = "active", limit = 20, offset = 0):
    res = {}
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        query = '''select 
            request_id as ID, 
            client_id as ClientID,
            date(requested_date) as date, 
            progress as Progress,
            is_confirmed as Confirmed,
            is_paid as Paid,
            amount as Amount,
            service_charge as ServiceCharge,
            delivery_charge as DeliveryCharge,
            vat as VAT,
            amt_total as Total,
            currency_symbol as Currency
            from okhati_requests where is_closed = 'N' order by requested_date desc limit 0, 1000'''
        cursor.execute(query)
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


def okhati_my_cases(user_id ):
    res = {}
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        query = '''select 
            request_id as ID, 
            client_id as ClientID,
            date(requested_date) as date, 
            progress as Progress,
            is_confirmed as Confirmed,
            is_paid as Paid,
            amount as Amount,
            service_charge as ServiceCharge,
            delivery_charge as DeliveryCharge,
            vat as VAT,
            amt_total as Total,
            currency_symbol as Currency
            from okhati_requests where is_closed = 'N' and assignee = %s order by requested_date desc limit 0, 1000'''
        cursor.execute(query, ( int(user_id), ) )
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