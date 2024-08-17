import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'appdb'

basedir = os.path.abspath(os.path.dirname(___file__))
app.config['SQLARCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLARChEMY_TRACK_MODIFICATIONS'] = False #dbの変更履歴無効

db = SQLAlchemy(app)


if __name__ == '__main__':
    app.run(debug=True)