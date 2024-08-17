# flask_wtfでフォーム構築、wtformsでフォームのフィールドを一括管理
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, ValidationError
# wtforms.validatorsでバリテーションチェック
from wtforms.validators import DataRequired, Email, EqualTo

from company_blog.models import User

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

