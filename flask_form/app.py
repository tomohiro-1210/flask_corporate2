from flask import Flask, render_template, url_for, redirect, session, flash, request
# flask_wtfでフォーム構築、wtformsでフォームのフィールドを一括管理
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
# wtforms.validatorsでバリテーションチェック
from wtforms.validators import DataRequired, Email, EqualTo
# DBの読み込み
import os 
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
#タイムゾーン
from datetime import datetime
from pytz import timezone

app = Flask(__name__)

app.config['SECRET_KEY'] = 'flaskform'

# dbの環境変数設定
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'data.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False #dbの変更履歴無効

# dbの作成
db = SQLAlchemy(app) #DBの生成？？
Migrate(app, db)


#外部キーの設定
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

# Userモデル、テーブル
class User(db.Model):
    __tablename__ = 'users'

    # dbのテーブルを定義
    id = db.Column(db.Integer, primary_key=True) # Integerで数値型を指定する
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    passsword_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))
    #リレーション設定
    post = db.relationship('BlogPost', backref='author', lazy='dynamic')

    def __init__(self, email, username, password_hash, administrator):
        self.email = email
        self.username = username
        self.passsword_hash = password_hash
        self.administrator = administrator

    def __repr__(self):
        return f"Username: {self.username}"

# ブログテーブル
class BlogPost(db.Model):
    __tablename__ = 'blog_post'

    # テーブルの設定
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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
        return f'postID: {self.id}, Title: {self.title}, Author: {self.author} \n'


# 登録フォーム
class RegistrationForm(FlaskForm):
    # フォームに表示する入力項目の設定
    email = StringField('メールアドレス',validators=[DataRequired(), Email(message='正しいメールアドレスを入力してください')])
    username = StringField('ユーザーネーム', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired(), EqualTo('pw_config', message='パスワードが一致していません')])
    pw_config = PasswordField('パスワード(確認用)', validators=[DataRequired()])
    submit = SubmitField('登録する')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('入力されたユーザー名は既に使われています。')
        
    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('入力されたメールアドレスは既に登録されています。')


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
        # session['email'] = form.email.data
        # session['username'] = form.username.data
        # session['password'] = form.password.data

        #フォームのデータをDBに格納する
        user = User(email=form.email.data, username=form.username.data, password_hash=form.password.data, administrator="0")
        db.session.add(user)
        db.session.commit()

        # 登録後に表示するメッセージ
        flash('ユーザーが登録されました')
        return redirect(url_for('user_maintenance'))
    return render_template('register.html', form=form)

# ユーザー更新
class UpdateUserForm(FlaskForm):
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください。")])
    username = StringField('ユーザー名', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[EqualTo('password_confirm', message='パスワードが一致していません')])
    password_confirm = PasswordField('パスワード(確認用)')
    submit = SubmitField('データ更新')

    def __init__(self, user_id, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args,  **kwargs)
        self.id = user_id

    # メールアドレスエラー
    def validate_email(self, field):
        if User.query.filter(User.id != self.id).filter_by(email=field.data).first():
            raise ValidationError('入力されたメールアドレスは登録されています。')
        
    # ユーザーネームエラー
    def validate_username(self, field):
        if User.query.filter(User.id != self.id).filter_by(username=field.data).first():
            raise ValidationError('入力されたユーザー名は既に使われています。')

# ユーザー管理ページ
@app.route('/user_maintenance')
def user_maintenance():
    page = request.args.get('page', 1 ,type=int)
    # usersテーブルからデータを全件取得
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('user_maintenance.html', users=users)

# ユーザー更新ページ
@app.route('/<int:user_id>/account', methods=['GET', 'POST'])
def account(user_id):
    user = User.query.get_or_404(user_id)
    form = UpdateUserForm(user_id)
    # 初期表示後tの処理
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        
        if form.password.data:
            user.password_hash = form.password.data
            
        db.session.commit()
        flash('ユーザーアカウントが更新されました。')

        return redirect(url_for('user_maintenance'))
    # 初期表示
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    
    return render_template('account.html', form=form)

# ユーザーデータ削除
@app.route('/<int:user_id>/delete', methods=['GET', 'POST'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f'ユーザーのアカウントが削除されました。')
    return redirect(url_for('user_maintenance'))

if __name__ == '__main__':
    app.run(debug=True)
