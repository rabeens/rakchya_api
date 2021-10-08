from lib.logger import Logger
logger = Logger.get_logger()

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