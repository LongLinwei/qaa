import os

# DEBUG=True

SECRET_KEY=os.urandom(24)

HOST_NAME='127.0.0.1'
PORT='3306'
DATABASE='xlwd'
USERNAME='root'
PASSWORD='123qwe'
SQLALCHEMY_DATABASE_URI='mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME,PASSWORD,HOST_NAME,PORT,DATABASE)




