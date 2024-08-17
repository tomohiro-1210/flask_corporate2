from flask import Flask, render_template, url_for, redirect, session, flash, request, abort
# flask_wtfでフォーム構築、wtformsでフォームのフィールドを一括管理
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
# wtforms.validatorsでバリテーションチェック
from wtforms.validators import DataRequired, Email, EqualTo
# ログイン
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash

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

# ログイン関係
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

def localize_callback(*args, **kwargs):
    return 'このページにアクセスするには、ログインが必要です。'
login_manager.localize_callback = localize_callback


#外部キーの設定
from sqlalchemy.engine import Engine
from sqlalchemy import event

@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

# Userモデル、テーブル
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    # dbのテーブルを定義
    id = db.Column(db.Integer, primary_key=True) # Integerで数値型を指定する
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)
    passsword_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))
    #リレーション設定
    post = db.relationship('BlogPost', backref='author', lazy='dynamic')

    def __init__(self, email, username, password, administrator):
        self.email = email
        self.username = username
        self.passsword = password
        self.administrator = administrator

    def __repr__(self):
        return f"Username: {self.username}"
    
    # パスワードのチェック
    def check_password(self, password):
        return check_password_hash(self.passsword_hash, password)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    # フォームから受け取ったパスワードのハッシュ化処理をする。そして上のpassword_hashに戻っていくのか？
    @password.setter
    def password(self, password):
        self.passsword_hash = generate_password_hash(password)

    # 管理者か一般ユーザーかの判断
    def is_administrator(self):
        if self.administrator == "1":
            return 1
        else: 
            return 0

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

#ログインフォーム
class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください")])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('ログイン')

# 登録フォーム
class RegistrationForm(FlaskForm):
    # フォームに表示する入力項目の設定
    email = StringField('メールアドレス',validators=[DataRequired(), Email(message='正しいメールアドレスを入力してください')])
    username = StringField('ユーザーネーム', validators=[DataRequired()])
    password = PasswordField('パスワード', validators=[DataRequired(), EqualTo('password_confirm', message='パスワードが一致していません')])
    password_confirm = PasswordField('パスワード(確認用)', validators=[DataRequired()])
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

# ログインページ
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    # 入力された内容に問題がないかを見る
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None:
            if user.check_password(form.password.data):
                login_user(user)
                next = request.args.get('next')
                if next == None  or not next[0] ==  '/':
                    next = url_for('user_maintenance')
                return redirect(next)

            else:
                flash('パスワードが一致しません')
        else:
            flash('入力されたユーザーは存在しません')

    return render_template('login.html', form=form)

# ログアウト
@app.route('/logput')
def logout():
    logout_user()
    return redirect(url_for('login'))

#View関数
@app.route('/register', methods=['GET', 'POST'])
@login_required
def register():
    # フォームを使えるようにインスタンス化
    form = RegistrationForm()
    if not current_user.is_administrator():
        abort(403)
    # 入力したデータをチェックする
    if form.validate_on_submit():

        # セッションにデータ格納
        # session['email'] = form.email.data
        # session['username'] = form.username.data
        # session['password'] = form.password.data

        #フォームのデータをDBに格納する
        user = User(email=form.email.data, username=form.username.data, password=form.password.data, administrator="0")
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
@login_required
def user_maintenance():
    page = request.args.get('page', 1 ,type=int)
    # usersテーブルからデータを全件取得
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('user_maintenance.html', users=users)

# ユーザー更新ページ
@app.route('/<int:user_id>/account', methods=['GET', 'POST'])
@login_required
def account(user_id):
    user = User.query.get_or_404(user_id)
    if user.id != current_user.id and not current_user.is_administrator():
        abort(403)
    form = UpdateUserForm(user_id)
    # 初期表示後の処理
    if form.validate_on_submit():
        user.username = form.username.data
        user.email = form.email.data
        
        if form.password.data:
            user.password = form.password.data
            
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
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # 管理者権限
    if not current_user.is_administrator():
        abort(403)
    if user.is_administrator():
        flash('管理者は削除できません')
        return redirect(url_for('account', user_id=user_id))
    db.session.delete(user)
    db.session.commit()
    flash(f'ユーザーのアカウントが削除されました。')
    return redirect(url_for('user_maintenance'))

# 403ページ
@app.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403

# 404ページ
@app.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
