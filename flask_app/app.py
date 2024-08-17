# company_blog>__init__.pyからappを読み込み
from company_blog import app

if __name__ == '__main__':
    app.run(debug=True)
