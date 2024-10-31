from flask import Flask
from flask_mysqldb import MySQL
from config import SECRET_KEY,DB_NAME, DB_USERNAME, DB_PASSWORD, DB_HOST
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv


load_dotenv('.env')

mysql = MySQL()
app = Flask(__name__, instance_relative_config=True)

from modules.students import students_bp
from modules.payments import payments_bp
from modules.transactions import transactions_bp
from modules.verifications import verifications_bp

def start_app():
    app.config.from_mapping(
        SECRET_KEY=SECRET_KEY,
        MYSQL_USER=DB_USERNAME,
        MYSQL_PASSWORD=DB_PASSWORD,
        MYSQL_DB=DB_NAME,
        MYSQL_HOST=DB_HOST
    )
    app.register_blueprint(students_bp, url_prefix="/students")
    app.register_blueprint(payments_bp, url_prefix="/payments")
    app.register_blueprint(transactions_bp, url_prefix="/transactions")
    app.register_blueprint(verifications_bp, url_prefix="/verifications")

    mysql.init_app(app)
    CSRFProtect(app)
    return app

from . import routes