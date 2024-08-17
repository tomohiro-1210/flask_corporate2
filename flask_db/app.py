from enum import unique
import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#タイムゾーン
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

app.config['SECRET_KEY'] = 'appdb'

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #dbの変更履歴無効

db = SQLAlchemy(app) #DBの生成？？
Migrate(app, db)

# テーブルの定義
class User(db.Model):
    __tablename__ = 'users'

    # dbのテーブルを定義
    id = db.Column(db.Integer, primary_key=True) # Integerで数値型を指定する
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    passsword_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))

    def __init__(self, email, username, password_hash, administrator):
        self.email = email
        self.username = username
        self.passsword_hash = password_hash
        self.administrator = administrator

    def __repr__(self):
        return f"Username: {self.username}"

# ブログテーブル
class BlogPost(db.Model):
    __tablename_ = 'blog_post'

    # テーブルの設定
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/tokyo')))
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    summary = db.Column(db.String(140))
    featured_image = db.Column(db.String(140))

    def __init__(self, user_id, title, text, summary, featured_image):
        self.title = title
        self.text = text
        self.featured_image = featured_image
        self.user_id = user_id
        self.summary = summary

    def __repr__(self):
        return f'postID: {self.id}, Title: {self.title}'

if __name__ == '__main__':
    app.run(debug=True)