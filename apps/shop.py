import json

from lib.logger import Logger
from lib.DB_CONN import DB_CONN
from apps.User import encrypt_pwd
from datetime import datetime


logger = Logger.get_logger()


def shop_categories(user):
	_msg = "Error getting product categories!"
	_code = 400
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor()
		cursor.execute("select * from product_categories limit 50")
		_msg = DB_CONN.get_dict(cursor)
		_code = 200
	except Exception as e:
		logger.error(e)
		_msg = "Cannot fetch product categories"
		_code = 400
	finally:
		if (conn.is_connected()):
			cursor.close()
			conn.close()
	return {
		"status":_code,
		"msg":_msg
	}


def shop_search(user, search_query,  limit = 50, offset = 0):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		_case_query = "select * from products where lower(name) like %s and is_active = true limit %s, %s"
		# logger.info(user_id)
		logger.info(_case_query)
		cursor.execute(_case_query, ( "%{}%".format(search_query.lower()), offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
		# logger.info(user_id)
		logger.info(res)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res



def shop_search_categories(user, cat_id,  limit = 50, offset = 0):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		_case_query = "select * from products where category_id = %s and is_active = true limit %s, %s"
		# logger.info(user_id)
		logger.info(_case_query)
		cursor.execute(_case_query, ( cat_id, offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
		# logger.info(user_id)
		logger.info(res)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res



def shop_sales(user,  limit = 50, offset = 0):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		_case_query = "select * from products where is_active = true limit %s, %s"
		# logger.info(user_id)
		logger.info(_case_query)
		cursor.execute(_case_query, ( offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
		# logger.info(user_id)
		logger.info(res)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res


def shop_recommended(user,  limit = 50, offset = 0):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		_case_query = "select * from products where is_active = true limit %s, %s"
		# logger.info(user_id)
		logger.info(_case_query)
		cursor.execute(_case_query, ( offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
		# logger.info(user_id)
		logger.info(res)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res


def shop_popular(user,  limit = 50, offset = 0):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		_case_query = "select * from products where is_active = true limit %s, %s"
		# logger.info(user_id)
		logger.info(_case_query)
		cursor.execute(_case_query, ( offset, limit))
		res["msg"] = DB_CONN.get_dict(cursor)
		# logger.info(user_id)
		logger.info(res)
	except Exception as e:
		logger.error(e)
		res["status"] = 400
	finally:
		conn.close()
	return res


def shop_add_to_cart(user, product_id):
	res = {
		"status":200,
		"msg":[]
	}
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor(buffered = True)
		_case_query = "insert into carts (user_id, product_id) values(%s, %s)"
		logger.info(_case_query)
		logger.info((user, product_id))
		cursor.execute(_case_query, (user, product_id))
		conn.commit()
		res["msg"] = "Added to cart!"
		# logger.info(user_id)
		logger.info(res)
	except Exception as e:
		logger.error(e)
		raise e
		res["msg"]="Failed to insert to cart!"
		res["status"] = 400
	finally:
		conn.close()
	return res