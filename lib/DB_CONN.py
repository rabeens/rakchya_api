from config.db import DB_CONFIG
from lib.logger import Logger
import mysql.connector
from mysql.connector.pooling import PooledMySQLConnection

import time
from concurrent.futures import ThreadPoolExecutor
from config.db import DB_CONFIG

from config.config import DB_CONNECTION_RETRY_COUNT


logger = Logger.get_logger()
# pool = mysql.connector.pooling.MySQLConnectionPool(
# 	pool_name="rakshya_conn_pool",
# 	pool_size=2,
# 	host=DB_CONFIG["DB_HOST"],
# 	user=DB_CONFIG["DB_USER"],
# 	password=DB_CONFIG["DB_PWD"],
# 	database = DB_CONFIG["DB_NAME"]
# )

# print("creating pool")
class DB_CONN():
	__pool__ = None
	__creating__ = False
	# pool = mysql.connector.connect(
	# 				host=DB_CONFIG["DB_HOST"],
	# 				user=DB_CONFIG["DB_USER"],
	# 				password=DB_CONFIG["DB_PWD"],
	# 				database = DB_CONFIG["DB_NAME"]
	# 			)

	def __init__(self):
		print("DB_CONN init")
		if DB_CONN.__pool__ is None:
			print("creating pool")
			DB_CONN.__pool__ = DB_CONN.__create_pool()

	@staticmethod
	def __create_pool():
		logger.info("Creating db connection pool")
		try:
			_retry_wait_ts = DB_CONNECTION_RETRY_WAIT_SECONDS
		except:
			_retry_wait_ts = 5
		retry = 0
		while retry < DB_CONNECTION_RETRY_COUNT:
			try:
				# mydb = mysql.connector.connect(
				mydb = mysql.connector.pooling.MySQLConnectionPool(
					pool_name="rakshya_conn_pool",
					pool_size=10,
					host=DB_CONFIG["DB_HOST"],
					user=DB_CONFIG["DB_USER"],
					password=DB_CONFIG["DB_PWD"],
					database = DB_CONFIG["DB_NAME"],
					# reset_session=True
				)
				return mydb
			except Exception as e:
				logger.error("Cannot connect to database. Attempt: {}".format(retry))
			retry = retry + 1
			time.sleep(_retry_wait_ts)
		
	@staticmethod
	def get_conn():
		if DB_CONN.__pool__ is None:
			DB_CONN()
		conn = None
		while conn is None:
			# print("conn is none:{}".format(conn))
			try:
				conn = DB_CONN.__pool__.get_connection()
				break
			except Exception as e:
				print(e)
				raise(e)
				print("conn :{}".format(conn))
				print("exception while getting connection. waiting for 1 sec")
				time.sleep(1)
		return conn

	@staticmethod
	def get_dict(cursor):
		try:
			columns = [col[0] for col in cursor.description]
			data = cursor.fetchall()
			res = []
			for row in data:
				res.append( dict( zip( columns, row) ) )
			return res
		except Exception as e:
			logger.error(e)
		return []