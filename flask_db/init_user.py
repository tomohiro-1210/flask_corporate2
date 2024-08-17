from db import db, User

# db.drop_all()
#dbの生成
db.create_all()

#登録するデータ
user1 = User("doragon@doragon.com", "doragon", "doragon")
user2 = User("master@doragon.com", "master doragon", "master")
user3 = User("kinghidora@doragon.com", "king hidora", "king")

#dbに引き渡し(全件)
db.session.add_all([user1, user2, user3])

db.session.commit() # dbに追加

print(user1.email)
print(user2.email)
print(user3.email)