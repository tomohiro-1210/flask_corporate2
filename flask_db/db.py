import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SECRET_KEY'] = 'appdb'

basedir = os.path.abspath(os.path.dirname(___file__))
app.config['SQLARCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')


if __name__ == '__main__':
    app.run(debug=True)