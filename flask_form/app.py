from flask import Flask, render_template, url_for, redirect, session, flash
# flask_wtfでフォーム構築、wtformsでフォームのフィールドを一括管理
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
# wtforms.validatorsでバリテーションチェック
from wtforms.validators import DataRequired, Email, EqualTo

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flaskform'

class RegistrationForm(FlaskForm):
    # フォームに表示する入力項目の設定
    email = StringField('メールアドレス',validators=[DataRequired(), Email()])
    username = StringField('ユーザーネーム', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired(), EqualTo('pw_config')])
    pw_config = PasswordField('パスワード(確認用)', validators=[DataRequired()])
    submit = SubmitField('登録する')

@app.route('/')
def index():
    return 'TOPページ'

#View関数
@app.route('/register', methods=['GET', 'POST'])
def register():
    # フォームを使えるようにインスタンス化
    form = RegistrationForm()
    # 入力したデータをチェックする
    if form.validate_on_submit():

        # セッションにデータ格納
        session['email'] = form.email.data
        session['username'] = form.username.data
        session['password'] = form.password.data
        # 登録後に表示するメッセージ
        flash('ユーザーが登録されました')
        return redirect(url_for('user_maintenance'))
    return render_template('register.html', form=form)

@app.route('/user_maintenance')
def user_maintenance():
    return render_template('user_maintenance.html')


if __name__ == '__main__':
    app.run(debug=True)
