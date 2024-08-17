from db import User,db

# user4 = User("sinryu@doragon.com", "Shinryu", "Shinryu")
# db.session.add(user4)
# db.session.commit()
user5 = User("skydragon@doragon.com", "skydragon", "skydragon")
db.session.add(user5)
db.session.commit()

# DBのデータ全件取得
all_dragons = User.query.all()
print(all_dragons)

# DBをID指定して取得する
userid_1 = User.query.get(1)
print(userid_1.username)

# レコードの取得
# username_user2 = User.query.filter_by(username="shinryu")
# print(username_user2.all())

# レコードの更新
userid_1 = User.query.get(1)
userid_1.username = "doragon kids"
db.session.add(userid_1)
db.session.commit()

# レコードの削除
userid_2 = User.query.get(2)
db.session.delete(userid_2)
db.session.commit()