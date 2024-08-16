from flask import Flask, render_template, url_for, redirect, session
# flask_wtfでフォーム構築、wtformsでフォームのフィールドを一括管理
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flaskform'

class RegistrationForm(FlaskForm):
    # フォームに表示する入力項目の設定
    email = StringField('メールアドレス')
    userame = StringField('ユーザーネーム')
    password = PasswordField('パスワード')
    pw_config = PasswordField('パスワード(確認用)')
    submit = SubmitField('登録')

#View関数
@app.route('/register', methods=['GET', 'POST'])
def register():
    # フォームを使えるようにインスタンス化
    form = RegistrationForm()
    # 入力したデータを保持する
    if form.validate_on_submit():
        session['email'] = form.email.data
        session['username'] = form.usename.data
        session['password'] = form.password.data
        return redirect(url_for('user_maintenance'))
    return render_template('register.html', form=form)





if __name__ == '__main__':
    app.run(debug=True)
