import logging
from logging.handlers import RotatingFileHandler

from config.config import LOG_FILE, LOG_LEVEL, APP_NAME

class Logger():
	_logger = None	

	@staticmethod
	def setLogging():
		print("Creating new logger")
		try:
			_path = LOG_FILE
		except:
			_path = "logs/user.logs"
		handler = RotatingFileHandler(_path, maxBytes=5000000, backupCount=10)
		formatter = logging.Formatter('{"ts":"%(asctime)s", "name":"%(name)s", "level":"%(levelname)s", "path":"%(pathname)s", "file":"%(filename)s", "function":"%(funcName)s", "line":"%(lineno)d", "msg":"%(message)s"}')
		handler.setFormatter(formatter)
		try:
			_level = logging.getLevelName(LOG_LEVEL)
		except:
			_level = logging.WARN
		logger = logging.getLogger(APP_NAME)
		logger.setLevel(_level)
		logger.addHandler(handler)

		Logger._logger = logger

	@staticmethod
	def get_logger():
		if Logger._logger == None:
			Logger.setLogging()
		return Logger._logger



if __name__ == "__main__":
	log = Logger.get_logger()
	print(log)