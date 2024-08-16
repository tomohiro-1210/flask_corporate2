from flask import Flask, render_template, session, redirect, url_for
# フォーム関係
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

app = Flask(__name__)

#シークレットキー　
app.config['SECRET_KEY'] = 'runindex'

class InputForm(FlaskForm):
    email = StringField('メールアドレス')
    username = StringField('名前')
    input = SubmitField('入力する')

# TOPページ
@app.route('/')
def run_index():
    return render_template('run_index.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
    # クラス手で定義したInputFormをインスタンス化
    form = InputForm()
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['username'] = form.username.data
        return redirect(url_for('run_index'))
    return render_template('input.html', form=form)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()