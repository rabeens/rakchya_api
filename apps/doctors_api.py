import json

from lib.logger import Logger
from lib.DB_CONN import DB_CONN
from apps.User import encrypt_pwd
from datetime import datetime


logger = Logger.get_logger()

login_query = "select client_id as id, token as token from users as u inner join doctors as d on u.client_id = d.user_id where (u.contact_number = %s or u.email = %s) and u.password = %s and u.status = 1"

case_query = "select cs.case_id as ID, cl.name as name, sy.name as speciality, cs.create_date as start_date, cs.severity from cases as cs inner join users as cl on cs.client_id = cl.client_id inner join symptoms as sy on cs.symptom_id = sy.id"

def doc_signin(user):
	_msg = "Error signing in!"
	_code = 400
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor()
		cursor.execute(login_query, (user.username,user.username, encrypt_pwd(user.password) ) )
		_data = DB_CONN.get_dict(cursor)
		if cursor.rowcount != 1:
			logger.warn("None or Multiple rows received for {} and password".format(user.username))
			return {
				"msg":"Cannot login",
				"status":401
			}
		_msg = _data[0]["token"]
		_code = 200
		cursor.execute("update users set last_login = %s where client_id = %s", (datetime.now(), _data[0]["id"]))
		conn.commit()
	except Exception as e:
		logger.error(e)
		_msg = "Failed to login"
		_code = 400
	finally:
		if (conn.is_connected()):
			cursor.close()
			conn.close()
	return {
		"status":_code,
		"msg":_msg
	}


def doc_active_cases(user_id,  limit = 5, offset = 0):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		_case_query = case_query + " where lower(cs.is_active) = 'y' and cs.doc_id = %s  and cs.is_paid = 1 limit %s, %s"
		logger.info(user_id)
		logger.info(_case_query)
		cursor.execute(_case_query, (user_id,offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
		logger.info(user_id)
		logger.info(res)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res


# def doc_appointments( user_id, case,  limit = 20, offset = 0):
# 	res = {
# 		"status":200,
# 		"msg":[]
# 	}
# 	if case == "active":
# 		is_active = 'Y'
# 	else:
# 		is_active = "N"

# 	try:
# 		conn = DB_CONN.get_conn()
# 		cursor = conn.cursor(buffered = True)
# 		cursor.execute(case_query + " where lower(c.is_active) = %s  and doc_id = %s limit %s, %s", (is_active,user_id, offset, limit))
# 		res["msg"] = DB_CONN.get_dict(cursor)
# 	except Exception as e:
# 		logger.error(e)
# 		res["status"] = 400
# 	finally:
# 		conn.close()
# 	return res



# def post_appointment(user_id, form):
# 	# print(form)
# 	res = {
# 		"status":200,
# 		"msg":"Symptom added"
# 	}
# 	try:
# 		conn = DB_CONN.get_conn()
# 		cursor = conn.cursor(buffered = True)
# 		cursor.execute("Insert into cases (client_id, doc_id, symptom_id, is_active) values (%s, %s, %s, 'Y')", (int(user_id), int(form.doc_id), int(form.symptom_id)))
# 		conn.commit()
# 		cursor.execute(case_query + " where c.case_id = %s and c.client_id = %s", (cursor.lastrowid,user_id))
# 		res["msg"] = DB_CONN.get_dict(cursor)[0]
# 	except Exception as e:
# 		logger.error(e)
# 		res = {
# 			"status":400,
# 			"msg":"Failed to insert"
# 		}

# 	finally:
# 		conn.close()
# 	return res