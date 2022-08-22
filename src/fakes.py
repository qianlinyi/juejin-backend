import random
from faker import Faker
from sqlalchemy.exc import IntegrityError

from src.extensions import db
from src.models import User, Category, Post

fake = Faker('zh-CN')


# 生成虚拟用户信息
def fake_user(count=10):
    for i in range(count):
        user = User(
            username=fake.user_name()
        )
        user.set_password('12345678')
        db.session.add(user)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


# 生成虚拟分类
def fake_categories(count=10):
    for i in range(count):
        category = Category(name=fake.word())
        db.session.add(category)
        try:
            db.session.commit()
        except IntegrityError:
            db.session.rollback()


# 生成虚拟文章
def fake_posts(count=5):
    for i in range(User.query.count()):
        for j in range(count):
            post = Post(
                title=fake.sentence(),
                body=fake.text(2000),
                category=Category.query.get(random.randint(1, Category.query.count())),
                user=User.query.get(i + 1)
            )
            db.session.add(post)
        db.session.commit()
