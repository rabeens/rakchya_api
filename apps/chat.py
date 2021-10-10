import json
from mysql.connector import IntegrityError
from fastapi.responses import HTMLResponse
import os
from lib.logger import Logger
from lib.DB_CONN import DB_CONN


logger = Logger.get_logger()

msg_query = '''select 
	c.id as msg_id,
	CASE WHEN %s = usender.id then 'Y' else 'N' END  as is_my_msg, 
	concat_ws(' ',usender.fname, usender.lname) as sender,
	usender.id as sender_id, 
	c.ts as ts,
	c.msg as message
	from 
		chat_msg as c 
	inner join 
		users as usender 
	on c.sender = usender.id 
'''

receive_query = '''insert into chat_msg (case_id, sender, msg) values (%s, %s, %s)'''

def get_msgs(user_id,  case_id,  last_msg_id:int = 0):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor()
		cursor.execute(msg_query + " where c.case_id = %s and c.id > %s order by c.ts ", (user_id, case_id,last_msg_id))
		res["msg"] = DB_CONN.get_dict(cursor)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res

def get_old_msgs(user_id,  case_id,  offset, limit):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor()
		cursor.execute(msg_query + " where c.case_id = %s order by c.ts desc limit %s, %s", (user_id, case_id,offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res


def receive_msgs( user_id, case_id, msg):
	res = {
		"status":200,
		"msg":"failed to send msg"
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		print((user_id, case_id, msg))
		cursor.execute(receive_query, ( case_id,user_id, msg))
		conn.commit()
		res["msg"] = "ok"
	except IntegrityError as err:
		logger.error(err)
		res = {
			"msg":"No such case ID found",
			"status": 400
		}
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res



def chat_app_view(user_id):
	print(os.getcwd())
	try:
		with open("static/resources/chat_view_app.html", 'r') as _file:
			html_content=_file.read()
	except FileNotFoundError as fe:
		html_content="none"
	return HTMLResponse(content=html_content, status_code=200)