# フォーム関係読み込み
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError, TextAreaField, SelectField
from wtforms.validators import DataRequired, Email
from company_blog.models import BlogCategory
#ファイル読み込み関係
from flask_wtf.file import FileField, FileAllowed

# カテゴリーフォーム
class BlogCategoryForm(FlaskForm):
    category = StringField('カテゴリー名', validators=[DataRequired()])
    submit = SubmitField('保存')

    def validate_category(self, field):
        if BlogCategory.query.filter_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリーは既に使われています。')
        
# カテゴリーフォーム
class UpdateCategoryForm(FlaskForm):
    category  = StringField('カテゴリー名', validators=[DataRequired()])
    submit = SubmitField('更新')

    def __init__(self, blog_category_id, *args, **kwargs):
        super(UpdateCategoryForm, self).__init__(*args, **kwargs)
        self.id = blog_category_id

    def validate_category(self, field):
        if BlogCategory.query.filter_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリー名は既に使われております。')
        
# ブログ投稿フォーム
class BlogPostForm(FlaskForm):
    title = StringField('タイトル', validators=[DataRequired()])
    category = SelectField('カテゴリー', coerce=int)
    summary = StringField('要約', validators=[DataRequired()])
    text = TextAreaField('本文', validators=[DataRequired()])
    picture = FileField('アイキャッチ画像', validators=[FileAllowed(['jpg', 'png', 'gif', 'mp3'])])
    submit = SubmitField('投稿')

    def _set_category(self):
        blog_categories = BlogCategory.query.all()
        # 内包表記、リストの中にタプルがたくさん入っている。
        self.category.choices = [(blog_category.id, blog_category.category) for blog_category in blog_categories] 

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._set_category()

# ブログ記事検索フォーム
class BlogSearchForm(FlaskForm):
    searchtext = StringField('検索テキスト', validators=[DataRequired()])
    submit = SubmitField('検索')

# お問い合わせフォーム
class InquiryForm(FlaskForm):
    name = StringField('お名前', validators=[DataRequired()])
    email = StringField('メールアドレス', validators=[DataRequired(), Email(message="正しいメールアドレスを入力してください")])
    title = StringField('題名', validators=[DataRequired()])
    text = TextAreaField('メッセージ本文', validators=[DataRequired()])
    submit = SubmitField('送信')
