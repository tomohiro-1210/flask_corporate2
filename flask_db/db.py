import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'appdb'

basedir = os.path.abspath(os.path.dirname(___file__))
app.config['SQLARCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLARChEMY_TRACK_MODIFICATIONS'] = False #dbの変更履歴無効

db = SQLAlchemy(app) #DBの生成？？

# テーブルの定義
class User(db.Model):
    __tablename__ = 'users'

    # dbのテーブルを定義
    id = db.Column(db.Integer, primary_key=True) # Integerで数値型を指定する
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    passsword_hash = db.Column(db.String(128))

    def __init__(self, email, username, password_hash):
        self.email = email
        self.username = username
        self.passsword_hash = password_hash

    def __repr__(self):
        return f"Username: {self.username}"


if __name__ == '__main__':
    app.run(debug=True)