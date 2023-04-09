from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import cloudinary

app = Flask(__name__)
app.secret_key = '#%^&(*$%^&(78678675$%&^&$^%*&^%&*^'

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:123456@localhost/qlhs1?charset=utf8mb4"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

db = SQLAlchemy(app)
login = LoginManager(app)


cloudinary.config(cloud_name='dkcq9dgui', api_key='586758563261442', api_secret='VUEoTXbDRMiDSc9PXRcu_dqEoe0')

#Kết nối với mySQL