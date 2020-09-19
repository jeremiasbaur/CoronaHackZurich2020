from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#from sqlalchemy import MetaData

# naming_convention = {
#     "ix": 'ix_%(column_0_label)s',
#     "uq": "uq_%(table_name)s_%(column_0_name)s",
#     "ck": "ck_%(table_name)s_%(column_0_name)s",
#     "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
#     "pk": "pk_%(table_name)s"
# }
# db = SQLAlchemy(app, metadata=MetaData(naming_convention=naming_convention))

app = Flask(__name__)
app.config.from_object(Config)
app.static_url_path='/static'
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import routes, models

	
