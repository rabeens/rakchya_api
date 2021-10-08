import json

from lib.logger import Logger
from lib.DB_CONN import DB_CONN


logger = Logger.get_logger()


def welcome_msg(user_id):
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        cursor.execute("select banner_json as msg from welcome_msg where user_id  in (0, %s) limit 2", (user_id, ))
        _tmp_data = DB_CONN.get_dict(cursor)
        # print(_data)
        _data = []
        for row in _tmp_data:
            parsed_row = json.loads(row["msg"])
            _data.append(parsed_row)
    except Exception as e:
        logger.error(e)
        _data = []
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    return {
        "msg":_data,
        'status':200
    }
    # _txt = {"type":"text", "link":"https://google.com",  "msg":"Healthcare at your tooltip!", "bgcolor":"#a55", "paddingTop":5,"paddingBottom":5, "color":"#fff", "fontWeight":"bold", "fontSize":22}
    # _internalLink = {"type":"text", "linkType":"route", "link":"Okhati",  "msg":"Buy medicine", "bgcolor":"#a55", "paddingTop":5,"paddingBottom":5, "color":"#fff", "fontWeight":"bold", "fontSize":22}
    # _data = {}
    # _img = {"type":"image", "height":250,  "msg":"https://www.circleone.in/images/products_gallery_images/PVC-Banner.jpg"}
    # _data = [_txt, _img]
    # return [_txt]


def banners(user_id):
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        cursor.execute("select banner_json as msg from banners where user_id  in (0, %s) limit 10", (user_id, ))
        _tmp_data = DB_CONN.get_dict(cursor)
        # print(_data)
        _data = []
        for row in _tmp_data:
            # print(row)
            # parsed_row = row["msg"]
            parsed_row = json.loads(row["msg"])
            _data.append(parsed_row)
    except Exception as e:
        logger.error(e)
        _data = []
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    return {
        "msg":_data,
        'status':200
    }


def categories(user_id, _type = "category"):
    # _data = [{"id":1, "title":"Category 1", "icon" :"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":2, "title":"Category 2"}, {"id":3, "title":"Category 3"},{"id":4, "title":"Category 1"},{"id":5, "title":"Category 2"}, {"id":6, "title":"Category 3"}, {"id":7, "title":"Category 7"}]
    # return _data
    _data = {
        "status":200,
        "msg":""
    }
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        cursor.execute("select id as id, name, label as title, icon, description from symptoms where type = %s limit 100", (_type,  ))
        _data["msg"] = DB_CONN.get_dict(cursor)
        # _data = [{"id":1, "title":"Symptom 1", "icon" :"https://4.bp.blogspot.com/-krdeTqQLML8/Wyf2oV7eedI/AAAAAAAABpI/OZ759swV7L8wWtt2pwBXIgp6aPz33r01gCLcBGAs/s400/fist%2Bapp.jpg"},{"id":2, "title":"Symptom 2"}, {"id":3, "title":"Symptom 3"},{"id":4, "title":"Symptom 1"},{"id":5, "title":"Symptom 2"}, {"id":6, "title":"Symptom 3"}, {"id":7, "title":"Symptom 7"}]
    except Exception as e:
        logger.error(e)
        _data = {
            "status":400,
            "msg":"Cannot fetch categories"
        }
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    return _data


def symptoms(user_id):
    return categories(user_id, "symptom")


def doctors(user_id, category = '*', limit = 20, offset = 0):
    _res = {
        "status":400,
        "msg":[]
    }
    try:
        _params = (offset, limit)
        # query = "select  from doctors as doc inner join doc_to_symptoms_mapping as dtsm on doc.doc_id = dtsm.doc_id inner join symptoms as s on dtsm.symptom_id = s.id "
        query = "select distinct doc.doc_id as id, doc.name as Name, rating as rating, doc.icon, doc.description as description from doctors as doc inner join doc_to_symptoms_mapping as dtsm on doc.doc_id = dtsm.doc_id inner join symptoms as smpt on smpt.id = dtsm.symptom_id"
        if category != "*":
            where_query = "where lower(smpt.label) = %s or lower(smpt.name) = %s "
            query = "{} {}".format(query, where_query)
            _params = (category.lower(),category.lower(),  offset, limit)
        query = "{} {}".format(query, "limit %s, %s")

        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        cursor.execute(query, _params )
        _res["msg"] = DB_CONN.get_dict(cursor)
        _res["status"] = 200
    except Exception as e:
        logger.error(e)
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    return _res


def doctor(user_id, doctor_id):
    _res = {
        "status":400,
        "msg":[]
    }
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        query = "select * from doctors  where doc_id = %s"
        cursor.execute(query, (int(doctor_id), ))
        _res["msg"] = DB_CONN.get_dict(cursor)
        _res["status"] = 200
    except Exception as e:
        logger.error(e)
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    return _res

def carts(user_id, offset=0, limit=100):
    _res = {
        "status":400,
        "msg":[]
    }
    try:
        conn = DB_CONN.get_conn()
        cursor = conn.cursor()
        query = "select * from carts limit %s, %s"
        cursor.execute(query, (limit*offset, limit*offset+limit ))
        _res["msg"] = DB_CONN.get_dict(cursor)
        _res["status"] = 200
    except Exception as e:
        logger.error(e)
    finally:
        if (conn.is_connected()):
            cursor.close()
            conn.close()
    return _res