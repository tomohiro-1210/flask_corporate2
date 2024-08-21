from flask import Blueprint, render_template ,request, url_for, redirect, flash, abort
from flask_login import login_required, current_user
from company_blog.models import BlogCategory, BlogPost, Inquiry
from company_blog.main.forms import BlogCategoryForm, UpdateCategoryForm, BlogPostForm, BlogSearchForm, InquiryForm
from company_blog import db
from company_blog.main.image_handler import add_featured_image

main = Blueprint('main', __name__)

# TOPページ
@main.route('/')
def index():
    form = BlogSearchForm()
    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリーの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template('index.html', blog_posts=blog_posts, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form)


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

# ブログ投稿
@main.route('/create_post', methods=['GET', 'POST'])
@login_required
def create_post():
    form = BlogPostForm()
    if form.validate_on_submit():
        if form.picture.data:
            pic = add_featured_image(form.picture.data)
        else:
            pic = ''
        blog_post = BlogPost(title=form.title.data, text=form.text.data, summary=form.summary.data, featured_image=pic,  user_id=current_user.id, category_id=form.category.data)
        db.session.add(blog_post)
        db.session.commit()
        flash('ブログが投稿されました。')
        return redirect(url_for('main.blog_maintenance'))
    return render_template('create_post.html', form=form)

# ブログ管理ページ
@main.route('/blog_maintenance')
@login_required
def blog_maintenance():
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)
    return render_template('blog_maintenance.html', blog_posts=blog_posts)

# ブログ詳細
@main.route('/<int:blog_post_id>/blog_post')
def blog_post(blog_post_id):
    form = BlogSearchForm()

    # 最新記事の取得
    recent_blog_posts = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリーの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    # 検索ページの処理
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    return render_template('blog_post.html', post=blog_post, recent_blog_posts=recent_blog_posts, blog_categories=blog_categories, form=form)

# ブログの削除機能
@main.route('/<int:blog_post_id>/blog_delete', methods=['GET', 'POST'])
@login_required
def blog_delete(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    db.session.delete(blog_post)
    db.session.commit()
    return redirect(url_for('main.blog_maintenance'))

# ブログ更新
@main.route('/<int:blog_post_id>/update_blog', methods=['GET', 'POST'])
@login_required
def update_blog(blog_post_id):
    blog_post = BlogPost.query.get_or_404(blog_post_id)
    if blog_post.author != current_user:
        abort(403)
    form = BlogPostForm()
    if form.validate_on_submit():
        blog_post.title = form.title.data
        if form.picture.data:
            blog_post.featured_image = add_featured_image(form.picture.data)
        blog_post.text = form.text.data
        blog_post.summary = form.summary.data
        blog_post.category_id = form.category.data
        db.session.commit()
        flash('ブログ投稿が更新されました')
        return redirect(url_for('main.blog_post', blog_post_id=blog_post.id))
    elif request.method == 'GET':
        form.title.data = blog_post.title
        form.picture.data = blog_post.featured_image
        form.text.data = blog_post.text
        form.summary.data = blog_post.summary
        form.category.data = blog_post.category_id
    return render_template('create_post.html', form=form)

# ブログ記事検索
@main.route('/search', methods=['GET', 'POST'])
def search():
    form = BlogSearchForm()
    search_text = ""

    # 検索キーワードが送信されたときの処理
    if form.validate_on_submit():
        search_text = form.searchtext.data
    elif request.method == 'GET':
        form.searchtext.data = ""

    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter((BlogPost.text.contains(search_text)) | (BlogPost.title.contains(search_text)) | (BlogPost.summary.contains(search_text))).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_post = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリーの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template('index.html', blog_posts=blog_posts, recent_blog_post=recent_blog_post, blog_categories=blog_categories, form=form, search_text=search_text)

# カテゴリー別の機能
@main.route('/<int:id>/category_posts', methods=['GET', 'POST'])
def category_posts(id):
    form = BlogSearchForm()

    # カテゴリー名の取得
    blog_category = BlogCategory.query.filter_by(id=id).first_or_404()

    # ブログ記事の取得
    page = request.args.get('page', 1, type=int)
    blog_posts = BlogPost.query.filter_by(id=id).order_by(BlogPost.id.desc()).paginate(page=page, per_page=10)

    # 最新記事の取得
    recent_blog_post = BlogPost.query.order_by(BlogPost.id.desc()).limit(5).all()

    # カテゴリーの取得
    blog_categories = BlogCategory.query.order_by(BlogCategory.id.asc()).all()

    return render_template('index.html', blog_posts=blog_posts, recent_blog_post=recent_blog_post, blog_categories=blog_categories, id=id, form=form)

# お問い合わせフォーム
@main.route('/inquiry', methods=['GET', 'POST'])
def inquiry():
    form = InquiryForm()

    if form.validate_on_submit():
        inquiry = Inquiry(name=form.name.data, email=form.email.data, title=form.title.data, text=form.text.data)
        db.session.add(inquiry)
        db.session.commit()
        flash('お問い合わせが送信されました')
        return redirect(url_for('main.inquiry'))
    return render_template('inquiry.html', form = form)

# お問い合わせ管理画面
@main.route('/inquiry_maintenance', methods=['GET', 'POST'])
@login_required
def inquiry_maintenance():
    page = request.args.get('page', 1, type=int)
    inquiries = Inquiry.query.order_by(Inquiry.id.desc()).paginate(page=page, per_page=10)
    return render_template('inquiry_maintenance.html', inquiries=inquiries)