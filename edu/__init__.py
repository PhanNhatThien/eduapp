from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import quote
import cloudinary
from flask_login import LoginManager

app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:%s@localhost/edudb?charset=utf8mb4' % quote('12345678')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key = 'jfgwadfgow124324@#@$@#sdfdsf923u1?'

db = SQLAlchemy(app=app)

cloudinary.config(
            cloud_name='dogosq8z4',
            api_key='338272838275355',
            api_secret='IirWac17xXkmWSBbixT_29LuGOM',
)

login = LoginManager(app=app)