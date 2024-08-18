from flask import Blueprint, render_template ,request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from company_blog.models import BlogCategory
from company_blog.main.forms import BlogCategoryForm, UpdateCategoryForm
from company_blog import db

main = Blueprint('main', __name__)

# カテゴリー一覧
@main.route('/category_maintenance', methods=['GET', 'POST'])
@login_required
def category_maintenance():
    # データの読み込み
    page = request.args.get('page', 1, type=int)
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).paginate(page=page, per_page=10)
    form = BlogCategoryForm()

    if form.validate_on_submit():
        blog_category = BlogCategory(category=form.category.data)
        db.session.add(blog_category)
        db.session.commit()
        flash('ブログカテゴリーが追加されました')
        return redirect(url_for('main.category_maintenance'))
    elif form.errors:
        form.category.data = ''
        flash(form.errors['category'][0])
    return render_template('category_maintenance.html', blog_categories=blog_categories, form=form)

# カテゴリー更新
@main.route('/<int:blog_category_id>/blog_category', methods=['GET', 'POST'])
@login_required
def blog_category(blog_category_id):
    # 管理者でないとき
    if not current_user.is_administrator():
        abort(403)
    blog_category = BlogCategory.query.get_or_404(blog_category_id)
    form = UpdateCategoryForm(blog_category_id)

    # 間違ったときの処理
    if form.validate_on_submit():
        blog_category.category = form.category.data
        db.session.commit()
        flash('ブログカテゴリーが更新されました。')
        return redirect(url_for('main.category_maintenance'))

    elif request.method == 'GET':
        form.category.data = blog_category.category
    return render_template('blog_category.html', form=form)

# カテゴリー削除
@main.route('/<int:blog_category_id>/delete_category', methods=['GET', 'POST'])
@login_required
def delete_category(blog_category_id):
    # 管理者でないとき
    if not current_user.is_administrator():
        abort(403)

    # カテゴリーの削除処理
    blog_category = BlogCategory.query.get_or_404(blog_category_id)
    db.session.delete(blog_category)
    db.session.commit()
    flash('ブログカテゴリーが削除されました')
    return redirect(url_for('main.category_maintenance'))