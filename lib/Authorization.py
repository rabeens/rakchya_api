from lib.DB_CONN import DB_CONN

from lib.logger import Logger
logger = Logger.get_logger()
logger.info("Starting app...")


def get_user_by_token(token):
	print("received token:{}".format(token))
	return {
		"userid":1,
		"access":{
			"app1":"1",
			"app2":"2",
		}
	}


def get_user_by_session(session_header):
	token = session_header
	user_id = False
	try:
		conn = DB_CONN.get_conn()
	except:
		logger.error("Cannot connect to db")
		return False

	try:
		
		cursor = conn.cursor()
		cursor.execute("select client_id from users where token = %s", (token,))
		_tmp_data = DB_CONN.get_dict(cursor)
		if len(_tmp_data) !=1:
			logger.error("Multiple users found for token {}".format(token))
			return False
		user_id = _tmp_data[0]["client_id"]
	except Exception as e:
		logger.error(e)
	finally:
		if (conn.is_connected()):
			cursor.close()
			conn.close()
	return user_id