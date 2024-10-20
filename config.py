import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
        SECRET_KEY = '1234'
        SQLALCHEMY_DATABASE_URI = 'sqlite:///path/to/app.db'


