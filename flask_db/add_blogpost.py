from app import db, BlogPost

blog_post1 = BlogPost(1, "Blog Title1", "Blog Test1", "Summary1", "Image1.png")
blog_post2 = BlogPost(4, "Blog Title2", "Blog Test2", "Summary2", "Image2.png")
blog_post3 = BlogPost(3, "Blog Title3", "Blog Test3", "Summary3", "Image3.png")
blog_post4 = BlogPost(4, "Blog Title4", "Blog Test4", "Summary4", "Image4.png")

db.session.add_all([blog_post1, blog_post2, blog_post3, blog_post4])
db.session.commit()