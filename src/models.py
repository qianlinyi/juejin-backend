# 数据库模型
from werkzeug.security import generate_password_hash, check_password_hash

from src.extensions import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', back_populates='user')  # 建立用户和文章的一对多关系

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return dict(id=self.id, username=self.username)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)

    # 建立分类和文章的一对多关系
    posts = db.relationship('Post', back_populates='category')

    def to_dict(self):
        return dict(id=self.id, name=self.name)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category', back_populates='posts')

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship('User', back_populates='posts')

    def to_dict(self):
        return dict(id=self.id, title=self.title, body=self.body,
                    timestamp=self.timestamp.strftime("%Y-%m-%d %H:%M:%S"), category=self.category.to_dict(),
                    user=self.user.to_dict())
