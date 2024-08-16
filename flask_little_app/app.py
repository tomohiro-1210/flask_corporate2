from flask import Flask
import random

app = Flask(__name__)

# index
@app.route('/')
def index():
    return 'ミミック'

@app.route('/product')
def product():
    return '<h1>プロダクト</h1>'

# ルーティング
@app.route('/monster')
def monster():
    return 'モンスター'

# 動的なルーティング
@app.route('/<name>')
def name(name):
    return f'{name}'

@app.route('/monster/<monster_name>')
def monstername(monster_name):
    return 'monstername:{0} {1} {2}'.format(monster_name[0], monster_name[1], monster_name[2])

if __name__ == '__main__':
    app.run(debug=True)