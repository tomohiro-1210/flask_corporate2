from app import db, User

# db.drop_all()
#dbの生成
db.create_all()

#登録するデータ
user0 = User("admin@doragon.com", "admin", "admin" ,"1")
user1 = User("doragon@doragon.com", "doragon", "doragon", "0")
user2 = User("master@doragon.com", "master doragon", "master", "0")
user3 = User("kinghidora@doragon.com", "king hidora", "king", "0")

#dbに引き渡し(全件)
db.session.add_all([user0, user1, user2, user3])

db.session.commit() # dbに追加

print(user1.email)
print(user2.email)
print(user3.email)