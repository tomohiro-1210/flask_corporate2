from flask import Flask, render_template, url_for, redirect, flash, request, abort

# ログイン
from flask_login import login_user, logout_user, login_required, current_user

# 別ファイルからの読み込み
from company_blog import db
from company_blog.models import User
from company_blog.users.forms import RegistrationForm, LoginForm, UpdateUserForm
from flask import Blueprint

users = Blueprint('users', __name__)


# ログインページ
@users.route('/login', methods=['GET', 'POST'])
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
                    next = url_for('users.user_maintenance')
                return redirect(next)

            else:
                flash('パスワードが一致しません')
        else:
            flash('入力されたユーザーは存在しません')

    return render_template('users/login.html', form=form)

# ログアウト
@users.route('/logput')
def logout():
    logout_user()
    return redirect(url_for('users.login'))

#View関数
@users.route('/register', methods=['GET', 'POST'])
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
        return redirect(url_for('users.user_maintenance'))
    return render_template('users/register.html', form=form)

# ユーザー管理ページ
@users.route('/user_maintenance')
@login_required
def user_maintenance():
    page = request.args.get('page', 1 ,type=int)
    # usersテーブルからデータを全件取得
    users = User.query.order_by(User.id).paginate(page=page, per_page=10)
    return render_template('users/user_maintenance.html', users=users)

# ユーザー更新ページ
@users.route('/<int:user_id>/account', methods=['GET', 'POST'])
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

        return redirect(url_for('users.user_maintenance'))
    # 初期表示
    elif request.method == 'GET':
        form.username.data = user.username
        form.email.data = user.email
    
    return render_template('users/account.html', form=form)

# ユーザーデータ削除
@users.route('/<int:user_id>/delete', methods=['GET', 'POST'])
@login_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    # 管理者権限
    if not current_user.is_administrator():
        abort(403)
    if user.is_administrator():
        flash('管理者は削除できません')
        return redirect(url_for('users.account', user_id=user_id))
    db.session.delete(user)
    db.session.commit()
    flash(f'ユーザーのアカウントが削除されました。')
    return redirect(url_for('users.user_maintenance'))
