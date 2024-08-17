from flask import Flask, render_template, Blueprint

# Blueprintでフォルダをデフォルトに設定
error_pages = Blueprint('error_pages', __name__)

# 403ページ
@error_pages.errorhandler(403)
def error_403(error):
    return render_template('403.html'), 403

# 404ページ
@error_pages.errorhandler(404)
def error_404(error):
    return render_template('404.html'), 404