# フォーム関係読み込み
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired
from company_blog.models import BlogCategory

# カテゴリーフォーム
class BlogCategoryForm(FlaskForm):
    category = StringField('カテゴリー名', validators=[DataRequired()])
    submit = SubmitField('保存')

    def validate_category(self, field):
        if BlogCategory.query.filter_by(category=field.data).first():
            raise ValidationError('入力されたカテゴリーは既に使われています。')