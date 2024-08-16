from flask import Flask, render_template
# フォーム関係
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

# TOPページ
@app.route('/')
def run_index():
    render_template('run_index.html')

if __name__ == ('__main__'):
    app.run()