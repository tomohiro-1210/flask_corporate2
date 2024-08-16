from flask import Flask, render_template
from product_list import user_list

app = Flask(__name__)

@app.route('/')
def top():
    user_name = 'ひとくいばこ'
    return render_template('index.html', user_name=user_name)

@app.route('/product')
def product():
    product_list = ["computer1" ,"computer2", "computer3"]
    product_dict = {"product_name":"computer1", "product_price":"4500", "product_maker":"windows"}
    return render_template('product.html', product_list=product_list, product_dict=product_dict)

@app.route('/user')
def user():
    return render_template('users.html', user_list=user_list)

#404ページ
@app.errorhandler(404)
def error_404(error):
    return render_template('error_pages/404.html'), 404

if __name__ == '__main__':
    app.run()