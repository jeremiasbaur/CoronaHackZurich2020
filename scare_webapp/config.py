import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hackzurichscare'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or \
        'sqlite:///' + os.path.join(basedir, 'gis_data.db')
        # "postgresql://postgres:deneme123@34.121.242.98:5432/aoe2serv"
    SQLALCHEMY_TRACK_MODIFICATIONS = False