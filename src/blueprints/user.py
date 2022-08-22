from flask import Blueprint, flash, jsonify, request
from src.extensions import db
from src.models import User, Category, Post

user_bp = Blueprint('user', __name__)


@user_bp.route('/category', methods=['GET', "POST"])
def get_category():
    response = {}
    categorys = [_.name for _ in Category.query.all()]
    response['category'] = categorys
    return jsonify(response)


@user_bp.route('/post', methods=['GET', "POST"])
def get_post():
    response = {}
    posts = {}
    for _ in Post.query.all():
        posts.update({_.id: [_.title, _.category.name, _.body]})
    response['post'] = posts
    return jsonify(response)


@user_bp.route('/post/new', methods=['GET', 'POST'])
def new_post():
    user = User.query.get(1)
    title = request.form.get('title')
    category = Category.query.filter_by(name=request.form.get('category')).first()
    body = request.form.get('body')
    post = Post(title=title, body=body, category=category, user=user)
    db.session.add(post)
    db.session.commit()
    response = {'status': 'success'}
    return jsonify(response)


# 删除文章
@user_bp.route('/post/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    response = {'status': 'success'}
    return jsonify(response)
