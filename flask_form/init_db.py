from app import db, User
# パスワードのハッシュ化モジュール読み込み
from werkzeug.security import generate_password_hash

# db.drop_all()
db.create_all()

password = "123"
password_hash = generate_password_hash(password)
user1 = User(email="admin_monster@mon.com", username="Admin monster", password_hash=password_hash, administrator="1")
db.session.add(user1)
db.session.commit()