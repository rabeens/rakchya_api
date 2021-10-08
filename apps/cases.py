import json

from lib.logger import Logger
from lib.DB_CONN import DB_CONN


logger = Logger.get_logger()

case_query = "select case_id as ID, d.name as doc_name, s.name as speciality, c.create_date as start_date, is_history_taken, severity, is_paid  from cases as c join doctors as d on c.doc_id = d.doc_id inner join symptoms as s on c.symptom_id = s.id"

def active_cases(user_id,  limit = 5, offset = 0):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		cursor.execute(case_query + " where lower(c.is_active) = 'y' and client_id = %s limit %s, %s", (user_id,offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res


def appointments( user_id, case,  limit = 20, offset = 0):
	res = {
		"status":200,
		"msg":[]
	}
	if case == "active":
		is_active = 'Y'
	else:
		is_active = "N"

	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		cursor.execute(case_query + " where lower(c.is_active) = %s  and client_id = %s limit %s, %s", (is_active,user_id, offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res



def post_appointment(user_id, form):
	# print(form)
	res = {
		"status":200,
		"msg":"Symptom added"
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		cursor.execute("Insert into cases (client_id, doc_id, symptom_id, is_active) values (%s, %s, %s, 'Y')", (int(user_id), int(form.doc_id), int(form.symptom_id)))
		conn.commit()
		cursor.execute(case_query + " where c.case_id = %s and c.client_id = %s", (cursor.lastrowid,user_id))
		res["msg"] = DB_CONN.get_dict(cursor)[0]
	except Exception as e:
		logger.error(e)
		res = {
			"status":400,
			"msg":"Failed to insert"
		}

	finally:
		conn.close()
	return res