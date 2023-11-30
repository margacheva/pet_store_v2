from flask import Flask
from flask_mail import Mail
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = True
app.config["SECRET_KEY"] = "SECRET_Kedrftgyhujmikjhswedfrgthyju8kie4dfrgt6hyjukiefrgthyjuiEY"
app.config["JSON_AS_ASCII"] = True
app.config["MAIL_SERVER"] = 'smtp.gmail.com'
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'petts.shop123@gmail.com'
app.config["MAIL_PASSWORD"] = 'knhd witv dzub zspd '
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql+psycopg2://yana:yana@localhost:44444/postgres'
mail = Mail(app)
db = SQLAlchemy()
login_manager = LoginManager()
db.init_app(app)
mail.init_app(app)
login_manager.init_app(app)

with app.app_context():
    db.create_all()
