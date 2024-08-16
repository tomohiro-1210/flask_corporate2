from flask import Flask, render_template, session, redirect, url_for, flash
# フォーム関係
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
# バリテーション設定
from wtforms.validators import DataRequired, Email

app = Flask(__name__)

#シークレットキー　
app.config['SECRET_KEY'] = 'runindex'

class InputForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message="メールアドレスは正しい形式で入力してください")])
    username = StringField('名前', validators=[DataRequired(message="名前を入力してください")])
    input = SubmitField('入力する')

# TOPページ
@app.route('/')
def run_index():
    return render_template('run_index.html')

@app.route('/input', methods=['GET', 'POST'])
def input():
    # クラスで定義したInputFormをインスタンス化
    form = InputForm()
    if form.validate_on_submit():
        # sessionにフォームから入力したデータを引き渡し
        session['email'] = form.email.data
        session['username'] = form.username.data
        # flashを利用して入力したことを知らせる
        flash("入力したデータが表示されています。確認してください。")
        # TOPページにリダイレクト
        return redirect(url_for('run_index'))
    return render_template('input.html', form=form)

@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run()