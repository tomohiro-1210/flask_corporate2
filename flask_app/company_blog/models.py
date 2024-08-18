# ログイン
from flask_login import UserMixin

from werkzeug.security import check_password_hash, generate_password_hash
#タイムゾーン
from datetime import datetime
from pytz import timezone

from company_blog import db, login_manager

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
    password_hash = db.Column(db.String(128))
    administrator = db.Column(db.String(1))
    #リレーション設定
    post = db.relationship('BlogPost', backref='author', lazy='dynamic')

    def __init__(self, email, username, password, administrator):
        self.email = email
        self.username = username
        self.password = password
        self.administrator = administrator

    def __repr__(self):
        return f"Username: {self.username}"
    
    # パスワードのチェック
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    
    # フォームから受け取ったパスワードのハッシュ化処理をする。そして上のpassword_hashに戻っていくのか？
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

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
    category_id = db.Column(db.Integer, db.ForeignKey('blog_category.id'))
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/tokyo')))
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    summary = db.Column(db.String(140))
    featured_image = db.Column(db.String(140))

    def __init__(self, user_id, title, text, summary, featured_image, category_id):
        self.title = title
        self.text = text
        self.featured_image = featured_image
        self.user_id = user_id
        self.category_id = category_id
        self.summary = summary

    def __repr__(self):
        return f'postID: {self.id}, Title: {self.title}, Author: {self.author} \n'

# ブログカテゴリ
class BlogCategory(db.Model):
    __tablename__ = 'blog_category'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(140))
    # BlogPostとリレーションシップ
    posts = db.relationship('BlogPost', backref='blogcategory', lazy='dynamic')

    def __init__(self, category):
        self.category = category

    def __repr__(self):
        return f'CategoryID: {self.id}, CategoryName: {self.category} \n'
    
# お問い合わせフォーム
class Inquiry(db.Model):
    __tablename__ = 'inquiry'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64))
    title = db.Column(db.String(140))
    text = db.Column(db.Text)
    date = db.Column(db.DateTime, default=datetime.now(timezone('Asia/Tokyo')))

    def __init__(self, name, email, title, text):
        self.name = name
        self.email = email
        self.title = title
        self.text = text

    def __repr__(self):
        return f'InquiryID: {self.id}, Name: {self.name}, Text: {self.text} \n'