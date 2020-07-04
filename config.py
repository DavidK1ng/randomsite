import os
BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = '8JBSO789E_#*@*)sjKNEI_@&*SBY'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Akira240611@localhost:3306/flaskblog?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = False