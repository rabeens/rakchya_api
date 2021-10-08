from pydantic import BaseModel
from lib.logger import Logger
from datetime import datetime
import hashlib
import re
logger = Logger.get_logger()
from lib.DB_CONN import DB_CONN

# hashlib.md5("RAKSHYA".encode()).hexdigest()
SALT = "9fe78f0f826b221b0445a0b860babdef"


class SignInForm(BaseModel):
	username: str
	password: str



class ForgotPasswordForm(BaseModel):
	email: str = ""
	contact_number: str = ""


class SignUpForm(BaseModel):
	name:str
	password: str
	dob:str
	address:str
	contact_number:str
	email:str


def get_token(user):
	try:
		_key = "{}||{}".format(user.name, user.password).encode("utf8") 
		return hashlib.md5(_key).hexdigest()
	except Exception as e:
		logger.error("Error while creating token!")
		logger.error(e)


def encrypt_pwd(pwd):
	try:
		return hashlib.md5(pwd.encode()).hexdigest()
	except Exception as e:
		logger.error(e)

def signin(user):
	_msg = "Error signing in!"
	_code = 400
	print(user)
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor()
		# print(encrypt_pwd(user.password))
		cursor.execute("select client_id as id, token as token from users where (contact_number = %s or email = %s) and password = %s and status = 1", (user.username,user.username, encrypt_pwd(user.password) ) )
		_data = DB_CONN.get_dict(cursor)
		if cursor.rowcount != 1:
			logging.warn("None or Multiple rows received for {} and password".format(user.username))
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
	finally:
		if (conn.is_connected()):
			cursor.close()
			conn.close()
	return {
		"status":_code,
		"msg":_msg
	}

def forgot_password(user):
	return {
		"msg":" Password reset link has been sent to email"
	}

def signup(user):


	_msg = "Error signing up!"
	_code = 400
	token = get_token(user)
	# print(token)
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor()
		query = "select count(*) as count from users  where email = %s or contact_number = %s"
		# cursor.execute("select client_id as id, token as token from client where username = %s and password = %s and status = 1", (user.username, user.password))
		cursor.execute(query, (user.email, user.contact_number))
		_data = DB_CONN.get_dict(cursor)
		# print(_data)
		if _data[0]["count"] >0:
			return {
				"msg":"User already exists",
				"status":401
			}

		user_data = (user.name, encrypt_pwd(user.password), user.contact_number, user.address, user.dob, token, user.email)
		# print(user_data)
		query = "Insert into users (name, password, contact_number, address, dob, token, email) values(%s, %s, %s, %s, %s, %s, %s )"
		# cursor.execute("select client_id as id, token as token from client where username = %s and password = %s and status = 1", (user.username, user.password))
		cursor.execute(query, user_data)
		conn.commit()


		_msg = "Successful"
		_code = 200
	except Exception as e:
		logger.error(e)
	finally:
		if (conn.is_connected()):
			cursor.close()
			conn.close()
	return {
		"status":_code,
		"msg":_msg
	}


def reset_link(user_id, token):
	# print(user_id)
	# print(token)
	return {
		"msg":"Login successful"
	}



def about_me(user_id):
	_msg = "Error fetching details!"
	_code = 400
	try:
		conn = DB_CONN.get_conn()
		cursor = conn.cursor()
		cursor.execute("select username, name, contact_number, address, date_format(dob, '%Y-%m-%d') as dob, case  when status=1 then 'active' else 'inactive' end as status  from users where client_id = %s;", (int(user_id), ) )
		_data = DB_CONN.get_dict(cursor)
		# print(_data)
		if cursor.rowcount != 1:
			raise Exception("None or Multiple rows received for {} and password".format(user.username))
		_msg = _data[0]
		_code = 200
	except Exception as e:
		logger.error(e)
	finally:
		if (conn.is_connected()):
			cursor.close()
			conn.close()
	return {
		"status":_code,
		"msg":_msg
	}