from app import db, User

user_list = []

for i in range(200):
    user_list.append(User(f"seeder_user{i}@seeder.com", f"Seeder User{i}", "111", "0"))

db.session.add_all(user_list)
db.session.commit()