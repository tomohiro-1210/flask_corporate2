# ログイン
from flask_login import LoginManager

# DBの読み込み
import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# flask関係
app = Flask(__name__)
app.config['SECRET_KEY'] = 'flaskform'

# dbの環境変数設定
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #dbの変更履歴無効

# dbの作成
db = SQLAlchemy(app) #DBの生成？？
Migrate(app, db)

# ログイン関係
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


def localize_callback(*args, **kwargs):
    return 'このページにアクセスするには、ログインが必要です。'
login_manager.localize_callback = localize_callback

#外部キーの設定
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()