from app import db, User, BlogPost

# BlogPostの__repr__で設定した物を読み込み
all_posts = BlogPost.query.all()
print(all_posts) 

for post in all_posts:
    print(post)